from collections.abc import Callable
import requests
import server_wrapper

BASE_URL = 'http://localhost:8000/'

def status_up() -> bool:
    return server_wrapper.status_up(lambda: requests.get(BASE_URL))

def get_measurement(angle: float) -> float:
    return server_wrapper.get_measurement(
        lambda: requests.get(f'{BASE_URL}/measure/', params={'angle': angle}),
        angle)
