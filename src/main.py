import sys
import socket
import threading

from state import State


def tcp_listener(state: State, port: int) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), port))
    serversocket.listen()

    while True:
        connection, client_address = serversocket.accept()
        connection.sendall(state.get_state())
        connection.close()


def gossiper(state: State, port: int) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), port))

    serversocket.connect(state.get_random_ip())
    data: str = serversocket.recv()

    for line in data.splitlines():
        values: list[str] = line.split(",")
        ip_values: list[str] = values[0].split(":")

        node_ip: str = ip_values[0]
        node_port: int = int(ip_values[1])
        time: int = int(values[1])
        digit: int = int(values[2])

        state.update_node(node_ip, node_port, time, digit)

    # run the gossiper again in 3 seconds
    threading.Timer(3, gossiper).start()


def terminal_listener(state: State) -> None:
    pass


def main():
    args = sys.argv

    if (len(args) != 1 or type(args[0]) != int):
        print("Usage: python main.py PORT")
        return

    port: int = sys.argv[0]

    state: State = state()

    thread1 = threading.Thread(target=tcp_listener, args=(state, port))
    thread2 = threading.Thread(target=gossiper, args=(state, port))
    thread3 = threading.Thread(target=terminal_listener, args=(state))

    thread1.start()
    thread2.start()
    thread3.start()


if __name__ == "__main__":
    main()
