"""
Test the ZorpTestCase
"""

import re
import warnings

from zorp import Client
from zorp.test import mock_method, ZorpTestCase

class TestCaseTestCase(ZorpTestCase):
    """
    ZorpTestCase tests
    """

    @mock_method("ping")
    def ping(self, message):
        """
        Mock method - returns a "pong" message.
        """

        return "pong {}".format(message)

    @mock_method
    def i_have_no_name(self):
        """
        Mock method which has accidentally used the decorator without providing
        a `name` parameter.
        """

        return "and I must scream"

    def setUp(self):
        """
        Create a client object.
        """

        self.client = Client()

    def test_mock_method_registration(self):
        """
        Test that `@mock_method` registers methods on our mock object.
        """

        self.assertEqual(self.client.call("ping", "o hai"), "pong o hai")

    def test_mock_method_warning(self):
        """
        Test that calling `@mock_method` without parameters will show a
        warning to the developer.
        """

        self.assertEqual(len(self.captured_warnings), 1)
        self.assertIsNotNone(re.search(
            r"^.*\.i_have_no_name: did you mean to pass a name to @mock_method\?$",
            str(self.captured_warnings[0].message)
        ), str(self.captured_warnings[0].message))

    def _get_zorp_mock_methods(self):
        """
        Subclass `_get_zorp_mock_methods`, capturing warnings to
        `self.captured_warnings`.
        """

        with warnings.catch_warnings(record=True) as self.captured_warnings:
            warnings.simplefilter("always")
            return super(TestCaseTestCase, self)._get_zorp_mock_methods()
