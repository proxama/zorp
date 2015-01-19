"""
Zorp example client
"""

from zorp import Client

client = Client(timeout=3000, tries=2)

message = client.call("hello", "world")

print(message)
