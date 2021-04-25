from shared import Server, get_host_port_from_argv

if __name__ == "__main__":
  host, port = get_host_port_from_argv()
  server = Server()
  server.serve(host, port)


def other(self, a, b):
  return a + b

Server.other = other