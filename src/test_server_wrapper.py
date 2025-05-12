import unittest
import json
import requests
import server_wrapper

class TestServerWrapper(unittest.TestCase):

    class MockResponse:
        def __init__(self, json_string=None, text=None):
            self.json_string = json_string
            self.text = text

        def json(self):
            return json.loads(self.json_string)

        def raise_for_status(self):
            pass

    def test_status_up_returns_up_status(self):
        self.assertTrue(
            server_wrapper.status_up(
                lambda: self.MockResponse(json_string='{"status": "up"}')))

    def test_status_up_returns_down_status(self):
        self.assertFalse(
            server_wrapper.status_up(
                lambda: self.MockResponse(json_string='{"status": "down"}')))

    def test_status_up_throws(self):
        request_exceptions = [
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException]
        for exception in request_exceptions:
            with self.subTest(exception), self.assertRaises(SystemExit) as cm:
                server_wrapper.status_up(lambda: self.__raise(exception))
            self.assertEqual(type(cm.exception.__cause__), exception)

    def test_get_measurement_valid_angle(self):
        for angle in range(0, 360, 90):
            with self.subTest(angle):
                self.assertEqual(
                    server_wrapper.get_measurement(lambda: self.MockResponse(text='100'), angle),
                100)

    def test_get_measurement_invalid_angle(self):
        for angle in [-1, 361]:
            with self.subTest(angle), self.assertRaises(ValueError):
                server_wrapper.get_measurement(lambda: self.MockResponse(text='100'), angle)

    def test_get_measurement_result_text_not_float(self):
        with self.assertRaises(ValueError):
            server_wrapper.get_measurement(lambda: self.MockResponse(text='foo'), 180)

    def test_get_measurement_throws(self):
        request_exceptions = [
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException]
        for exception in request_exceptions:
            with self.subTest(exception), self.assertRaises(SystemExit) as cm:
                server_wrapper.get_measurement(lambda: self.__raise(exception), 180)
            self.assertEqual(type(cm.exception.__cause__), exception)

    def __raise(self, exception):
        raise exception
