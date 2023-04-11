from .ChannelBase import *
from .Exceptions import ChannelNotOpenException, InvalidResponseException, DeviceErrorException, InvalidArgumentException, AbortException
from .Command import Command, InternalCommandCodes
from .MessageFactory import MessageFactory
from .ApplicationSerializer import ApplicationSerializer
from .TypeCode import TypeCode
from .SpectralData import SpectralData
from .CounterData import CounterData
from .RegionOfInterest import RegionOfInterest
from .ParameterAttributes import ParameterAttributes
from .ListData import ListDataBase
from .Parameter import Parameter
from .PhaData import PhaData
from .Spectrum import Spectrum
from .StreamChannel import StreamChannel
from .SCAbuffer import SCAbuffer
from .SCAdefinitions import SCAdefinitions

class ConfigurationChannel(ChannelBase):
    """
    Description:
        An instance of this class is used communicate with a Lynx.
    """
    def __init__(self):
        """
        Description:
            Initializes this instance.
        Arguments:
            None
        Returns:
            None
        """
        ChannelBase.__init__(self)     
        self.__streamChannel = StreamChannel()
    
    def open(self, localAddr, devAddr):
        """
        Description:
            Establishes a connection between this client
            and the device
        Arguments:
            localAddr (in, string)    The IP address of the client
            devAddr (in. string)      The IP address of the device
        Returns:
            None        
        """
        ChannelBase.open(self, localAddr, devAddr)
        self.__streamChannel.open(localAddr, devAddr)        
    
    def close(self):
        """
        Description:
            Terminates a connection between this client
            and the device
        Arguments:
            localAddr (in, string)    The IP address of the client
            devAddr (in. string)      The IP address of the device
        Returns:
            None        
        """
        ChannelBase.close(self)
        self.__streamChannel.close()            
    def __controlWithResponse(self, cmd):
        """
        Description:
            This method will execute a command.  It will examine
            the response from the device to the command to determine
            any errors.  The assumption is that there is response
            data.  This response data is returned via the return
            value
        Arguments:
            cmd (in, Command)    The command to execute
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            any                Data from the device
        """
        if (self.getIsOpen() is False):
            raise ChannelNotOpenException()
        stream = MessageFactory.serializeToMessage(cmd)
        self.send(stream)
        stream=self.recv(4)
        [msgSize, dum] = ApplicationSerializer.deserialize(stream, TypeCode.Int)
        stream+=self.recv(msgSize-len(stream))
        [msg, stream] = MessageFactory.deserializeFromMessage(stream)
        if (isinstance(msg, Command) is False):
            raise InvalidResponseException()
        if (InternalCommandCodes.Response != msg.getCommandCode()):
            raise InvalidResponseException()
        
        resp = msg.getArguments()
        if ((len(resp) > 0) and (isinstance(resp[0], int) or isinstance(resp[0], int))):
            raise DeviceErrorException(resp[0])
        return msg.getArguments()
    def __controlWithoutResponse(self, cmd):
        """
        Description:
            This method will execute a command.  It will examine
            the response from the device to the command to determine
            any errors.  The assumption is that there is not response
            data.  If there is then a exception is raised
        Arguments:
            cmd (in, Command)    The command to execute
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        resp = self.__controlWithResponse(cmd)
        if (None == resp):
            return
        elif(0 == len(resp)):
            return
        raise InvalidResponseException()
    def getSpectrum(self, input, group=1):
        """
        Description:
            This method will get the spectrum
            from an input and memory group
        Arguments:
            input (in, int)    The input
            group (in, int)    The memory group
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            Spectrum
        """
        cmd = Command(InternalCommandCodes.GetSpectrum, input)
        cmd.addArgument(group)
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp[0], Spectrum) is False):
            raise InvalidResponseException()
        return resp[0]
    def setSpectrum(self, data, input, group=1):
        """
        Description:
            This method will set the spectrum
            into an input and memory group
        Arguments:
            data (in, Spectrum) The spectrum
            input (in, int)    The input
            group (in, int)    The memory group
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.PutSpectrum, input)
        cmd.addArgument(group)
        if (isinstance(data, Spectrum) is False):
            raise InvalidArgumentException()
        cmd.addArgument(data)
        self.__controlWithoutResponse(cmd)
    def getMSSData(self, input=1):
        """
        Description:
            This method will get MSS data from an
            input
        Arguments:
            input (in, int)    The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            PhaData[]
        """        
        if (self.__streamChannel.getActive()):            
            try:
                msg = self.__streamChannel.receiveCommand()
            except AbortException:
                return None            
            if (InternalCommandCodes.Response != msg.getCommandCode()):
                raise InvalidResponseException()            
            resp = msg.getArguments()
        else:
            cmd = Command(InternalCommandCodes.GetMSSData, input)
            resp=self.__controlWithResponse(cmd)
            
        for data in resp:            
            if (isinstance(data, PhaData) is False):
                raise InvalidResponseException()
        return resp
    def getSpectralData(self, input, group=1):
        """
        Description:
            This method will get spectral data which
            includes: elapsed realtime, elapsed livetime, starttime,
            counts, elapsed computational value, dwell, and
            elapsed sweeps.
        Arguments:
            input (in, int)    The input
            group (in, int)    The group
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            SpectralData
        """
        cmd = Command(InternalCommandCodes.GetSpectralData, input)
        cmd.addArgument(group)
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp[0], SpectralData) is False):
            raise InvalidResponseException()
        return resp[0]
    def getCounterData(self, input=1):
        """
        Description:
            This method will get auxillary counter data which includes:
            sample time, elapsed, corrected counts, and uncorrected counts
        Arguments:
            input (in, int)    The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            CounterData
        """
        cmd = Command(InternalCommandCodes.GetCounterData, input)
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp[0], CounterData) is False):
            raise InvalidResponseException()
        return resp[0]
    def getListData(self, input=1):
        """
        Description:
            This method will get list data
        Arguments:
            input (in, int)    The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            ListDataBase
        """
        if (self.__streamChannel.getActive()):            
            try:
                msg = self.__streamChannel.receiveCommand()
            except AbortException:
                return None
            resp = msg.getArguments()
            if ((len(resp) > 0) and (isinstance(resp[0], int))):
                raise DeviceErrorException(resp[0])
            resp = msg.getArguments()
            if (isinstance(resp[0], ListDataBase) is False):
                raise InvalidResponseException()
            return resp[0]
        else:
            cmd = Command(InternalCommandCodes.GetListData, input)
            resp=self.__controlWithResponse(cmd)
            if (isinstance(resp[0], ListDataBase) is False):
                raise InvalidResponseException()
            return resp[0]
    def control(self, code, input):
        """
        Description:
            This method will execute a command on a specific input
        Arguments:
            code (in, int)     The command code. See CommandCodes class
            input (in, int)    The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(code, input)
        self.__controlWithoutResponse(cmd)
    def lock(self, usr, pwd, input):
        """
        Description:
            This method will lock an input for exclusive access
        Arguments:
            usr (in, string)    The user name
            pwd (in, string)    The password
            input (in, int)     The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.Lock, input)
        cmd.addArgument(usr)
        cmd.addArgument(pwd)
        cmd.addArgument(self.getLocalAddress())
        self.__controlWithoutResponse(cmd)
    def unlock(self, usr, pwd, input):
        """
        Description:
            This method will unlock an input
        Arguments:
            usr (in, string)    The user name
            pwd (in, string)    The password
            input (in, int)     The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.Unlock, input)
        cmd.addArgument(usr)
        cmd.addArgument(pwd)
        locAddr=self._ChannelBase__localAddress
        cmd.addArgument(locAddr)
        self.__controlWithoutResponse(cmd)
    def addUser(self, usr, pwd, desc, attr):
        """
        Description:
            This method will add a user account
        Arguments:
            usr (in, string)    The user name
            pwd (in, string)    The password
            desc (in, string)   The descriptio
            attr (in, int)      Attributes (future)
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.AddUser, 0)
        cmd.addArgument(usr)
        cmd.addArgument(pwd)
        cmd.addArgument(desc)
        cmd.addArgument(attr)
        self.__controlWithoutResponse(cmd)
    def updateUser(self, usr, pwd, desc, attr):
        """
        Description:
            This method will update a user account
        Arguments:
            usr (in, string)    The user name
            pwd (in, string)    The password
            desc (in, string)   The descriptio
            attr (in, int)      Attributes (future)
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.UpdateUser, 0)
        cmd.addArgument(usr)
        cmd.addArgument(pwd)
        cmd.addArgument(desc)
        cmd.addArgument(attr)
        self.__controlWithoutResponse(cmd)
    def deleteUser(self, usr):
        """
        Description:
            This method will delete a user account
        Arguments:
            usr (in, string)    The user name
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.DeleteUser, 0)
        cmd.addArgument(usr)
        self.__controlWithoutResponse(cmd)
    def validateUser(self, usr, pwd):
        """
        Description:
            This method will validate a user account
        Arguments:
            usr (in, string)    The user name
            pwd (in, string)    The password            
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.ValidateUser, 0)
        cmd.addArgument(usr)
        cmd.addArgument(pwd)   
        try:     
            self.__controlWithoutResponse(cmd)
        except DeviceErrorException as info:
            DSA3K_USERNOTEXIST=0xEFA1A108
            if (DSA3K_USERNOTEXIST != info.getDeviceErrorCode()): raise e        
            else: return False
                
        return True
    def enumerateUsers(self):
        """
        Description:
            This method will enumerate all user accounts
        Arguments:
            none
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            string[]    
        """
        cmd = Command(InternalCommandCodes.EnumerateUsers, 0)
        resp=self.__controlWithResponse(cmd)
        return resp
    def save(self, input, group):
        """
        Description:
            This method will sava an inputs measurement
            data to file on the device
        Arguments:
            input (in, int)     The input
            group (in, int)    The memory group
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            string    The file name
        """
        cmd = Command(InternalCommandCodes.Save, input)
        cmd.addArgument(group)
        resp = self.__controlWithResponse(cmd)
        if (isinstance(resp[0], str) is False):
            raise InvalidResponseException()
        return resp[0]
    def getRegionsOfInterest(self, input):
        """
        Description:
            This method will get the display regions of interest
        Arguments:
            input (in, int)   The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            RegionOfInterest[]
        """
        cmd = Command(InternalCommandCodes.GetRegionsOfInterest, input)        
        resp=self.__controlWithResponse(cmd)
        for rgn in resp:
            if (isinstance(rgn, RegionOfInterest) is False):
                raise InvalidResponseException()
        return resp
    def setRegionsOfInterest(self, rgns, input):
        """
        Description:
            This method will set the display regions of interest
        Arguments:
            input (in, int)                 The input
            rgns (in, RegionOfInterest[])   The regions
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.PutRegionsOfInterest, input)
        for rgn in rgns:
            if (isinstance(rgn, RegionOfInterest) is False):
                raise InvalidArgumentException()
            cmd.addArgument(rgn)        
        self.__controlWithoutResponse(cmd)
    def getParameterAttributes(self, code, input):
        """
        Description:
            This method will get metadata about a parameter.
            Metadata consists of: name, code, description,
            min val, max val, step size, etc...
        Arguments:
            code (in, int)    The parameter code.  See ParameterCodes class
            input (in, int)   The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            ParameterAttributes
        """
        cmd = Command(InternalCommandCodes.GetParameter, input)
        cmd.addArgument(code)
        cmd.addArgument(0)
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp[0], ParameterAttributes) is False):
            raise InvalidResponseException()
        return resp[0]
    def getParameter(self, code, input):
        """
        Description:
            This method will get a parameter from the device
        Arguments:
            code (in, int)    The parameter code.  See ParameterCodes class
            input (in, int)   The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            any
        """
        cmd = Command(InternalCommandCodes.GetParameter, input)
        cmd.addArgument(code)
        return self.__controlWithResponse(cmd)[0].getValue()
    def getParameterList(self, code, input):
        """
        Description:
            This method will get a list of parameters from the device
        Arguments:
            code (in, int[])  Array of parameter codes.  See ParameterCodes class
            input (in, int)   The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException 
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            any[]
        """
        cmd = Command(InternalCommandCodes.GetParameterList, input)
        for c in code:
            cmd.addArgument(c)
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp, list) is False):
            raise InvalidResponseException()
        ret = []
        for p in resp:
            ret.append(p.getValue())
        return ret
    def setParameter(self, code, val, input):
        """
        Description:
            This method will get a parameter from the device
        Arguments:
            code (in, int)    The parameter code.  See ParameterCodes class
            val (in, any)     The value
            input (in, int)   The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.PutParameter, input)
        cmd.addArgument(Parameter(code, val))
        self.__controlWithoutResponse(cmd)
    def setParameterList(self, param, input):
        """
        Description:
            This method will get a list of parameters from the device
        Arguments:
            param (in, Parameter[])  Array of parameters.
            input (in, int)   The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
            InvalidArgumentException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.PutParameterList, input)
        for p in param:
            if (isinstance(p, Parameter) is False):
                raise InvalidArgumentException()
            cmd.addArgument(p)
        self.__controlWithoutResponse(cmd)
    def getSCAdefinitions(self, input=1):
        """
        Description:
            This method will get the SCA definition
        Arguments:
            input (in, int)    The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            SCAdefinitions
        """
        cmd = Command(InternalCommandCodes.GetSCAdefinitions, input)        
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp[0], SCAdefinitions) is False):
            raise InvalidResponseException()
        return resp[0]
    def setSCAdefinitions(self, defs, input=1):
        """
        Description:
            This method will get the SCA definition
        Arguments:
            defs (in,  SCAdefinitions) The definitions
            input (in, int)            The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            none
        """
        cmd = Command(InternalCommandCodes.PutSCAdefinitions, input)
        cmd.addArgument(defs)
        self.__controlWithoutResponse(cmd)        
    def getSCAbufferData(self, input=1):
        """
        Description:
            This method will get the SCA acquisition buffer
        Arguments:
            input (in, int)    The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            SCAdefinitions
        """
        cmd = Command(InternalCommandCodes.GetSCAbuffer, input)    
        resp=self.__controlWithResponse(cmd)
        if (isinstance(resp[0], SCAbuffer) is False):
            raise InvalidResponseException()
        return resp[0]
    def setProperty(self, name, val):
        """
        Description:
            This method will set the value of
            a named property
        Arguments:
            name (in, string)    The name of the property
            val (in, any)        The value for the property
        Returns:
            none
        """        
        name = name.lower()
        if ("port" == name):
            self.setPort(val)
        else:
            ChannelBase.setProperty(self, name, val)       
            self.__streamChannel.setProperty(name, val)
            
    def getProperty(self, name):
        """
        Description:
            This method will get the value of
            a named property
        Arguments:
            name (in, string)    The name of the property            
        Returns:
            any                  The value
        """
        name = name.lower()  
        if ("port" == name):
            return self.getPort()      
        else:
            val = ChannelBase.getProperty(self, name)    
            if (None == val): return self.__streamChannel.getProperty(name)
            else: return val