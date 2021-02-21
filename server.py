import socketserver
import time


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        time.sleep(1.5)
        data = self.request.recv(1024)
        self.request.sendall(data.upper())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
