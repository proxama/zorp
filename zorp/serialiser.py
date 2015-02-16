"""
Zorp serialiser
"""

from bson import BSON

class Serialiser(object):
    """
    This is simply a wrapper for the bson encoder/decoder
    that can deal with non-dict types
    """

    WRAPPER = "data"

    @staticmethod
    def encode(obj):
        """
        Wrap the object in a dict and bson encode it
        """

        return BSON.encode({
            Serialiser.WRAPPER: obj
        })

    @staticmethod
    def decode(obj):
        """
        bson decode the object and unwrap it
        """

        return BSON(obj).decode()[Serialiser.WRAPPER]
