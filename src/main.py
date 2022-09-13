import threading


def tcp_listener():
    pass


def gossiper():
    pass


def terminal_listener():
    pass


def main():
    thread1 = threading.Thread(target=tcp_listener, args=())
    thread2 = threading.Thread(target=gossiper, args=())
    thread3 = threading.Thread(target=terminal_listener, args=())

    thread1.start()
    thread2.start()
    thread3.start()


if __name__ == "__main__":
    main()
