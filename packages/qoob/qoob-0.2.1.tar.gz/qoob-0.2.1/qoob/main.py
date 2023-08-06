#!/usr/bin/python3
import copy
import os
import sys
from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia, uic

try:
    from Xlib import X, display
    from Xlib.ext import record
    from Xlib.protocol import rq
except ImportError:
    pass

try:
    from .__id__ import ID, FULLNAME
    from .backend import cli, tools, player, parser, library
    from .frontend import preferences, trinkets, playlist, trinkets
    from .ui import player_ui
except ImportError:
    from __id__ import ID, FULLNAME
    from backend import cli, tools, player, parser, library
    from frontend import preferences, trinkets, playlist, trinkets

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
DB_DIR = os.path.expanduser(f"~/.config/{ID}/")


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        try:
            self.ui = player_ui.Ui_MainWindow()
            self.ui.setupUi(self)
        except NameError:
            self.ui = uic.loadUi(f"{LOCAL_DIR}ui/player_ui.ui", self)

        self.copied = []
        self.pending = False
        self.parent = parent
        self.logger = tools.Logger(name=ID, path=DB_DIR)
        self.log = self.logger.new(ID)
        self.preferences = preferences.PreferencesDatabase(self)
        self._styleInit()
        self.preferencesForm = preferences.PreferencesForm(self)
        self.popup = trinkets.PopupWidget(self)
        self.process = QtCore.QProcess()
        self.random = QtCore.QRandomGenerator()
        if not self.preferences.db["general"]["music database"]:
            self._findDefaultMusicFolder()

        self.player = player.MediaPlayer(self)
        self.parser = parser.Parser(self)
        self.tabWidget = playlist.Tabs(self)
        self.libraryView = self.tabWidget.tabs["Library viewer"]
        self.library = library.LibraryTree(self)
        self.trayIcon = trinkets.TrayIcon(self)

        self.player.currentMediaChanged.connect(self.currentMediaChanged)
        self.player.setItemColor.connect(self.setItemColor)
        self.player.setSliderRange.connect(self.ui.playbackSlider.setRange)
        self.player.setSliderValue.connect(self.ui.playbackSlider.setValue)
        self.player.setPlayPauseIcon.connect(self.ui.playButton.setIcon)
        self.player.setShuffleIcon.connect(self.ui.shuffleButton.setIcon)
        self.player.setRepeatIcon.connect(self.ui.repeatButton.setIcon)
        self.player.setStatusMessage.connect(self.setStatusMessage)
        self.player.shuffle = self.preferences.get("state", "shuffle")
        self.player.repeat = self.preferences.get("state", "repeat")
        self.ui.volumeSlider.setValue(self.player.volume())

        filters = self.preferences.get("state", "filters")
        self.libraryThread = QtCore.QThread()
        self.libraryWorker = library.LibraryWorker(self)
        self.libraryWorker.moveToThread(self.libraryThread)
        self.libraryWorker.expand.connect(self.library.expand)
        self.libraryWorker.addArtist.connect(self.library.addArtist)
        self.libraryWorker.setStatusMessage.connect(self.setStatusMessage)
        self.libraryWorker.state.connect(self.libraryState)
        self.library.selectEvent.connect(self.librarySelectEvent)
        self.library.selectEvent.connect(self.libraryWorker.selectEvent)
        self.library.selectEvent.connect(self.player.clearViewerPlaylist)
        self.ui.libraryFilterLine.keyPressEvent = self.libraryFilterKeyPressEvent
        self.ui.libraryFilterLine.textEdited.connect(self.player.clearViewerPlaylist)
        self.ui.libraryFilterLine.textEdited.connect(self.libraryFilterEditEvent)
        self.ui.filterArtistBox.stateChanged.connect(self.filtersEditEvent)
        self.ui.filterAlbumBox.stateChanged.connect(self.filtersEditEvent)
        self.ui.filterTitleBox.stateChanged.connect(self.filtersEditEvent)
        self.ui.filterArtistBox.setChecked("artist" in filters)
        self.ui.filterAlbumBox.setChecked("album" in filters)
        self.ui.filterTitleBox.setChecked("title" in filters)
        self.libraryThread.start()

        self.tabWidget.keyEvent.connect(self.parseHotkeys)
        self.tabWidget.clearTabPlaylist.connect(self.player.clearTabPlaylist)
        self.preferencesForm.accepted.connect(self.preferencesSave)
        self.preferencesForm.resetMetadata.connect(self.libraryReset)
        self.preferencesForm.activateWindow()

        artEnabled = self.preferences.get("art", "show empty") and self.preferences.get("art", "enable")
        self.artLabel = trinkets.ArtLabel(self)
        self.artLabel.setArtButtonIcon.connect(self.ui.artButton.setIcon)
        self.artLabel.setFrameVisible.connect(self.ui.artFrame.setVisible)
        self.ui.horizontalLayout.addWidget(self.artLabel)
        self.ui.artFrame.setVisible(artEnabled)
        if self.preferences.get("art", "enable"):
            self.ui.artButton.setIcon(self.icon["art_on"])
        else:
            self.ui.artButton.setIcon(self.icon["art_off"])

        self.menu = playlist.Menu(self)
        self.menu.action.connect(self.action)

        self.parserThread = QtCore.QThread()
        self.parser.moveToThread(self.parserThread)
        self.parser.addArtist.connect(self.library.addArtist)
        self.parser.addAlbum.connect(self.library.addAlbum)
        self.parser.clear.connect(self.libraryClearEvent)
        self.parser.doneDb.connect(self.preferencesForm.dbDoneSlot)
        self.parser.startDb.connect(self.preferencesForm.dbStartSlot)
        self.parser.state.connect(self.libraryState)
        self.parser.filterEnable.connect(self.libraryFilterEnable)
        self.parser.setStatusMessage.connect(self.setStatusMessage)
        self.parser.saveTreeCache.connect(self.libraryWorker.saveTreeCache)
        self.parserThread.start()

        self.trayIcon.hideWindow.connect(self.hide)
        self.trayIcon.showWindow.connect(self.show)
        self.trayIcon.close.connect(self.close)
        self.trayIcon.play.connect(self.player.playPauseEvent)
        self.trayIcon.stop.connect(self.player.stopEvent)
        self.trayIcon.next.connect(self.player.nextEvent)
        self.trayIcon.previous.connect(self.player.previousEvent)
        self.trayIcon.shuffle.connect(self.player.shuffleEvent)
        self.trayIcon.showPreferencesForm.connect(self.preferencesForm.show)
        self.trayIcon.popup.connect(self.popup.display)

        if "Xlib" in sys.modules:
            self.mediaKeyMonitor = XMediaKeysMonitor()
            self.mediaKeyMonitor.playPause.connect(self.player.playPauseEvent)
            self.mediaKeyMonitor.stop.connect(self.player.stopEvent)
            self.mediaKeyMonitor.previous.connect(self.player.previousEvent)
            self.mediaKeyMonitor.next.connect(self.player.nextEvent)
            self.mediaKeyMonitor.pause.connect(self.player.pauseEvent)
            self.mediaKeyThread = QtCore.QThread()
            self.mediaKeyMonitor.moveToThread(self.mediaKeyThread)
            self.mediaKeyThread.started.connect(self.mediaKeyMonitor.init)
            self.mediaKeyThread.start()

        self.ui.statusRightLabel = QtWidgets.QLabel()
        self.ui.statusBar = QtWidgets.QStatusBar()
        self.ui.statusBar.addPermanentWidget(self.ui.statusRightLabel)
        self.ui.statusBar.setStyleSheet("QStatusBar::item { border: 0 }")
        self.ui.libraryLayout.insertWidget(1, self.library)
        self.ui.tabLayout.addWidget(self.tabWidget, 1, 1, 1, 8)

        self.ui.playButton.clicked.connect(self.player.playPauseEvent)
        self.ui.stopButton.clicked.connect(self.player.stopEvent)
        self.ui.nextButton.clicked.connect(lambda: self.player.nextEvent(forced=True))
        self.ui.previousButton.clicked.connect(self.player.previousEvent)
        self.ui.shuffleButton.clicked.connect(self.player.shuffleEvent)
        self.ui.repeatButton.clicked.connect(self.player.repeatEvent)
        self.ui.preferencesButton.clicked.connect(self.preferencesShow)
        self.ui.refreshButton.clicked.connect(self.libraryRefresh)
        self.ui.collapseButton.clicked.connect(self.library.collapseAll)
        self.ui.expandButton.clicked.connect(self.library.expandAll)
        self.ui.libraryFilterClearButton.clicked.connect(self.libraryFilterClear)
        self.ui.volumeSlider.valueChanged.connect(self.player.setVolume)
        self.ui.playbackSlider.installEventFilter(self)
        self.ui.volumeSlider.installEventFilter(self)
        self.ui.artButton.clicked.connect(self.artLabel.toggle)

        self._styleLoad()
        self.setStatusBar(self.ui.statusBar)
        self.setWindowTitle(ID)
        self.setWindowIcon(self.icon[ID])
        width = self.preferences.get("state", "width")
        height = self.preferences.get("state", "height")
        self.resize(width, height)
        self.tabWidget.setFocus(True)
        self._resumePlayback()
        self.libraryWorker._fetchTree()
        self.show()

        if self.preferences.db["general"]["refresh on startup"]:
            self.libraryRefresh()

    def closeEvent(self, event):
        self.preferences.db["state"]["shuffle"] = self.player.shuffle
        self.preferences.db["state"]["repeat"] = self.player.repeat
        self.preferences.db["state"]["volume"] = self.player.volume()
        self.preferences.db["state"]["tab"] = self.tabWidget.tabBar().currentIndex()
        self.preferences.db["state"]["playback position"] = self.player.position()
        self.preferences.db["state"]["media state"] = self.player.state()
        self.preferences.db["state"]["file"] = self.player.path
        self.preferences.db["state"]["width"] = self.width()
        self.preferences.db["state"]["height"] = self.height()
        self.preferences.db["state"]["filters"] = []
        if self.ui.filterArtistBox.isChecked():
            self.preferences.db["state"]["filters"].append("artist")
        if self.ui.filterAlbumBox.isChecked():
            self.preferences.db["state"]["filters"].append("album")
        if self.ui.filterTitleBox.isChecked():
            self.preferences.db["state"]["filters"].append("title")
        self.preferences.save()
        self.tabWidget.playlistSave()
        self.parent.exit()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            mouseEvent = QtGui.QMouseEvent(event)
            position = QtWidgets.QStyle.sliderValueFromPosition(obj.minimum(), obj.maximum(), mouseEvent.x(), obj.width())
            obj.setValue(position)
            if obj == self.ui.playbackSlider:
                self.player.setPosition(obj.value())
        return QtCore.QObject.event(obj, event)

    def changeEvent(self, event):
        # Override minimize event
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                if self.preferences.get("general", "tray minimize") and self.preferences.get("general", "tray icon"):
                    self.setWindowState(QtCore.Qt.WindowNoState)
                    self.hide() if self.isVisible() else self.show()

    def _delete(self, files):
        currentTab = self.tabWidget.current
        selection = currentTab.selectedItems()

        for f in files:
            if os.path.isfile(f):
                os.remove(f)

            # Remove empty folder
            if self.preferences.get("general", "clean folder"):
                parent = os.path.abspath(os.path.join(f, os.pardir))
                if os.path.isdir(parent):
                    if len(os.listdir(parent)) == 0:
                        os.rmdir(parent)
                        self.libraryRefresh()
                        return

        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            if self.player.path in files:
                self.player.nextEvent()

        # Remove items from playlist
        for item in selection:
            index = currentTab.indexOfTopLevelItem(item)
            currentTab.takeTopLevelItem(index)

    def _deletePrompt(self, files):
        if self.preferences.get("general", "delete confirm"):
            filenames = ""
            for f in files:
                filenames += "\n" + os.path.basename(f)

            msg = trinkets.DeletePrompt()
            msg.setText(f"Please confirm deletion of :\n{filenames}")
            if msg.exec_() == QtWidgets.QMessageBox.Apply:
                self._delete(files)
        else:
            self._delete(files)

    def _findDefaultMusicFolder(self):
        xdgDirectories = os.path.expanduser("~/.config/user-dirs.dirs")
        if os.path.isfile(xdgDirectories):
            with open(xdgDirectories) as f:
                for line in f.read().splitlines():
                    line = line.split("=")
                    if line[0] == "XDG_MUSIC_DIR":
                        musicFolder = line[1].replace("$HOME", "~")
                        musicFolder = os.path.expanduser(musicFolder[1:-1])
                        self.preferences.db["general"]["music database"].append(musicFolder)
                        self.preferences.save()
                        break

    def _styleInit(self):
        # Init icons
        iconTheme = self.preferences.get("general", "icon theme")
        iconPath = f"{LOCAL_DIR}icons/{iconTheme}/"
        self.icon = {}
        for icon in os.listdir(iconPath):
            iconName = os.path.splitext(icon)
            if iconName[1] == ".svg":
                self.icon[iconName[0]] = QtGui.QIcon(f"{iconPath}{icon}")

        # Init stylesheet
        stylesheet = f"QPushButton#libraryFilterClearButton {{ border-image: url({iconPath}filter_clear.svg); }}\n"
        stylesheet += f"QPushButton#libraryFilterClearButton:hover {{ border-image: url({iconPath}filter_hover.svg); }}"
        self.ui.libraryFilterClearButton.setStyleSheet(stylesheet)

    def _styleLoad(self):
        self.ui.playButton.setIcon(self.icon["play"])
        self.ui.stopButton.setIcon(self.icon["stop"])
        self.ui.nextButton.setIcon(self.icon["next"])
        self.ui.previousButton.setIcon(self.icon["previous"])
        self.ui.preferencesButton.setIcon(self.icon["preferences"])
        self.ui.refreshButton.setIcon(self.icon["refresh"])
        self.ui.collapseButton.setIcon(self.icon["collapse"])
        self.ui.expandButton.setIcon(self.icon["expand"])

        icon = {0: "repeat_off", 1: "repeat_all", 2: "repeat_single"}
        stateIcon = icon[self.player.repeat]
        self.ui.repeatButton.setIcon(self.icon[stateIcon])

        if self.player.shuffle:
            self.ui.shuffleButton.setIcon(self.icon["shuffle_on"])
        else:
            self.ui.shuffleButton.setIcon(self.icon["shuffle_off"])

        if self.preferences.get("art", "enable"):
            self.ui.artButton.setIcon(self.icon["art_on"])
        else:
            self.ui.artButton.setIcon(self.icon["art_off"])

    def _resumePlayback(self):
        self.player.resumePlayback = self.preferences.get("general", "resume playback")
        playing = self.preferences.get("state", "media state") == QtMultimedia.QMediaPlayer.PlayingState
        if self.player.resumePlayback and playing:
            self.player.setCurrentMedia(self.preferences.get("state", "file"))

    def _titleFormat(self, title):
        replace = ("artist", "album", "track", "title")
        for tag in replace:
            title = title.replace("%" + tag + "%", self.player.tags[tag])
        return title

    def _viewerLoadSort(self, content):
        self.tabWidget.tabBar().setCurrentIndex(0)
        tags = self.libraryWorker._fetchTag(content)
        tags = self.libraryWorker._sort(tags)
        self.libraryWorker._fillView(tags)

    def action(self, action):
        currentTab = self.tabWidget.current
        selection = currentTab.selectedItems()
        if action == "paste" and self.copied:
            if not currentTab.topLevelItemCount():
                self.copied.reverse()
            for path in self.copied:
                item = currentTab.add(path)

            # Select pasted item
            currentTab.clearSelection()
            currentTab.setCurrentItem(item)

        elif selection:
            files = []
            for item in selection:
                files.append(item.text(5))

            if action == "copy":
                self.copied = files

            if action == "cut":
                self.copied = files
                for item in selection:
                    index = currentTab.indexOfTopLevelItem(item)
                    currentTab.takeTopLevelItem(index)

            elif action == "delete from playlist":
                for item in selection:
                    index = currentTab.indexOfTopLevelItem(item)
                    currentTab.takeTopLevelItem(index)

            elif action == "delete prompt":
                self._deletePrompt(files)

            elif action == "delete no confirm":
                self._delete(files)

            elif action == "browse":
                folder = os.path.abspath(os.path.join(currentTab.currentItem().text(5), os.pardir))
                cmd = f'{self.preferences.get("general", "file manager")} "{folder}"'
                self.process.startDetached(cmd)

    def currentMediaChanged(self, path):
        titlePopup = self._titleFormat(self.preferences.get("viewer", "notification format"))
        titleWindow = self._titleFormat(self.preferences.get("viewer", "title format"))
        titleTooltip = self._titleFormat(self.preferences.get("viewer", "tooltip format"))
        self.popup.display(titlePopup)
        self.setWindowTitle(titleWindow)
        self.trayIcon.setToolTip(titleTooltip)
        self.artLabel.load(path)
        if self.preferences.get("art", "media trigger"):
            self.artLabel.display()

    def filtersEditEvent(self):
        text = self.ui.libraryFilterLine.text()
        if text:
            sift = QtCore.Q_ARG(str, text)
            QtCore.QMetaObject.invokeMethod(self.libraryWorker, "filterEvent", QtCore.Qt.QueuedConnection, sift)

    def libraryClearEvent(self):
        self.libraryWorker.sift = ""
        self.library.clear()
        self.ui.libraryFilterLine.clear()

    def libraryState(self, pending):
        self.pending = pending
        if pending:
            self.preferencesForm.setPending()
        else:
            self.library.addAllMusic()

    def libraryFilterClear(self):
        if self.ui.libraryFilterLine.text():
            self.ui.libraryFilterLine.clear()
            self.libraryFilterEditEvent()
        self.ui.libraryFilterLine.setFocus(True)

    def libraryFilterEnable(self, state):
        self.ui.refreshButton.setEnabled(state)
        self.ui.libraryFilterLine.setEnabled(state)
        self.ui.libraryFilterClearButton.setEnabled(state)

    def libraryFilterEditEvent(self, text=""):
        sift = QtCore.Q_ARG(str, text)
        QtCore.QMetaObject.invokeMethod(self.libraryWorker, "filterEvent", QtCore.Qt.QueuedConnection, sift)
        self.tabWidget.tabBar().setCurrentIndex(0)

    def libraryFilterKeyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.libraryFilterClear()
        QtWidgets.QLineEdit.keyPressEvent(self.ui.libraryFilterLine, event)

    def libraryRefresh(self):
        if not self.pending:
            QtCore.QMetaObject.invokeMethod(self.parser, "scanAll", QtCore.Qt.QueuedConnection)

    def libraryReset(self):
        if not self.pending:
            QtCore.QMetaObject.invokeMethod(self.parser, "reset", QtCore.Qt.QueuedConnection)

    def librarySelectEvent(self, selection):
        self.tabWidget.tabBar().setCurrentIndex(0)
        self.artLabel.load(selection[0].text(1))
        if self.preferences.get("art", "library trigger"):
            self.artLabel.display()

    def menuShow(self):
        if self.tabWidget.current.selectedItems() or self.copied:
            self.menu.popup(QtGui.QCursor.pos())

    @QtCore.pyqtSlot(dict)
    def cli(self, cmd):
        if "delete" in cmd:
            self.action("delete prompt")

        elif "delete-no-confirm" in cmd:
            self.action("delete no confirm")

        if "shuffle" in cmd:
            if len(cmd["shuffle"]) > 0:
                if cmd["shuffle"][0] == "on":
                    self.player.shuffleEvent(enable=True)
                elif cmd["shuffle"][0] == "off":
                    self.player.shuffleEvent(enable=False)
            else:
                self.player.shuffleEvent()
            self.popup.display("Shuffle enabled" if self.player.shuffle else "Shuffle disabled")

        if "repeat" in cmd:
            if len(cmd["repeat"]) > 0:
                states = {"off": 0, "all": 1, "single": 2}
                arg = cmd["repeat"][0]
                self.player.repeatEvent(state=states[arg])
            else:
                self.player.repeatEvent()
            states = {0: "off", 1: "all", 2: "single"}
            self.popup.display(f"Repeat {states[self.player.repeat]}")

        if "clear" in cmd:
            self.libraryView.clear()

        if "file" in cmd:
            if len(cmd["file"]) == 0:
                return False
            for f in cmd["file"]:
                if not os.path.isfile(f):
                    cmd["file"].remove(f)
            self._viewerLoadSort(cmd["file"])

        if "folder" in cmd:
            if len(cmd["folder"]) == 0:
                return False
            content = set()
            for folder in cmd["folder"]:
                if os.path.isdir(folder):
                    for root, subfolder, files in os.walk(folder):
                        for f in files:
                            path = os.path.join(root, f)
                            content.add(path)
            self._viewerLoadSort(content)

        if "stop" in cmd:
            self.player.stopEvent()

        if "previous" in cmd:
            self.player.previousEvent()

        if "next" in cmd:
            self.player.nextEvent()

        if "play" in cmd:
            self.player.playEvent()
            titlePopup = self._titleFormat(self.preferences.get("viewer", "notification format"))
            self.popup.display(titlePopup)

        if "play-pause" in cmd:
            self.player.playPauseEvent()
            if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
                titlePopup = self._titleFormat(self.preferences.get("viewer", "notification format"))
                self.popup.display(titlePopup)
            else:
                self.popup.display("Paused")

        if "pause" in cmd:
            self.player.pauseEvent()
            self.popup.display("Paused")

        if "quit" in cmd:
            self.close()

    def parseHotkeys(self, modifier, key):
        ctrl = (modifier == QtCore.Qt.ControlModifier)
        if ctrl and key == QtCore.Qt.Key_C:
            self.action("copy")
        elif ctrl and key == QtCore.Qt.Key_X:
            self.action("cut")
        elif ctrl and key == QtCore.Qt.Key_V:
            self.action("paste")
        elif key == QtCore.Qt.Key_Left:
            self.player.skip(-5)
        elif key == QtCore.Qt.Key_Right:
            self.player.skip(5)
        elif key == QtCore.Qt.Key_Backspace:
            self.action("delete from playlist")
        elif key == QtCore.Qt.Key_Delete:
            self.action("delete prompt")
        elif key == QtCore.Qt.Key_Space:
            self.player.playPauseEvent()

    def preferencesSave(self):
        self.preferencesForm.settingsSave()
        oldDb = self.preferences.get("general", "music database")
        newDb = self.preferencesForm.db["general"]["music database"]
        oldSort = self.preferences.get("viewer", "sorting routine")
        newSort = self.preferencesForm.db["viewer"]["sorting routine"]
        changedDb = not oldDb == newDb
        changedSortRoutine = not oldSort == newSort
        self.preferences.db = copy.deepcopy(self.preferencesForm.db)
        self.preferences.save()

        if changedDb:
            for path in oldDb:
                if path not in newDb:
                    path = QtCore.Q_ARG(str, path)
                    QtCore.QMetaObject.invokeMethod(self.libraryWorker, "removeViewCache", QtCore.Qt.QueuedConnection, path)
                    QtCore.QMetaObject.invokeMethod(self.parser, "removeMetaDatabase", QtCore.Qt.QueuedConnection, path)
            self.libraryRefresh()

        if changedSortRoutine:
            self.libraryWorker.clearViewCache()

        self._styleInit()
        self._styleLoad()
        self.artLabel.display()
        self.player.icon = self.icon
        self.artLabel.icon = self.icon
        self.tabWidget.initStyle()
        self.popup.updateView()
        if self.preferences.get("general", "tray icon"):
            self.trayIcon.show()
        else:
            self.trayIcon.hide()

    def preferencesShow(self):
        self.preferencesForm.show()
        self.preferencesForm.raise_()

    def setItemColor(self, color):
        current = self.tabWidget.current.currentItem()
        if current:
            self.tabWidget.current.currentItem().setColor(color)

    def setStatusMessage(self, left=None, right=None):
        if left:
            self.ui.statusBar.showMessage(left)
        if right:
            self.ui.statusRightLabel.setText(right)


class XMediaKeysMonitor(QtCore.QObject):
    playPause = QtCore.pyqtSignal()
    pause = QtCore.pyqtSignal()
    stop = QtCore.pyqtSignal()
    previous = QtCore.pyqtSignal()
    next = QtCore.pyqtSignal()

    def _begin(self):
        self.context = \
            self.dpy.record_create_context(0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
                'device_events': (X.KeyPress, X.KeyRelease),
            }])
        self.dpy.record_enable_context(self.context, self._callback)
        self.dpy.record_free_context(self.context)

    def _callback(self, reply):
        if reply.category == record.FromServer:
            event, data = rq.EventField(None).parse_binary_value(reply.data, self.dpy.display, None, None)
            if event.type == X.KeyPress:
                key = self.dpy.keycode_to_keysym(event.detail, 0)
                self._parse(key)

    def _parse(self, key):
        if key == 269025044:
            self.playPause.emit()
        elif key == 269025045:
            self.stop.emit()
        elif key == 269025046:
            self.previous.emit()
        elif key == 269025047:
            self.next.emit()
        elif key == 269025073:
            self.pause.emit()

    @QtCore.pyqtSlot()
    def init(self):
        self.dpy = display.Display()
        if self.dpy.has_extension("RECORD"):
            self._begin()


def main(cmd=""):
    app = QtWidgets.QApplication(sys.argv)
    app.setDesktopFileName(ID)
    app.setApplicationName(FULLNAME)
    app.setQuitOnLastWindowClosed(False)
    cmd = cli.parse(cmd)
    widget = Main(app)
    widget.cli(cmd)
    widgetBus = cli.QDBusObject(parent=widget)
    sys.exit(app.exec_())
