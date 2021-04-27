from cli.common import do_after_sigint
from core.client import Client


class CliClient:
    _client: Client
    _host: str
    _port: int

    def __init__(self, client: Client, host: str, port: int) -> None:
        self._client = client
        self._host = host
        self._port = port

    def _reciver_callback(self, message: str):
        print(f"\r{message}")

    def start(self):
        self._client.connect(self._host, self._port)
        self._client.register_recive_callback(self._reciver_callback)
        do_after_sigint(self._client.terminate)
        self._input_loop()

    def _input_loop(self):
        while True:
            message = input()
            self._client.send(message)
