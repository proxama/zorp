"""
Zorp tests
"""

import unittest

from registry import Registry

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
        self.schema = {
            "properties": {
                "args": {
                    "type": "array",
                    "items": [{}],
                    "additionalItems": False
                },
                "kwargs": {
                    "type": "object",
                    "properties": {
                        "y": {}
                    },
                    "additionalProperties": False
                }
            },
            "required": ["args", "kwargs"]
        }

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
