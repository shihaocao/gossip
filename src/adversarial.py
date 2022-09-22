import random
from state import State


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
    pass


def whitespace_in_state(state: State, ip: str, port: int) -> str:
    pass


def bad_ip_port(state: State, ip: str, port: int) -> str:
    pass
