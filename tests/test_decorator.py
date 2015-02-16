"""
Decorator tests
"""

import unittest

from zorp import remote_method
from zorp.registry import Registry

class TestRemoteMethod(unittest.TestCase):
    """
    Test the remote_method decorator
    """

    def setUp(self):
        """
        Create a new registry
        """

        def func(x):
            return x * 2

        self.registry = Registry()

        self.func = func

        self.assertDictEqual({}, self.registry.methods)
        self.assertDictEqual({}, self.registry.schemas)

    def test_automatic_name(self):
        """
        Test the decorator results in a function
        registered using its own name
        """

        remote_method(use_registry=self.registry)(self.func)

        (schema, func) = self.registry.get("tests.test_decorator.func")

    def test_explicit_name(self):
        """
        Test the decorator results in a function
        registered using a supplied name
        """

        remote_method("my func", use_registry=self.registry)(self.func)

        (schema, func) = self.registry.get("my func")

    def test_function_still_works(self):
        """
        Test that decorated functions still work
        """

        func = remote_method(self.func)

        self.assertEqual(self.func(2), func(2))
