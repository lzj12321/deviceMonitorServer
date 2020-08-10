from enum import IntEnum

class RobotState(IntEnum):
    OFFLINE=0
    ONLINE=1
    HIPOT=2
    ANFANG=3
    CATCH_ERROR=4
    STOP=5
    PAUSE=6
    OTA=7
    MONITOR=8


class MonitorState(IntEnum):
    MONITOR_STATE=0
    CHOOSING_MONITOR_STATE=1
    CHOOSING_OTA_STATE=2
