import random
from state import State
import time

def get_random_attack():
    attacks = [random_data, negative_digits, long_response,
               change_their_digit, whitespace_in_state, bad_ip_port]
    return attacks[random.randint(0, len(attacks))]


def random_data(state: State, ip: str, port: int) -> str:
    pass


def negative_digits(state: State, ip: str, port: int) -> str:
    pass


def long_response(state: State, ip: str, port: int) -> str:
    pass


def change_their_digit(state: State, ip: str, port: int) -> str:
    state_list = state.get_state(printable=False)
    state_list.append(f'{ip}:{port},{int(time.time())},{1}')
    state_str = '\n'.join(state_list)
    return state_str
    pass


def whitespace_in_state(state: State, ip: str, port: int) -> str:
    state_list = state.get_state(printable=False)
    state_list.append(f'1234.1 .1 .1:3000, {int(time.time())},  {1}')
    state_str = '\n'.join(state_list)
    return state_str
    pass


def bad_ip_port(state: State, ip: str, port: int) -> str:
    state_list = state.get_state(printable=False)
    state_list.append(f'1234.1.1.1:3000,{int(time.time())},{1}')
    state_str = '\n'.join(state_list)
    return state_str
    pass
