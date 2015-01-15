"""
Schema generation tests
"""

import unittest

from registry import schema_from_function

class TestSchemaFromFunction(unittest.TestCase):
    """
    Test the schema_from_function function
    """

    def setUp(self):
        """
        Create a base schema to compare
        """

        self.base = {
            "properties": {
                "args": {
                    "type": "array",
                    "items": [],
                    "additionalItems": False
                },
                "kwargs": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            },
            "required": ["args", "kwargs"],
            "additionalProperties": False
        }

    def test_no_params(self):
        """
        Test schema with no parameters
        """

        func = lambda: 10

        schema = schema_from_function(func)

        self.assertDictEqual(self.base, schema)

    def test_one_arg(self):
        """
        Confirm behaviour with one arg parameter
        """

        func = lambda x: x * 2

        schema = schema_from_function(func)

        expected_schema = self.base
        expected_schema["properties"]["args"]["items"] = [{}]

        self.assertDictEqual(expected_schema, schema)

    def test_two_args(self):
        """
        Confirm behaviour with two arg parameter
        """

        func = lambda x, y: x * y

        schema = schema_from_function(func)

        expected_schema = self.base
        expected_schema["properties"]["args"]["items"] = [{}, {}]

        self.assertDictEqual(expected_schema, schema)

    def test_one_kwarg(self):
        """
        Confirm behaviour with one kwarg parameters
        """

        func = lambda x=10: x * 2

        schema = schema_from_function(func)

        expected_schema = self.base
        expected_schema["properties"]["kwargs"]["properties"] = {"x": {}}

        self.assertDictEqual(expected_schema, schema)

    def test_two_kwargs(self):
        """
        Confirm behaviour with two kwarg parameters
        """

        func = lambda x=10, y=2: x * y

        schema = schema_from_function(func)

        expected_schema = self.base
        expected_schema["properties"]["kwargs"]["properties"] = {
            "x": {},
            "y": {},
        }

        self.assertDictEqual(expected_schema, schema)

    def test_args_and_kwarg(self):
        """
        Confirm behaviour with args and kwarg parameters
        """

        func = lambda x, y=10: (x + y) * 2

        schema = schema_from_function(func)

        expected_schema = self.base
        expected_schema["properties"]["args"]["items"] = [{}]
        expected_schema["properties"]["kwargs"]["properties"] = {"y": {}}

        self.assertDictEqual(expected_schema, schema)
