"""
Zorp example server
"""

from zorp import remote_method, Server

@remote_method
def hello(who):
    return "Hello, {}".format(who)

server = Server()
server.start()
server.join()
