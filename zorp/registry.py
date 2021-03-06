"""
Remote method registry
"""

from copy import deepcopy
from inspect import getargspec, ismethod

BASE_SCHEMA = {
    "additionalProperties": False,
    "required": ["args", "kwargs"],
    "properties": {
        "args": {
            "type": "array",
        },
        "kwargs": {
            "type": "object",
            "additionalProperties": False,
        },
    },
}

def schema_from_function(func):
    """
    Return a json schema derived from
    the provided function's signature
    """

    (args, _, _, defaults) = getargspec(func)

    # `getargspec` returns the `self` arg for bound methods, even though it's
    # implicitly provided when calling the function. Let's remove it.
    if ismethod(func):
        args = args[1:]

    args = args or []
    defaults = defaults or []

    if defaults:
        defaults = args[-len(defaults):]
        args = args[:-len(defaults)]
    else:
        defaults = []

    schema = deepcopy(BASE_SCHEMA)

    schema["properties"]["args"]["minItems"] = len(args)
    schema["properties"]["args"]["maxItems"] = len(args)

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

        schema = schema_from_function(func)

        self.methods[name] = func
        self.schemas[name] = schema

    def get(self, name):
        """
        Return a tuple containing the schema and function
        using `name` as the key

        Throw a KeyError if it doesn't exist
        """

        return (self.schemas[name], self.methods[name])

registry = Registry()
