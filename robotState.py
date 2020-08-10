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
