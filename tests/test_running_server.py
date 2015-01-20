"""
Server tests
"""

import json
import unittest
import zmq

from zorp import remote_method
from zorp.registry import Registry
from zorp.server import Server
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
        def hello(name):
            return "Hello, {}".format(name)

        self.context = zmq.Context()

    def test_defaults(self):
        """
        Test that the server successfully listens
        on the default address and port
        """

        expected = {
            "error": "Invalid payload"
        }

        Server(use_registry=self.registry, call_count=1)

        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://{}:{}".format(DEFAULT_HOST, DEFAULT_PORT))
        socket.send_string("foo")
        response = socket.recv_string()

        self.assertDictEqual(expected, json.loads(response))

    def test_specified_host_and_port(self):
        """
        Test that the server successfully listens
        on the specified address and port
        """

        new_host = "127.0.0.2"
        new_port = 8001

        expected = {
            "error": "Invalid payload"
        }

        Server(
            new_host,
            port=new_port,
            use_registry=self.registry,
            call_count=1
            )

        # Connect to the default to prove
        # we're not listening there
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://{}:{}".format(DEFAULT_HOST, DEFAULT_PORT))
        socket.send_string("foo")

        # Make sure we clean up nicely
        socket.setsockopt(zmq.RCVTIMEO, 500)
        socket.setsockopt(zmq.LINGER, 0)

        with self.assertRaises(zmq.error.Again):
            response = socket.recv_string()

        socket.close()

        # Connect to the specified host/port
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://{}:{}".format(new_host, new_port))
        socket.send_string("foo")
        response = socket.recv_string()

        self.assertDictEqual(expected, json.loads(response))
