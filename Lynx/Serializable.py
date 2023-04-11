class Serializable(object):
    """
    Description:
        This is an abstract class used to define a
        common serialization interface
    """
    def serialize(self, stream=''): 
        """
        Description:
            This method serializes the data contained
            in this instance into the stream
        Arguments:
            stream    (in, char[]) The stream to receive the data
        Return:
            char []    The stream containing the data
        """
        pass
    def deserialize(self, stream): 
        """
        Description:
            This method deserializes the data contained
            in the stream and place it into this instance 
        Arguments:
            stream    (in, char[]) The stream that contains the data
        Return:
            char []   The stream minus the data
        """
        pass
    