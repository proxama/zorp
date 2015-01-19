"""
remote_method decorator
"""

from registry import registry

def remote_method(name=None, use_registry=registry):
    """
    Register the decorated function
    Use the function's own name if none is supplied
    """

    def wrap(func):
        """
        function wrapper
        """

        use_registry.put(name or func.__name__, func)

        return func

    if callable(name):
        # Allow calling without arguments

        func = name
        name = func.__name__

        return wrap(func)

    return wrap
