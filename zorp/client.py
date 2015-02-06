"""
Client
"""

import zmq

from zorp.serialiser import Serialiser
from zorp.settings import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_TRIES
)

class TriesExceededException(Exception):
    """
    Represents a failure to get a reply from a server
    """

class Client(object):
    """
    Constructs a request payload
    and sends it to the server
    """

    def __init__(
            self,
            host=DEFAULT_HOST,
            port=DEFAULT_PORT,
            timeout=DEFAULT_TIMEOUT,
            max_tries=DEFAULT_TRIES
            ):
        """
        Store the host and port
        """

        self.host = host
        self.port = port

        self.timeout = timeout
        self.max_tries = max_tries

        self.context = zmq.Context()

    def _handle_response(self, response):
        """
        Handle a received response
        """

        return Serialiser.decode(response)

    def _create_request(self, method, *args, **kwargs):
        """
        Construct a request payload
        """

        return Serialiser.encode({
            "method": method,
            "parameters": {
                "args": list(args),
                "kwargs": kwargs
            }
        })

    def _create_connection(self, timeout):
        """
        Create the creation to the server
        """

        socket = self.context.socket(zmq.REQ)
        socket.setsockopt(zmq.RCVTIMEO, timeout)
        socket.connect("tcp://{}:{}".format(self.host, self.port))

        return socket

    def call(self, method, *args, **kwargs):
        """
        Call a remote method with the arguments supplied
        and return the response
        """

        timeout = kwargs.pop("timeout", self.timeout)
        max_tries = kwargs.pop("max_tries", self.max_tries)

        request = self._create_request(method, *args, **kwargs)

        call_count = 0

        while call_count < max_tries:
            socket = self._create_connection(timeout)
            socket.send(request)

            try:
                response = socket.recv()
                return self._handle_response(response)
            except zmq.error.Again:
                # Close the socket and try again
                call_count += 1

                socket.setsockopt(zmq.LINGER, 0)
                socket.close()

        raise TriesExceededException

    def fire_and_forget(self, method, *args, **kwargs):
        """
        Call a remote method but don't wait for it to return
        """

        timeout = kwargs.pop("timeout", self.timeout)
        max_tries = kwargs.pop("max_tries", self.max_tries)

        request = self._create_request(method, *args, **kwargs)

        socket = self._create_connection(timeout)
        socket.setsockopt(zmq.LINGER, timeout * max_tries)
        socket.send(request)
