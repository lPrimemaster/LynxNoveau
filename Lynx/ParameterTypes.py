class WebSecurityPrivileges(object):
    """
    Description:
        Contains definitions for security privs for
        the web application.  Setting or unsetting these
        bits will show/hide features in the web application.
        These bits should be used when invoking addUser or updateUser
        methods.    
    """
    calibrationSetup = 2              #Allow access to setup calibrations     
    networkSetup = 4                  #Allow access to setup network
    hardwareAdjust = 8                #Allow access to hardware adjust
    hvpsLimitSetup = 16               #Allow access to setup HVPS limit
    systemSetup = 32                  #Allow access to setup system
    securitySetup = 64                #Allow access to setup security
    firmwareUpdate = 128              #Allow access to update firmware
    auditSetup = 256                  #Allow access to setup audit logs
    presetSetup = 512                 #Allow access to setup acquisition
    inputDefinition = 1024            #Allow access to define inputs
    digitalOscilloscope = 2048        #Allow access to DSO
    backupAndRestore = 4096           #Allow access to backup and restore
    takeOver = 8192                   #Allow a user to take over an input
    diagnostics = 16384               #Allow access to diagnostics
        
class GPIOcontrolCodes(object):
    """
    Description:
        Contains definitions for the values that may be specified
        for the GPIOx_Control parameters where x has a value of 1,2,3 or 4
    """    
    input = 0        
    outputLow = 1    
    outputHigh = 2   


class DataTypes(object):
    """
    Description:
        Contains all of the data types that may be retrieved using
        the getData method
    """    
    counterData = 1        #Counter data
    listData = 2           #List data
    scaBufferData = 3      #SCA counter data
    mssData = 4            #MSS data
    
class StorageMediaStates(object):
    """
    Description:
        Contains all of the storage media states.  Media state is
        accessible via the System_StorageMediaState parameter
    """   
    storageMediaIdle = 0                   #Media idle
    storageMediaBusy = 1                   #Media busy transfering files
    storageMediaCompactFlashPresent = 2    #Compact Flash detected
    storageMediaUsbFlashPresent = 4        #USB Flash detected    
    storageMediaNandFlashPresent=8         #NAND flash present
        
class StorageOptions(object):
    """
    Description:
        Contains all of the options for saving information onto persistent media        
        Simply bitwise OR these values with the value returned from the 
        parameter System_StorageOptions to enable features
    """
    storageDisabled=0                            #Stores nothing
    storageAutoStoreToRemovableMedia=2       #Stores input data to removable media automatically
    storageManualStoreRemovableToMedia=4     #Stores input data to removable media during manual save command
    storageSaveCAM=8                         #Stores input to CAM file
    storageSaveN42=16                        #Stores input to N42 file
    storageSaveAuditLog=32                   #Stores the audit log
    storageDeleteAfterTransfer=64	         #Deletes files after they have been transfered to removable media

class StatusBits(object):
    """
    Description:
        Contains all of the device status bits.  Simply bitwise OR these
        values with the value returned from the parameter Input_Status
        to determine the current state of an input
    """
    Idle=0                #Input is idle
    Busy=1                #Input is busy acquiring
    Fault=2               #Input has a fault
    Rebooting=4           #Device is rebooting
    UpdatingImage=8       #Device is updating firmware
    GroupComplete=16      #MSS acquisition group is complete
    Waiting=32            #Waiting for external start or sample changer ready
    Diagnosing=64         #Running diag tests
    APZinprog=128         #Running automatic pole zero on this input
    HVramping=256         #HVPS is ramping for this input
    Group1Active=512      #Acq started on group 1 of this input
    Disconnected=1024     #Lost connection
    PresetReached=2048|4096|16384   #Preset limit was reached
    PresetTimeReached=2048          #Preset time reached
    PresetCompReached=4096          #Computational Preset reached
    ExternalTriggerEvent=8192       #External trigger event
    PresetSweepsReached=16384       #Preset sweeps reached
    ExternalStop=32768		    #The acquisition has been stopped because external stop (BNC)
    OverflowStop=65536		    #The acquisition has been stopped because channel data overflow
    ManualStop=131072		    #The acquisition has been stopped because was commanded to
    AcqNotStarted=262144	    #Acquire not started because previous preset was reached
    
class DeviceStatus(StatusBits): pass

class ListAcquisitionOptions(object): 
    """
    Description:
        Encapsulates all of the bitmask definitions for list mode
        acquisition options.  Simply bitwise and these masks with 
        the value obtained from Input_ListAcqOptions to determine 
        the exact fault condition of the device
    """
    TimeBase100ns=1                #Timebase is 100ns.  If option is disabled the timebase is 1000ns
    LatchOnFastDiscPedge=2         #Events are latched on fast discriminator positive edge.  If disabled events are latched on peak detect positive edge
    UseExternalSyncClockSrc=4      #Enabled indicates use externally generated clock source on external sync input. Disabled indicates sync clock source is internal 1uSec clock
    
class FaultBits(object):
    """
    Description:
        Encapsulates all of the bitmask definitions for device faults
        Simply bitwise and these masks with the value obtained from
        Input_Faults to determine the exact fault condition of the 
        device
    """
    ResourceFault=1          #Error allocating resources
    LvpsFault=2              #LVPS error
    HvpsCommFault=4          #HVPS comm. error
    ParamInitFault=8         #Parameter init error
    Pos5VFault=16            #+5V fault
    Neg5VFault=32            #-5V fault
    Pos24VFault=64           #+24V fault
    Neg24VFault=128          #-24V fault
    Pos12VFault=512          #+12V fault
    Neg12VFault=1024         #-12V fault
    RTCBatFault=2048         #RTC battery range fault                    
    RTCInitFault=4096        #RTC init error                    
    LEDFault=8192            #Problem detected with LEDs
    McaMemFault=16384        #MCA memory fault
    StabORangeFault=32768    #Stabilizer overrange fault
    StabURangeFault=65536    #Stabilizer underrange fault
    StabFineGainChgFault=131072    #Stabilizer fine gain changed fault
    StabRatioFault=262144          #Stabilizer ratio error
    HVinhibitFault=524288           #HV inhibit 
    NANDFault=1048576               #Unable to access NAND drive
    NORFault=2097152                #Unable to access NOR drive    
    RAMLowFault=4194304             #Low program memory
    StoreLowFault=8388608           #Low persistent memory
    BadFileSysFault=16777216        #Persistent store is bad
    GenericFault=33554432           #A generic fault see audit log for further details
    ExtSyncTimeO=67108864           #Indicates that an external sync pulse was expected within the current sync timeout period but none was received
    
class StabilizerStatusBits(object):
    """
    Description:
        Encapsulates all of the stabilizer states.  Each state
        is a bitmask that can be bitwise AND'd with the value
        returned from Input_StabilizerGainStatus
    """
    Off=0              #Stabilizer is off
    On=1               #Stabilizer is on
    Hold=2             #Stabilizer is holding
    FineGainChg=128    #The fine gain was changed invalidating centroid
    UnderRange=512     #Underrange error
    OverRange=256      #Overrange error    
    RatioError=1024    #Ratio error
  
class AutoPoleZeroStatusBits(object):
    """
    Description:
        Encapsulates all of the automatic pole zero states.  Each state
        is a bitmask that can be bitwise AND'd with the value
        returned from Input_PoleZeroError
    """
    Inprogress=1        #Inprogress            
    SucessFailure=2     #Success (enabled) or failure             
    TimeOut=4           #Timed out
    Aborted=8           #Aborted
    Rate2Lo=256         #Input rate is too low
    Rate2Hi=512         #Input rate is too high
   
class DiagnosticOptions(object):
    """
    Description:
        Encapsulates all of the diagnostic tests that can be performed.  
        Each test may be enabled by bitwise OR'ing each of the tests
        defined in this class.  The parameter value that should be
        written to for enabling these tests is System_DiagnosticsOptions
    """
    TestMemory=1        #Test memory            
    TestLEDs=2          #Test LEDs             
    TestFileSystem=4    #Test file system        
    
class DiagnosticEnableOptions(object):
    """
    Description:
        Encapsulates all of the methods for enabling the
        diagnostic tests.  The parameter value that should be
        written to for enabling these tests is System_DiagnosticsEnableOptions.
        You can bitwise OR the attributes below.
    """
    RunNow=1          #Run tests now            
    RunAtStartup=2    #Run tests at startup                    
    
class PresetModes(object):
    """
    Description:
        Encapsulates all of the preset options for the following 
        acquisition modes: PHA, DLFC, MCS, MSS, List, and TList
        Time presets are enabled by setting the Preset_Options to
        either: PresetLiveTime or PresetRealTime.  You may bitwise
        OR computational presets with time preset bits.  MCS only
        supports PresetNone or PresetSweeps Not computational presets
    """
    PresetNone=0        #No preset
    PresetLiveTime=1    #Count to the specified live time
    PresetRealTime=2    #Count to the specified real time
    PresetSweeps=4      #Count to the specified sweeps
    PresetIntegral=8    #Count to the specified integral value (requires start and stop region)
    
class FwhmCalibrationModels(object):
    """
    Description:
        Encapsulates all of the FWHM calibration
        models.  Set the value of Calibrations_FWHM_CurrentModel
        to one of the attributes below
    """
    SquareRoot=0    #Square-Root model
    Polynomial=1    #Polynomial model
    
class RASenableLine(object):
    """
    Description:
        Encapsulates all of the Remote Access Services
        options.  Set the value of Network_RAS_Enable
        to one of the attributes below
    """
    Disable=0   #Disable RAS
    Direct=1    #Enable the serial line
    Modem=2     #Enable the modem
    
class InputCapabilities(object):
    """
    Description:
        Encapsulates all of the input capabilities.
        Each input has specific capabilites that are
        defined by the device.  Simply query the input
        for its capabilities via Input_Capabilities
        and bitwise OR the attributes below to determine
        the supported capabilities
    """
    SupportsPHAmode=1            #Input supports PHA mode
    SupportsLFCmode=2            #Input supports LFC mode        
    SupportsMCSmode=4            #Input supports MCS mode
    SupportsGainCntl=8           #Input supports gain adjust control
    SupportsFilterCntl=16        #Input supports dsp filter adjust control
    SupportsStabilizerCntl=32    #Input supports stabilizer adjust control
    SupportsHVPSCntl=64          #Input supports HVPS adjust control
    SupportsChanger=128          #Input supports sample changer
    SupportsCounters=256         #Input supports counters
    SupportsCoincGate=512        #Input supports coinc gate parameters
    SupportsExternalSync=1024    #Input supports external sync control
    SupportsGPIOs=2048           #Input supports GPIOs
    SupportsMSSmode=4096         #Input supports MSS mode
    SupportsDLFCmode=8192        #Input supports DLFC mode
    SupportsRWregisters=16384    #Input supports read/write registers
    SupportsListmode=32768       #Input supports List mode
    SupportsMonitorCntl=65536    #Input supports monitor output control
    SupportsTlistmode=131072     #Input supports Time Stamped List mode  
    SupportsSCAs = 1048576       #Input supports SCA collection                              
   
class InputModes(object):
    """
    Description:
        Encapsulates all of the acquisition modes for 
        an input.  Simply set the value for the parameter
        Input_Mode.  Before setting the value query the
        input capabilities to verify the input supports
        the specific acquisition mode
    """
    Pha=0    #PHA
    Mcs=1    #MCS
    Dlfc=3   #DLFC
    List=4   #List 
    Tlist=5  #Time stamped list
    Mss=6    #MSS mode
    
class McsDiscModes(object):
    """
    Description:
        Encapsulates all of the MCS discriminator
        modes.  Set the value for the parameter
        Input_DiscMode to one of the attributes below
    """
    FDisc=0                    
    TTL=1                        
    ROI=2                                
    
class Polarity(object):
    """
    Description:
        Encapsulates all of the polarity values
    """
    PositivePolarity=0
    NegativePolarity=1
      
class BLRmode(object):
    """
    Description:
        Encapsulates all of the BLR mode values
        Simply set the value of Input_BLRmode
        to one of the attributes below
    """
    BlrAutomatic=0
    BlrSoft=3
    BlrMedium=2
    BlrHard=1
      
class PreampType(object):
    """
    Description:
        Encapsulates all of the preamp types
        Simply set the value of Input_PreampType
        to one of the attributes below
    """
    RC=0
    TRP=1
      
class FDiscShaping(object):
    """
    Description:
        Encapsulates all of the fast discriminator
        shaping values.  Simply set the value of Input_FastDiscShaping
        to one of the attributes below
    """
    Normal=0
    LowEnergy=1

class AutomaticManual(object):
    """
    Description:
        Encapsulates all of the automatic
        or manual options
    """
    Automatic=0
    Manual=1    

class OnOff(object):
    """
    Description:
        Encapsulates all of the on/off
        states
    """   
    Off=0
    On=1    
      
class ExternalControlMode(object):
    """
    Description:
        Encapsulates all of the external acquisition
        control modes.  Simply set the Input_xxxExternalControlMode
        parameter where xxx is Pha or Mcs to
        one of the attributes below
    """
    Disable=0
    DSA2K=2    
    Lynx=1
    
class ExternalControl(object):
    """
    Description:
        Encapsulates all of the external acquisition
        control modes.  Simply set the Input_xxxExternalControl
        parameter where xxx is Pha or Mcs to
        one of the attributes below
    """
    StartOnly=0
    StopOnly=1    
    StartAndStop=2
    
class StabilizerCorrectionRange(object):
    """
    Description:
        Encapsulates all of the stabilizer correction
        range options.  Simply set the Input_StabilizerGainCorrRange
        to one of the attributes below
    """
    Ge=0
    NaI=1    

class StabilizerMode(object):
    """
    Description:
        Encapsulates all of the stabilizer modes
        range options.  Simply set the Input_StabilizerGainMode
        to one of the attributes below
    """
    StabOff=0
    StabOn=1    
    StabHold=2
    
class CoincGateMode(object):
    """
    Description:
        Encapsulates all of the coincidence gate modes
        Simply set the Input_CoincGateMode to
        one of the attributes below
    """
    CoincOff=0
    Coinc=1    
    AntiCoinc=2

class ExternalSyncMode(object): 
    """
    Description:
        Encapsulates all of the external synchronization
        modes Simply set the Input_ExternalSyncMode to
        one of the attributes below
    """
    SyncMasterB=2
    SyncMaster=1
    SyncSlave=0
    
class ExternalSyncStatus(object): 
    """
    Description:
        Encapsulates all of the external synchronization
        status Simply set the Input_ExternalSyncStatus to
        one of the attributes below
    """
    Disabled=0       #Disable
    Enabled=1        #Enable Ext Sync to all acquisition modules, which includes Mss, Aux, Sca, and List modules
    Independent=2    #Enable Ext Sync module only.   This allows independent ext-sync control to individual acquisition modules (Mss, Aux, Sca, and List)

class MonitorOutControl(object):
    """
    Description:
        Encapsulates all of the monitor out controls.  Simply set 
        the Input_MonitorControl to one of the attributes below
    """
    Disabled=0              #Disable
    SlowShaper=1            #Route slow shaper signal to MON OUT BNC
    FastShaper=2            #Route fast shaper signal to MON OUT BNC
    ADCAfterDelay=3         #Route ADC after delay signal to MON OUT BNC
    
class ClockSource(object):    
    """
    Description:
        Encapsulates all of the synchronization clock source options.  
        This is used to set Input_SCAexternalSyncMode, Input_MSSexternalSyncMode, Counter_ExternalSyncMode
    """
    InternalClockSrc=0    #Internal 1uS clock source
    ExternalClockSrc=1    #External clock source via Ext Sync BNC
    
class CounterStatus(object):    
    """
    Description:
        Encapsulates the acquisition status for aux counters and SCAs.  
        This is used with Input_SCAstatus, Counter_Status.
        Write to this parameter to start/stop data acquisition.  
        Read this parameter to get current acquisition status
    """
    IdleCntrStatus=0        #Not acquiring
    BusyCntrStatus=1        #Acquiring
    WaitingCntrStatus=32    #Armed for acquiring and waiting to start
class SCApresetModes(object):    
    """
    Description:
        Encapsulates the preset modes for the SCAs.  
        This is used with Input_SCApresetMode.
    """ 
    ScaPresetLive=1
    ScaPresetReal=2
    
    
