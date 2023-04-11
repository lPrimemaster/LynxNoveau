
class AbortException(Exception): 
    """
    Description:
        Defines an abort error.  This is thrown
        when the a client aborts an operation        
    """
    def __str__(self):
        return "AbortException"
class ChecksumException(Exception): 
    """
    Description:
        Defines a checksum error.  This is thrown
        when the communications layer see's an 
        determines that the checksum in the data
        does not match the computed value
        
    """
    def __str__(self):
        return "ChecksumException"
class DeviceErrorException(Exception): 
    """
    Description:
        Defines a device error.  This is thrown
        when device returns an error back to the
        caller.  The error returned is a Win32
        error or a Lynx specific error code.
        See Programmer's Reference Manual for
        list of Lynx specific error codes   
    """
    def __init__(self, code):
        """
        Description:
            Initializes this instance with the supplied info
        Arguments:
            code (in, int)    The device error code
        Return:
            none
        """
        Exception.__init__(self)
        self.__deviceCode=code
    def getDeviceErrorCode(self):
        """
        Description:
            Returns the device error code
        Arguments:
            none
        Return:
            (int)    The value
        """
        return self.__deviceCode
    def getErrorCode(self):
        """
        Description:
            Returns the device error code
        Arguments:
            none
        Return:
            (int)    The value
        """
        return self.__deviceCode
    def __str__(self):
        from .MessageLoader import MessageLoader
        errMsg = MessageLoader.load(self.__deviceCode)
        if (len(errMsg) < 1):
            return "DeviceErrorException-Error Code: %d"%self.__deviceCode
        else:
            return "DeviceErrorException-Description: %s"%errMsg
class DigitalSignatureException(Exception):
    """
    Description:
        Defines a digital signature error.  This is
        thrown if the digital signature contained in
        the communications message has been tampered with
    """
    def __str__(self):
        return "DigitalSignatureException"
class InvalidResponseException(Exception):
    """
    Description:
        Defines an invalid device response error.  This is
        thrown when the device returns information that was
        not expected.  This can happen in a multithreaded env
        when a consumer is not synchronizing an instance of
        the Device() class when accessed in multiple threads
    """
    def __str__(self):
        return "InvalidResponseException"
class InvalidArgumentException(Exception):
    """
    Description:
        Defines an invalid argument error.  This is
        thrown when you pass invalid data to a
        class method
    """
    def __str__(self):
        return "InvalidArgumentException"
class MessageVersionException(Exception):
    """
    Description:
        Defines a message version error.  This is thrown
        when the messaging protocol used to communicated with
        the Lynx has changed and differs from this programming
        libraries.  Basically, under this condition the programming
        library must be updated to match the device communication
        protocol
    """
    def __str__(self):
        return "MessageVersionException" 
class SerializationException(Exception):
    """
    Description:
        Defines a problem encountered during the serialization/
        deserialization of information.
    """
    def __init__(self, details):
        """
        Description:
            Initializes this instance with the supplied info
        Arguments:
            details (in, string)    The details
        Return:
            none
        """
        self.__details=details
    def getDetails(self):
        """
        Description:
            Initializes this instance with the supplied info
        Arguments:
            details (in, string)    The details
        Return:
            none
        """
        return self.__details
    def __str__(self):
        return "SerializationException-Details: %s" % self.getDetails()
class UnsupportedCompressionException(Exception):
    """
    Description:
        Defines a unsupported spectral compression error.  This occurs
        when the compression algorithm specified in the communications
        message differs than what this library supports.
    """
    def __str__(self):
        return "UnsupportedCompressionException"
class UnsupportedTypeException(Exception):
    """
    Description:
        Defines a unsupported type error.  This occurs
        you attempt to write a Python parameter type that
        is not supported by the Lynx.
    """
    def __str__(self):
        return "UnsupportedTypeException"
    
class ChannelNotClosedException(Exception):
    """
    Description:
        Defines the channel not closed exception.  This occurs
        when you invoke Device.open() multiple times without
        invoking Device.close()
    """
    def __str__(self):
        return "ChannelNotClosedException"
class ChannelNotOpenException(Exception):
    """
    Definition:
        Defines a channel not open exceptio.  This occurs when
        you invoke any Device.xxx() method before establishing
        a communications session with the device via Device.open()
    """
    def __str__(self):
        return "ChannelNotOpenException"