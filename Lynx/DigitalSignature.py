from .Serializable import Serializable
from .TypeCode import TypeCode
from . import ApplicationSerializer

class DigitalSignature(Serializable):
    """
    Description:
        An instance of this class is used to create or verify
        a digital signature.  As of version 1.0 of the Lynx
        this is not implemented.
    """
    def __init__(self, data=None): 
        """
        Description:
            Initializes this instance
        Arguments:
            data (in, char[])    The data to sign
        Returns:
            none
        """
        self._Key = []
        self._Signature = []
        self._RandomData = [] #range(0,8)
    def sign(self):
        """
        Description:
            Signs the data
        Arguments:
            none
        Returns:
            none
        """
        pass
    def verify(self):
        """
        Description:
            Verifies the signed data
        Arguments:
            none
        Exception:
            DigitalSignatureException
        Returns:
            none
        """
        pass
    def serialize(self, stream=''):
        """
        Description:
            Serializes the data into the stream
        Arguments:
            stream (in, char[])    Addition data to add to the serialized data
        Returns:
            char[]    The serialized data and any addition info supplied in the stream
        """
        stream+=ApplicationSerializer.ApplicationSerializer.serialize(len(self._Key))
        stream+=ApplicationSerializer.ApplicationSerializer.serialize(len(self._Signature))
        stream+=ApplicationSerializer.ApplicationSerializer.serialize(len(self._RandomData))
        for v in self._RandomData:
            stream+=ApplicationSerializer.ApplicationSerializer.serialize(v, TypeCode.Byte)
        return stream
    def deserialize(self, stream):
        """
        Description:
            Deserializes the data from the stream into this instance
        Arguments:
            stream (in, char[])    Stream to deserialize
        Returns:
            char[]    The stream minus the deserialized data
        """
        self._RandomData = []
        [self._Key, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        [self._Signature, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        [length, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        for i in range(0, length):
            [v, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Byte)
            self._RandomData.append(v)
        return stream
            
        