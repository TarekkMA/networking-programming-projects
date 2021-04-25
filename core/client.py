import socket
from .constants import BUFFSIZE, ENCODING
from threading import Thread

class Client:
  connection: socket.socket
  nickname: str
  listen_thread: Thread

  def __init__(self, connection: socket.socket = None, nickname: str = None) -> None:
    if connection == None:
      self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
      self.connection = connection
    self.nickname = nickname

  def connect(self, host, port):
    self.connection.connect((host, port))
    listen_thread = Thread(target=Client._listen_loop, args=(self,))
    listen_thread.start()
    self._input_loop()

  def _input_loop(self):
    while True:
      message = input('>')
      self.send(message)

  def _listen_loop(self):
    while True:
      message = self.connection.recv(BUFFSIZE).decode(ENCODING)
      print(message)

  def send(self, message):
    if isinstance(message, str):
      message = message.encode(ENCODING)
    self.connection.send(message)

