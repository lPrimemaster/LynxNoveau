from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from .Exceptions import UnsupportedCompressionException
from . import ApplicationSerializer

class SpectrumEncodingType(object):
    """
    Description:
        This class defines the different encoding schemes used for
        spectral data transmission.
    """
    EncodingNone=0
    DifferenceCompression=1
    
    
class Spectrum(SerializableObject):
    """
    Description:
        An instance of this class is used to encapsulate all data related
        to a spectrum such as counts, number of channels, and encoding
        scheme.
    """
    def __init__(self):
        """
        Description:
            Initializes this instance.
        Arguments:
            None
        Return:
            None
        """
        SerializableObject.__init__(self, TypeCode.SpectralData)
        self.__encoding = SpectrumEncodingType.EncodingNone
        self.__numChannels = 0
        self.__counts = []
    def getEncoding(self):
        """
        Description:
            Gets the encoding type.  See EncodingNone class
        Arguments:
            none
        Return:
            (int) the value
        """
        return self.__encoding
    def getNumberOfChannels(self):
        """
        Description:
            Gets the number of channels
        Arguments:
            none
        Return:
            (int) the value
        """
        return self.__numChannels
    def getCounts(self):
        """
        Description:
            Gets the spectrum counts
        Arguments:
            none
        Return:
            (int []) the value
        """
        return self.__counts
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Exception:
            UnsupportedCompressionException
        Return:
            (int) the value
        """
        if (SpectrumEncodingType.EncodingNone == self.__encoding):
            return self.__numChannels*4 + 3*4
        raise UnsupportedCompressionException
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__encoding)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__numChannels)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__counts))
        for cnt in self.__counts:
            stream += ApplicationSerializer.ApplicationSerializer.serialize(cnt)
        return stream
    def deserializeData(self, stream):
       """
        Description:
            Deserializes all data contained in thi into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream containing the results
        """
       self.__counts = []
       [self.__encoding, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
       [self.__numChannels, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
       [numEncoded, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
       for i in range(0, self.__numChannels):
           [cnt, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
           self.__counts.append(cnt)
       return stream
