from .client import Client
import socket
from typing import List
from .constants import BUFFSIZE, ENCODING
from threading import Thread


class Server:
    client_name_counter: int = 0
    connected_clients: List[Client] = []
    connection: socket.socket
    client_loop_thread: Thread

    def __init__(self) -> None:
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port) -> None:
        self.connection.connect((host, port))

    def serve(self, host, port) -> None:
        self.connection.bind((host, port))
        self.connection.listen(100)
        self.client_loop_thread = Thread(target=self._client_loop)
        self.client_loop_thread.start()

    def _client_loop(self) -> None:
        while True:
            client_connection, address = self.connection.accept()
            print(f"[LOG] client with {address} is connected")
            Server.client_name_counter += 1
            nickname = f"Client {Server.client_name_counter}"
            client = Client(client_connection, nickname)
            client.send(f"[SERVER] Your nickname is {nickname}")
            self.connected_clients.append(client)
            t = Thread(
                target=Server._client_listen_loop,
                args=(
                    self,
                    client,
                ),
            )
            t.start()

    def broadcast(self, message, exceptionList: List[Client] = []) -> None:
        for client in self.connected_clients:
            if client not in exceptionList:
                try:
                    client.send(message)
                except:
                    client._connection.close()
                    self.connected_clients.remove(client)
                    self.broadcast(f"[SERVER] {client.nickname} is no longer connected")

    def _client_listen_loop(self, client: Client) -> None:
        while True:
            try:
                recv_bytes = client._connection.recv(BUFFSIZE)
                if recv_bytes == b"":
                    self.broadcast(f"{client.nickname} > left the chat", [client])
                    print(f'[LOG] "{client.nickname}" Left')
                    break
                message = recv_bytes.decode(ENCODING)
                print(f'[LOG] recived "{message}" from "{client.nickname}"')
                if message.startswith("/"):
                    self._handle_command(client, message)
                else:
                    self.broadcast(f"{client.nickname} > {message}", [client])
            except:
                continue

    def _handle_command(self, client: Client, command: str):
        try:
            if command.startswith("/"):
                command = command[1:]
            parts = command.split(" ")

            if parts[0] == "nick":
                new_nick = parts[1]
                if new_nick in [c.nickname for c in self.connected_clients]:
                    client.send("[SERVER] This nickname is already taken")
                    return
                old_nick = client.nickname
                client.nickname = new_nick
                client.send(f"[SERVER] Your nickname is now {new_nick}")
                self.broadcast(
                    f'[SERVER] "{old_nick}" changed nickname to "{new_nick}"'
                )
                return
        except:
            pass
        client.send("[SERVER] Cannot handle your last command")

    def wait(self):
        self.client_loop_thread.join()

    def terminate(self):
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()
