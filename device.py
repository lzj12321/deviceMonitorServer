from robotState import RobotState
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal


class Device(QObject):
    stateChanged=pyqtSignal(str)
    def __init__(self,_name):
        super(Device,self).__init__()
        self.name=_name
        self.state=RobotState.OFFLINE
        self.fsm=None
    
    def enter_offline(self):
        self.stateChanged.emit(self.name)
        print("%s enter offline state!"% self.name)
        pass
    def exit_offline(self):
        print("%s exit offline state!"% self.name)
        pass

    def enter_idle(self):
        self.stateChanged.emit(self.name)
        print("%s enter idle state!"% self.name)
        pass
    def exit_idle(self):
        print("%s exit idle state!"% self.name)
        pass

    def enter_monitor(self):
        self.stateChanged.emit(self.name)
        print("%s enter monitor state!"% self.name)
        pass
    def exit_monitor(self):
        print("%s exit monitor state!"% self.name)
        pass

    def enter_ota(self):
        self.stateChanged.emit(self.name)
        print("%s enter ota state!"% self.name)
        pass
    def exit_ota(self):
        print("%s exit ota state!"% self.name)
        pass

    def enter_pause(self):
        self.stateChanged.emit(self.name)
        print("%s enter pause state!"% self.name)
        pass
    def exit_pause(self):
        print("%s exit pause state!"% self.name)
        pass
        
    def enter_stop(self):
        self.stateChanged.emit(self.name)
        print("%s enter stop state!"% self.name)
        pass
    def exit_stop(self):
        print("%s exit stop state!"% self.name)
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

class StopState(State):
    def exit(self,obj):
        obj.exit_stop()
        pass

    def enter(self,obj):
        obj.enter_stop()

class StateMachine(object):
    def __init__(self):
        self.states={RobotState.OFFLINE:OfflineState(),RobotState.IDLE:IdleState(),RobotState.STOP:StopState(),RobotState.PAUSE:PauseState(),RobotState.OTA:OtaState,RobotState.MONITOR:MonitorState()}

    def getFsm(self,state):
        return self.states[state]

    def changeState(self,newState,obj):
        if newState==obj.state:
            print('state unchanged')
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
    testDevice.bind(RobotState.OFFLINE,testMachine.getFsm(RobotState.OFFLINE))
    testMachine.changeState(RobotState.MONITOR,testDevice)
    testMachine.changeState(RobotState.IDLE,testDevice)
    pass