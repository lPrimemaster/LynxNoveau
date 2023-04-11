from .ApplicationSerializer import ApplicationSerializer


class Variant(Serializable):
    """
    Description:
        An instance of this class represents a data 
        type that the Lynx device can use.
    """
    def __init__(self, val=None):
        """
        Description:
            Initializes this instance with
            the data supplied
        Arguments:
            val (in, any)                The value to assign to this instance
        Exceptions:
            UnsupportedTypeException    The data type is not supported
        Return:
            none
        """
        self.setValue(val)
    def getValue(self):
        """
        Description:
            Returns the value contained within
            this instance
        Arguments:
            None
        Return:
            any    The value
        """
        return self.__value
    def setValue(self, val):
        """
        Description:
            Sets the value into this instance
        Arguments:
            none
        Exceptions:
            UnsupportedTypeException    The data type is not supported
        Return:
            any (in, any)                The value
        """
        #See if this type is supported
        try:
            ApplicationSerializer.getType(val)
        except SerializationException:
            raise UnsupportedTypeException()
        self.__value = val
    def getSize(self):
        """
        Description:
            Returns the number of bytes necessary to serialize
            all data contained in this instance
        Arguments:
            none
        Returns:
            (int)    The value
        """
        cnt = 4
        cnt += ApplicationSerializer.getTypeSize(self.__value)
        return cnt
    def serialize(self, stream=''):
        """
        Description:
            Serializes all data contained in this instace into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream containing the results
        """
        stream += struct.pack("i", ApplicationSerializer.getTypeSize(self.__value))
        stream += ApplicationSerializer.serialize(self.__value)
        return stream
    def deserialize(self, stream):
        """
        Description:
            Deserializes all data contained in this instace into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream minus the deserialized data
        """
        typeCode = struct.unpack("i", stream[0:4])
        stream = stream[4:]
        res = ApplicationSerializer.deserialize(stream, typeCode) 
        self.__value = res[0]
        return res[1]
        