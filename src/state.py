from collections import defaultdict
from typing import Dict, List, Tuple

import random
import time
import threading

random.seed(123)

class DataPoint:
    data_time: int
    digit: int
    def __init__(self, data_time: int, digit: int):
        self.data_time = data_time
        self.digit = digit



class State:

    ip_map: Dict[str, Dict[int, DataPoint]]
    lock: threading.Lock

    def __init__(self):
        self.ip_map = defaultdict({})
        self.banned_set = set()
        self.lock = threading.Lock()

    def update_node(self, ip: str, port: int, data_time: int, digit: int):
        
        if data_time > int(time.time()):
            # time is in the future, reject
            return
        
        self.lock.acquire()
        
        if (ip, port) in self.banned_set:
            # reject if banned
            return
                
        if port in self.ip_map[ip]:
            existing_data_point = self.ip_map[ip][port]
            if data_time > existing_data_point.data_time:
                # valid newer time, perform update
                self.ip_map[ip][port] = DataPoint(data_time, digit)

        else:
            # data is not pre-existing so add to state
            self.ip_map[ip][port] = DataPoint(data_time, digit)

            port_data_point_pairs = self.ip_map[ip].items()
            if len(port_data_point_pairs) > 3:
                # too many saved ports, eject the stalest

                stalest_time = 1700000000
                stalest_port = 0
                
                for port, data_point in port_data_point_pairs:
                    if data_point.data_time < stalest_time:
                        stalest_time = data_point.data_time
                        stalest_port = port
                
                self.ip_map[ip].pop(stalest_port)
        
        self.lock.release()

    def add_to_banned_set(self, ip: str, port: int) -> None:
        self.lock.acquire()
     
        self.banned_set.add((ip, port))
        
        # remove from self.ip_map as well
        if ip in self.ip_map and port in self.ip_map[ip]:
            self.ip_map[ip].pop(port)
            if len(self.ip_map[ip]) == 0:
                self.ip_map.pop(ip)
                
        self.lock.release()

        return

    def get_random_ip(self) -> Tuple[str, int]:
        self.lock.acquire()
                
        random_ip = random.choice([self.ip_map.keys()])
        random_port = random.choice([self.ip_map[random_ip]])

        self.lock.release()

        return random_ip, random_port
    
    def _get_node_data_as_str(self, ip: str, port: int) -> str:      
        data_point = self.ip_map[ip][port]
        return f"{ip}:{port},{data_point.data_time},{data_point.digit}"

    def get_state(self) -> List[str]:
        
        self.lock.acquire()
        
        return_list = []
        for ip, port_map in self.ip_map.items():
            for port in port_map.keys():
                return_list.append(self._get_node_data_as_str(ip, port))

        self.lock.release()
        
        return return_list
