"""
Zorp serialiser
"""

import datetime
from json import JSONEncoder

EPOCH = datetime.datetime(1970, 1, 1)

class Serialiser(JSONEncoder):
    """
    This is simply a JSON encode/decoder
    that converts datetimes into unix timestamps
    """

    def default(self, obj):
        """
        Convert dates
        """

        if isinstance(obj, datetime.datetime):
            # return obj.timestamp()
            # O, to be python3 only :(

            delta = obj - EPOCH

            return delta.total_seconds()

        return super(Serialiser, self).default(obj)
