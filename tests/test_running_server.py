"""
Server tests
"""

import unittest

from zorp import Client, ServerProcess, TriesExceededException
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

        self.expected = "ACK"
        self.method_name = "my method"

        self.registry = Registry()

        self.registry.put(self.method_name, lambda: self.expected)

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

        proc = ServerProcess(use_registry=self.registry)
        proc.start()

        response = self.__get_client().call(self.method_name)

        self.assertEqual(self.expected, response)

        proc.terminate()

    def test_specified_host_and_port(self):
        """
        Test that the server successfully listens
        on the specified address and port
        """

        new_host = "127.0.0.2"
        new_port = 8001

        proc = ServerProcess(
            new_host,
            port=new_port,
            use_registry=self.registry,
        )
        proc.start()

        with self.assertRaises(TriesExceededException):
            response = self.__get_client().call(self.method_name)

        # Connect to the specified host/port
        response = self.__get_client(new_host, new_port).call(self.method_name)

        self.assertEqual(self.expected, response)

        proc.terminate()

    def test_call_count(self):
        """
        Test that specifying a call count stops the server
        after the expected number of calls
        """

        proc = ServerProcess(call_count=2)
        proc.start()

        client = self.__get_client()

        # Still running after the first call
        client.call(self.method_name)
        self.assertTrue(proc.is_alive())

        # Dead after the second call
        client.call(self.method_name)
        proc.join(1) # We'll let it die properly
        self.assertFalse(proc.is_alive())
