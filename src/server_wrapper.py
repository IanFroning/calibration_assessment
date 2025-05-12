import requests

BASE_URL = 'http://localhost:8000/'

def status_up(request) -> bool:
    result = _handle_request(request)
    try:
        return result.json()['status'] == 'up'
    except requests.exceptions.JSONDecodeError as e:
        raise SystemExit('Failed to decode expected JSON response.', e)

def get_measurement(request, angle: float) -> float:
    if angle < 0.0 or angle > 360.0:
        raise ValueError("Angle must be between 0 and 360 degrees.")
    result = _handle_request(request)
    return float(result.text)

def _handle_request(request):
    try:
        result = request()
        result.raise_for_status()
        return result
    except requests.exceptions.RequestException as er:
        raise SystemExit('Request failed.', er) from er
