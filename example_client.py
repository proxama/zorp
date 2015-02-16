"""
Zorp example client
"""

from zorp import Client

client = Client(timeout=3000, max_tries=2)

message = client.call("hello", "world")
print(message)

client.fire_and_forget("hello", "world")

message = client.call("goodbye", timeout=500, max_tries=1)
print(message)
