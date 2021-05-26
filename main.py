import sys
from PySide6.QtWidgets import QApplication
from package.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.resize(1366,768)
    window.show()

    sys.exit(app.exec_())

