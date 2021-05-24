from PySide6.QtCore import QSize, QTime, QTimer, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QStackedWidget, QToolButton, QWidget
import time
from package.WindowSearch import WindowSearch

class OverlayTop(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setParent(parent)
        
        # Set the colour of the overlay
        self.setStyleSheet("QWidget { background-color: rgba(255, 255, 255, 0.05)}")

        # Set OverlayTop heights
        # TODO: Change heights with increasing resolution
        self.setFixedHeight(50)

        # Create layout with margins/spacings
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Initialise MarqueeText
        self.marqueeText = self.MarqueeText(self)
        layout.addWidget(self.marqueeText, 0, 0, 2, 1)
        
        # Initialise search button
        self.initButton()
        layout.addWidget(self.button, 0, 1, 2, 1)

        # Initialise elapsedTime/localTime
        self.initTimes()
        layout.addWidget(self.elapsedTime, 0, 2, 1, 1)
        layout.addWidget(self.localTime, 1, 2, 1, 1)
        
        self.setLayout(layout)

    def initButton(self):
        # Create the search button
        self.button = QToolButton()
        self.button.setFixedSize(100, 50)
        self.button.setIcon(QIcon("icons/search-1.svg"))
        self.button.setIconSize(QSize(30, 30))
        self.button.setAutoRaise(True)
        self.button.setStyleSheet("QToolButton:pressed { background-color: rgba(255, 255, 255, 0.1)}")
        # TODO: Connect button clicked action to search action
        self.button.clicked.connect(self.buttonTitle)

    def buttonTitle(self):
        stack = QStackedWidget(self)
        stack.addWidget(WindowSearch("搜索全部/Search"))
        self.window().changeWindow(stack)

    def initTimes(self):        
        # Create the local and elapsed times labels
        self.counter = 0
        self.elapsedTime = QLabel()
        self.localTime = QLabel()

        # Base font for colours
        font = QFont()
        font.setBold(True)
        font.setItalic(True)

        # Center labels, transparent backgrounds, fonts, and colours
        for x in [self.elapsedTime, self.localTime]:
            # TODO: Scale times with app resize
            x.setFixedWidth(100)
            x.setAlignment(Qt.AlignCenter)
            x.setFont(font)
            x.setStyleSheet("color: rgb(255, 255, 255)")

        # Start the elapsedTime timer
        timer = QTimer(self)
        timer.timeout.connect(self.updateTimes)
        # Call updateTimes first to get the times displayed on startUp
        self.updateTimes()
        timer.start(500)

    def updateTimes(self):
        # function which is called to update labels
        self.elapsedTime.setText(time.strftime('%H:%M:%S', time.gmtime(self.counter // 2)))
        self.localTime.setText("{}{}{} {}".format(str(QTime.currentTime().hour() % 12).zfill(2) if QTime.currentTime().hour() % 12 != 0 else "12", ":" if self.counter % 2 == 0 else " ", str(QTime.currentTime().minute()).zfill(2), "PM" if QTime.currentTime().hour() >= 12 else "AM"))
        self.counter = self.counter % (2*86400) + 1

    class MarqueeText(QScrollArea):
        def __init__(self, parent=None):
            QScrollArea.__init__(self)
            self.setParent(parent)

            # Set the background colour of the marquee text to white
            self.setStyleSheet("QScrollArea { background-color: rgba(255, 255, 255, 1)}")

            # Initialise the base label and text
            self.label = QLabel()

            # Set the font for marquee
            font = QFont()
            font.setItalic(True)
            font.setBold(True)
            font.setPixelSize(25)
            self.label.setFont(font)

            # Set the base label as the base widget of QScrollArea
            self.setWidget(self.label)

            # Set QScrollBar Policies
            self.setWidgetResizable(True)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Initialise timer and associated variables, used for marquee effect
            self.timer = QTimer(self)
            self.x = 0
            self.speed = 0
            
            # Connect a function to the timer, which controls the marquee effect
            self.timer.timeout.connect(self.updatePos)

            # TODO: Set a nominal speed
            self.setSpeed(33)

        def updatePos(self):
            self.x = (self.x + 1) % self.label.fontMetrics().horizontalAdvance(self.label.text())
            self.horizontalScrollBar().setValue(self.x)

        def setText(self, text):
            # Sets the text of the marquee label
            # text: (str) the text to be displayed

            # TODO: Change the separator bit when adding universal settings
            text = text + "          "

            # First need the widths of the current label windowspace and the text itself
            windowWidth = self.window().geometry().width()
            textWidth = self.label.fontMetrics().horizontalAdvance(text)
            # Concatenate the text on itself as many times as needed.
            self.label.setText(text + (text * (windowWidth // textWidth + (windowWidth % textWidth > 0))))

            # Finally, start the timer to start the effect
            self.timer.start(self.timer.interval())

        def setSpeed(self, speed):
            # Sets the speed of the scroll
            # speed: (int) how many pixels to move per second

            # Reset the timer with new interval.
            self.timer.setInterval(1000 / speed)