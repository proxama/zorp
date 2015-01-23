"""
Server tests
"""

import unittest

from zorp import Client, remote_method, Server, TriesExceededException
from zorp.registry import Registry
from zorp.settings import DEFAULT_HOST, DEFAULT_PORT

class TestRunningServer(unittest.TestCase):
    """
    Test an actual running server
    to prove that it accepts connections etc
    """

    def setUp(self):
        """
        Create a new registry
        and start a server
        """

        self.registry = Registry()

        @remote_method(use_registry=self.registry)
        def foo():
            return "ACK"

    def __get_client(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        """
        Construct a client
        """

        return Client(
            timeout=500,
            max_tries=1,
            host=host,
            port=port
        )

    def test_defaults(self):
        """
        Test that the server successfully listens
        on the default address and port
        """

        Server(use_registry=self.registry, call_count=1)

        response = self.__get_client().call("foo")

        self.assertEqual("ACK", response)

    def test_specified_host_and_port(self):
        """
        Test that the server successfully listens
        on the specified address and port
        """

        new_host = "127.0.0.2"
        new_port = 8001

        Server(
            new_host,
            port=new_port,
            use_registry=self.registry,
            call_count=1
        )

        with self.assertRaises(TriesExceededException):
            response = self.__get_client().call("foo")

        # Connect to the specified host/port
        response = self.__get_client(new_host, new_port).call("foo")

        self.assertEqual("ACK", response)
