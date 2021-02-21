import argparse
import multiprocessing as mp
import os
import socket
import time
from threading import Thread


class PacketMaker(mp.Process):
    def __init__(self, result_queue, max_packets=1, packet_size=1, num_poison_pills=1):
        mp.Process.__init__(self)
        self.result_queue = result_queue
        self.max_packets = max_packets
        self.packet_size = packet_size
        self.num_poison_pills = num_poison_pills
        self.num_packets_made = 0

    def run(self):
        while True:
            if self.num_packets_made >= self.max_packets:
                for _ in range(self.num_poison_pills):
                    self.result_queue.put(None, timeout=1)
                return
            self.result_queue.put(os.urandom(self.packet_size), timeout=1)
            self.num_packets_made += 1


class PacketSender(Thread):
    def __init__(self, task_queue, result_queue, addr, packet_size):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.server_addr = addr
        self.packet_size = packet_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)

    def run(self):
        while True:
            packet = self.task_queue.get(timeout=1)
            if packet is None:
                return
            try:
                self.sock.sendall(packet)
                response = self.sock.recv(self.packet_size)
            except socket.error:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(self.server_addr)
                self.sock.sendall(packet)
                response = self.sock.recv(self.packet_size)
            self.result_queue.put(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-packets', type=int, help='number of packets to send')
    parser.add_argument('--packet-size', type=int, help='packet size in bytes')
    parser.add_argument('--num-threads', type=int, help='number of threads sending packets')
    parser.add_argument('--host', type=str, help='name of host packets will be sent to')
    parser.add_argument('--port', type=int, help='port number of host packets will be sent to')
    args = parser.parse_args()

    packets_to_send = mp.Queue(args.num_packets + args.num_threads)
    packets_received = mp.Queue(args.num_packets)
    producers = [PacketMaker(packets_to_send, args.num_packets, args.packet_size, args.num_threads)]
    senders = [PacketSender(packets_to_send, packets_received, (args.host, args.port), args.packet_size)
               for _ in range(args.num_threads)]
    start_time = time.time()
    for worker in senders + producers:
        worker.start()
    for worker in senders:
        worker.join()
    end_time = time.time()
    print(f"{packets_received.qsize()} packets received in {end_time - start_time} seconds")
