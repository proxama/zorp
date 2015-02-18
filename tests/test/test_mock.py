"""
Test the Zorp mock feature
"""

import unittest

from zorp import Client
from zorp.test import Mock

class MockTestCase(unittest.TestCase):
    """
    Test the Zorp mock feature
    """

    def setUp(self):
        """
        Create a `Mock` object.
        """

        self.mock = Mock()

    def test_mock_call(self):
        """
        Test that mocked client->server communication calls our mock method.
        """

        @self.mock.method("ping")
        def ping(message):
            """
            Mock method - returns a "pong" message.
            """

            return "pong {}".format(message)

        self.mock.start()
        try:
            client = Client()
            self.assertEqual(client.call("ping", "o hai"), "pong o hai")
        finally:
            self.mock.stop()
