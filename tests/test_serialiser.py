"""
Serialiser tests
"""

from datetime import datetime
import unittest

from zorp import Client
from zorp.registry import Registry
from zorp.server import ServerThread

class TestSerialiser(unittest.TestCase):
    """
    Test the serialiser
    """

    def setUp(self):
        """
        Create a new registry
        and start a server
        """

        self.registry = Registry()

        self.server = ServerThread(use_registry=self.registry)
        self.client = Client()

        self.method_name = "my method"

    def test_datetime(self):
        """
        Test that a datetime is converted into a timestamp
        """

        now = datetime(1970, 1, 2)
        expected = 24 * 60 * 60  # A day

        self.registry.put(self.method_name, lambda: now)
        request = self.client._create_request(self.method_name)
        response = self.server._handle_request(request)
        actual = self.client._handle_response(response)

        self.assertEqual(expected, actual)
