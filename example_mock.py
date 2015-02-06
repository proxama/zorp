"""
Zorp example mocked client/server
"""

from zorp.client import Client
from zorp.test import Mock

mock = Mock()

@mock.method("hello")
def hello(who):
    print("Hello was called")

    return "Hello, {}".format(who)

@mock.method("goodbye")
def say_bye():
    print("Goodbye was called")

    return "Goodbye world"

mock.start()

client = Client(timeout=3000, max_tries=2)

message = client.call("hello", "world")
print(message)

client.fire_and_forget("hello", "world")

message = client.call("goodbye", timeout=500, max_tries=1)
print(message)

mock.stop()
