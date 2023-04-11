from . import ApplicationSerializer
from .Serializable import Serializable
from .TypeCode import TypeCode

class MessageHeader(Serializable):
    """
    Description:
        An instance of this class is used to create a message
        header that is used for all Lynx communications
    """
    def getHeaderSize(self):
        return 4*4
    def getCRC(self):  
        """
        Description:
            Returns the CRC
        Arguments:
            none
        Returns:
            (int) The value
        """       
        return self.__CRC
    def getVersion(self):         
        """
        Description:
            Returns the version
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__Version
    def getSequenceNumber(self): 
        """
        Description:
            Returns the UDP sequence #
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__SequenceNumber
    def getSize(self): 
        """
        Description:
            Returns the message size (bytes)
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__Size
    def __init__(self, crc=0, size=0):
        """
        Description:
            Initializes this instance with the following info
        Arguments:
            crc (in, int)     The CRC32 value
            size (in, int)    The size (bytes) of the message
        Returns:
            none
        """
        self.__Size=size+self.getHeaderSize()
        self.__Version=1
        self.__SequenceNumber=0
        self.__CRC=crc
    def serialize(self, stream=''):
        """
        Description:
            Serializes all contained data into a stream
        Arguments:
            stream (in, char[])    Stream to add.
        Returns:
            char[]    The serialized data
        """
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__Size)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__Version)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__SequenceNumber)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__CRC)
        return stream
    def deserialize(self, stream):
        """
        Description:
            Deserializes all data in the stream into this instance
        Arguments:
            stream (in, char[])    Stream containing the data.
        Returns:
            char[]    The serialized data minus the data
        """
        [self.__Size, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        [self.__Version, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        [self.__SequenceNumber, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        [self.__CRC, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        return stream
        
                        