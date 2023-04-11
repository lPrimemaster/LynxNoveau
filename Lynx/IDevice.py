class IDevice(object):
    """
    Description:
        This is the interface necessary for communicating with the
        Lynx.
    """
    def getPort(self): None                
    def setPort(self, val): None        
    def getSpectrum(self, input, group=1): None        
    def setSpectrum(self, data, input, group=1): None        
    def getMSSData(self, input=1): None        
    def getSpectralData(self, input, group=1): None        
    def getCounterData(self, input=1): None        
    def getListData(self, input=1): None        
    def control(self, code, input): None        
    def lock(self, usr, pwd, input): None        
    def unlock(self, usr, pwd, input): None        
    def addUser(self, usr, pwd, desc, attr): None    
    def updateUser(self, usr, pwd, desc, attr): None        
    def deleteUser(self, usr): None        
    def enumerateUsers(self): None        
    def validateUser(self, usr, pwd): None        
    def save(self, input, group): None        
    def open(self, localAddr, devAddr): None        
    def close(self): None        
    def getRegionsOfInterest(self, input): None        
    def setRegionsOfInterest(self, rgns, input): None        
    def getParameterAttributes(self, code, input): None        
    def getParameter(self, code, input): None        
    def getParameterList(self, code, input): None        
    def setParameter(self, code, val, input): None       
    def setParameterList(self, params, input): None
    def getIsOpen(self): None        
    def getSCAdefinitions(self, input=1): None        
    def setSCAdefinitions(self, defs, input): None            
    def getSCAbufferData(self, input=1): None            
    def setProperty(self, name, val): None        
    def getProperty(self, name): None
    def getData(self, dataType, input=1): None
    