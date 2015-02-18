"""
Mock Zorp calls within a unittest TestCase
"""

import unittest
import warnings

import six

from zorp.test.mock import Mock

def mock_method(name):
    """
    Decorator to "register" a mock method. `name` is required.

    Unlike `remote_method`, and `Mock.method`, this doesn't immediately add
    functions to a `Registry` - instead, it sets an attribute on the function,
    allowing such functions to be recognised when the test case is instantiated.

    Example:
        class MyTestCase(ZorpTestCase):
            @mock_method("ping")
            def ping(self):
                return "pong"

        print MyTestCase()._get_zorp_mock_methods()
    """

    def decorator(func):
        """
        Return `func`, with the `mock_method.attr_name` attribute set.
        """

        setattr(func, mock_method.attr_name, name)
        return func

    # Set an attribute on `decorator`. This can be used to discover situations
    # where `mock_method` has accidentally been called without any parameters.
    setattr(decorator, mock_method.decorator_attr_name, True)

    return decorator

mock_method.attr_name = "_zorp_test_remote_method_name"

mock_method.decorator_attr_name = "_zorp_test_mock_method_decorator"
mock_method.is_decorator = lambda func: hasattr(func, mock_method.decorator_attr_name)

class ZorpTestCaseMixin(object):
    """
    TestCase mixin to mock out Zorp client/server communication, and register
    methods.
    """

    def __getattribute__(self, name):
        """
        Hook attribute access, so we can run code before and after
        `setUp`/`tearDown`.
        """

        def setup():
            """
            Create `zorp_mock`. Register RPC methods, and activate the mock
            object.
            """

            self.zorp_mock = Mock()

            for name, func in six.iteritems(self._get_zorp_mock_methods()):
                self.zorp_mock.server.registry.put(name, func)

            self.zorp_mock.start()

        def teardown():
            """
            Deactivate the mock object.
            """

            self.zorp_mock.stop()

        def func_caller(*funcs):
            """
            Return a function that calls each of `funcs` in order.
            """

            def caller():
                """
                Call each of `funcs`.
                """

                for func in funcs:
                    func()

            return caller

        value = super(ZorpTestCaseMixin, self).__getattribute__(name)

        if name == "setUp":
            value = func_caller(setup, value)
        elif name == "tearDown":
            value = func_caller(value, teardown)

        return value

    def _get_zorp_mock_methods(self):
        """
        Return this instance's mock methods. These are recognised by the
        presence of the `mock_method.attr_name` attribute. This is set by the
        `@mock_method` decorator.
        """

        mock_methods = {}
        for name in dir(self):
            if name not in ("setUp", "tearDown"):
                try:
                    value = getattr(self, name)
                except AttributeError:
                    pass
                else:
                    if mock_method.is_decorator(value):
                        warnings.warn("{}.{}.{}: did you mean to pass a name to @mock_method?".format(
                            type(self).__module__, type(self).__name__, name
                        ))
                    elif hasattr(value, mock_method.attr_name):
                        mock_methods[getattr(value, mock_method.attr_name)] = value

        return mock_methods

class ZorpTestCase(ZorpTestCaseMixin, unittest.TestCase):
    """
    TestCase to mock out Zorp client/server communication, and register methods.
    """
