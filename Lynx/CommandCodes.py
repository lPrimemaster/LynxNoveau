class CommandCodes(object):
    """
    Description:
        Contains all of the device control commands.  Pass any one of these
        command codes to the .control method on a Device class instance.
    """
    Start = 3       #Start acquisition on this input
    Stop = 4        #Stop acquisition on this input
    Clear = 5       #Clear the acquisition memory for this input/group
    Commit = 9      #Commit all changes within the current transaction
    Save = 10       #Save the acquisition data to file on the device
    Rollback=12     #Undo all changes made within the current transaction
    ResetFactoryDefaults=24    #Reset to factory defaults for this input
    Reboot = 25     #Reboot the device
    BeginTrans=29   #Begin a transaction
    HvpsReset=32    #Reset the HVPS inhibit fault
    ClearFaults=35  #Clear all faults for this input
    StartAutoPoleZero=38     #Start automatic pole zero process
    StopAutoPoleZero=39      #Stop automatic pole zero process
    ChangerAdvance=40        #Advance the sample changer
    ResetStabilizer=44       #Reset the stabilizer
    Abort=45                 #Abort MSS or MCS acquisition now.  Do not wait till current group/sweep completes acq.
    CountersClear=46         #Clear the aux counters
    CountersLatch=47         #Latch the aux counters
    CountersLatchAndClear=48 #Latch and clear the aux counters
    SCAcountersClear=52      #Clears all SCA counters and timers
    SCAcountersLatch=53      #Latches SCA counters and timers
    SCAcountersLatchAndClear=54 #Latches SCA and clears counters and timers    