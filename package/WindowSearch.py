from PySide6 import QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QLineEdit, QScroller, QVBoxLayout, QWidget, QScrollArea, QSizePolicy, QToolButton, QHBoxLayout
import package.components.DatabaseAccess as DB
from package.components.PlaylistPopup import PlaylistPopup

#TODO: comment properly

class WindowSearch(QWidget):
    def __init__(self, heading, parent=None, counter=0, pastResults={}, grid=False):
        QWidget.__init__(self)
        self.setParent(parent)
        self.heading = heading
        self.counter = counter
        self.pastResults = pastResults

        # Set layout and spacings
        layout = QGridLayout()

        # The heading of the widget
        label = QLabel(heading)
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


        # Add back button
        if self.counter:
            backButton = QToolButton()
            backButton.setText("🡸")
            font = QFont()
            font.setPointSize(30)
            backButton.setFont(font)
            backButton.setFixedSize(QSize(40, 40))
            backButton.setAutoRaise(True)
            backButton.setStyleSheet("QToolButton { color: white; background-color: transparent;} QToolButton:pressed {background-color: rgba(255, 255, 255, 0.1);}")
            layout.addWidget(backButton, 0, 0)
            backButton.clicked.connect(self.goBack)

        # Sub heading if this is an indepth search
        sublabel = QLabel()
        sublabel.setFixedHeight(20)
        if self.pastResults:
            sublabel.setAlignment(Qt.AlignCenter)
            # TODO: Change with global themes
            sublabel.setStyleSheet("color: white;")
            if "artist_id" in self.pastResults:
                sublabel.setText("Artist: " + self.pastResults["artist_name"])
            elif "language_id" in self.pastResults:
                sublabel.setText("Language: " + self.pastResults["language_name"])
            elif "playlist_id" in self.pastResults:
                sublabel.setText("Playlist: " + self.pastResults["playlist_name"])
            font = QFont()
            font.setPixelSize(15)
            font.setItalic(True)
            sublabel.setFont(font)
        layout.addWidget(sublabel, 1, 0)


        # Set searchbar
        self.searchBar = QLineEdit(self)
        # TODO: change with resizeEvent
        self.searchBar.setMinimumWidth(800)
        font = QFont()
        font.setPointSize(20)
        self.searchBar.setFont(font)
        layout.addWidget(self.searchBar, 2, 0)
        layout.setAlignment(self.searchBar, Qt.AlignCenter)

        # Set results page
        if (grid):
            self.results = self.ResultsGrid(self)
            layout.addWidget(self.results, 3, 0)
        else:
            self.results = self.ResultsList(self)
            layout.addWidget(self.results, 3, 0)

        self.searchBar.textEdited.connect(self.updateResults)
        self.updateResults()

        self.setLayout(layout)

    def updateResults(self):
        if self.heading == "播放清单/Playlists":
            self.results.addResults(DB.getPlaylists(self.searchBar.text()))
        elif self.heading == "最喜欢的歌曲/Favourite Songs":
            self.results.addResults(DB.getFavouriteSongs(self.searchBar.text()))
        elif self.heading == "最喜欢的歌手/Favourite Artists":
            self.results.addResults(DB.getFavouriteArtists(self.searchBar.text()))
        elif self.heading == "搜索语言/Language Search":
            self.results.addResults(DB.getLanguages(self.searchBar.text()))
        elif self.heading == "搜索歌手/Artist Search":
            if self.pastResults:
                self.results.addResults(DB.getSongArtists(self.searchBar.text(), self.pastResults["language_id"]))
            else:
                self.results.addResults(DB.getSongArtists(self.searchBar.text()))
        elif self.heading == "搜索全部/Search":
            if self.pastResults:
                if self.pastResults["type"] == "artists":
                    self.results.addResults(DB.getSongTitles(self.searchBar.text(), artist=self.pastResults["artist_id"]))
                elif self.pastResults["type"] == "playlists":
                    self.results.addResults(DB.getSongTitles(self.searchBar.text(), playlist=self.pastResults["playlist_id"]))
            else:
                self.results.addResults(DB.getSongTitles(self.searchBar.text()))

    def goBack(self):
        if self.counter:
            self.window().content.setCurrentIndex(self.counter - 1)
            self.window().content.removeWidget(self)

    class ResultsList(QScrollArea):
        def __init__(self, parent=None):
            QScrollArea.__init__(self)
            self.setParent(parent)
            
            # Make QScrollArea transparent
            self.setStyleSheet("QScrollArea { background-color: transparent } .QFrame { background-color: transparent }")
            self.setWidgetResizable(True)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)

            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)

            frame = QFrame()
            frame.setLayout(self.layout)

            self.setWidget(frame)

        def clearResults(self):
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()

        def addResults(self, results):
            self.results = results
            self.clearResults()
            if results:
                for i in self.results:
                    item = self.ResultsListItem(i, self)
                    self.layout.addWidget(item)
                self.layout.addStretch(1)
            else:
                label = QLabel("没有结果/No Result")
                label.setStyleSheet("color: white")
                label.setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setPointSize(35)
                label.setFont(font)
                
                self.layout.addWidget(label)

        class ResultsListItem(QToolButton):
            def __init__(self, result, parent=None):
                QToolButton.__init__(self)
                self.setParent(parent)
                self.result = result

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

                if result["type"] == "songs":
                    self.formatTitle()
                    self.clicked.connect(self.clickedSong)
                elif result["type"] == "playlists":
                    self.formatPlaylist()
                    self.clicked.connect(self.clickedPlaylist)
                self.setLayout(self.layout)

            def formatTitle(self):
                labelQueue = self.formattedLabel(QLabel("", self))
                labelQueue.setFixedWidth(70)
                labelQueue.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(labelQueue)
                labelArtist = self.formattedLabel(QLabel(self.result["artist_name"]))
                labelArtist.setFixedWidth(300)
                self.layout.addWidget(labelArtist)
                labelTitle = self.formattedLabel(QLabel(self.result["song_title"]))
                self.layout.addWidget(labelTitle)
                # Add buttons for favourites and playlists
                self.favouriteButton = QToolButton()
                if self.result["favourited"] == 0:
                    self.favouriteButton.isFavourited = False
                    self.favouriteButton.setIcon(QIcon("icons/star.svg"))
                else:
                    self.favouriteButton.isFavourited = True
                    self.favouriteButton.setIcon(QIcon("icons/star-yellow.svg"))
                self.favouriteButton.setIconSize(QSize(30, 30))
                self.favouriteButton.setFixedSize(70, 70)
                self.favouriteButton.clicked.connect(self.clickedFavourite)
                self.layout.addWidget(self.favouriteButton)
                playlistButton = QToolButton()
                playlistButton.setIcon(QIcon("icons/music-player-2.svg"))
                playlistButton.setIconSize(QSize(30, 30))
                playlistButton.setFixedSize(70, 70)
                playlistButton.clicked.connect(self.addToPlaylist)
                self.layout.addWidget(playlistButton)

            def formatPlaylist(self):
                labelQueue = self.formattedLabel(QLabel("", self))
                labelQueue.setFixedWidth(70)
                labelQueue.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(labelQueue)
                labelPlaylist = self.formattedLabel(QLabel(self.result["playlist_name"]))
                self.layout.addWidget(labelPlaylist)
                btnRemove = QToolButton()
                btnRemove.setText("X")
                btnRemove.setFixedSize(70, 70)
                btnRemove.setStyleSheet("color: white")
                btnRemove.clicked.connect(self.removePlaylist)
                self.layout.addWidget(btnRemove)

            def formattedLabel(self, label):
                font = QFont()
                font.setPixelSize(25)
                # TODO: change with global themes
                label.setStyleSheet("color: white")
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setFont(font)
                return label

            def clickedSong(self):
                self.window().songQueue.addSong(self.result)

                if len(self.window().songQueue.getQueue()) < 2:
                    if not self.window().mediaPlayer.currentSong:
                        # If this is the first song to queue, signal media player to start it
                        self.window().mediaPlayer.skipSong()
                    self.window().mediaPlayer.updateMarquee()

            def clickedPlaylist(self):
                self.window().content.addWidget(WindowSearch("搜索全部/Search", self, self.window().content.currentWidget().counter + 1, self.result))
                self.window().content.setCurrentIndex(self.window().content.currentWidget().counter + 1)

            def clickedFavourite(self):
                if self.favouriteButton.isFavourited:
                    self.favouriteButton.isFavourited = False
                    self.favouriteButton.setIcon(QIcon("icons/star.svg"))
                else:
                    self.favouriteButton.isFavourited = True
                    self.favouriteButton.setIcon(QIcon("icons/star-yellow.svg"))
                DB.setFavouriteSong(self.result["song_id"])

            def addToPlaylist(self):
                popup = PlaylistPopup(self.result, self.window())
                popup.resize(1366, 768)
                popup.SIGNALS.CLOSE.connect(lambda: popup.close())
                popup.show()

            def removePlaylist(self):
                DB.removePlaylist(self.result["playlist_id"])
                self.window().content.currentWidget().results.results.remove(self.result)
                self.window().content.currentWidget().results.addResults(self.window().content.currentWidget().results.results)

    class ResultsGrid(QScrollArea):
        def __init__(self, parent=None):
            QScrollArea.__init__(self)
            self.setParent(parent)
            
            # Make QScrollArea transparent
            self.setStyleSheet("QScrollArea { background-color: transparent } .QFrame { background-color: transparent }")
            self.setWidgetResizable(True)
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            # Add Touch Gestures to menu.
            QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)

            self.layout = QGridLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)

            frame = QFrame()
            frame.setLayout(self.layout)

            self.setWidget(frame)

        def clearResults(self):
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                
        def addResults(self, results):
            self.clearResults()
            for i in range(len(results)):
                item = self.ResultsGridItem(results[i], self)
                self.layout.addWidget(item, i // 6, i % 6)
            if results:
                self.layout.setRowStretch(self.layout.rowCount(), 1)
                self.layout.setColumnStretch(self.layout.columnCount(), 1)
            else:
                label = QLabel("没有结果/No Result")
                label.setStyleSheet("color: white")
                label.setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setPointSize(35)
                label.setFont(font)
                
                self.layout.addWidget(label)

        class ResultsGridItem(QToolButton):
            def __init__(self, result, parent=None):
                QToolButton.__init__(self)
                self.setParent(parent)
                self.result = result

                self.setContentsMargins(0, 0, 0, 0)
                # Button formatting
                self.setFixedSize(200, 240)
                self.setAutoRaise(True)
                # TODO: change with global themes
                self.setStyleSheet("QToolButton:pressed { background-color: rgba(255, 255, 255, 0.1)} QToolButton { background-color: rgba(255, 255, 255, 0.05); border: 1px solid white; color: white}")

                self.layout = QGridLayout()
                self.layout.setContentsMargins(0, 0, 0, 0)
                self.layout.setSpacing(0)

                if result["type"] == "artists":
                    self.formattedImage(self.window().artistPath + result["artist_path"])
                    self.formattedLabel(result["artist_name"])
                    
                    self.favouriteButton = QToolButton()
                    self.favouriteButton.setStyleSheet("QToolButton:pressed { background-color: rgb(31, 41, 75)} QToolButton { background-color: rgb(25, 33, 60);}")
                    if self.result["favourited"] == 0:
                        self.favouriteButton.isFavourited = False
                        self.favouriteButton.setIcon(QIcon("icons/star.svg"))
                    else:
                        self.favouriteButton.isFavourited = True
                        self.favouriteButton.setIcon(QIcon("icons/star-yellow.svg"))
                    self.favouriteButton.setIconSize(QSize(30, 30))
                    self.favouriteButton.setFixedSize(70, 70)
                    self.favouriteButton.clicked.connect(self.clickedFavourite)
                    self.layout.addWidget(self.favouriteButton, 0, 0, Qt.AlignRight | Qt.AlignTop)
                    self.clicked.connect(self.clickedArtist)
                elif result["type"] == "languages":
                    self.formattedImage(self.window().languagePath + result["language_path"])
                    self.formattedLabel(result["language_name"])
                    self.clicked.connect(self.clickedLanguage)

                self.setLayout(self.layout)

            def clickedFavourite(self):
                if self.favouriteButton.isFavourited:
                    self.favouriteButton.isFavourited = False
                    self.favouriteButton.setIcon(QIcon("icons/star.svg"))
                else:
                    self.favouriteButton.isFavourited = True
                    self.favouriteButton.setIcon(QIcon("icons/star-yellow.svg"))
                DB.setFavouriteArtist(self.result["artist_id"])

            def formattedImage(self, path):
                self.setIcon(QIcon(path))
                self.setIconSize(QSize(180, 180))

            def formattedLabel(self, text):
                font = QFont()
                font.setPixelSize(18)
                self.setText(text)
                self.setFont(font)
                self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

            def clickedArtist(self):
                self.window().content.addWidget(WindowSearch("搜索全部/Search", self, self.window().content.currentWidget().counter + 1, self.result))
                self.window().content.setCurrentIndex(self.window().content.currentWidget().counter + 1)

            def clickedLanguage(self):
                print(self.parent())
                self.window().content.addWidget(WindowSearch("搜索歌手/Artist Search", self, self.window().content.currentWidget().counter + 1, self.result, grid=True))
                self.window().content.setCurrentIndex(self.window().content.currentWidget().counter + 1)