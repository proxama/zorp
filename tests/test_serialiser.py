"""
Serialiser tests
"""

from datetime import datetime
import unittest

from zorp.serialiser import Serialiser

class TestSerialiser(unittest.TestCase):
    """
    Test the serialiser
    """

    def __test_encode_decode(self, expected):
        """
        Test that encoding and decoding a value
        results in the original value
        """

        actual = Serialiser.decode(Serialiser.encode(expected))

        self.assertEqual(expected, actual)

    def test_string(self):
        """
        Test encoding/decoding a string
        """

        self.__test_encode_decode("This is a string")

    def test_datetime(self):
        """
        Test encoding/decoding a datetime
        """

        self.__test_encode_decode(datetime(1970, 1, 2))

    def test_empty_list(self):
        """
        Test encoding/decoding an empty list
        """

        self.__test_encode_decode([])

    def test_list(self):
        """
        Test encoding/decoding a list
        """

        self.__test_encode_decode([1, "two"])

    def test_empty_dict(self):
        """
        Test encoding/decoding an empty dict
        """

        self.__test_encode_decode({})

    def test_dict(self):
        """
        Test encoding/decoding a list
        """

        self.__test_encode_decode({"one": 1, "two": 2})
