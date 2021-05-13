from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget
from .OverlayTop import OverlayTop

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Create layout and set margins/spacings
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create overlays of the application
        self.overlayTop = OverlayTop(self)

        # Add overlays to layout
        self.layout.addWidget(self.overlayTop, 0, 0)

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