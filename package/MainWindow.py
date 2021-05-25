from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from .OverlayTop import OverlayTop
from .OverlayBottom import OverlayBottom
from .WindowHome import WindowHome
from package.components.DatabaseAccess import startUp
from package.components.SongQueue import SongQueue

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Database startup
        startUp()

        # Start Song Queue List
        self.songQueue = SongQueue()

        # Set the colour of the window
        self.setStyleSheet("MainWindow { background-color: rgb(25, 33, 60)}")

        # Create layout and set margins/spacings
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create overlays of the application
        self.overlayTop = OverlayTop(self)
        self.overlayBottom = OverlayBottom(self)

        # Add overlays to layout
        self.layout.addWidget(self.overlayTop, 0, 0)
        self.layout.addWidget(self.overlayBottom, 2, 0)

        # Create home page then add to layout
        self.content = WindowHome(self)
        self.layout.addWidget(self.content, 1, 0)

        # Create widget, then set layout to widget which gets added as central widget
        window = QWidget()
        window.setLayout(self.layout)
        self.setCentralWidget(window)

    def setMarquee(self, msg):
        # Sets the text of the marquee label
        # msg: (str/list) message(s) to be displayed]

        if type(msg) == list:
            # If msg is a list, change to workable string
            # TODO: Change the join bit when adding universal settings
            msg = "          ".join(msg)
        self.overlayTop.marqueeText.setText(msg)

    def changeWindow(self, widget):
        # removes the widget from the middle, then add a new one
        self.layout.removeWidget(self.content)
        self.content.close()
        self.content = widget
        self.layout.addWidget(self.content, 1, 0)
        self.layout.update()