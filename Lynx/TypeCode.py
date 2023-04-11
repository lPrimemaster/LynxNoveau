
class TypeCode(object): 
        """
        Description:
            This class defines all of the data types supported
            by the Lynx
        """
        Unknown = 0
        Byte=1
        Short=2
        Int=3
        Ushort=4
        Ubyte=5
        Uint=6
        Float=7
        Double=8
        String=9
        Long=10
        Ulong=11
        Bool=12
        Null=13
        DateTime=14
        CustomTypeOffset=20
        PhaData=CustomTypeOffset+1                     #Data for PHA 
        LfcData=CustomTypeOffset+2                     #Data for LFC
        McsData=CustomTypeOffset+3                     #Data for MCS
        TlistData=CustomTypeOffset+4                   #Timestamped List data
        SpectralData=CustomTypeOffset+5                #Simple spectrum (chans/counts)
        CommandData=CustomTypeOffset+6                 #Device Command
        ParameterData=CustomTypeOffset+7               #Parameter information
        ParameterMetaData=CustomTypeOffset+8           #Parameter meta information
        RegionOfInterestData=CustomTypeOffset+9        #Region of interest
        DsoData=CustomTypeOffset+10                    #DSO data
        CounterData=CustomTypeOffset+11                #Counter data
        DlfcData=CustomTypeOffset+12                   #Data for DLFC
        ListData=CustomTypeOffset+13                   #Data for List 
        SCAdefinitionData=CustomTypeOffset+14          #SCA definition data
        SCAbufferData=CustomTypeOffset+15              #SCA buffer data 
