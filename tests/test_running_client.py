"""
Clienht tests
"""

from datetime import datetime
import json
from threading import Thread
import unittest
import zmq

from zorp import Client
from zorp.client import TriesExceededException
from zorp.settings import DEFAULT_PORT

class FakeServer(Thread):
    """
    Fakes a zorp server
    """

    def __init__(self, call_count, *args, **kwargs):
        """
        Set up the socket
        """

        self.call_count = call_count

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.setsockopt(zmq.RCVTIMEO, 500)
        self.socket.bind("tcp://0.0.0.0:{}".format(DEFAULT_PORT))

        super(FakeServer, self).__init__(*args, **kwargs)

    def run(self):
        """
        Listen for the expected number of calls
        """

        call_count = 0

        while call_count < self.call_count:
            try:
                self.socket.recv_string()
            except zmq.error.Again:
                raise Exception("Expected more calls")

            self.socket.send_string(json.dumps("ACK"))

            call_count += 1

class TestRunningClient(unittest.TestCase):
    """
    Test an actual running client
    """

    def setUp(self):
        """
        Create a new client
        """

    def test_defaults(self):
        """
        Test the client connects to the default address
        """

        FakeServer(1).start()

        client = Client(timeout=500, max_tries=1)
        response = client.call("foo")

        self.assertEqual("ACK", response)

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
