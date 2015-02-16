"""
remote_method decorator
"""

from zorp.registry import registry

def remote_method(name=None, use_registry=registry):
    """
    Register the decorated function
    Use the function's own name if none is supplied
    """

    if callable(name):
        # Allow calling without arguments

        use_registry.put(name.__name__, name)

        return name

    def wrap(func):
        """
        function wrapper
        """

        use_registry.put(name or func.__name__, func)

        return func

    return wrap
