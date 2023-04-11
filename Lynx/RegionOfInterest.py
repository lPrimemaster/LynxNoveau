from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from . import ApplicationSerializer

class RegionOfInterestTypes(object):
    """
    Description:
        This class contains the definition for all
        types of regions of interest
    """
    Type1=1
    Type2=2
    Type3=3
    Type4=4
    
class RegionOfInterest(SerializableObject):
    """
    Description:
        An instance of this class is used to encapsulate the
        attributes of a region of interest
    """
    def __init__(self, left=0, right=1, type=1):
        """
        Description:
            Initializes this instance
        Arguments:
            left (int)    The left region channel
            right (int)   The right region channel
            type (int)    The type of region, see RegionOfInterestTypes class
        Return:
            none
        """
        SerializableObject.__init__(self, TypeCode.RegionOfInterestData)
        self.__left=left
        self.__right=right
        self.__rgnType=type
    def getLeft(self):
        """
        Description:
            Returns the left channel
        Arguments:
            none
        Return:
            (int)    The value
        """
        return self.__left
    def getRight(self):
        """
        Description:
            Returns the right channel
        Arguments:
            none
        Return:
            (int)    The value
        """
        return self.__right
    def getRgnType(self):
        """
        Description:
            Returns the type
        Arguments:
            none
        Return:
            (int)    The value
        """
        return self.__rgnType
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        return 12
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__left, objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__right, objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__rgnType, objTypeCode=TypeCode.Int)
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
        [self.__left, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__right, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__rgnType, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        return stream
        