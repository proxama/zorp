"""
Mock client/server communication
"""

import zmq

from zorp.client import Client
from zorp.decorator import remote_method
from zorp.registry import Registry
from zorp.server import Server

class Mock(object):
    """
    Mock Zorp client/server.

    Bypasses network communication by patching the `Client` class.
    Patched clients directly call the server's request handler.

    Example:
        mock = Mock()

        @mock.method("ping")
        def ping():
            return "pong"

        mock.start()
        client = Client()
        print client.call("ping")
        mock.stop()
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the class. Arguments are used to create a `Server` instance.
        """

        self.registry = Registry()
        self.server = Server(use_registry=self.registry, *args, **kwargs)
        self.mock_client_socket = MockClientSocket(self)

    def method(self, name):
        """
        Decorator to register a mocked server method.

        Example:
            @mock.method("ping")
            def ping():
                return "pong"

        Unlike `decorator.remote_method`, the `name` parameter is required.
        """

        return remote_method(name, use_registry=self.registry)

    def start(self):
        """
        Patch the `Client` class to call our mock server.
        """

        if hasattr(Client, "_pre_mock_values"):
            raise Exception("Client patches are already active")

        Client._pre_mock_values = self._patch_obj(Client, {
            "_create_connection": lambda client, timeout: self.mock_client_socket
        })

    def stop(self):
        """
        Unpatch the `Client` class.
        """

        self._patch_obj(Client, Client._pre_mock_values)
        del Client._pre_mock_values

    def _patch_obj(self, obj, patches):
        """
        Given an object and dictionary of new attribute values, patch in the
        new attributes and return the previous values.
        """

        original_values = {}
        for name, value in patches.iteritems():
            original_values[name] = getattr(obj, name)
            setattr(obj, name, value)

        return original_values

class MockClientSocket(object):
    """
    Mock client socket. On `send()`, call the server's request handler, and
    store the response. The response will be returned on `recv()`.
    """

    def __init__(self, mock):
        """
        Initialise the class. `mock` is an instance of a `Mock` object.
        """

        self.mock = mock
        self.response = None

    def send(self, data):
        """
        Mock `send` method. This is called by the client when requesting an
        RPC call on the server.
        """

        self.response = self.mock.server._handle_request(data)

    def recv(self):
        """
        Mock `recv` method. This is called by the client when fetching the
        response to an RPC call.
        """

        if self.response is None:
            raise Exception("Response unavailable, as no request has been sent")

        response = self.response
        self.response = None
        return response

    def setsockopt(self, option, value):
        """
        Set a socket option. These don't currently influence the mock socket
        behaviour. Raise `ValueError` if we're given an unrecognised option, as
        it may indicate a change in client logic.
        """

        if option == zmq.LINGER:
            return
        elif option == zmq.RCVTIMEO:
            return

        raise ValueError("Unsupported option {!r} (value = {!r})".format(option, value))
