import argparse
import socketserver
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="bind to host")
    parser.add_argument("--port", type=int, help="bind to port")
    parser.add_argument("--packet-size", type=int, help="size of packets")
    args = parser.parse_args()
    HOST, PORT = args.host, args.port

    class MyTCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            time.sleep(1.5)
            data = self.request.recv(args.packet_size)
            self.request.sendall(data.upper())

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
