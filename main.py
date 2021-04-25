from argparse import ArgumentParser
from enum import Enum
from operator import attrgetter
from shared import Client, Server

class ApplicationType(Enum):
  CLIENT = 'client'
  SERVER = 'server'

  def __str__(self):
    return self.value

  @staticmethod
  def from_string(s):
    try:
      return ApplicationType[s]
    except KeyError:
      raise ValueError()


def parse_args():
  parser = ArgumentParser(description='Chatting program')

  parser.add_argument('type', type=ApplicationType,
                      choices=list(ApplicationType))
  parser.add_argument('-p, --port', type=int, default=8080,
                      help='server port', dest='port')

  return parser.parse_args()


if __name__ == "__main__":
  type, port = attrgetter('type', 'port')(parse_args())
  host = 'localhost'

  if type == ApplicationType.SERVER:
    server = Server()
    server.serve(host, port)
  elif type == ApplicationType.CLIENT:
    client = Client()
    client.connect(host, port)
