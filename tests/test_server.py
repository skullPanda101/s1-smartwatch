import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from mac.server import PingHandler


class PingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), PingHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        cls.port = cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_ping(self):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=2)
        try:
            connection.request("GET", "/ping")
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "application/json")
            self.assertEqual(json.load(response), {"message": "pong from Mac"})
        finally:
            connection.close()

    def test_unknown_path(self):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=2)
        try:
            connection.request("GET", "/unknown")
            self.assertEqual(connection.getresponse().status, 404)
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
