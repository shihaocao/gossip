from cmath import atan
from datetime import datetime
import sys
import socket
import threading
import time
from typing import List
from adversarial import get_random_attack

from state import State
from update_line import UpdateLine, IP, Port


TCP_TIMEOUT = 1


def adversarial_tcp_listener(state: State, local_port: int) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), local_port))
    serversocket.listen()

    while True:
        connection, client_address = serversocket.accept()

        attack = get_random_attack()

        connection.sendall(
            attack(state, client_address[0], client_address[1]).encode('utf-8'))
        connection.close()


def tcp_listener(state: State, local_port: int) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), local_port))
    serversocket.listen()

    while True:
        connection, client_address = serversocket.accept()
        connection.sendall(state.encode_state_as_bytes())
        connection.close()


def gossip(state: State, target_ip: str, target_port: int, initial_gossip: bool) -> None:
    if state.is_banned(target_ip, target_port):
        return

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.settimeout(TCP_TIMEOUT)
        serversocket.connect((target_ip, target_port))
    except:
        print(f"Failed to connect to {target_ip}:{target_port}")
        state.add_to_banned_set(target_ip, target_port)
        return

    start = time.time()
    buffer: bytes = bytes()
    MAX_BUFFER_SIZE = 65535
    while time.time() < start + 1:
        serversocket.settimeout(TCP_TIMEOUT)
        data: str = serversocket.recv(256)
        buffer += data
        if len(buffer) > MAX_BUFFER_SIZE:
            break

    buffer_as_str = buffer.decode('utf-8')
    lines_to_parse = buffer_as_str.splitlines()[:256]
    updates_to_print: List[str] = []

    for line in lines_to_parse:
        update_line = UpdateLine(line)
        if update_line.valid:
            updated: bool = state.update_node(update_line.ip,
                                              update_line.port,
                                              update_line.update_time,
                                              update_line.digit)
            new_state = state.get_node_state(
                update_line.ip, update_line.port, printable=True)

            if updated and new_state != None:
                updates_to_print.append(new_state)

    serversocket.close()

    # print the necessary updates
    if len(updates_to_print) > 0:
        if not initial_gossip:
            print()
        for update in updates_to_print:
            print(update)
        if not initial_gossip:
            print(">> ", end="", flush=True)


def gossiper(state: State) -> None:
    return_tuple = state.get_random_ip()
    if return_tuple:
        target_ip, target_port = return_tuple
        gossip(state, target_ip, target_port, initial_gossip=False)

    # run the gossiper again in 3 seconds
    threading.Timer(3, gossiper, args=(state,)).start()


def terminal_listener(state: State, local_port: int) -> None:
    while True:
        input_val: str = input(">> ")
        if input_val == "?":
            for state_value in state.get_state(printable=True):
                print(state_value)
            if len(state.banned_set) > 0:
                print('Banned Set:')
                for banned_ip, banned_port in state.banned_set:
                    print(f'   {banned_ip}:{banned_port}')

        elif len(input_val) == 1 and input_val.isdigit():
            state.update_self(int(datetime.now().timestamp()), int(input_val))

        elif input_val.startswith("+"):
            ip_and_port: List[str] = input_val[1:].split(':')

            # make sure ip and port are present
            if len(ip_and_port) != 2:
                continue

            target_ip: IP = IP(ip_and_port[0])
            target_port: Port = Port(ip_and_port[1])

            # make sure ip and port are valid
            if target_ip.ip == None or target_port.port == None:
                continue

            gossip(state, target_ip.ip, target_port.port, initial_gossip=True)


def main():
    args = sys.argv

    adversarial: bool

    if (len(args) == 2 and args[1].isdigit()):
        adversarial = False
    elif (len(args) == 3 and args[1].isdigit() and (args[2] == "--adversarial" or args[2] == '-a')):
        adversarial = True
    else:
        print("Usage: python main.py PORT")
        return

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    local_ip: str = socket.gethostbyname(socket.gethostname())
    local_port: int = int(sys.argv[1])

    serversocket.close()

    state: State = State(local_ip, local_port)

    thread1: threading.Thread
    if adversarial:
        thread1 = threading.Thread(
            target=adversarial_tcp_listener, args=(state, local_port))
    else:
        thread1 = threading.Thread(
            target=tcp_listener, args=(state, local_port))

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
