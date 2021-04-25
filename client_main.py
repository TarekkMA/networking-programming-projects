from shared import Client, Server, get_host_port_from_argv

if __name__ == "__main__":
  host, port = get_host_port_from_argv()
  client = Client(None)
  client.connect(host, port)
