from .SerializableObject import SerializableObject, Serializable
from .TypeCode import TypeCode
from .CommandCodes import CommandCodes
from . import ApplicationSerializer
import struct

class InternalCommandCodes(CommandCodes):
    """
    Description:
        This class contains all of the command codes
        that are used internal to this package
    """
    Unknown=0            #Unknown command
    Lock = 1             #Lock input for exclusive access
    Unlock = 2           #Unlock input from exclusive access
    GetParameter = 6     #Get a parameter
    PutParameter = 7     #Put a parameter
    Response = 8         #Response to a command (received from a Lynx)
    GetSpectralData=13   #Gets the spectral data (time, preset, counts, etc)
    GetSpectrum=14       #Gets the spectrum data (counts only)
    PutSpectrum=15       #Sets the spectrum data (counts only)
    GetParameterList=16    #Gets a list of parameters for an input    
    PutParameterList = 17  #Sets a list of parameters for an input
    AddUser=18             #Adds a user account
    DeleteUser=19          #Deletes a user account
    EnumerateUsers=20      #Enumates all user accounts 
    GetRegionsOfInterest=21    #Gets the regions of interest
    PutRegionsOfInterest=22    #Sets the regions of interest
    UpdateUser=23              #Updates a user account
    ValidateUser = 26          #Validates the user
    GetDsoData=27              #Gets the latest DSO data
    GetCounterData=37          #Get the counter data
    GetListData=41             #Gets the List data
    GetMSSData=43              #Gets the MSS data
    GetSCAbuffer=49            #Gets the SCA buffer
    GetSCAdefinitions=50       #Gets the SCA definitions
    PutSCAdefinitions=51       #Sets the SCA definitions    
    
class Command(SerializableObject):
    """
    Description:
        An instance of this class is used to encapsulate a 
        command that is sent to the Lynx
    """
    def __init__(self, code=InternalCommandCodes.Unknown, input=0):
        """
        Description:
            Initializes this instance with the supplied information
        Arguments:
            code    (in, int) The command code.  See InternalCommandCodes
                    class or CommandCodes class
            input   (in, int) The input to receive the command (0-N)
        Returns:
            none
        """
        SerializableObject.__init__(self, TypeCode.CommandData)
        self.__input = input
        self.__commandCode = code
        self.__args = []
    def getInput(self):
        """
        Description:
            Returns the input number
        Arguments:
            none
        Returns:
            (int) The value
        """
        return self.__input
    def getCommandCode(self):
        """
        Description:
            Returns the command code.  See class InternalCommandCodes or
            CommandCode
        Arguments:
            none
        Returns:
            int    The value
        """
        return self.__commandCode
    def getArguments(self):
        """
        Description:
            Returns a list of arguments
        Arguments:
            none
        Returns:
            any[]    The arguments
        """
        args = []
        for v in self.__args:
            args.append(v)
        return args
    def addArgument(self, val):
        """
        Description:
            Sets argument into the list of
            arguments
        Arguments:
            val (in, SerializableObject)    The argument
        Exception:
            UnsupportedTypeException
        Returns:
            none
        """
        #Verify can serialize type by getting the type code
        tcode = ApplicationSerializer.ApplicationSerializer.getTypeCode(val)
        self.__args.append(val)
    def clearArguments(self):
        """
        Description:
            Clears the argument list
        Arguments:
            none
        Returns:
            none
        """
        self.__args = []
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
        cnt = 8
        for v in self.__args:
            cnt += ApplicationSerializer.ApplicationSerializer.getTypeSize(v)
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
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__commandCode)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(self.__input, objTypeCode=TypeCode.Short)
        stream += ApplicationSerializer.ApplicationSerializer.serialize(len(self.__args), objTypeCode=TypeCode.Short)
        for v in self.__args:
            stream += ApplicationSerializer.ApplicationSerializer.serialize(v, writeMeta=True)
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
        self.__args = []
        [self.__commandCode, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Int) 
        [self.__input, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Short) 
        [numArgs, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Short)
        for i in range(0, numArgs):
            [v,stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream) 
            self.__args.append(v)
        return stream
        