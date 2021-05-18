from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QVBoxLayout, QWidget, QScrollArea, QSizePolicy, QToolButton, QHBoxLayout
import package.DatabaseAccess as DB

class SearchTemplate(QWidget):
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
                sublabel.setText("Langauge: " + self.pastResults["language_name"])
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
            self.results = self.ResultsList(self)
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
        elif self.heading == "最喜欢的/Favourites":
            self.results.addResults(DB.getFavourites(self.searchBar.text()))
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
    
    def songClicked(self):
        print("songClicked")

    class ResultsList(QScrollArea):
        def __init__(self, parent=None):
            QScrollArea.__init__(self)
            self.setParent(parent)
            
            # Make QScrollArea transparent
            self.setStyleSheet("QScrollArea { background-color: transparent }")
            self.setWidgetResizable(True)

            self.layout = QVBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)

            self.setLayout(self.layout)

        def clearResults(self):
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()

        def addResults(self, results):
            self.clearResults()
            for i in results:
                item = self.ResultsListItem(i, self)
                self.layout.addWidget(item)
            if results:
                self.layout.addStretch(1)
            else:
                label = QLabel("没有结果/No Result")
                label.setStyleSheet("color: white")
                label.setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setPointSize(35)
                label.setFont(font)
                
                self.layout.addWidget(label)
        
        def songClicked(self):
            pass

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

                if result["type"] == "songs":
                    self.formatTitle(result)
                    self.clicked.connect(lambda: self.parent().parent().songClicked(result, self.parent().parent().pastResults))
                elif result["type"] == "playlists":
                    self.formatPlaylist(result)
                    self.clicked.connect(self.clickedPlaylist)

                self.setLayout(self.layout)

            def formatTitle(self, result):
                labelTitle = self.formattedLabel(QLabel(result["song_title"]))
                labelArtist = self.formattedLabel(QLabel(result["song_artist"]))
                labelArtist.setFixedWidth(100)
                self.layout.addWidget(labelTitle)
                self.layout.addWidget(labelArtist)

            def formatPlaylist(self, result):
                labelPlaylist = self.formattedLabel(QLabel(result["playlist_name"]))
                self.layout.addWidget(labelPlaylist)

            def formattedLabel(self, label):
                font = QFont()
                font.setPixelSize(25)
                # TODO: change with global themes
                label.setStyleSheet("color: white")
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setFont(font)
                return label

            def clickedPlaylist(self):
                self.window().content.addWidget(SearchTemplate("搜索全部/Search", self, self.parent().parent().counter + 1, self.result))
                self.window().content.setCurrentIndex(self.parent().parent().counter + 1)

    class ResultsGrid(QScrollArea):
        def __init__(self, parent=None):
            QScrollArea.__init__(self)
            self.setParent(parent)
            
            # Make QScrollArea transparent
            self.setStyleSheet("QScrollArea { background-color: transparent }")
            self.setWidgetResizable(True)

            self.layout = QGridLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)

            self.setLayout(self.layout)

        def clearResults(self):
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                
        def addResults(self, results):
            self.clearResults()
            col = 0
            row = 0
            for i in range(results):
                item = self.ResultsGridItem(results[i], self)
                self.layout.addWidget(item, i // 4, i % 4)
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

                # Button formatting
                self.setFixedSize(300, 300)
                self.setAutoRaise(True)
                # TODO: change with global themes
                self.setStyleSheet("QToolButton:pressed { background-color: rgba(255, 255, 255, 0.1)} QToolButton { background-color: rgba(255, 255, 255, 0.05); border: 1px solid white}")

                # Set layout
                self.layout = QHBoxLayout()

                if result["type"] == "artists":
                    self.formattedImage(result["artist_path"])
                    self.formattedLabel(result["artist_name"])
                    self.clicked.connect(self.clickedArtist)
                elif result["type"] == "langauges":
                    self.formattedImage(result["language_path"])
                    self.formattedLabel(result["language_name"])
                    self.clicked.connect(self.clickedLanguage)

                self.setLayout(self.layout)

            def formattedImage(self, path):
                image = QPixmap(path)
                image.scaled(250, 250)
                self.layout.addWidget(image)

            def formattedLabel(self, text):
                label = QLabel(text)
                font = QFont()
                font.setPixelSize(30)
                # TODO: change with global themes
                label.setStyleSheet("color: white")
                label.setAlignment(Qt.AlignCenter)
                label.setFont(font)
                self.layout.addWidget(label)

            def clickedArtist(self):
                self.window().content.addWidget(SearchTemplate("搜索全部/Search", self, self.parent().parent().counter + 1, self.result))
                self.window().content.setCurrentIndex(self.parent().parent().counter + 1)

            def clickedLanguage(self):
                self.window().content.addWidget(SearchTemplate("搜索歌手/Artist Search", self, self.parent().parent().counter + 1, self.result))
                self.window().content.setCurrentIndex(self.parent().parent().counter + 1)