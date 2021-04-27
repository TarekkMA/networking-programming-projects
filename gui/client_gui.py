from PySide2.QtGui import QStandardItem, QStandardItemModel
from core.client import Client
from PySide2.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import sys


class GuiClient:
    _host: str
    _port: int
    _client: Client

    def __init__(self, client: Client, host: str, port: int) -> None:
        self._client = client
        self._host = host
        self._port = port

    def start(self):
        app = QApplication(sys.argv)
        self._client.connect(self._host, self._port)
        window = GuiClientWindow(self._client)
        window.show()
        app.exec_()
        sys.exit(0)


class GuiClientWindow(QWidget):
    _client: Client
    _editor: QLineEdit
    _send_btn: QPushButton
    _chat_list: QListView
    _chat_history_model: QStandardItemModel

    def __init__(self, client: Client) -> None:
        super().__init__()
        self._client = client
        self._client.register_recive_callback(self._reciver_callback)
        self.setWindowTitle("Python Chatting Application")
        self.setGeometry(0, 0, 400, 600)
        self.center_window()
        box = QVBoxLayout(self)

        self._chat_history_model = QStandardItemModel()
        self._chat_list = QListView(self)
        box.addWidget(self._chat_list)
        self._chat_list.setModel(self._chat_history_model)

        text_box = QHBoxLayout(self)
        self._editor = QLineEdit(self)
        self._editor.returnPressed.connect(self.send)
        self._send_btn = QPushButton("Send", self)
        self._send_btn.clicked.connect(self.send)
        text_box.addWidget(self._editor)
        text_box.addWidget(self._send_btn)

        box.addLayout(text_box)

    def send(self):
        message = self._editor.text().strip()
        if message == "":
            return
        self._client.send(message)
        self._editor.clear()

    def _reciver_callback(self, message: str):
        self._chat_history_model.appendRow(QStandardItem(message))

    def closeEvent(self, event):
        print("Closing sockt")
        self._client.terminate()

    def center_window(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())
