from .Device import Device

class DeviceFactory(object):
    """
    Description:
        This is a class factory for creating the interface
        used to communicate with the device
    """
    
    class DeviceInterface(object):
        """
        Description:
            This class defines all of the possible interface
            types that can be created
        """
        IDevice = 0
           
    def _createInstance(cls, interfaceType):
        """
        Description:
            This method will return the socket port
        Arguments:
            none
        Returns:
            interfaceType (int)    The type of interface to create
        """
        if (DeviceFactory.DeviceInterface.IDevice == interfaceType):
            return Device()
        else:
            return None
        
    createInstance = classmethod(_createInstance)