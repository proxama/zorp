"""
Zorp example server
"""

from zorp import remote_method, Server

@remote_method
def hello(who):
    return "Hello, {}".format(who)

@remote_method("goodbye")
def say_bye():
    return "Goodbye world"

server = Server(call_count=2).join()
