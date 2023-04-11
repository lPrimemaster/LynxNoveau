from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from .CommandCodes import CommandCodes
from .ParameterCodes import ParameterCodes
from .Exceptions import SerializationException, UnsupportedTypeException
from . import ApplicationSerializer
import struct

class Parameter(SerializableObject):
    """
    Description:
        An instance of this class is used to encapsulate a parameter data type
        This data type is used to get and set Lynx settings.  A parameter
        is described by a code and a value.  This class contains both these
        attributes.
    """
    def getValue(self):
        """
        Description:
            Returns the parameter value
        Arguments:
            none
        Returns:
            any    The value
        """
        return self.__value
    def setValue(self, val):
        """
        Description:
            Sets the value into this instance
        Arguments:
            val (any)                   The value
        Exceptions:
            UnsupportedTypeException    The data type is not supported
        Return:
            none
        """
        #See if this type is supported
        try:
            ApplicationSerializer.ApplicationSerializer.getTypeCode(val)
        except SerializationException:
            raise UnsupportedTypeException()
        self.__value = val
    """
    Description:
        An instance of this class encapsulates information about
        a lynx parameter.
    """
    def __init__(self, code=0, value=None):
        """
        Description:
            Initializes this instance with the supplied information
        Arguments:
            code   (in, int) The parameter code.  See ParameterCodes
                   class
            val    (in, any) The value to assign to this parameter
        Exception:
            UnsupportedTypeException    Thrown whe the value specified 
                                        is not supported
        Returns:
            none
        """
        SerializableObject.__init__(self, TypeCode.ParameterData)
        self.__parameterCode = code
        #try:
        #    ApplicationSerializer.ApplicationSerializer.getTypeCode(value)
        #except SerializationException:
        #    raise UnsupportedTypeException()
        #self.__value = value
        self.setValue(value)
    def getParameterCode(self):
        """
        Description:
            Returns the parameter code.  See class ParameterCodes class
        Arguments:
            none
        Returns:
            int    The value
        """
        return self.__parameterCode    
    def getDataSize(self):
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
        cnt += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__value)
        return cnt
    def serializeData(self, stream=''):
        """
        Description:
            Serializes all data contained in this instace into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream containing the results
        """
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__parameterCode, objTypeCode=TypeCode.Int)
        typeCode = ApplicationSerializer.ApplicationSerializer.getTypeCode(self.__value)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(typeCode, objTypeCode=TypeCode.Int)
        if (TypeCode.String != typeCode):
            stream += ApplicationSerializer.ApplicationSerializer.serialize(ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__value), objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__value)
        return stream
    def deserializeData(self, stream):
        """
        Description:
            Deserializes all data contained in this instance into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream minus the deserialized data
        """
        [self.__parameterCode, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [typeCode, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        
        #
        #The appserializer requires length info in stream to deserialize a string. 
        #Therefore, leave this info in the stream.
        #
        if (TypeCode.String != typeCode):
            [size, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
            
        [self.__value, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, typeCode) 
        return stream
            