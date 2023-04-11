from .SerializableObject import SerializableObject
from .TypeCode import TypeCode
from .Exceptions import InvalidArgumentException
from . import ApplicationSerializer
from . import ParameterTypes
import datetime


class SCAdefinitions(SerializableObject):
    """
    Description:
        An instance of this class is used to contain
        all SCA region definitons
    """
    class Definition(object):
        """
        Description:
            An instance of this class is used to encapsulate
            the attributes of an SCA definition
        """
        def __init__(self, LLD, ULD):
            """
            Description:
                Initializes this instance
            Arguments:
                LLD (float)    The LLD %
                ULD (float)    The ULD %
            Return:
                none
            """
            self.__lld=LLD
            self.__uld=ULD
        def getLLD(self): 
            """
            Description:
                Returns the LLD %
            Arguments:
                none
            Return:
                float The value
            """
            return self.__lld
        def getULD(self): 
            """
            Description:
                Returns the ULD %
            Arguments:
                none
            Return:
                float The value
            """
            return self.__uld
    """
    Description:
        An instance of this class is used to contain
        all of the SCA definitions
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
        SerializableObject.__init__(self, TypeCode.SCAdefinitionData)
        self.__definitions = []        
    def getNumberOfDefinitions(self):
        """
        Description:
            Gets the number of definitions
        Arguments:
            none
        Return:
            (int) The number of
        """
        return len(self.__definitions)
    def getDefinitions(self):
        """
        Description:
            Gets the definitions
        Arguments:
            none
        Return:
            (Definition[]) The definitions
        """
        return self.__definitions
    def clear(self):
        """
        Description:
            Clears all the definitions
        Arguments:
            none
        Return:
            none
        """
        self.__definitions = []  
    def add(self, defin):
        """
        Description:
            Adds a definition
        Arguments:
            defin (Definition) A definition to add
        Return:
            none
        Exceptions:
            InvalidArgumentException
        """
        if (False == isinstance(defin, SCAdefinitions.Definition)):
            raise InvalidArgumentException('Argument must be of type Definition')   
        self.__definitions.append(defin)    
    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        return len(self.__definitions)*2*4 + 4    
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__definitions), objTypeCode=TypeCode.Int)
        for defin in self.__definitions:              
            stream += ApplicationSerializer.ApplicationSerializer.serialize(defin.getLLD(), objTypeCode=TypeCode.Float)
            stream += ApplicationSerializer.ApplicationSerializer.serialize(defin.getULD(), objTypeCode=TypeCode.Float)
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
        self.__definitions = []
        [numOf, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int)
        for i in range(0, numOf): 
            [LLD, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Float) 
            [ULD, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Float) 
            self.__definitions.append(SCAdefinitions.Definition(LLD, ULD))
        return stream
        
        