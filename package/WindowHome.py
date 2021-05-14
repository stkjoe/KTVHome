from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QToolButton, QWidget

class WindowHome(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setParent(parent)

        # Create layout with margins/spacings
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.setLayout(self.initButtons(layout))

    def initButtons(self, layout):
        # Create the buttons in the home page

        # Search Title
        button = self.HomeButton(self)
        button.setIcon("icons/search-1.svg")
        button.setText("搜索全部/Search")
        button.clicked.connect(lambda: self.buttonAction("title"))
        layout.addWidget(button, 0, 0, 2, 2)
        
        # Search Artist
        button = self.HomeButton(self)
        button.setIcon("icons/compact-disc.svg")
        button.setText("搜索歌手/Artist Search")
        button.clicked.connect(lambda: self.buttonAction("artist"))
        layout.addWidget(button, 2, 0, 1, 1)

        # Search Language
        button = self.HomeButton(self)
        button.setIcon("icons/worldwide.svg")
        button.setText("搜索语言/Language Search")
        button.clicked.connect(lambda: self.buttonAction("language"))
        layout.addWidget(button, 2, 1, 1, 1)
        
        # Playlists
        button = self.HomeButton(self)
        button.setIcon("icons/music-player-2.svg")
        button.setText("播放清单/Playlists")
        button.clicked.connect(lambda: self.buttonAction("playlists"))
        layout.addWidget(button, 0, 2, 1, 2)

        # Favourites
        button = self.HomeButton(self)
        button.setIcon("icons/star.svg")
        button.setText("最喜欢的/Favourites")
        button.clicked.connect(lambda: self.buttonAction("favourites"))
        layout.addWidget(button, 1, 2, 2, 1)

        # Queue
        button = self.HomeButton(self)
        button.setIcon("icons/windows.svg")
        button.setText("排队的歌曲/Queue List")
        button.clicked.connect(lambda: self.buttonAction("queue"))
        layout.addWidget(button, 1, 3, 1, 1)

        # Statistics
        button = self.HomeButton(self)
        button.setIcon("icons/notebook-2.svg")
        button.setText("统计数据/Statistics")
        button.clicked.connect(lambda: self.buttonAction("statistics"))
        layout.addWidget(button, 2, 3, 1, 1)

        return layout

    def buttonAction(self, i):
        # Pythonic switch-case

        def buttonTitle(self):
            pass

        def buttonArtist(self):
            pass

        def buttonLanguage(self):
            pass

        def buttonPlaylist(self):
            pass

        def buttonFavourites(self):
            pass

        def buttonQueue(self):
            pass

        def buttonStatistics(self):
            pass

        switcher = {
            "title": buttonTitle,
            "artist": buttonArtist,
            "language": buttonLanguage,
            "playlist": buttonPlaylist,
            "favourites": buttonFavourites,
            "queue": buttonQueue,
            "statistics": buttonStatistics
        }
        func = switcher.get(i, buttonTitle)
        func(self)
    
    class HomeButton(QToolButton):
        def __init__(self, parent=None):
            QToolButton.__init__(self)
            self.setParent(parent)\

            # Set the layout of the button
            layout = QGridLayout()

            # Button formatting
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Icon part of the button
            self.icon = QLabel()
            self.icon.setAlignment(Qt.AlignCenter)
            self.icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.iconPixmap = QPixmap()

            # Text part of the button
            # Initialise label
            self.text = QLabel()
            self.text.setAlignment(Qt.AlignBottom)
            # Add font styling
            font = QFont()
            font.setPixelSize(15)
            self.text.setFont(font)

            # Add components to the layer
            layout.addWidget(self.icon, 0, 0, 3, 3)
            layout.addWidget(self.text, 2, 0, 1, 3)
            self.setLayout(layout)

        def setIcon(self, path):
            # Set the icon part of the button
            # path: (str) path to the new icon to use
            self.icon.setPixmap(QPixmap(path))
            self.icon.repaint()

        def setText(self, text):
            # Set the text part of the button
            # text: (str) what the new text part should say
            self.text.setText(text)
            
        def setColour(self, r, g, b):
            # Set the colour to rgb
            # r: (int) red value
            # g: (int) green value
            # b: (int) blue value
            self.setStyleSheet("QToolButton {{ background-color:  rgba({}, {}, {}, 0.8)}}\n\nQToolButton:pressed {{ background-color: rgba({}, {}, {}, 1)}}".format(r, g, b, r, g, b))