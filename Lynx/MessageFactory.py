from .Exceptions import UnsupportedTypeException, ChecksumException, MessageVersionException
from .DigitalSignature import DigitalSignature
from .MessageHeader import MessageHeader
from .TypeCode import TypeCode
from .SerializableObject import SerializableObject
from . import ApplicationSerializer
import zlib

class MessageFactory(object):
    """
    Description:
        An instance of this class is used to contruct/deconstruct messages
        sent to and received from the Lynx
    """        
    def supportsMsgVersion(ver):
        """
        Description:
            This method validates the version information
        Arguments:
            ver (in, int)    The version to validate
        Returns:
            bool            True==valid version
        """
        if (1 == ver):
            return True
        else:
            return False
    supportsMsgVersion = staticmethod(supportsMsgVersion)
    def serializeToMessage(data):
        """
        Description:
            This method serializes the data into a stream
        Arguments:
            data (in, SerializableObject)    The data to serialize
        Exceptions:
            UnsupportedTypeException        Data type is not supported
        Returns:
            char[]    The stream
        """
        if (isinstance(data, SerializableObject) is False):
            raise UnsupportedTypeException()
        
        #Serialize the data
        dataStream = ApplicationSerializer.ApplicationSerializer.serialize(data, writeMeta=True);
        
        #Sign the data and serialize the signature
        DS = DigitalSignature(dataStream)
        DS.sign()
        dsStream = DS.serialize()
        crc = zlib.crc32(dsStream+dataStream)
        
        #Create the message header and serialize it
        msgHdr = MessageHeader(crc, len(dsStream)+len(dataStream))
        hdrStream = msgHdr.serialize()
        
        #Return the entire message serialized (sum of all parts)
        return hdrStream+dsStream+dataStream
    serializeToMessage = staticmethod(serializeToMessage)
    def deserializeFromMessage(stream):
        """
        Description:
            This method serializes the data into a stream
        Arguments:
            stream (in, char[])    The message stream
        Exceptions:
            MessageVersionException
            ChecksumException
            DigitalSignatureException
        Returns:
            [any, char[]]    [Data, the stream minus deserialized info]
        """
        msgHdr = MessageHeader()
        stream = msgHdr.deserialize(stream)
        if (MessageFactory.supportsMsgVersion(msgHdr.getVersion()) is False):
            raise MessageVersionException()
        
        crc = zlib.crc32(stream)
        if (crc != msgHdr.getCRC()):
            raise ChecksumException()
        
        ds = DigitalSignature()
        stream = ds.deserialize(stream)
        ds.verify()
        
        return ApplicationSerializer.ApplicationSerializer.deserialize(stream)
    deserializeFromMessage = staticmethod(deserializeFromMessage)
                              