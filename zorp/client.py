"""
Client
"""

import json
import zmq

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

    def _create_request(self, method, *args, **kwargs):
        """
        Construct a request payload
        """

        return json.dumps({
            "method": method,
            "parameters": {
                "args": list(args),
                "kwargs": kwargs
            }
        })

    def __create_connection(self, timeout):
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
        """

        request = self._create_request(method, *args, **kwargs)

        call_count = 0

        while call_count < self.max_tries:
            socket = self.__create_connection(self.timeout)
            socket.send_string(request)

            try:
                response = socket.recv_string()
            except zmq.error.Again:
                # Close the socket and try again
                call_count += 1

                socket.setsockopt(zmq.LINGER, 0)
                socket.close()

                continue

            return json.loads(response)

        raise TriesExceededException
