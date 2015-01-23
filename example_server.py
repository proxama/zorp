"""
Zorp example server
"""

from zorp import remote_method, Server

@remote_method
def hello(who):
    print("Hello was called")

    return "Hello, {}".format(who)

@remote_method("goodbye")
def say_bye():
    print("Goodbye was called")

    return "Goodbye world"

Server(call_count=3).join()
