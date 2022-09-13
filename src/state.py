from typing import Dict, List


class State:

    ip_map: Dict[str, int]

    def __init__(self):
        self.ip_map = map()

    def add_node(ip: str, port: int):
        pass

    def add_node_with_data(ip: str, port: int, time: int, digit: int):
        pass

    def update_node(ip: str, port: int, time: int, digit: int):
        pass

    def get_random_ip() -> str:
        pass

    def get_state() -> List[str]:
        pass
