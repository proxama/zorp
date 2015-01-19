"""
Registry tests
"""

import unittest

from registry import Registry, schema_from_function

class TestRegistry(unittest.TestCase):
    """
    Test the registry
    """

    def setUp(self):
        """
        Create a new registry
        """

        self.registry = Registry()

        self.name = "my func"
        self.func = lambda x, y=1: (x + y) * 2
        self.schema = schema_from_function(self.func)

        self.name2 = "my other func"
        self.func2 = lambda z: z * 2
        self.schema2 = schema_from_function(self.func2)

    def test_init(self):
        """
        Check the registry is empty on initialisation
        """

        self.assertEqual({}, self.registry.methods)
        self.assertEqual({}, self.registry.schemas)

    def test_put(self):
        """
        Confirm that a function is successfully registered
        """

        self.registry.put(self.name, self.func)

        self.assertIn(self.name, self.registry.methods)
        self.assertIn(self.name, self.registry.schemas)

        self.assertEqual(self.func, self.registry.methods[self.name])
        self.assertDictEqual(self.schema, self.registry.schemas[self.name])

    def test_get(self):
        """
        Confirm that getting a function works correctly
        """

        self.registry.put(self.name, self.func)

        (schema, func) = self.registry.get(self.name)

        self.assertEqual(self.func, func)
        self.assertDictEqual(self.schema, schema)

    def test_multiple_funcs(self):
        """
        Test the registry can successfully store multiple functions
        """

        self.registry.put(self.name, self.func)
        self.registry.put(self.name2, self.func2)

        (schema, func) = self.registry.get(self.name)
        (schema2, func2) = self.registry.get(self.name2)

        self.assertEqual(self.func, func)
        self.assertDictEqual(self.schema, schema)

        self.assertEqual(self.func2, func2)
        self.assertDictEqual(self.schema2, schema2)
