from .SpectralData import SpectralData
from .TypeCode import TypeCode
from .Exceptions import UnsupportedCompressionException
from . import ApplicationSerializer

class PhaData(SpectralData):
    """
    Description:
        An instance of this class is used to encapsulate all data related
        to Pha data such as spectrum, real time, live time, computational
        value.
    """
    def __init__(self):
        """
        Description:
            This method will initialize the instance
        Arguments:
            None
        Returns:
            None
        """
        SpectralData.__init__(self, TypeCode.PhaData)
        self.__liveTime = 0
        self.__realTime = 0
        self.__compValue = 0
    def getLiveTime(self):
        """
        Description:
            This method will return the live time (uS)
        Arguments:
            None
        Returns:
            (double) The value
        """
        return self.__liveTime
    def getRealTime(self):
        """
        Description:
            This method will return the real time (uS)
        Arguments:
            None
        Returns:
            (double) The value
        """
        return self.__realTime
    def getComputationalValue(self):
        """
        Description:
            This method will return the computational
            value provided computational preset is enabled
        Arguments:
            None
        Returns:
            (Long) The value
        """
        return self.__compValue
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        return SpectralData.getDataSize(self) + 3*8
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__liveTime, objTypeCode=TypeCode.Long)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__realTime, objTypeCode=TypeCode.Long)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__compValue, objTypeCode=TypeCode.Long)
        stream += SpectralData.serializeData(self)
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
        [self.__liveTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
        [self.__realTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
        [self.__compValue, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
        return SpectralData.deserializeData(self, stream)
        