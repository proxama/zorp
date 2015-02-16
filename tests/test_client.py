"""
Client tests
"""

import unittest

from zorp import Client
from zorp.serialiser import Serialiser

class TestClient(unittest.TestCase):
    """
    Test the client

    We don't actually connect to a server
    as there's no point in testing zmq itself
    We just call the _create_request method directly
    """

    def setUp(self):
        """
        Create a new client
        """

        self.client = Client()

    def test_payload_no_params(self):
        """
        Test a valid payload with no params
        """

        expected = {
            "method": "hello",
            "parameters": {
                "args": [],
                "kwargs": {}
            }
        }

        request = self.client._create_request("hello")

        self.assertDictEqual(expected, Serialiser.decode(request))

    def test_payload_with_args(self):
        """
        Test a valid payload with args
        """

        expected = {
            "method": "hello",
            "parameters": {
                "args": ["world"],
                "kwargs": {}
            }
        }

        request = self.client._create_request("hello", "world")

        self.assertDictEqual(expected, Serialiser.decode(request))

    def test_payload_with_kwargs(self):
        """
        Test a valid payload with kwargs
        """

        expected = {
            "method": "hello",
            "parameters": {
                "args": [],
                "kwargs": {
                    "who": "world"
                }
            }
        }

        request = self.client._create_request("hello", who="world")

        self.assertDictEqual(expected, Serialiser.decode(request))

    def test_payload_with_args_and_kwargs(self):
        """
        Test a valid payload with args and kwargs
        """

        expected = {
            "method": "hello",
            "parameters": {
                "args": ["world"],
                "kwargs": {
                    "alias": "Gaia"
                }
            }
        }

        request = self.client._create_request("hello", "world", alias="Gaia")

        self.assertDictEqual(expected, Serialiser.decode(request))
