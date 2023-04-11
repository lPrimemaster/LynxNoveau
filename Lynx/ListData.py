from .SerializableObject import SerializableObject
from .Exceptions import DeviceErrorException
from .TypeCode import TypeCode
from .Spectrum import Spectrum
from . import ApplicationSerializer
import datetime

class ListMasks(object):
    """
    Description:
        This clas contains the masks for the list flag
    """
    ListOverflowBufferA = 0x1        #First buffer overflowed
    ListOverflowBufferB = 0x2        #Second buffer overflowed
    ListMissingData = 0x4            #Failed to send previous data buffers.  Hence, data is missing
    ListVersionMask = 0xFFFF0000     #Version information
    
class ListDataBase(SerializableObject):
    DSA3K_UNSUPPORTED_LISTFORMAT = 4020306293    #unsupported protocol format for list data    
    
    """
    Description:
        This is the base class for all list data.  It encapsulates data
        common to all types of list data
    """
    def __init__(self, type):
        """
        Description:
            Initializes this instance
        Arguments:
            type        The type of list data
        Returns:
            none
        """
        SerializableObject.__init__(self, type)
        self.__startTime=datetime.datetime.now()
        self.__realTime=0.0
        self.__liveTime=0.0
        self.__timeBase=0
        self.__flags=0
    def getStartTime(self):
        """
        Description:
            Returns the start time value
        Arguments:
            none
        Returns:
            (DateTime)    The value
        """
        return self.__startTime
    def getRealTime(self):
        """
        Description:
            Returns the real time value (us)
        Arguments:
            none
        Returns:
            (long)    The value
        """
        return self.__realTime    
    def getLiveTime(self):
        """
        Description:
            Returns the live time value (us)
        Arguments:
            none
        Returns:
            (long)    The value
        """
        return self.__liveTime    
    def getTimebase(self):
        """
        Description:
            Returns the timebase value (ns)
        Arguments:
            none
        Returns:
            (int)    The value
        """
        return self.__timeBase
    def getFlags(self):
        """
        Description:
            Returns the flags value.  See class ListMasks
        Arguments:
            none
        Returns:
            (int)    The value
        """
        return self.__flags
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
        return 3*8 + 3*4        
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__startTime)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__realTime, objTypeCode=TypeCode.Long)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__liveTime, objTypeCode=TypeCode.Long)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__timeBase, objTypeCode=TypeCode.Int)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__flags, objTypeCode=TypeCode.Int)
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
        [self.__startTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.DateTime) 
        [self.__realTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long) 
        [self.__liveTime, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Long) 
        [self.__timeBase, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__flags, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        return stream
    
class ListData(ListDataBase):
    """
    Description:
          This class encapsulates all information for List data
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
        ListDataBase.__init__(self, TypeCode.ListData)
        self.__events = []
    def getEvents(self):
        """
        Description:
            Returns the events
        Arguments:
            none
        Returns:
            short[]    The value
        """
        return self.__events
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
        return ListDataBase.getDataSize(self) + len(self.__events)*2
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
        stream += ListDataBase.serializeData(self)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__events))
        for event in self.__events:                    
            stream += ApplicationSerializer.ApplicationSerializer.serialize(event, objTypeCode=TypeCode.Ushort)
        return stream
    def deserializeData(self, stream):
        """
        Description:
            Deserializes all data contained in this instance into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Exceptions:
            DeviceErrorException    Unsupported protocol list format
        Returns:
            char[]    The stream minus the deserialized data
        """
        self.__events = []
        stream = ListDataBase.deserializeData(self, stream)
        version = ((self.getFlags()&(ListMasks.ListVersionMask)) >> 16)
        if (version != 0):
            raise DeviceErrorException(ListDataBase.DSA3K_UNSUPPORTED_LISTFORMAT)
        [numEvents, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        for i in range(0, numEvents):
            [event, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
            self.__events.append(event)
        return stream
    
class TlistDataS(object):
    """
    Description:
        This class encapsulates all information for a single time stamped list data
        event
    """
    def __init__(self, event, time):
        """
        Description:
            Initializes this instance
        Arguments:
            event (in, int)    The event
            time (in, int)     The time
        Returns:
            none
        """
        self.__event = event
        self.__time = time
        
    def getEvent(self):
        """
        Description:
            Returns the event
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__event
    def getTime(self):
        """
        Description:
            Returns the time (uS)
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__time

class TlistData(ListDataBase):
    """
    Description:
        This class encapsulates all information for time stamped list data
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
        ListDataBase.__init__(self, TypeCode.TlistData)
        self.__events = []
    def getEvents(self):
        """
        Description:
            Returns the events
        Arguments:
            none
        Returns:
            TlistDataS[]    The value
        """
        return self.__events
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
        return ListDataBase.getDataSize(self) + len(self.__events)*4
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
        stream += ListDataBase.serializeData(self)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__events))
        for event in self.__events:                    
            stream += ApplicationSerializer.ApplicationSerializer.serialize(event.event, objTypeCode=TypeCode.Ushort)
            stream += ApplicationSerializer.ApplicationSerializer.serialize(event.time, objTypeCode=TypeCode.Ushort)
        return stream
    def deserializeData(self, stream):
        """
        Description:
            Deserializes all data contained in this instance into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Exceptions:
            DeviceErrorException    Unsupported protocol list format
        Returns:
            char[]    The stream minus the deserialized data
        """
        self.__events = []
        stream = ListDataBase.deserializeData(self, stream)
        version = ((self.getFlags()&(ListMasks.ListVersionMask)) >> 16)
        if (version != 0):
            raise DeviceErrorException(ListDataBase.DSA3K_UNSUPPORTED_LISTFORMAT)        
        [numEvents, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        for i in range(0, numEvents):
            [event, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
            [time, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
            self.__events.append(TlistDataS(event, time))
        return stream
