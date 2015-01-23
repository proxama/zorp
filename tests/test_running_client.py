"""
Clienht tests
"""

from datetime import datetime
import unittest

from zorp import Client, Server, remote_method
from zorp.registry import Registry
from zorp.client import TriesExceededException

class TestRunningClient(unittest.TestCase):
    """
    Test an actual running client
    """

    def setUp(self):
        """
        Create a new client
        """

        self.registry = Registry()

        @remote_method(use_registry=self.registry)
        def foo():
            return "ACK"

    def test_defaults(self):
        """
        Test the client connects to the default address
        """

        Server(call_count=1, use_registry=self.registry)

        client = Client(timeout=500, max_tries=1)
        response = client.call("foo")

        self.assertEqual("ACK", response)

    def test_fire_and_forget(self):
        """
        Test that fire and forget doesn't wait for a response
        """

        # Don't start a server
        client = Client(timeout=500, max_tries=1)
        client.fire_and_forget("foo")
        # No exception is raised

        # Now start the server
        Server(call_count=1, use_registry=self.registry).join()
        # It doesn't raise an exception

    def _test_failing_call_time(self, timeout, tries, client_params=True):
        """
        Make a call against a server that's not there
        Time how long we take to fail

        if client_params is True, set the options on the client
        otherwise, set the options on the call
        """

        if client_params:
            client = Client(timeout=timeout, max_tries=tries)
        else:
            client = Client()

        start = datetime.now()

        with self.assertRaises(TriesExceededException):
            if not client_params:
                client.call("foo", timeout=timeout, max_tries=tries)
            else:
                client.call("foo")

        end = datetime.now()

        delta = end - start

        delta /= 1000

        self.assertAlmostEqual(timeout * tries, delta.microseconds, delta=10)

    def test_class_timeout_and_tries(self):
        """
        Test that we can specify timeout and tries in the constructor
        """

        # A single try
        self._test_failing_call_time(100, 1)

        # Multiple tries
        self._test_failing_call_time(100, 3)

    def test_call_timeout_and_tries(self):
        """
        Test that we can specify timeout and tries in the call
        """

        # A single try
        self._test_failing_call_time(100, 1, False)

        # Multiple tries
        self._test_failing_call_time(100, 3, False)
