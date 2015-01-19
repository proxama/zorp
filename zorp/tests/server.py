"""
Registry tests
"""

import unittest

from decorator import remote_method
from registry import Registry
from server import Server

class TestServer(unittest.TestCase):
    """
    Test the server
    """

    def setUp(self):
        """
        Create a new registry
        """

        self.registry = Registry()

    def test_bind(self):
        """
        Test that the server binds on the specified
        or default address and port
        """

    def test_bad_payload(self):
        """
        Test we get an error for an invalid payload
        """

    def test_unknown_method(self):
        """
        Test we get an error for an unknown method
        """

    def test_invalid_parameters(self):
        """
        Test we get an error for invalid parameters
        """

    def test_successful_call(self):
        """
        Test a successful call
        """

    def test_failing_method(self):
        """
        Test errors in the method are trapped and returned
        """
