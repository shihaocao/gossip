from collections import defaultdict
from typing import Dict, List

class DataPoint:
    time: int
    data: int
    def __init__(self, time: int, digit: int):
        self.time = time
        self.digit = digit
    

class State:

    ip_map: Dict[str, Dict[int, DataPoint]]

    def __init__(self):
        self.ip_map = defaultdict({})

    def add_node(self, ip: str, port: int):
        self.ip_map[ip][port] = None
        pass

    def add_node_with_data(self, ip: str, port: int, time: int, digit: int):
        self.ip_map[ip][port] = DataPoint(time, digit)
        pass

    def update_node(self, ip: str, port: int, time: int, digit: int):
        self.ip_map[ip][port] = DataPoint(time, digit)
        pass

    def get_random_ip(self) -> str:
        pass

    def get_state() -> List[str]:
        pass
