"""
Client
"""

class Client(object):
    """
    Constructs a request payload
    and sends it to the server
    """

    def _create_request(self, method, *args, **kwargs):
        """
        Construct a request payload
        """

        return {
            "method": method,
            "parameters": {
                "args": list(args),
                "kwargs": kwargs
            }
        }
