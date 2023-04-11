from .ConfigurationChannel import ConfigurationChannel
from .ParameterTypes import DataTypes
from .IDevice import IDevice
import _thread

class Device(IDevice):
    """
    Description:
        An instance of this class is used communicate with a Lynx.
    """
    def __init__(self):
        """
        Description:
            This method will initialize this instance
        Arguments:
            none
        Returns:
            none
        """ 
        self.__configChannel = ConfigurationChannel()
        self.__lock = _thread.allocate_lock()
    def getPort(self):
        """
        Description:
            This method will return the socket port
        Arguments:
            none
        Returns:
            int    The value
        """
        try:
            self.__lock.acquire()
            return self.__configChannel.getPort()
        finally:
            self.__lock.release()            
    def setPort(self, val):
        """
        Description:
            This method will set the socket port
        Arguments:
            val (in, int)    The value
        Returns:
            none
        """
        try:
            self.__lock.acquire()
            self.__configChannel.setPort(val)
        finally:
            self.__lock.release()     
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getSpectrum(input, group)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            self.__configChannel.setSpectrum(data, input, group)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getMSSData(input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getSpectralData(input, group)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getCounterData(input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getListData(input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            self.__configChannel.control(code, input) 
        finally:
            self.__lock.release()   
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
        try:
            self.__lock.acquire()
            self.__configChannel.lock(usr, pwd, input)
        finally:
            self.__lock.release()   
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
        try:
            self.__lock.acquire()
            self.__configChannel.unlock(usr, pwd, input)
        finally:
            self.__lock.release() 
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
        try:
            self.__lock.acquire()
            self.__configChannel.addUser(usr, pwd, desc, attr)
        finally:
            self.__lock.release() 
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
        try:
            self.__lock.acquire()
            self.__configChannel.updateUser(usr, pwd, desc, attr)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            self.__configChannel.deleteUser(usr)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.enumerateUsers()
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.validateUser(usr, pwd)
        finally:
            self.__lock.release()
    def save(self, input, group):
        """
        Description:
            This method will sava an inputs measurement
            data to file on the device
        Arguments:
            input (in, int)     The input
            group (in, int)     The memory group 
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
        try:
            self.__lock.acquire()
            return self.__configChannel.save(input, group)
        finally:
            self.__lock.release()
    def open(self, localAddr, devAddr):
        """
        Description:
            This method will establish a connection between
            the local system and the Lynx
        Arguments:
            localAddr (in, string)    The local IP address
            devAddr (in, string)      The device IP address
        Exceptions:
            Exception
        Returns:
            none
        """
        try:
            self.__lock.acquire()
            self.__configChannel.open(localAddr, devAddr)
        finally:
            self.__lock.release()
    def close(self):
        """
        Description:
            This method will end communications with the Lynx
        Arguments:
            none
        Returns:
            none
        """
        try:
            self.__lock.acquire()
            self.__configChannel.close()
        finally:
            self.__lock.release()
    def getRegionsOfInterest(self, input):
        """
        Description:
            This method will get all display regions of interest
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getRegionsOfInterest(input)
        finally:
            self.__lock.release()
    def setRegionsOfInterest(self, rgns, input):
        """
        Description:
            This method will set all display regions of interest
        Arguments:        
            input (in, int)                   The input
            rgns  (in, RegionOfInterest[])    The regions
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
        try:
            self.__lock.acquire()
            self.__configChannel.setRegionsOfInterest(rgns, input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getParameterAttributes(code, input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getParameter(code, input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getParameterList(code, input)
        finally:
            self.__lock.release()
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
        try:
            self.__lock.acquire()
            self.__configChannel.setParameter(code, val, input)
        finally:
            self.__lock.release()
    def setParameterList(self, params, input):
        """
        Description:
            This method will get a list of parameters from the device
        Arguments:
            params(in, Parameter[])  Array of parameters.
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
        try:
            self.__lock.acquire()
            self.__configChannel.setParameterList(params, input)
        finally:
            self.__lock.release()
    def getIsOpen(self):
        """
        Description:
            This method will return the open state
        Arguments:
            none
        Returns:
            bool
        """
        try:
            self.__lock.acquire()
            return self.__configChannel.getIsOpen()
        finally:
            self.__lock.release() 
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getSCAdefinitions(input)
        finally:
            self.__lock.release() 
    def setSCAdefinitions(self, defs, input):
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
        try:
            self.__lock.acquire()
            self.__configChannel.setSCAdefinitions(defs, input)
        finally:
            self.__lock.release()      
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
        try:
            self.__lock.acquire()
            return self.__configChannel.getSCAbufferData(input)
        finally:
            self.__lock.release()    
    def getData(self, dataType, input=1):
        """
        Description:
            This method will get data from the device.  The type of data is
            defined by the dataType argument
        Arguments:
            dataType (in, int)     The data to get (see DataTypes class)
            input (in, int)        The input
        Exceptions:
            ChecksumException
            DigitalSignatureException
            InvalidResponseException
            MessageVersionException
            SerializationException
            UnsupportedCompressionException
            UnsupportedTypeException
        Returns:
            object
        """
        try:
            self.__lock.acquire()
            if (DataTypes.counterData == dataType):
                return self.getCounterData(input)
            elif (DataTypes.listData == dataType):
                return self.getListData(input)
            elif (DataTypes.scaBufferData == dataType):
                return self.getSCAbufferData(input)
            elif (DataTypes.mssData == dataType):
                return self.getMSSData(input)
            return None
        finally:
            self.__lock.release()
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
        #The locking has been removed intentionally
        #sync locks are handled lower
        self.__configChannel.setProperty(name, val)
        
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
        #The locking has been removed intentionally
        #sync locks are handled lower            
        return self.__configChannel.getProperty(name)