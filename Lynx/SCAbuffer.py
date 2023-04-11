from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from .Spectrum import Spectrum
from .Exceptions import InvalidArgumentException
from . import ApplicationSerializer
from . import ParameterTypes
import datetime

class SCAbuffer(SerializableObject):
    """
    Description:
        An instance of this class is used to contain
        SCA acquisition data over a time span
    """    
    class BufferEntry(object):
        """
        Description:
            An instance of this class encapsulates the
            header for a buffer entry
        """            
        class EntryHeader(object):
            """
            Description:
                An instance of this class is used to encapsulate
                the attributes of an SCA buffer header
            """
            def __init__(self):
                """
                Description:
                    Initializes this instance
                Arguments:
                    None
                Return:
                    None
                """
                self.clear()
            def clear(self):
                """
                Description:
                    Resets all contained data to the initial
                    values
                Arguments:
                    none
                Return:
                    none
                """
                self.__startTime=datetime.datetime.now()
                self.__elapsedReal=int(0)
                self.__elapsedLive=int(0)                
                self.__flags=int(0)
                self.__spare=int(0)                
            def getStartTime(self): 
                """
                Description:
                    Returns the start time
                Arguments:
                    none
                Return:
                    Date The value
                """
                return self.__startTime
            def getElapsedLive(self): 
                """
                Description:
                    Returns the elapsed live time (uS)
                Arguments:
                    none
                Return:
                    long  The value
                """
                return self.__elapsedLive
            def getElapsedReal(self): 
                """
                Description:
                    Returns the elapsed real time (uS)
                Arguments:
                    none
                Return:
                    long  The value
                """
                return self.__elapsedReal
            def getFlags(self): 
                """
                Description:
                    Returns the flags
                Arguments:
                    none
                Return:
                    int  The value
                """
                return self.__flags
            def getSpare(self): 
                """
                Description:
                    Returns the spare
                Arguments:
                    none
                Return:
                    int  The value
                """
                return self.__spare
            def getDataSize(self):
                """
                Description:
                    Returns the serialization byte size
                Arguments:
                    none
                Return:
                    int  The value
                """
                return 2*4+3*8
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
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__startTime)
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__elapsedReal)
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__elapsedLive)
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__flags)
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__spare)
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
                self.clear()
                try:
                    [self.__startTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.DateTime)
                    [self.__elapsedReal, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
                    [self.__elapsedLive, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long)
                    [self.__flags, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                    [self.__spare, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                    return stream                
                except Exception as e:
                    self.clear()
                    raise e        
        class SCAdata(object):
            """
            Description:
                An instance of this class is used to encapsulate
                the attributes of  SCA data
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
                self.clear()            
            def clear(self):
                """
                Description:
                    Initializes this instance
                Arguments:
                    none              
                Return:
                    none
                """
                self.__counts=int(0)
                self.__flags=int(0)            
            def getCounts(self): 
                """
                Description:
                    Returns the counts
                Arguments:
                    none
                Return:
                    int The value
                """
                return self.__counts
            def getFlags(self): 
                """
                Description:
                    The flags
                Arguments:
                    none
                Return:
                    int  The value
                """
                return self.__flags 
            def getDataSize(self):
                """
                Description:
                    Returns the serialization byte size
                Arguments:
                    none
                Return:
                    int  The value
                """
                return 2*4
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
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__counts)
                stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__flags)                
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
                self.clear()
                try:
                    [self.__counts, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                    [self.__flags, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)                    
                    return stream                
                except Exception as e:
                    self.clear()
                    raise e       
        def __init__(self):
            """
            Description:
                Initializes this instance
            Arguments:
                none
            Return:
                none
            """
            self.clear()
        def clear(self):
            """
            Description:
                Initializes this contained data members
                to the default values
            Arguments:
                none
            Return:
                none
            """
            self.__data = []
            self.__header = SCAbuffer.BufferEntry.EntryHeader()          
        def getHeader(self):
            """
            Description:
                Gets the header
            Arguments:
                none
            Return:
                (SCAbuffer.BufferHeader) The header
            """
            return self.__header
        def getData(self):
            """
            Description:
                Returns the SCA array
            Arguments:
                none
            Return:
                SCAbuffer.SCAdata[]
            """
            return self.__data    
        def getDataSize(self):
            """
            Description:
                Gets the size in bytes of data to serialize
            Arguments:
                none
            Return:
                (int) the value
            """
            size = self.__header.getDataSize() + 4
            for data in self__data:
                size += data.getDataSize()
            return size
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
            stream += self.__header.serializeData(stream)
            stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__data), objTypeCode=TypeCode.Int)
            for data in self.__data:              
                stream += data.serializeData(stream)
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
            self.clear()
            try:
                stream = self.__header.deserializeData(stream)
                [numEntries, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                for i in range(0, numEntries):
                    data = SCAbuffer.BufferEntry.SCAdata()
                    stream = data.deserializeData(stream)
                    self.__data.append(data)
                return stream
            except Exception as e:
                self.clear()
                raise e                 
    class BufferHeader(object): 
        """
        Description:
            An instance of this class is used to encapsulate
            the attributes of an buffer header
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
            self.clear()
        def clear(self):
            """
            Description:
                Resets all contained data to the initial
                values
            Arguments:
                none
            Return:
                none
            """
            self.__startTime=datetime.datetime.now()
            self.__flags=int(0)
            self._bytesPerSample=int(0)                
        def getStartTime(self): 
            """
            Description:
                Returns the start time
            Arguments:
                none
            Return:
                Date The value
            """
            return self.__startTime
        def getFlags(self): 
            """
            Description:
                Returns the elapsed live time (uS)
            Arguments:
                none
            Return:
                int  The value
            """
            return self.__flags
        def getDataSize(self):
            """
            Description:
                Returns the serialization byte size
            Arguments:
                none
            Return:
                int  The value
            """
            return 2*4+8
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
            stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__startTime)
            stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__flags)
            stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__bytesPerSample)
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
            self.clear()
            try:
                [self.__startTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.DateTime)
                [self.__flags, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                [self.__bytesPerSample, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
                return stream                
            except Exception as e:
                self.clear()
                raise e     
    def __init__(self):
        """
        Description:
            Initializes this instance
        Arguments:
            none
        Return:
            none
        """
        SerializableObject.__init__(self, TypeCode.SCAbufferData)
        self.clear()
    
    def clear(self):
        """
        Description:
            Resets the contained data to default value
        Arguments:
            none
        Return:
            none
        """
        self.__entries = [] 
        self.__header = SCAbuffer.BufferHeader()       
    def getHeader(self):
        """
        Description:
            Gets the header
        Arguments:
            none
        Return:
            (SCAbuffer.BufferHeader) The header
        """
        return self.__header
    def getEntries(self):
        """
        Description:
            Returns the entry array
        Arguments:
            none
        Return:
            SCAbuffer.BufferEntry[]
        """
        return self.__entries    
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        size = self.__header.getDataSize() + 4
        for entry in self__entries:
            size += entry.getDataSize()
        return size
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
        stream += self.__header.serializeData(stream)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__entries), objTypeCode=TypeCode.Int)
        for entry in self.__entries:              
            stream += entry.serializeData(stream)
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
        self.clear()
        try:
            stream = self.__header.deserializeData(stream)
            [numEntries, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
            for i in range(0, numEntries):
                entry = SCAbuffer.BufferEntry()
                stream = entry.deserializeData(stream)
                self.__entries.append(entry)
            return stream
        except Exception as e:
            self.clear()
            raise e