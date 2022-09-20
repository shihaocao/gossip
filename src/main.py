from datetime import datetime
from symbol import return_stmt
from typing import List
import sys
import socket
import threading
import time

from state import State


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
    # serversocket.bind((socket.gethostbyname(socket.gethostname()), local_port))

    serversocket.connect((target_ip, target_port))
    
    start = time.time()
    buffer: bytes = bytes()
    while time.time() < start + 1:
        data: str = serversocket.recv(256)
        # print(type(data))
        buffer += data

    buffer_as_str = buffer.decode('utf-8')

    for line in buffer_as_str.splitlines():
        values: list[str] = line.split(",")
        ip_values: list[str] = values[0].split(":")

        node_ip: str = ip_values[0]
        node_port: int = int(ip_values[1])
        update_time: int = int(values[1])
        digit: int = int(values[2])

        state.update_node(node_ip, node_port, update_time, digit)


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
            # TODO add validation
            ip_and_port: List[str] = input_val[1:].split(':')
            target_ip = ip_and_port[0]
            target_port = int(ip_and_port[1])

            gossip(state, target_ip, target_port)


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
