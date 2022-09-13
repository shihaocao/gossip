from collections import defaultdict
from typing import Dict, List, Tuple

import random
random.seed(123)

class DataPoint:
    time: int
    digit: int
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

    def get_random_ip(self) -> Tuple[str, int]:
        random_ip = random.choice([self.ip_map.keys()])
        random_port = random.choice([self.ip_map[random_ip]])

        return random_ip, random_port
    
    def _get_node_as_str(self, ip: str, port: int) -> str:
        data_point = self.ip_map[ip][port]
        return f"{ip}:{port},{data_point.time},{data_point.digit}"

    def get_state(self) -> List[str]:
        
        return_list = []
        for ip, port_map in self.ip_map.items():
            for port in port_map.keys():
                return_list.append(self._get_node_as_str(ip, port))
        
        return return_list
