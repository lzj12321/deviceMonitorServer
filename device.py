from deviceState import DeviceState
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal


class Device(QObject):
    stateChanged=pyqtSignal(str,int)
    def __init__(self,_deviceInfo):
        super(Device,self).__init__()
        # self.deviceSerial=_deviceInfo['deviceSerial']
        self.ip=_deviceInfo['ip']
        self.deviceSerial=_deviceInfo['serial']
        self.firmWareVersion=_deviceInfo['firmWareVersion']
        self.macAddress=_deviceInfo['macAddress']
        self.productModel=_deviceInfo['productModel']
        self.productNum=_deviceInfo['productNum']

        self.state=DeviceState.OFFLINE
        self.fsm=None
    
    def enter_offline(self):
        self.state=DeviceState.OFFLINE
        self.stateChanged.emit(self.deviceSerial,DeviceState.OFFLINE)
        print("%s enter offline state!"% self.deviceSerial)
        pass
    def exit_offline(self):
        print("%s exit offline state!"% self.deviceSerial)
        pass

    def enter_calculate(self):
        self.state=DeviceState.CALCULATE
        self.stateChanged.emit(self.deviceSerial,DeviceState.CALCULATE)
        print("%s enter calculate state!"% self.deviceSerial)
        pass
    def exit_calculate(self):
        print("%s exit calculate state!"% self.deviceSerial)
        pass

    def enter_idle(self):
        self.state=DeviceState.IDLE
        self.stateChanged.emit(self.deviceSerial,DeviceState.IDLE)
        print("%s enter idle state!"% self.deviceSerial)
        pass

    def exit_idle(self):
        print("%s exit idle state!"% self.deviceSerial)
        pass

    def enter_monitor(self):
        self.state=DeviceState.MONITOR
        self.stateChanged.emit(self.deviceSerial,DeviceState.MONITOR)
        print("%s enter monitor state!"% self.deviceSerial)
        pass
    def exit_monitor(self):
        print("%s exit monitor state!"% self.deviceSerial)
        pass

    def enter_ota(self):
        self.state=DeviceState.OTA
        self.stateChanged.emit(self.deviceSerial,DeviceState.OTA)
        print("%s enter ota state!"% self.deviceSerial)
        pass
    def exit_ota(self):
        print("%s exit ota state!"% self.deviceSerial)
        pass

    def enter_pause(self):
        self.state=DeviceState.PAUSE
        self.stateChanged.emit(self.deviceSerial,DeviceState.PAUSE)
        print("%s enter pause state!"% self.deviceSerial)
        pass
    def exit_pause(self):
        print("%s exit pause state!"% self.deviceSerial)
        pass
        
    def enter_stop(self):
        self.state=DeviceState.STOP
        self.stateChanged.emit(self.deviceSerial,DeviceState.STOP)
        print("%s enter stop state!"% self.deviceSerial)
        pass
    def exit_stop(self):
        print("%s exit stop state!"% self.deviceSerial)
        pass

    def enter_unknown(self):
        self.state=DeviceState.UNKNOWN_WORKMODE
        self.stateChanged.emit(self.deviceSerial,DeviceState.UNKNOWN_WORKMODE)
        print("%s enter unknown state!"% self.deviceSerial)
        pass
    def exit_unknown(self):
        print("%s exit unknown state!"% self.deviceSerial)
        pass

    def bind(self,_state,_fsm):
        self.state=_state
        self.fsm=_fsm
    

class State():
    def exit(self):
        pass

    def enter(self):
        pass

class OfflineState(State):
    def exit(self,obj):
        obj.exit_offline()
        pass

    def enter(self,obj):
        obj.enter_offline()

class CalculateState(State):
    def exit(self,obj):
        obj.exit_calculate()
        pass

    def enter(self,obj):
        obj.enter_calculate()

class IdleState(State):
    def exit(self,obj):
        obj.exit_idle()
        pass

    def enter(self,obj):
        obj.enter_idle()

class MonitorState(State):
    def exit(self,obj):
        obj.exit_monitor()
        pass

    def enter(self,obj):
        obj.enter_monitor()

class OtaState(State):
    def exit(self,obj):
        obj.exit_ota()
        pass

    def enter(self,obj):
        obj.enter_ota()

class PauseState(State):
    def exit(self,obj):
        obj.exit_pause()
        pass

    def enter(self,obj):
        obj.enter_pause()

class UnkonwnState(State):
    def exit(self,obj):
        obj.exit_unknown()
        pass

    def enter(self,obj):
        obj.enter_unknown()


class StopState(State):
    def exit(self,obj):
        obj.exit_stop()
        pass

    def enter(self,obj):
        obj.enter_stop()

class StateMachine(object):
    def __init__(self):
        self.states={DeviceState.OFFLINE:OfflineState(),
        DeviceState.IDLE:IdleState(),
        DeviceState.STOP:StopState(),
        DeviceState.PAUSE:PauseState(),
        DeviceState.OTA:OtaState(),
        DeviceState.MONITOR:MonitorState(),
        DeviceState.UNKNOWN_WORKMODE:UnkonwnState(),
        DeviceState.CALCULATE:CalculateState()
        }

    def getFsm(self,state):
        return self.states[state]

    def changeState(self,obj,newState):
        if newState==obj.state:
            return
            pass
            # fsm=self.getFsm(obj.state)
            # fsm.enter(obj)
        else:
            oldFsm=self.getFsm(obj.state)
            oldFsm.exit(obj)
            newFsm=self.getFsm(newState)
            newFsm.enter(obj)
            obj.state=newState

if __name__=="__main__":
    testMachine=StateMachine()
    testDevice=Device('testRobot')
    testDevice.bind(DeviceState.OFFLINE,testMachine.getFsm(DeviceState.OFFLINE))
    testMachine.changeState(DeviceState.MONITOR,testDevice)
    testMachine.changeState(DeviceState.IDLE,testDevice)
    pass