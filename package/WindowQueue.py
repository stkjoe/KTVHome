from PySide6 import QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QScrollArea, QScroller, QSizePolicy, QToolButton, QVBoxLayout, QWidget
from package.components.PlaylistPopup import PlaylistPopup
import package.components.DatabaseAccess as DB

class WindowQueue(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setParent(parent)

        # Set layout and spacings
        layout = QGridLayout()

        # The heading of the widget
        label = QLabel("排队的歌曲/Queue List")
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(40)
        # TODO: Change with global themes
        label.setStyleSheet("color: white;")
        # Font for the label
        font = QFont()
        font.setPixelSize(25)
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label, 0, 0)
        self.queueList = self.QueueList(self)
        layout.addWidget(self.queueList, 1, 0)

        self.setLayout(layout)

    class QueueList(QScrollArea):
        def __init__(self, parent=None):
            QScrollArea.__init__(self)
            self.setParent(parent)
            
            # Make QScrollArea transparent
            self.setStyleSheet("QScrollArea { background-color: transparent } .QFrame { background-color: transparent }")
            self.setWidgetResizable(True)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            # Add Touch Gestures to menu.
            QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)

            # Set layout settings
            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)

            # A singular widget frame is needed to set the scroll area properly.
            frame = QFrame()
            frame.setLayout(self.layout)

            self.setWidget(frame)

            self.updateQueue()

        class QueueListItem(QToolButton):
            def __init__(self, song, parent=None):
                QToolButton.__init__(self)
                self.setParent(parent)
                self.song = song

                # Button formatting
                self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                self.setFixedHeight(70)
                self.setAutoRaise(True)
                # TODO: change with global themes
                self.setStyleSheet("QToolButton:pressed { background-color: rgba(255, 255, 255, 0.1)} QToolButton { background-color: rgba(255, 255, 255, 0.05); border: 1px solid white}")

                # Set layout
                self.layout = QHBoxLayout()
                self.layout.setContentsMargins(0, 0, 0, 0)
                self.layout.setSpacing(0)

                self.createItem()
                self.setLayout(self.layout)

            def createItem(self):
                # Create a song item

                # Add Space to the beginning of the item
                labelQueue = self.formattedLabel(QLabel("", self))
                labelQueue.setFixedWidth(70)
                labelQueue.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(labelQueue)

                # Artist name
                labelArtist = self.formattedLabel(QLabel(self.song["artist_name"]))
                labelArtist.setFixedWidth(300)
                self.layout.addWidget(labelArtist)

                # Song Title
                labelTitle = self.formattedLabel(QLabel(self.song["song_title"]))
                self.layout.addWidget(labelTitle)

                # Set font (icon) size
                font = QFont()
                font.setPointSize(48)                

                # Add buttons for queue-specific actions
                
                # Move the song up the queue
                btnMoveUp = QToolButton()
                btnMoveUp.setText("▲")
                btnMoveUp.setFixedSize(70, 70)
                btnMoveUp.setStyleSheet("color: white")
                btnMoveUp.setFont(font)
                btnMoveUp.clicked.connect(self.moveUp)
                self.layout.addWidget(btnMoveUp)

                # Move the song down the queue
                btnMoveDown = QToolButton()
                btnMoveDown.setText("▼")
                btnMoveDown.setFixedSize(70, 70)
                btnMoveDown.setStyleSheet("color: white")
                btnMoveDown.setFont(font)
                btnMoveDown.clicked.connect(self.moveDown)
                self.layout.addWidget(btnMoveDown)

                # Move the song to the top of the queue
                btnMoveTop = QToolButton()
                btnMoveTop.setText("⍏")
                btnMoveTop.setFixedSize(70, 70)
                btnMoveTop.setStyleSheet("color: white")
                btnMoveTop.setFont(font)
                btnMoveTop.clicked.connect(self.moveTop)
                self.layout.addWidget(btnMoveTop)

                # Play the song immediately
                btnPlay = QToolButton()
                btnPlay.setText("➤")
                btnPlay.setFixedSize(70, 70)
                btnPlay.setStyleSheet("color: white")
                btnPlay.setFont(font)
                btnPlay.clicked.connect(self.playSong)
                self.layout.addWidget(btnPlay)

                # Remove the song from the queue
                btnRemove = QToolButton()
                btnRemove.setText("X")
                btnRemove.setFixedSize(70, 70)
                btnRemove.setStyleSheet("color: white")
                btnRemove.setFont(font)
                btnRemove.clicked.connect(self.removeSong)
                self.layout.addWidget(btnRemove)

            def formattedLabel(self, label):
                font = QFont()
                font.setPixelSize(25)
                # TODO: change with global themes
                label.setStyleSheet("color: white")
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setFont(font)
                return label
            
            def moveUp(self):
                # Move the song up the queue
                self.window().songQueue.moveUp(self.song)
                self.window().content.queueList.updateQueue()

            def moveDown(self):
                # Move the song down the queue
                self.window().songQueue.moveDown(self.song)
                self.window().content.queueList.updateQueue()

            def moveTop(self):
                # Move the song to the top of the queue
                self.window().songQueue.moveTop(self.song)
                self.window().content.queueList.updateQueue()
            
            def playSong(self):
                # Play the song immediately
                self.window().songQueue.moveTop(self.song)
                self.window().overlayBottom.buttonAction("next")
                self.window().content.queueList.updateQueue()
            
            def removeSong(self):
                # Remove the song from the queue
                self.window().songQueue.removeSong(self.song)
                self.window().content.queueList.updateQueue()
                if len(self.window().mediaPlayer.songQueue.getQueue()) == 0:
                    self.window().mediaPlayer.updateMarquee()
                
        def updateQueue(self):
            # "Refresh" the queue visually
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
            for i in self.window().songQueue.getQueue():
                item = self.QueueListItem(i, self)
                self.layout.addWidget(item)
            if self.window().songQueue.getQueue():
                self.layout.addStretch(1)
            else:
                label = QLabel("没有结果/No Result")
                label.setStyleSheet("color: white")
                label.setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setPointSize(35)
                label.setFont(font)
                
                self.layout.addWidget(label)