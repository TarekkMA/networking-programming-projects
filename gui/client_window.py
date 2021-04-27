from PySide2.QtWidgets import QApplication, QWidget
import sys


def show_gui_client():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
    sys.exit(0)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Python Chatting Application")
        self.setGeometry(300, 300, 300, 300)
