from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QComboBox, QGridLayout, QLabel, QLineEdit, QSizePolicy, QToolButton, QWidget
import package.components.DatabaseAccess as DB

class PlaylistPopup(QWidget):
    def __init__(self, result, parent=None):
        # Popup when "Add song to playlist" is clicked on
        # How this works is a QWidget that encompasses the entire window area, representing an unclickable translucent background.
        # Another QWidget is then contained inside that QWidget representing the popup.
        # result: (dict) Python dict containing information of the song clicked
        QWidget.__init__(self)
        self.setParent(parent)
        self.result = result

        # Signals are used to indicate to close the window
        self.SIGNALS = self.TranslucentWidgetSignals()

        # Make the window frameless and expanding.
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Makes the window background colour translucent
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("PlaylistPopup { background-color: rgba(255, 255, 255, 0.5)}")

        # Sets the grid settings of the "background" and the "popup"
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        playlistAdd = QWidget(self)
        playlistAdd.setFixedSize(800, 300)
        playlistAdd.setStyleSheet(".QWidget { background-color: rgba(255, 255, 255, 1)}")
        innerLayout = QGridLayout()
        innerLayout.setContentsMargins(20, 20, 20, 20)
        innerLayout.setSpacing(30)

        # Heading font
        font = QFont()
        font.setPointSize(24)

        # Default label font
        font2 = QFont()
        font2.setPointSize(16)

        # Heading
        label = QLabel("添加到播放列表/Add to Playlist", self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        innerLayout.addWidget(label, 0, 0)

        # Playlist selection
        self.comboBox = QComboBox(self)
        self.comboBox.setFont(font)
        playlists = DB.getPlaylists("")
        for playlist in playlists:
            self.comboBox.addItem(playlist["playlist_name"])
        self.comboBox.setCurrentIndex(-1)
        innerLayout.addWidget(self.comboBox, 1, 0)

        # Textbox to create a new playlist
        self.textBox = QLineEdit(self)
        self.textBox.setFont(font2)
        self.textBox.setAlignment(Qt.AlignCenter)
        self.textBox.setPlaceholderText("输入以创建新的播放列表/Type to create a new playlist")
        self.textBox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        # TODO: resize textbox with window
        self.textBox.setFixedWidth(760)
        innerLayout.addWidget(self.textBox, 2, 0, Qt.AlignCenter)

        # Add actions for then the QComboBox or QLineEdit is changed.
        # This is done so there is only one action between "Add to existing Playlist" or "Add to new Playlist"
        self.comboBox.currentIndexChanged.connect(self.comboBoxChanged)
        self.textBox.textEdited.connect(self.textBoxChanged)

        # Confirm button
        confirmButton = QToolButton(self)
        confirmButton.setText("确认/Confirm")
        confirmButton.setFont(font)
        confirmButton.clicked.connect(self.processPlaylistRequest)
        innerLayout.addWidget(confirmButton, 3, 0, Qt.AlignCenter)

        # Exit button
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
        # Called when the ComboBox is changed
        # Clears the text in the "Create Playlist" TextBox
        if self.textBox.text() != "":
            self.textBox.setText("")

    def textBoxChanged(self):
        # Called when the TextBox is changed
        # Clears the selection in the "Add to Playlist" ComboBox
        if self.comboBox.currentIndex != -1:
            self.comboBox.setCurrentIndex(-1)

    def processPlaylistRequest(self):
        # Called when the Confirm button is clicked
        def addToPlaylist(self, playlistID):
            # Adds the song to the playlist
            # Get song ID
            song = self.result["song_id"]
            DB.addPlaylistSong(playlistID, song)

        if self.textBox.text() != "":
            # New playlist
            playlistName = self.textBox.text()
            counter = 1
            while DB.checkPlaylist(playlistName):
                playlistName = "{} ({})".format(self.textBox.text(), counter)
                counter += 1
            playlistID = DB.newPlaylist(playlistName)[0]["playlist_id"]
            addToPlaylist(self, playlistID)
            self.SIGNALS.CLOSE.emit()
        elif self.comboBox.currentIndex != -1:
            playlistID = DB.checkPlaylist(self.comboBox.currentText())[0]["playlist_id"]
            # Add to existing playlist
            addToPlaylist(self, playlistID)                   
            self.SIGNALS.CLOSE.emit()
    
    # Taken from https://stackoverflow.com/questions/44264852/pyside-pyqt-overlay-widget
    class TranslucentWidgetSignals(QtCore.QObject):
        CLOSE = QtCore.Signal()