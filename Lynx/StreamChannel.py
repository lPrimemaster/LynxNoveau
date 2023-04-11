from .MessageFactory import MessageFactory
from .ApplicationSerializer import ApplicationSerializer
from .TypeCode import TypeCode
from .Exceptions import AbortException, InvalidResponseException
from .ChannelBase import *
from .Command import Command, InternalCommandCodes
import errno

class StreamChannel(ChannelBase):
    """
    Description:
        An instance of this class is used for streaming 
        measurement data from the Lynx to the client application.
        The history of the Lynx communications is as follows:
            1. Release 1.0 of the Lynx requires the client side to
               send a command to the Lynx requesting measurement data.
               The Lynx responds with the requested data.  
            2. Release 1.1 which contains streaming does not require
               the client side to send a command to the Lynx requesting
               measurement data.  The Lynx always sends measurement data 
               as soon as it is received from the hardware.  This improves
               performance.
        An instance of this class is used to receive data that is sent by
        the Lynx.
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
        self.setPort(16386)
        self.__enable = False        
        self.__abort = False
    def open(self, localAddr, devAddr):
        """
        Description:
            This opens a connection to the device.  This overrides the
            base class implementation in order to setup the socket for
            streaming
        Arguments:
            localAddr    (in, string) IP address of the local machine
            destAddr     (in, string) IP address of the Lynx
        Exceptions:
            Exception
        Returns:
            none
        """
        if (False == self.__enable): return
        
        ChannelBase.open(self, localAddr, devAddr)
        
        #We are not performing blocking operations with this
        #channel so disable it
        self.channel.setblocking(0)            
    def getEnable(self): 
        """
        Description:
            Gets the enable state
        Arguments:
            None
        Returns:
            boolean
        """
        return self.__enable
    def setEnable(self, v): 
        """
        Description:
            Sets the enable state
        Arguments:
            v (in, bool) The value
        Returns:
            none
        """
        self.__enable=v    
    def getActive(self):
        """
        Description:
            Returns the active state.  Active state means that streaming 
            is enabled and the streaming channel is open.
        Arguments:
            v (in, bool) The value
        Returns:
            none
        """
        if (self.__enable and self.getIsOpen()): 
            return True
        else: 
            return False        
    def receiveCommand(self):
        """
        Description:
            This method will get a command sent by the lynx
            over the stream channel.  It will block until a
            command is received
        Arguments:
            none
        Exceptions:
            AbortException    Command was aborted by client
        Returns:
            Command    A command from the Lynx
        """
        try:
            stream=self.recv(4)
            [msgSize, dum] = ApplicationSerializer.deserialize(stream, TypeCode.Int)
            stream+=self.recv(msgSize-len(stream))
            [msg, stream] = MessageFactory.deserializeFromMessage(stream)                        
        except AbortException:
            self.close()
            self.open(self.getLocalAddress(), self.getDeviceAddress())
            raise AbortException()

        #Verify we received the correct type
        if (isinstance(msg, Command) is False):
            raise InvalidResponseException()
        
        #Verify it is the correct type of command
        if (InternalCommandCodes.Response != msg.getCommandCode()):
                raise InvalidResponseException()
        return msg
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
        if (("enable" == name) or ("enablestreaming" == name) or ("usestream" == name)):
            self.__enable = val
        elif ("streamingport" == name):
            self.setPort(val)
        elif (("abort" == name) or ("aborted" == name) or ("abortstreaming" == name)):
            self.__abort = val
        else:
            ChannelBase.setProperty(self, name, val)
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
        if (("enable" == name) or ("enablestreaming" == name) or ("usestream" == name)):
            return self.__enable
        elif ("streamingport" == name):
            return self.getPort()
        elif (("abort" == name) or ("aborted" == name) or ("abortstreaming" == name)):
            return self.__abort
        elif (("streamingdataavailable" == name) or ("dataavailable" == name)):
            if (self.__enable): return self.getIsReceiving()
            else: return False
        else:
            return ChannelBase.getProperty(self, name)
    def recv(self, nBytes):
        """
        Description:
            Reads N-bytes from the communications channel.  This method
            will block until N-bytes are received.  This method
            overrides the base class implementation in order to support
            aborting the process of receiving data.
        Arguments:
            nBytes (int)    The number of bytes to read
        Exceptions:
            AbortException  Raised when user sets the abort state
        Returns:
            (char [])       The data        
        """
        stream = ""
        nBufBytes=len(stream)
        while(nBufBytes < nBytes):
            try:
                if (self.__abort): 
                    raise AbortException()
                stream += self.channel.recv(nBytes-nBufBytes)            
            except error as msg:
                if (errno.EWOULDBLOCK == error):
                    continue
                
            nBufBytes = len(stream)
        return stream
    def send(self, stream):
        """
        Description:
            Writes N-bytes to the communications channel. This method
            will block until N-bytes are sent.  This method
            overrides the base class implementation in order to support
            aborting the process of sending data.
        Arguments:
            nBytes (int)    The number of bytes to write
        Exceptions:
            AbortException  Raised when user sets the abort state
        Returns:
            int             The number of bytes sent
        """
        bufSize=len(stream)
        nBufBytes=0        
        while(nBufBytes != bufSize):
            try:
                if (self.__abort): raise AbortException()
                nBufBytes+=self.channel.send(stream[nBufBytes:])
            except error as msg:
                if (errno.EWOULDBLOCK == error):
                    continue
            
        return nBufBytes