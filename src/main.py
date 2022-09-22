from datetime import datetime
import sys
import socket
import threading
import time
from typing import List

from state import State
from update_line import UpdateLine, IP, Port


def tcp_listener(state: State, local_port: int) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), local_port))
    serversocket.listen()

    while True:
        connection, client_address = serversocket.accept()
        connection.sendall(state.encode_state_as_bytes())
        connection.close()


def gossip(state: State, target_ip: str, target_port: int) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect((target_ip, target_port))

    start = time.time()
    buffer: bytes = bytes()
    MAX_BUFFER_SIZE = 65535
    while time.time() < start + 1:
        data: str = serversocket.recv(256)
        buffer += data
        if len(buffer) > MAX_BUFFER_SIZE:
            break

    buffer_as_str = buffer.decode('utf-8')

    for line in buffer_as_str.splitlines():
        update_line = UpdateLine(line)
        if update_line.valid:
            state.update_node(update_line.ip,
                              update_line.port,
                              update_line.update_time,
                              update_line.digit)


def gossiper(state: State) -> None:
    return_tuple = state.get_random_ip()
    if return_tuple:
        target_ip, target_port = return_tuple
        gossip(state, target_ip, target_port)

    # run the gossiper again in 3 seconds
    threading.Timer(3, gossiper, args=(state,)).start()


def terminal_listener(state: State, local_port: int) -> None:
    while True:
        input_val: str = input(">> ")
        if input_val == "?":
            for state_value in state.get_state():
                print(state_value)

        elif len(input_val) == 1 and input_val.isdigit():
            state.update_self(int(datetime.now().timestamp()), int(input_val))

        elif input_val.startswith("+"):
            ip_and_port: List[str] = input_val[1:].split(':')

            # make sure ip and port are present
            if len(ip_and_port) != 2:
                return

            target_ip: IP = IP(ip_and_port[0])
            target_port: Port = Port(ip_and_port[1])

            # make sure ip and port are valid
            if target_ip.ip == None or target_port.port == None:
                return

            gossip(state, target_ip.ip, target_port.port)


def main():
    args = sys.argv

    if (len(args) != 2 or not args[1].isdigit()):
        print("Usage: python main.py PORT")
        return

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    local_ip: str = socket.gethostbyname(socket.gethostname())
    local_port: int = int(sys.argv[1])

    serversocket.close()

    state: State = State(local_ip, local_port)

    thread1 = threading.Thread(target=tcp_listener, args=(state, local_port))
    thread2 = threading.Thread(target=gossiper, args=(state,))
    thread3 = threading.Thread(
        target=terminal_listener, args=(state, local_port))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


if __name__ == "__main__":
    main()
