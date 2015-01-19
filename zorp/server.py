"""
Server
"""

from threading import Thread
import zmq

from registry import registry

class Server(Thread):
    """
    Zorp server
    """

    def __init__(self, address="0.0.0.0", port=5560, use_registry=registry, *args, **kwargs):
        """
        Set the bind address and port
        """

        self.registry = use_registry

        self.address = address
        self.port = port

        super(Server, self).__init__(*args, **kwargs)

    def _handle_request(self, request):
        """
        Wait for a request and process it
        """

        return "goodbye, world"

    def run(self):
        """
        Open the socket and process requests
        """

        # Create the bind socket
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://{}:{}".format(self.address, self.port))

        # Wait for requests and process them
        while True:
            request = socket.recv_string()

            response = self._handle_request(request)

            socket.send_string(response)
