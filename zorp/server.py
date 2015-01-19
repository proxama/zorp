"""
Server
"""

import json
from jsonschema import Draft4Validator, ValidationError
from threading import Thread
import zmq

from registry import registry
from settings import DEFAULT_PORT

REQUEST_SCHEMA = {
    "type": "object",
    "required": ["method", "parameters"],
    "additionalProperties": False,
    "properties": {
        "method": {
            "type": "string"
        },
        "parameters": {
            "type": "object",
            "required": ["args", "kwargs"],
            "additionalProperties": False,
            "properties": {
                "args": {
                    "type": "array"
                },
                "kwargs": {
                    "type": "object"
                }
            }
        }
    }
}

class ServerThread(Thread):
    """
    Zorp server
    """

    daemon = True

    def __init__(
            self,
            address="0.0.0.0",
            port=DEFAULT_PORT,
            use_registry=registry,
            *args, **kwargs
            ):
        """
        Set the bind address and port
        """

        self.registry = use_registry

        self.address = address
        self.port = port

        self.validator = Draft4Validator(REQUEST_SCHEMA)

        super(ServerThread, self).__init__(*args, **kwargs)

    def _error(self, message):
        """
        Construct an error response with the given message
        """

        return json.dumps({
            "error": message
        })

    def _handle_request(self, request):
        """
        Wait for a request and process it
        """

        try:
            request = json.loads(request)

            self.validator.validate(request, REQUEST_SCHEMA)
        except (ValueError, ValidationError):
            return self._error("Invalid payload")

        try:
            (schema, func) = self.registry.get(request["method"])
        except KeyError:
            return self._error("Unknown method")

        try:
            self.validator.validate(request["parameters"], schema)
        except ValidationError:
            return self._error("Parameters do not match the method signature")

        args = list(request["parameters"]["args"])
        kwargs = request["parameters"]["kwargs"]

        try:
            response = func(*args, **kwargs)
        except Exception as exc:
            return self._error(str(exc))

        return json.dumps(response)

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

def Server(*args, **kwargs):
    """
    A wrapper for creating, starting,
    and returning a new ServerThread
    """

    thread = ServerThread(*args, **kwargs)
    thread.start()

    return thread
