import socket
from .constants import BUFFSIZE, ENCODING
from threading import Thread

class Client:
  connection: socket.socket
  nickname: str
  listen_thread: Thread
  input_thread: Thread

  def __init__(self, connection: socket.socket = None, nickname: str = None) -> None:
    if connection == None:
      self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
      self.connection = connection
    self.nickname = nickname

  def connect(self, host, port):
    self.connection.connect((host, port))
    self.listen_thread = Thread(target=self._listen_loop,)
    self.input_thread = Thread(target=self._input_loop,)
    self.listen_thread.start()
    self.input_thread.start()

  def wait(self):
    self.input_thread.join()
    self.listen_thread.join()

  def _input_loop(self):
    while True:
      message = input('>')
      self.send(message)

  def _listen_loop(self):
    while True:
      recv_bytes = self.connection.recv(BUFFSIZE)
      if recv_bytes == b'':
        break
      message = recv_bytes.decode(ENCODING)
      print(message)

  def send(self, message):
    if isinstance(message, str):
      message = message.encode(ENCODING)
    self.connection.send(message)

  def terminate(self):
    self.connection.shutdown(socket.SHUT_RDWR)
    self.connection.close()
