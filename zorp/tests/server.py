"""
Server tests
"""

import json
import unittest

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

        @remote_method(use_registry=self.registry)
        def hello(name):
            return "Hello, {}".format(name)

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

        expected = {
            "error": "Unknown method"
        }

        request = json.dumps({
            "method": "not a method",
            "parameters": {
                "args": [],
                "kwargs": {}
            }
        })

        response = self.server._handle_request(request)
        response = json.loads(response)

        self.assertDictEqual(expected, response)

    def test_invalid_parameters(self):
        """
        Test we get an error for invalid parameters
        """

        expected = {
            "error": "Parameters do not match the method signature"
        }

        request = json.dumps({
            "method": "hello",
            "parameters": {
                "args": [],
                "kwargs": {}
            }
        })

        response = self.server._handle_request(request)
        response = json.loads(response)

        self.assertDictEqual(expected, response)

    def test_successful_call(self):
        """
        Test a successful call
        """

        expected = "Hello, Fred"

        request = json.dumps({
            "method": "hello",
            "parameters": {
                "args": ["Fred"],
                "kwargs": {}
            }
        })

        response = self.server._handle_request(request)
        response = json.loads(response)

        self.assertEqual(expected, response)

    def test_failing_method(self):
        """
        Test errors in the method are trapped and returned
        """

        error_message = "Houston, we have a problem"

        @remote_method(use_registry=self.registry)
        def bad_method():
            raise Exception(error_message)

        expected = {
            "error": error_message
        }

        request = json.dumps({
            "method": "bad_method",
            "parameters": {
                "args": [],
                "kwargs": {}
            }
        })

        response = self.server._handle_request(request)
        response = json.loads(response)

        self.assertEqual(expected, response)
