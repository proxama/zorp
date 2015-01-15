"""
Remote method registry
"""

from inspect import getargspec

BASE_SCHEMA = {
    "additionalProperties": False,
    "required": ["args", "kwargs"],
    "properties": {
        "args": {
            "type": "array",
            "items": [],
            "additionalItems": False,
        },
        "kwargs": {
            "type": "object",
            "additionalProperties": False,
            "properties": {},
        },
    },
}

def schema_from_function(func):
    """
    Return a json schema derived from
    the provided function's signature
    """

    (args, _, _, defaults) = getargspec(func)

    args = args or []
    defaults = defaults or []

    if defaults:
        defaults = args[-len(defaults):]
        args = args[:-len(defaults)]
    else:
        defaults = []

    schema = BASE_SCHEMA

    schema["properties"]["args"]["items"] = [{}] * len(args)
    schema["properties"]["kwargs"]["properties"] = {
        key: {}
        for key
        in defaults
    }

    return schema

class Registry(object):
    """
    Generate json schema for each registered function
    Store functions by a name string
    Retrieve a schema and function by a name string
    """

    def __init__(self):
        """
        Initialise the store
        """

        self.methods = {}
        self.schemas = {}

    def put(self, name, func):
        """
        Generate a JSON schema for `func`
        Store the function and the schema
        using `name` as the key
        """

    def get(self, name):
        """
        Return a tuple containing the schema and function
        using `name` as the key

        Throw a KeyError if it doesn't exist
        """
