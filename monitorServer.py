from socketTool import Socket
from mysqlTool import MysqlTool
from yamlTool import Yaml_Tool
import logging
from PyQt5.QtCore import *
from PyQt5 import QtNetwork
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
from loggerTool import Logger
from robotState import RobotState
import copy
from device import Device,StateMachine


class MonitorServer(QObject):
    appendRunMsg=pyqtSignal(str)
    updateDeviceState=pyqtSignal(str,int)
    def __init__(self):
        super(MonitorServer,self).__init__()
        pass

    def paramIni(self):
        self.outLog('param initialize')
        paramPath="configure.yaml"
        confirmConfigureFile=QFile(paramPath)
        if not confirmConfigureFile.exists():
            QMessageBox.critical(self,'Critical','配置文件丢失!')
            exit(0)

        self.yamlTool=Yaml_Tool()
        self.params=self.yamlTool.getValue(paramPath)
        
        ######## initializi robot && socket#########
        self.isCheckDeviceOnline={}
        self.devices={}
        self.onlineRobotIp={}
        self.ipSocket={}
        self.workshop=self.params['workshop']

        self.stateMachine=StateMachine()
        for _device in self.params['devices'].keys():
            self.isCheckDeviceOnline[_device]=False
            newDevice=Device(_device)
            newDevice.bind(RobotState.OFFLINE,self.stateMachine.getFsm(RobotState.OFFLINE))
            self.devices[_device]=newDevice
            newDevice.stateChanged.connect(self.processDeviceStateChanged)
        pass

    def serverIni(self):
        self.outLog('server initialize')
        self.serverSocket=QtNetwork.QTcpServer()
        if self.serverSocket.listen(QtNetwork.QHostAddress.Any,self.params['server']['port']):
            self.serverSocket.newConnection.connect(self.newConnection)
        else:
            exit(0)
        pass

    def mysqlToolIni(self):
        self.outLog('mysql initialize')
        self.mysqlTool=MysqlTool()
        # if not self.mysqlTool._connectState:
            # self.outLog("Can't connect to mysql server")

    def setRobotToOtaState(self,_otaRobots):
        for _robot in _otaRobots:
            if self.devices[_robot].state==RobotState.OTA:
                continue
            if _robot in self.onlineRobotIp.keys():
                print('send ota msg to:'+_robot)
                self.ipSocket[self.onlineRobotIp[_robot]].sendMsg('ota')
                pass
            else:
                self.appendRunMsg.emit('cant set '+_robot+' into ota mode because it not online!')
        pass

    def setRobotToMonitorState(self,_monitorList):
        for _device in self.devices.keys():
            if _device in _monitorList:
                if self.devices[_device].state==RobotState.MONITOR:
                    continue
                if _device in self.onlineRobotIp.keys():
                    self.ipSocket[self.onlineRobotIp[_device]].sendMsg('monitor')
                    print('send monitor msg to '+_device)
                else:
                    pass
                    # self.appendRunMsg.emit('cant set '+_device+' into monitor model because it not on line!')
            elif self.devices[_device].state!=RobotState.OTA:
                if _device in self.onlineRobotIp.keys():
                    self.ipSocket[self.onlineRobotIp[_device]].sendMsg('idle')
                    print('send idle msg to '+_device)
                else:
                    pass
                    # self.appendRunMsg.emit('cant set '+_device+' into idle model because it not on line!')
                
        pass

    def checkTimerTimeout(self):
        #### only detect offline time more than three times it will close the connection #########
        for _device in self.isCheckDeviceOnline.keys():
            if self.devices[_device].state!=RobotState.OFFLINE:
                if not self.isCheckDeviceOnline[_device]:
                    self.appendRunMsg.emit(_device+" offline!")
                    self.outLog(_device+' alter robot state to offline!')
                    self.stateMachine.changeState(self.devices[_device],RobotState.OFFLINE)
                    self.closeRobotConnection(_device)
            self.isCheckDeviceOnline[_device]=False
        pass

    def closeRobotConnection(self,_robotFlag):
        self.outLog("close the connection with "+self.onlineRobotIp[_robotFlag])
        self.ipSocket[self.onlineRobotIp[_robotFlag]].close()
        self.ipSocket.pop(self.onlineRobotIp[_robotFlag])
        self.onlineRobotIp.pop(_robotFlag)
        pass

    def timerIni(self):
        self.outLog('timer initialize')
        checkTimer=QTimer(self)
        checkTimer.timeout.connect(self.checkTimerTimeout)
        checkTimer.setInterval(20000)
        checkTimer.start()
        pass

    def addRunMessage(self,msg):
        self.appendRunMsg.emit(msg)
        pass

    def run(self):
        self.paramIni()
        self.serverIni()
        self.timerIni()
        self.mysqlToolIni()
        
    def newConnection(self):
        print("a new connection")
        newSock=self.serverSocket.nextPendingConnection()
        _sock=Socket()
        _sock.setSocket(newSock)
        _sock.receivedMsg.connect(self.processMsgFromRobot)

        newSockIp = newSock.peerAddress().toString().split(':')[-1]
        self.outLog("a new connection from "+newSockIp)
        if newSockIp in self.ipSocket.keys():
            self.ipSocket[newSockIp].close()
        self.ipSocket[newSockIp]=_sock
        pass

    def saveRobotStateChangeLog(self,_robotFlag,_robotState):
        description="null"
        if not self.mysqlTool.saveRobotState(self.workshop,_robotFlag,str(_robotState),description):
            self.outLog("save log to mysql server error!"+_robotFlag+' '+_robotState)
        pass

    def outLog(self,logMsg):
        time=QDate.currentDate().toString('yyyy-MM-dd')+str('.log')
        log = Logger()
        log.outputLog('log/'+time,logMsg)
        pass

    def process_unknownWorkmode_msg(self,_robotFlag):
        pass

    def process_stop_msg(self,_robotFlag):
        self.stateMachine.changeState(self.devices[_robotFlag],RobotState.STOP)
        pass

    def process_pause_msg(self,_robotFlag):
        self.stateMachine.changeState(self.devices[_robotFlag],RobotState.PAUSE)
        pass

    def process_ota_check_msg(self,_robotFlag):
        self.stateMachine.changeState(self.devices[_robotFlag],RobotState.OTA)
        pass

    def process_monitor_check_msg(self,_robotFlag):
        self.stateMachine.changeState(self.devices[_robotFlag],RobotState.MONITOR)
        pass

    def process_idle_check_msg(self,_robotFlag):
        self.stateMachine.changeState(self.devices[_robotFlag],RobotState.IDLE)
        pass

    def processDeviceStateChanged(self,_device,_state):
        self.updateDeviceState.emit(_device,_state)
        self.saveRobotStateChangeLog(_device,_state)
        # self.addRunMessage(_device+':'+_validMsg)
        # print(_device+' alter robot state to '+str(_state))
        pass

    def processMsgFromRobot(self,msg,sockIp):
        print('                 msg                    :'+msg)
        _msgs=msg.split(':')
        if len(_msgs)==2:
            _robotFlag=msg.split(':')[0]
            _validMsg=msg.split(':')[1]

            ######## update robot socket ##########
            if _robotFlag in self.onlineRobotIp.keys():
                ### the connected robot use the new ip to connect server ###
                if sockIp != self.onlineRobotIp[_robotFlag]:
                    if self.onlineRobotIp[_robotFlag] in self.ipSocket.keys():
                        self.ipSocket[self.onlineRobotIp[_robotFlag]].close()
                        self.ipSocket.pop(self.onlineRobotIp[_robotFlag])
                    else:
                        self.outLog("error self.onlineRobotIp[_robotFlag] in self.ipSocket.keys() "+sockIp+' '+_robotFlag)
            elif _robotFlag in self.devices.keys():
                self.onlineRobotIp[_robotFlag]=sockIp
            else:
                self.outLog('receivd a error msg:'+msg)
                return

            if _robotFlag in self.devices.keys():
                self.isCheckDeviceOnline[_robotFlag]=True
                if _validMsg=='stop':
                    self.process_stop_msg(_robotFlag)
                elif _validMsg=='pause':
                    self.process_pause_msg(_robotFlag)
                elif _validMsg=='ota_check':
                    self.process_ota_check_msg(_robotFlag)
                elif _validMsg=='monitor_check':
                    self.process_monitor_check_msg(_robotFlag)
                elif _validMsg=='idle_check':
                    self.process_idle_check_msg(_robotFlag)
                elif _validMsg=='unknownWorkmode':
                    self.process_unknownWorkmode_msg(_robotFlag)
                else:
                    self.outLog('receivd a error msg without valid msg:'+msg)
                    return
            else:
                self.outLog('receivd a error msg without valid robot:'+msg)
        else:
            self.outLog('receivd a error msg:'+msg)
        pass
    
    def getMonitoringDevice(self):
        _monitoringDevices=[]
        for _device in self.devices.keys():
            _state=self.devices[_device].state
            if _state!=RobotState.IDLE and _state!=RobotState.OFFLINE and _state!=RobotState.OTA:
                _monitoringDevices.append(_device)
        return _monitoringDevices
        pass

    def getOtaDevice(self):
        _otaDevices=[]
        for _device in self.devices.keys():
            if self.devices[_device].state==RobotState.OTA:
                _otaDevices.append(_device)
        return _otaDevices

if __name__ == '__main__':
    server=MonitorServer()
    server.run()