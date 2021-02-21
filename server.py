import argparse
import socketserver
import time


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        time.sleep(1.5)
        data = self.request.recv(1024)
        self.request.sendall(data.upper())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="bind to host")
    parser.add_argument("--port", type=int, help="bind to port")
    parser.add_argument("--packet-size", type=int, help="size of packets")
    HOST, PORT = "localhost", 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
