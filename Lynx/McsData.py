from .SpectralData import SpectralData
from .TypeCode import TypeCode
from .Exceptions import UnsupportedCompressionException
from . import ApplicationSerializer

class McsData(SpectralData):
    """
    Description:
        An instance of this class is used to encapsulate all data related
        to Mcs data such as spectrum, sweeps, dwell
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
        SpectralData.__init__(self, TypeCode.McsData)
        self.__sweeps = 0
        self.__dwell = 0
    def getDwellTime(self):
        """
        Description:
            This method will return the dwell time (nS)
        Arguments:
            None
        Returns:
            (double) The value
        """
        return self.__dwell
    def getSweeps(self):
        """
        Description:
            This method will return the sweeps
        Arguments:
            None
        Returns:
            (long) The value
        """
        return self.__sweeps
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        return SpectralData.getDataSize(self) + 2*8
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__dwell, objTypeCode=TypeCode.Long)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__sweeps, objTypeCode=TypeCode.Long)
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
        [self.__dwell, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
        [self.__sweeps, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
        return SpectralData.deserializeData(self, stream)
        