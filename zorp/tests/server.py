"""
Registry tests
"""

import json
import unittest
import zmq

from decorator import remote_method
from registry import Registry
from server import Server

class TestServer(unittest.TestCase):
    """
    Test the server

    We don't actually start a server
    as there's no point in testing zmq itself
    We just call the _handle_request method directly
    """

    def setUp(self):
        """
        Create a new registry
        and start a server
        """

        self.registry = Registry()

        self.server = Server(use_registry=self.registry)

    def test_bad_payload(self):
        """
        Test we get an error for an invalid payload
        """

        expected = {
            "error": "Invalid payload"
        }

        # Invalid json
        response = self.server._handle_request("")
        response = json.loads(response)
        self.assertDictEqual(expected, response)

        # Doesn't match the request schema
        response = self.server._handle_request("{}")
        response = json.loads(response)
        self.assertDictEqual(expected, response)

    def test_unknown_method(self):
        """
        Test we get an error for an unknown method
        """

    def test_invalid_parameters(self):
        """
        Test we get an error for invalid parameters
        """

    def test_successful_call(self):
        """
        Test a successful call
        """

    def test_failing_method(self):
        """
        Test errors in the method are trapped and returned
        """
