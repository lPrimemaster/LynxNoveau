from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from .Spectrum import Spectrum
from . import ApplicationSerializer

class EnumerationValueAttributes(object):
    """
    Description:
        This class encapsulates all of the attributes
        of an enumeration value.  An enumeration value
        consists of the name (English), value, and 
        name resource identifier
    """
    def __init__(self, name, val, nameId):
        """
        Description:
            Initializes this instance
        Arguments:
            none
        Return:
            none
        """
        self.__name = name
        self.__value = val
        self.__nameId = nameId
    def getName(self):
        """
        Description:
            Accessor to the English name
        Arguments:
            none
        Return:
            (string) the value
        """
        return self.__name
    def getValue(self):
        """
        Description:
            Accessor to the value
        Arguments:
            none
        Return:
            (object) the value
        """
        return self.__value
    def getNameId(self):
        """
        Description:
            Accessor to the name resource identifier
        Arguments:
            none
        Return:
            (int) the value
        """
        return self.__nameId
        
class ParameterAttributeType(object):
    """
    Description:
        The class definitions for the types of parameter
        attributes
    """
    ReadOnly=1                #Parameter is read-only
    HardwareWrite=2           #Parameter is written to hardware
    Array=4                   #Parameter is an array type of parameter
    PerInput=8                #Parameter is a per input parameter (input 1-N)
    RealTime=16               #Parameter is a real time parameter
    Required=32               #Parameter is required    
    Enumerable=64             #Parameter is enumerable (i.e., it has discrete values)
    
class ParameterValueType(object):
    """
    Description:
        the class definitions for the types of parameter
        values
    """
    Unknown = 0        
    Ubyte = 1
    Ushort = 2
    Ulong = 3
    Byte = 4
    Short = 5
    Long = 6
    Float = 7
    Double = 8
    String =  9
    Int64 = 10
    Uint64 = 11
    Bool = 12
    DateTime = 13
    Null = 14
class ParameterAttributes(SerializableObject):
    """
    Description:
        This class encapsulates all of the meta-data for
        a parameter such as: min, max, default, name, desc,....
    """
    def __init__(self):
        """
        Description:
            Initializes this instance
        Arguments:
            none
        Return:
            none
        """
        SerializableObject.__init__(self, TypeCode.ParameterMetaData)
        self.__name=""
        self.__description=""
        self.__code=0
        self.__min=None
        self.__max=None
        self.__def=None
        self.__step=None
        self.__attr=None
        self.__enum=[]
        self.__paramDataType=None
        self.__enumAttributes=[]
        
    def getEnumerationAttributes(self):
        """
        Description:
            Returns the enumeration attributes
        Arguments:
            none
        Return:
            EnumerationValueAttributes[]    The value
        """
        return self.__enumAttributes
    def getName(self):
        """
        Description:
            Returns the name of the parameter
        Arguments:
            none
        Return:
            string    The value
        """
        return self.__name
    def getDescription(self):
        """
        Description:
            Returns the description of the parameter
        Arguments:
            none
        Return:
            string    The value
        """
        return self.__description
    def getCode(self):
        """
        Description:
            Returns the parameter code. See ParameterCodes
        Arguments:
            none
        Return:
            int    The value
        """
        return self.__code
    def getMinimum(self):
        """
        Description:
            Returns the min val
        Arguments:
            none
        Return:
            any    The value
        """
        return self.__min
    def getMaximum(self):
        """
        Description:
            Returns the max val
        Arguments:
            none
        Return:
            any    The value
        """
        return self.__max
    def getDefault(self):
        """
        Description:
            Returns the default val
        Arguments:
            none
        Return:
            any    The value
        """
        return self.__def
    def getStepSize(self):
        """
        Description:
            Returns the step size
        Arguments:
            none
        Return:
            any    The value
        """
        return self.__step
    def getAttributes(self):
        """
        Description:
            Returns the parameter attributes.  See ParameterAttributes class
        Arguments:
            none
        Return:
            int    The value
        """
        return self.__attr
    def getEnumeration(self):
        """
        Description:
            Returns the enumeration
        Arguments:
            none
        Return:
            any[]    The value
        """
        return self.__enum
    def getValueType(self):
        """
        Description:
            Returns the parameter data type.  See ParameterValueType class
        Arguments:
            none
        Return:
            int    The value
        """
        return self.__paramDataType
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        size=len(self.__description)
        size+=len(self.__name)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__code)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__min)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__max)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__def)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__step)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__attr)
        size += ApplicationSerializer.ApplicationSerializer.getTypeSize(self.__paramDataType)
        for e in self.__enum:
            size += ApplicationSerializer.ApplicationSerializer.getTypeSize(e)
        for enum in self.__enumAttributes:
             size += ApplicationSerializer.ApplicationSerializer.getTypeSize(enum.getName())
        for enum in self.__enumAttributes:
             size += ApplicationSerializer.ApplicationSerializer.getTypeSize(enum.getNameId())                 
        return size;
    def serializeData(self, stream):
        """
        Description:
            Serializes all data contained in this instance into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream containing the results
        """        
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__code, objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.serialize(self.__attr, objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.serialize(self.__paramDataType, objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.serialize(len(self.__enum), objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.serialize(len(self.__min))
        stream += ApplicationSerializer.serialize(len(self.__max))
        stream += ApplicationSerializer.serialize(len(self.__def))
        stream += ApplicationSerializer.serialize(len(self.__description))
        stream += ApplicationSerializer.serialize(len(self.__name))
        stream += ApplicationSerializer.serialize(len(self.__step))        
        for enum in self.__enum:
             stream += ApplicationSerializer.serialize(enum)        
        for enum in self.__enumAttributes:
             stream += ApplicationSerializer.serialize(enum.getName())
        for enum in self.__enumAttributes:
             stream += ApplicationSerializer.serialize(enum.getNameId())
        return stream
    def deserializeData(self, stream):
        """
        Description:
            Deserializes all data contained in this instace into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream minus the deserialized data
        """
        self.__enumAttributes = []
        self.__enum = []
        [self.__code, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__attr, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__paramDataType, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [numEnums, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__min, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream) 
        [self.__max, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream) 
        [self.__def, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream) 
        [self.__description, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream) 
        [self.__name, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream)
        [self.__step, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream) 
                        
        for i in range(0, numEnums):
            [enum, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream)
            self.__enum.append(enum)        
        names = []    
        for i in range(0, numEnums):
            [n, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream)
            names.append(n)
        ids = []    
        for i in range(0, numEnums):
            [id, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream)
            ids.append(id)        
        for i in range(0, numEnums):
            self.__enumAttributes.append(EnumerationValueAttributes(names[i], self.__enum[i], ids[i]))

        return stream
