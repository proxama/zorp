"""
Load remote methods from Django apps
"""

import collections

from django.conf import settings

def register_remote_methods_from_apps():
    """
    Load remote methods from Django apps.

    Returns a namedtuple with one element, `loaded_apps`. This is a list of
    apps with successfully imported `rpc` modules.
    """

    loaded_apps = []
    for app in settings.INSTALLED_APPS:
        try:
            # Try to import the app's `rpc` module. If successful,
            # the imported functions will register themselves with Zorp.
            __import__("{}.rpc".format(app))
        except ImportError:
            # No remote methods, or error importing the module.
            pass
        else:
            # `rpc` module was successfully loaded.
            loaded_apps.append(app)

    return collections.namedtuple("Result", ("loaded_apps",))(loaded_apps)
