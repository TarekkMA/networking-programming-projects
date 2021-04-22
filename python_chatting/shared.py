import socket
import sys
import threading
from typing import ClassVar, List

BUFFSIZE = 1024
ENCODING = 'utf-8'

def get_host_port_from_argv():
  if len(sys.argv) != 2:
    print('You must pass the server port')
    exit()
  return 'localhost', int(sys.argv[1])

class Client:
  connection: socket.socket
  nickname: str
  listen_thread: threading.Thread

  def __init__(self, connection: socket.socket, nickname: str) -> None:
    self.connection = connection
    self.nickname = nickname

  def connect(self, host, port):
    self.connection.connect((host, port))
    listen_thread = threading.Thread(target=Client._listen_loop, args=(self,))
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


class Server:
  # static counter used for naming clients
  client_name_counter: int = 0
  connected_clients: List[Client] = []
  connection: socket.socket

  def __init__(self) -> None:
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self, host, port) -> None:
    self.connection.connect((host, port))

  def serve(self, host, port) -> None:
    self.connection.bind((host, port))
    self.connection.listen(100)
    self._client_loop()

  def _client_loop(self) -> None:
    while True:
      client_connection, address = self.connection.accept()
      print(f'[LOG] client with {address} is connected')
      Server.client_name_counter += 1
      nickname = f'Client {Server.client_name_counter}'
      client = Client(client_connection, nickname)
      client.send(f'[SERVER] Your nickname is {nickname}')
      self.connected_clients.append(client)
      threading.Thread(target=Server._client_listen_loop,
                       args=(self, client,)).start()

  def broadcast(self, message, exceptionList: List[Client] = []) -> None:
    for client in self.connected_clients:
      if client not in exceptionList:
        try:
          client.send(message)
        except:
          client.connection.close()
          self.connected_clients.remove(client)
          self.broadcast(f'[SERVER] {client.nickname} is no longer connected')

  def _client_listen_loop(self, client: Client) -> None:
    while True:
      try:
        message = client.connection.recv(BUFFSIZE).decode(ENCODING)
        print(f'[LOG] recived "{message}" from "{client.nickname}"')
        if message.startswith('/'):
          self._handle_command(client, message)
        else:
          self.broadcast(f'{client.nickname} > {message}', [client])
      except:
        continue

  def _handle_command(self, client: Client, command: str):
    try:
      if command.startswith('/'):
        command = command[1:]
        parts = command.split(' ')

        if parts[0] == 'nick':
          new_nick = parts[1]
          if new_nick in [c.nickname for c in self.connected_clients]:
            client.send('[SERVER] This nickname is already taken')
            return
          old_nick = client.nickname
          client.nickname = new_nick
          client.send(f'[SERVER] Your nickname is now {new_nick}')
          self.broadcast(
              f'[SERVER] "{old_nick}" changed nickname to "{new_nick}"')
          return
    except:
      pass
    client.send('[SERVER] Cannot handle your last command')
