from .Serializable import *
import struct

class MetaData(Serializable):
    """
    Description:
        An instance of this contains metadata about
        a Lynx data type
    """
    def __init__(self, type=0, size=0):
        """
        Description:
            Initializes this instance
        Arguments:
            type    (in, int) Defines the type of data.  See TypeCode class
            size    (in, int) Defines the size of the data in bytes
        """        
        self.__type = type
        self.__size = size
    def getDataType(self): 
        """
        Description:
            Returns the data type member
        Arguments:
            none
        Return:
            The value
        """ 
        return self.__type
    def getDataSize(self):
        """
        Description:
            Returns the data size member (in bytes)
        Arguments:
            none
        Return:
            The value
        """ 
        return self.__size
    def serialize(self, stream=''):
        """
        History:
            This method serializes the data contained
            in this instance into the stream
        Arguments:
            stream    (in, out) The stream to receive the data
        Return:
            none
        """
        stream += struct.pack("<ii", self.__type, self.__size)
        return stream
    def deserialize(self, stream):
        """
        History:
            This method deserializes the data contained
            in the stream into this instance 
        Arguments:
            stream    (in, out) The stream to receive the data
        Return:
            char[]    The stream minus the deserialized data
        """
        v=stream[0:8]
        data=struct.unpack("<ii", v)
        self.__type = data[0]
        self.__size = data[1]
        stream=stream[8:]
        return stream
        
        