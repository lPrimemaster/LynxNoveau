from socket import *
import select
from .Exceptions import ChannelNotClosedException
import platform

class ChannelBase(object):    
    def getLocalHostIP(self, remote = ("www.python.org", 80)):
        """
        Description:
            This method determines the IP address of the currently active
            network adapter.  This method hides the differences in operating
            system platforms this code executes on.
        Arguments:
            remote (in, tuple-(ip, port)) The remote system to connect to.  Recommend using
                                          the default argument
        Returns:
            string                        The local ip address
        """
        if ("Linux" == platform.system()):
            try:
                s = socket(AF_INET, SOCK_STREAM)
                s.connect( remote )
                ip, localport = s.getsockname()
                s.close()
            except:
                ip = input("Unable to determine local network address.  Please enter it: ")
            return ip            
        else:
            return gethostname()
    """
    Description:
        This is the base class for any socket based data communications
        within this library.  It provides common routines for setting
        up, connecting, and closing a socket
    """
    def setPort(self, val):
        """
        Description:
            This sets the communications port.
        Arguments:
            val (in, int)    The value
        Returns:
            none
        """
        self.__port = val
    def getPort(self):
        """
        Description:
            This gets the communications port.
        Arguments:
            none
        Returns:
            int        The value
        """
        return self.__port
    def __init__(self):
        """
        Description:
            This initializes this instance
        Arguments:
            none
        Returns:
            none
        """
        self.__localAddress = ""
        self.__deviceAddress = ""
        self.__connected=False
        self.channel = None
        self.__port = 16385
        self.__sendTimeOut = 60000
        self.__recvTimeOut = 60000
        self.__sendBufferSize = 32768
        self.__recvBufferSize = 32768
        self.__keepAlive = 1
        self.__noDelay = 1        
    def getLocalAddress(self):
        """
        Description:
            This gets the local IP address
        Arguments:
            none
        Returns:
            string        The value
        """
        return self.__localAddress
    def getDeviceAddress(self):
        """
        Description:
            This gets the local IP address
        Arguments:
            none
        Returns:
            string        The value
        """
        return self.__deviceAddress    
    def open(self, localAddr, devAddr):
        """
        Description:
            This opens a connection to the device
        Arguments:
            localAddr    (in, string) IP address of the local machine
            destAddr     (in, string) IP address of the Lynx
        Exceptions:
            Exception
        Returns:
            none
        """
        if (self.getIsOpen()):
            raise ChannelNotClosedException()
        self.channel = socket()
        if (len(localAddr) == 0):
            #localAddr = self.getLocalHostIP()
            localAddr = ""
            
        self.channel.bind((localAddr, 0)) 
        
        #
        #Try setting up the socket to desired configuration settings
        #However, do not return errors to caller because these errors
        #will not prevent communications from operating.  Each OS 
        #may support different features so an error may occur
        #
        try:
            self.channel.setsockopt(SOL_SOCKET, SO_RCVBUF, self.__recvBufferSize)
        except: pass
        try:
            self.channel.setsockopt(SOL_SOCKET, SO_SNDBUF, self.__sendBufferSize)
        except: pass

        #Handle timeouts based on what is supported
        timeoutErr=False
        try:
            self.channel.setsockopt(SOL_SOCKET, SO_SNDTIMEO, self.__sendTimeOut)
        except: timeoutErr=True
        try:
            self.channel.setsockopt(SOL_SOCKET, SO_RCVTIMEO, self.__recvTimeOut)
        except: timeoutErr=True
        if (timeoutErr):
            try:
                #Choose the max timeout value
                timeOut = self.__sendTimeOut
                if (timeOut < self.__recvTimeOut): timeOut = self.__recvTimeOut
                self.channel.settimeout(timeOut)
            except: pass
            
        try:
            self.channel.setsockopt(IPPROTO_TCP, TCP_NODELAY, self.__noDelay) 
        except: pass        
        try:
            self.channel.setsockopt(SOL_SOCKET, SO_KEEPALIVE, self.__keepAlive) 
        except: pass
        
        #The default is to enable blocking
        self.channel.setblocking(1)
        
        #Try to connect
        self.channel.connect((devAddr, self.__port))
        if (len(localAddr) == 0):
            try:
                localAddr=self.channel.getsockname()[0]
            except: pass
         
        self.__connected=True
        self.__localAddress = localAddr
        self.__deviceAddress = devAddr
    def close(self):
        """
        Description:
            This close a connection to the device
        Arguments:
            none
        Exceptions:
            Exception
        Returns:
            none
        """
        if (self.getIsOpen() is False): 
            return
        try:
            self.channel.shutdown(SHUT_RDWR)
        except:pass
        try:
            self.channel.close()
        except:pass
        self.channel = None
        self.__connected=False
    def getIsOpen(self):
        """
        Description:
            Returns the open state
        Arguments:
            none
        Returns:
            bool    open state
        """
        if (None == self.channel): 
            return False
        else:
            return self.__connected
    def recv(self, nBytes):
        """
        Description:
            Reads N-bytes from the communications channel
        Arguments:
            nBytes (int)    The number of bytes to read
        Returns:
            (char [])       The data
        """
        stream = ""
        nBufBytes=len(stream)
        while(nBufBytes < nBytes):
            stream += self.channel.recv(nBytes-nBufBytes)
            nBufBytes = len(stream)
        return stream
    def send(self, stream):
        """
        Description:
            Writes N-bytes to the communications channel
        Arguments:
            nBytes (int)    The number of bytes to write
        Returns:
            int             The number of bytes sent
        """
        bufSize=len(stream)
        nBufBytes=0
        while(nBufBytes != bufSize):
            nBufBytes+=self.channel.send(stream[nBufBytes:])
        return nBufBytes    
    def getIsReceiving(self):
        """
        Description:
            Returns state indicating whether there is data
            available in the receive buffer
        Arguments:
            none
        Returns:
            bool        The state
        """
        if (self.getIsOpen()): 
            inp,outp,err = select.select([self.channel], [], [])
            if (None == inp):
                return False
            elif(len(inp) > 0):
                return True
            else:
                return False
        return False
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
        if ("sendbuffersize" == name):            
            val = int(val)
            if (None != self.channel):                 
                self.channel.setsockopt(SOL_SOCKET, SO_SNDBUF, val)
                self.__sendBufferSize = val
            else: self.__sendBufferSize = val
                
        elif ("receivebuffersize" == name):            
            val = int(val)
            if (None != self.channel): 
                self.channel.setsockopt(SOL_SOCKET, SO_RCVBUF,  val)            
                self.__recvBufferSize = val
            else: self.__recvBufferSize = val
                
        if ("sendtimeout" == name):
            val = int(val)            
            if (None != self.channel):
                timeOutErr=False
                try:
                    self.channel.setsockopt(SOL_SOCKET, SO_SNDTIMEO, val)
                except: timeOutErr=True
                if (timeOutErr):
                    self.channel.settimeout(val)
                self.__sendTimeOut = val
            else: self.__sendTimeOut = val
            
        elif ("receivetimeout" == name):    
            val = int(val)                     
            if (None != self.channel):
                timeOutErr=False
                try:
                    self.channel.setsockopt(SOL_SOCKET, SO_RCVTIMEO, val)
                except: timeOutErr=True
                if (timeOutErr):
                    self.channel.settimeout(val)
                self.__recvTimeOut = val
            else: self.__recvTimeOut = val
            
        elif ("keepalive" == name):
            val = int(val)                        
            if (None != self.channel): 
                self.channel.setsockopt(SOL_SOCKET, SO_KEEPALIVE, val)            
                self.__keepAlive = val
            else: self.__keepAlive = val
            
        elif ("nodelay" == name):            
            val = int(val)
            if (None != self.channel): 
                self.channel.setsockopt(IPPROTO_TCP, TCP_NODELAY, val) 
                self.__noDelay = val
            else: self.__noDelay = val
            
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
        if ("sendbuffersize" == name):
            return self.__sendBufferSize
        elif ("receivebuffersize" == name):            
            return self.__recvBufferSize
        if ("sendtimeout" == name):
            return self.__sendTimeOut
        elif ("receivetimeout" == name):            
            return self.__recvTimeOut
        elif ("keepalive" == name):            
            return self.__keepAlive
        elif ("nodelay" == name):            
            return self.__noDelay
        
