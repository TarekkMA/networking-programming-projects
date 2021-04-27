import socket
from typing import Callable
from .constants import BUFFSIZE, ENCODING
from threading import Thread


class Client:
    _connection: socket.socket
    nickname: str
    _recive_thread: Thread
    _recive_callback: Callable[[str], None] = None

    def __init__(self, connection: socket.socket = None, nickname: str = None) -> None:
        if connection is None:
            self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._connection = connection
        self.nickname = nickname

    def connect(self, host, port):
        self._connection.connect((host, port))
        self._recive_thread = Thread(
            target=self._listen_loop,
        )
        self._recive_thread.start()

    def register_recive_callback(self, callback: Callable[[str], None]):
        self._recive_callback = callback

    def _listen_loop(self):
        while True:
            recv_bytes = self._connection.recv(BUFFSIZE)
            if recv_bytes == b"":
                break
            message = recv_bytes.decode(ENCODING)
            if self._recive_callback is not None:
                self._recive_callback(message)

    def send(self, message):
        if isinstance(message, str):
            message = message.encode(ENCODING)
        self._connection.send(message)

    def terminate(self):
        self._connection.shutdown(socket.SHUT_RDWR)
        self._connection.close()
