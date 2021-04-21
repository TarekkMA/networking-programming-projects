from shared import Client, Server, get_host_port_from_argv

if __name__ == "__main__":
  host, port = get_host_port_from_argv()
  server = Server()
  client = Client(server.connection, None)
  client.connect(host, port)
