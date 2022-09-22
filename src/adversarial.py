import random
import string
from typing import List
from state import State


def get_random_attack():
    attacks = [random_data, negative_digits, long_response,
               change_their_digit, whitespace_in_state, bad_ip_port]
    return attacks[random.randint(0, len(attacks))]


def random_data(state: State, ip: str, port: int) -> str:
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(100))


def negative_digits(state: State, ip: str, port: int) -> str:
    current_state: List[str] = state.get_state()
    for idx in range(len(current_state)):
        current_state[idx] = current_state[idx][-1:] + \
            str(random.randint(-9, -1))

    return '\n'.join(current_state)


def long_response(state: State, ip: str, port: int) -> str:
    return '\n'.join('\n'.join(state.get_state(printable=False)) for i in range(100000))


def change_their_digit(state: State, ip: str, port: int) -> str:
    pass


def whitespace_in_state(state: State, ip: str, port: int) -> str:
    pass


def bad_ip_port(state: State, ip: str, port: int) -> str:
    pass
