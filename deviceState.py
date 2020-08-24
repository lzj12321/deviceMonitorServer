from enum import IntEnum

class DeviceState(IntEnum):
    OFFLINE=0
    ONLINE=1
    HIPOT=2
    ANFANG=3
    CATCH_ERROR=4
    STOP=5
    PAUSE=6
    OTA=7
    MONITOR=8
    UNKNOWN_WORKMODE=9
    IDLE=10
    CALCULATE=11


class MonitorState(IntEnum):
    MONITOR_STATE=0
    CHOOSING_MONITOR_STATE=1
    CHOOSING_OTA_STATE=2
    CHOOSING_CALCULATE_STATE=3
