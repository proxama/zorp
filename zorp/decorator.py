"""
remote_method decorator
"""

from registry import registry

def remote_method(func, name=None, use_registry=registry):
    """
    Register the decorated function
    Use the function's own name if none is supplied
    """

    if not name:
        name = func.__name__

    use_registry.put(name, func)

    return func
