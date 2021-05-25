from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QComboBox, QGridLayout, QLabel, QLineEdit, QSizePolicy, QToolButton, QWidget
import package.components.DatabaseAccess as DB

#TODO: comment properly

class PlaylistPopup(QWidget):
    def __init__(self, result, parent=None):
        QWidget.__init__(self)
        self.setParent(parent)
        self.result = result

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)
        self.SIGNALS = self.TranslucentWidgetSignals()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("PlaylistPopup { background-color: rgba(255, 255, 255, 0.5)}")

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        playlistAdd = QWidget(self)
        playlistAdd.setFixedSize(800, 300)
        playlistAdd.setStyleSheet(".QWidget { background-color: rgba(255, 255, 255, 1)}")
        innerLayout = QGridLayout()
        innerLayout.setContentsMargins(20, 20, 20, 20)
        innerLayout.setSpacing(30)

        font = QFont()
        font.setPointSize(24)

        font2 = QFont()
        font2.setPointSize(16)

        label = QLabel("添加到播放列表/Add to Playlist", self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        innerLayout.addWidget(label, 0, 0)

        self.comboBox = QComboBox(self)
        self.comboBox.setFont(font)
        playlists = DB.getPlaylists("")
        for playlist in playlists:
            self.comboBox.addItem(playlist["playlist_name"])
        self.comboBox.setCurrentIndex(-1)
        innerLayout.addWidget(self.comboBox, 1, 0)

        self.textBox = QLineEdit(self)
        self.textBox.setFont(font2)
        self.textBox.setAlignment(Qt.AlignCenter)
        self.textBox.setPlaceholderText("输入以创建新的播放列表/Type to create a new playlist")
        self.textBox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        # TODO: resize textbox with window
        self.textBox.setFixedWidth(760)
        innerLayout.addWidget(self.textBox, 2, 0, Qt.AlignCenter)

        self.comboBox.currentIndexChanged.connect(self.comboBoxChanged)
        self.textBox.textEdited.connect(self.textBoxChanged)

        confirmButton = QToolButton(self)
        confirmButton.setText("确认/Confirm")
        confirmButton.setFont(font)
        confirmButton.clicked.connect(self.processPlaylistRequest)
        innerLayout.addWidget(confirmButton, 3, 0, Qt.AlignCenter)

        btn = QToolButton(self)
        btn.setFixedSize(44, 44)
        btn.setText("X")
        btn.setFont(font)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.clicked.connect(lambda: self.SIGNALS.CLOSE.emit())
        innerLayout.addWidget(btn, 0, 0, Qt.AlignRight)

        playlistAdd.setLayout(innerLayout)

        layout.addWidget(playlistAdd, 0, 0, Qt.AlignCenter)
        self.setLayout(layout)

    def comboBoxChanged(self):
        if self.textBox.text() != "":
            self.textBox.setText("")

    def textBoxChanged(self):
        if self.comboBox.currentIndex != -1:
            self.comboBox.setCurrentIndex(-1)

    def processPlaylistRequest(self):
        def addToPlaylist(self):
            # Get playlist ID
            if self.textBox.text() != "":
                playlist = self.comboBox.count()
            else:
                playlist = self.comboBox.currentIndex()
            # Get song ID
            song = self.result["song_id"]
            DB.addPlaylistSong(playlist, song)

        if self.textBox.text() != "":
            # New playlist
            DB.newPlaylist(self.textBox.text())
            addToPlaylist(self)
            self.SIGNALS.CLOSE.emit()
        elif self.comboBox.currentIndex != -1:
            # Add to existing playlist
            addToPlaylist(self)                   
            self.SIGNALS.CLOSE.emit()
    
    # Taken from https://stackoverflow.com/questions/44264852/pyside-pyqt-overlay-widget
    class TranslucentWidgetSignals(QtCore.QObject):
        CLOSE = QtCore.Signal()