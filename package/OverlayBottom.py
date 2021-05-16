from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSizePolicy, QToolButton, QWidget, QHBoxLayout

class OverlayBottom(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setParent(parent)

        # Set the colour of the overlay
        self.setStyleSheet("QWidget { background-color: rgba(255, 255, 255, 0.05)}")

        # Set OverlayBottom heights
        # TODO: Change heights with increasing resolution
        self.setFixedHeight(100)

        # Create layout with margins/spacings
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Initialise buttons
        buttons = []
        args = ["home", "user", "windows", "back", "play-button", "next"]
        for i in args:
            button = QToolButton()
            button.setIcon(QIcon("icons/{}.svg".format(i)))
            button.setAutoRaise(True)
            button.setStyleSheet("QToolButton:pressed { background-color: rgba(255, 255, 255, 0.1)}")
            buttons.append(button)

        # TODO: Solve this. Lambda functions cannot be used in loops. This is a stupid workaround
        buttons[0].clicked.connect(lambda: self.buttonAction(args[0]))
        buttons[1].clicked.connect(lambda: self.buttonAction(args[1]))
        buttons[2].clicked.connect(lambda: self.buttonAction(args[2]))
        buttons[3].clicked.connect(lambda: self.buttonAction(args[3]))
        buttons[4].clicked.connect(lambda: self.buttonAction(args[4]))
        buttons[5].clicked.connect(lambda: self.buttonAction(args[5]))

        # Add blank widget to start and end to group and center buttons (pt1)
        layout.addWidget(QWidget())

        # Set IconSize, widths, and SizePolicy of each button. Then proceed to add to layout
        for x in buttons:
            x.setIconSize(QSize(35, 35))
            # TODO: Scale with resize
            x.setFixedWidth(150)
            x.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            layout.addWidget(x)

        # Add blank widget to start and end to group and center buttons (pt2)
        layout.addWidget(QWidget())

        self.setLayout(layout)

    def buttonAction(self, i):
        # Pythonic switch-case

        def buttonHome(self):
            pass

        def buttonVocal(self):
            pass

        def buttonQueue(self):
            pass

        def buttonRestart(self):
            pass

        def buttonPlay(self):
            pass

        def buttonSkip(self):
            pass

        switcher = {
            "home": buttonHome,
            "user": buttonVocal,
            "windows": buttonQueue,
            "back": buttonRestart,
            "play-button": buttonPlay,
            "next": buttonSkip
        }
        func = switcher.get(i, buttonHome)
        func(self)