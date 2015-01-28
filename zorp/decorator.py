"""
remote_method decorator
"""

from zorp.registry import registry

def func_name(func):
    """
    Return the functions fully-qualified name
    """

    if hasattr(func, "__module__"):
        return "{}.{}".format(func.__module__, func.__name__)

    return func.__name__

def remote_method(name=None, use_registry=registry):
    """
    Register the decorated function
    Use the function's own name if none is supplied
    """

    if callable(name):
        # Allow calling without arguments

        use_registry.put(func_name(name), name)

        return name

    def wrap(func):
        """
        function wrapper
        """

        use_registry.put(name or func_name(func), func)

        return func

    return wrap
