from .Serializable import Serializable

class SerializableObject(Serializable):
    def getDataSize(self): 
        """
        Description:
            This method returns the number of bytes used to
            serialize the data contained in this instance
        Arguments:
            none
        Return:
            int    Number of bytes
        """
        pass    
    def serializeData(self, stream=''): 
        """
        Description:
            This method serializes the data contained
            in this instance into the stream
        Arguments:
            stream    (in, char[]) The stream to receive the data
        Return:
            char []   The stream containing the data
        """
        pass
    def deserializeData(self, stream): 
        """
        Description:
            This method deserializes the data contained
            in the stream and places it into this instance
        Arguments:
            stream    (in, char[]) The stream to receive the data
        Return:
            char []   The stream minus the data
        """
        pass
    def getType(self):
        """
        Description:
            This method returns the type code for this
            instance
        Arguments:
            none
        Return:
            int        The type code.  See TypeCode class
        """
        return self.__type
    """
    This is an abstract class used to define a
    common serialization interface
    """
    def __init__(self, type):
        self.__type=type
    def serialize(self, stream=''):
        """
        Description:
            This method serializes the data contained
            in this instance into the stream
        Arguments:
            stream    (in, char[]) The stream to receive the data
        Return:
            char []   The stream containing the data
        """
        return self.serializeData(stream)
    def deserialize(self, stream):
        """
        Description:
            This method deserializes the data contained
            in the stream and places it into this instance
        Arguments:
            stream    (in, char[]) The stream to receive the data
        Return:
            char []   The stream minus the data
        """
        return self.deserializeData(stream)
    def getSize(self): 
        """
        Description:
            This method returns the number of bytes used to
            serialize the data contained in this instance
        Arguments:
            none
        Return:
            int    Number of bytes
        """
        return self.getDataSize()    
        
         
