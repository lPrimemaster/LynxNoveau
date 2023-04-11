from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from .Exceptions import UnsupportedCompressionException
from . import ApplicationSerializer
import datetime
class CounterAttribute(object):
    """
    Description:
        An instance of this class is used to encapsulate the
        attributes of a counter
    """
    def __init__(self, corrVal=0, uncorrVal=0, flags=0):
        """
        Description:
            Initializes this instance with the supplied information
        Arguments:
            corrVal    (in, int) The corrected val
            uncorrVal  (in, int) The uncorrected val
            flags      (in, int) Flags
        Returns:
            none
        """
        self.__corrVal=corrVal
        self.__uncorrVal = uncorrVal
        self.__flags = flags
    def getCorrectedValue(self):
        """
        Description:
            Returns the corrected value
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__corrVal
    def getUncorrectedValue(self):
        """
        Description:
            Returns the uncorrected value
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__uncorrVal
    def getFlags(self):
        """
        Description:
            Returns the flags
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__flags
    def getDataSize(self):
        """
        Description:
            Returns the number of bytes for serializing
        Arguments:
            none
        Returns:
            (int) The value
        """
        return 4
    
class CounterSample(object):
    """
    Description:
        An instance of this class is used to encapsulate a
        sample from a counter
    """
    def __init__(self, startTime=datetime.datetime.now(), elapsed=0, attr=[]):
        """
        Description:
            Initializes this instance
        Arguments:
            startTime (in, DateTime)            The start time
            elapsed   (in, int)                 The elapsed time (uS)
            attr      (in, CounterAttribute[])  The counter attributes
        Returns:
            none
        """
        self.__startTime = startTime
        self.__elapsed = elapsed
        self.__attributes = attr
    def getStartTime(self):
        """
        Description:
            Returns the start time
        Arguments:
            none
        Returns:
            (DateTime) The value
        """
        return self.__startTime
    def getElapsed(self):
        """
        Description:
            Returns the elapsed time (uS)
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__elapsed
    def getAttributes(self):
        """
        Description:
            Returns a collection of counter
            attributes
        Arguments:
            none
        Returns:
            (CounterAttributes[]) The value
        """
        return self.__attributes
    def getDataSize(self):
        """
        Description:
            Returns the number of bytes necessary to
            serialize this instance
        Arguments:
            none
        Returns:
            (int) The value
        """
        size = 16
        nAttrs = len(self.__attributes)
        if (nAttrs > 0):
            size += nAttrs*self.__attributes[0].getDataSize()
        return size
    def serializeData(self, stream):
        """
        Description:
            Serializes the data in this instance into a
            stream
        Arguments:
            stream (char[])  The stream to append to
        Returns:
            (char[]) The stream containing the serialized data
        """
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__startTime, objTypeCode=TypeCode.DateTime)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__elapsed, objTypeCode=TypeCode.Long)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__attributes), objTypeCode=TypeCode.Short)
        for i in range(0, len(self.__counts)):
            stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__attributes[i].getUncorrectedValue())
            stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__attributes[i].getValue())
            stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__attributes[i].getFlags())

class CounterData(SerializableObject):
    """
    Description:
        An instance of this class is used to encapsulate all
        counter data
    """
    def __init__(self):
        """
        Description:
            Initializes this instance
        Arguments:
            none
        Returns:
            none
        """
        SerializableObject.__init__(self, TypeCode.CounterData)
        self.__samples = []
    def getSamples(self):
        """
        Description:
            Returns a collection of samples
        Arguments:
            none
        Returns:
            (CounterSample []) The value
        """
        return self.__samples
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
        size = 4
        nSamps = len(self.__samples)
        if (nSamp > 0):
            size += nSamps*self.__samples[0].getDataSize()
        return size
    def serializeData(self, stream):
        """
        Description:
            Serializes all data contained in this instace into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream containing the results
        """
        numSamps = len(self.__samples)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(numSamps, objTypeCode=TypeCode.Short)
        size=0
        if (numSamps > 0):
            size = self.__samples[0].getDataSize()
        stream += ApplicationSerializer.ApplicationSerializer.serialize(size, objTypeCode=TypeCode.Short)
        for i in range(0, nSamps):
            stream += self.__samples[i].serializeData()
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
        [nSamp, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Short)
        [bytesPerSamp, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Short)
        for i in range(0, nSamp):
            numRead=0;
            numCnts=0;
            attrs = []
            if (bytesPerSamp > numRead): 
                [start, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.DateTime)
                numRead += 8
            if (bytesPerSamp > numRead):
                [elapsed, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
                numRead += 8
            if (bytesPerSamp > numRead):
                [numCnts, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                numRead += 4 
            for j in range(0, numCnts):
                if (bytesPerSamp > numRead):
                    [uVal, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
                    numRead += 4
                    [val, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                    numRead += 4
                    [flags, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                    numRead += 4
                    attrs.append(CounterAttribute(val, uVal, flags))          
            samp=CounterSample(start, elapsed, attrs)
            if (bytesPerSamp > numRead):
                stream = stream[(bytesPerSamp-numRead):]
            self.__samples.append(samp)
        return stream