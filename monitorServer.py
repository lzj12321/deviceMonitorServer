from socketTool import Socket
from mysqlTool import MysqlTool
from yamlTool import Yaml_Tool
import logging
from PyQt5.QtCore import *
from PyQt5 import QtNetwork
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
from loggerTool import Logger
from deviceState import DeviceState
from device import Device,StateMachine
import datetime
from soundPlayerTherad import SoundPlayerThread
import time


class MonitorServer(QObject):
    appendRunMsg=pyqtSignal(str)
    updateDeviceState=pyqtSignal(str,int)
    def __init__(self):
        super(MonitorServer,self).__init__()
        pass

    def paramIni(self):
        self.hour=int(datetime.datetime.now().strftime('%H'))
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
        self.onlineDeviceIp={}
        self.ipSocket={}
        self.workshop=self.params['workshop']
        self.stopDeviceList=[]
        self.waitPlayAlarmDevice=[]
        self.isPlayingAlarmSound=False
        self.alarmingDevice=''
        self.stateMachine=StateMachine()
        for _device in self.params['devices'].keys():
            self.isCheckDeviceOnline[_device]=False
            newDevice=Device(self.params['devices'][_device])
            newDevice.bind(DeviceState.OFFLINE,self.stateMachine.getFsm(DeviceState.OFFLINE))
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

    def setDeviceToOtaState(self,_otaDeviceList):
        for _device in self.devices.keys():
            if _device in _otaDeviceList:
                if self.devices[_device].state==DeviceState.OTA:
                    continue
                if _device in self.onlineDeviceIp.keys():
                    self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('ota')
                    # self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('clear_productData')
                    pass
                else:
                    self.appendRunMsg.emit('can\'t set '+_device+' into ota mode because it not online!')
            elif self.devices[_device].state==DeviceState.OTA:
               # print('test idle')
                self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('idle')
        pass

    def setDeviceToMonitorState(self,_monitorList):
        for _device in self.devices.keys():
            if _device in _monitorList:
                if self.devices[_device].state==DeviceState.MONITOR:
                    continue
                if _device in self.onlineDeviceIp.keys():
                    self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('monitor')
                    # self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('calculate')
                   # print('send monitor msg to '+_device)
                else:
                    pass
                    # self.appendRunMsg.emit('cant set '+_device+' into monitor model because it not on line!')
            elif self.devices[_device].state!=DeviceState.OTA:
                if _device in self.onlineDeviceIp.keys():
                    self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('idle')
                 #   print('send idle msg to '+_device)
                else:
                    pass
                    # self.appendRunMsg.emit('cant set '+_device+' into idle model because it not on line!')
        pass

    def setDeviceToCalculateState(self,_calculateList):
        for _device in self.devices.keys():
            if _device in _calculateList:
                if self.devices[_device].state==DeviceState.CALCULATE:
                    continue
                if _device in self.onlineDeviceIp.keys():
                    self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('calculate')
                   # print('send calculate msg to '+_device)
            elif self.devices[_device].state==DeviceState.CALCULATE:
                if _device in self.onlineDeviceIp.keys():
                    self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('idle')
                    #print('send idle msg to '+_device)


    def clearDeviceHourProduction(self,_productList):
        for _device in self.devices.keys():
            if _device in _productList:
                if _device in self.onlineDeviceIp.keys():
                    self.ipSocket[self.onlineDeviceIp[_device]].sendMsg('clear_productData')
        pass

    def checkTimerTimeout(self):
        ####play alarm sound####
        if len(self.waitPlayAlarmDevice)!=0:
            self.playAlarmSound(self.waitPlayAlarmDevice[0])

        for _device in self.getMonitoringDevice():
            if self.devices[_device].state==DeviceState.STOP or self.devices[_device].state==DeviceState.PAUSE:
                if _device not in self.waitPlayAlarmDevice:
                    self.waitPlayAlarmDevice.append(_device)
            
        ####clear the production if the hour is changed###
        _hour=int(datetime.datetime.now().strftime('%H'))
        if _hour!=self.hour:
            self.clearDeviceHourProduction(self.getCalculatingDevice())

        #### only detect offline time more than three times it will close the connection #########
        for _device in self.isCheckDeviceOnline.keys():
            if self.devices[_device].state!=DeviceState.OFFLINE:
                if not self.isCheckDeviceOnline[_device]:
                    self.appendRunMsg.emit(_device+" offline!")
                    self.outLog(_device+' alter device state to offline!')
                    self.stateMachine.changeState(self.devices[_device],DeviceState.OFFLINE)
                    self.closeDeviceConnection(_device)
            self.isCheckDeviceOnline[_device]=False
        pass

    def closeDeviceConnection(self,_device):
        self.outLog("check this connection time out,close this connection with "+self.onlineDeviceIp[_device])
        print(self.onlineDeviceIp)
        self.ipSocket[self.onlineDeviceIp[_device]].close()
        self.ipSocket.pop(self.onlineDeviceIp[_device])
        self.onlineDeviceIp.pop(_device)
        pass

    def timerIni(self):
        self.outLog('timer initialize')
        checkTimer=QTimer(self)
        checkTimer.timeout.connect(self.checkTimerTimeout)
        checkTimer.setInterval(30000)
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
        _sock.receivedMsg.connect(self.processMsgFromDevice)

        newSockIp = newSock.peerAddress().toString().split(':')[-1]
        self.outLog("a new connection from "+newSockIp)
        if newSockIp in self.ipSocket.keys():
            self.ipSocket[newSockIp].close()
        self.ipSocket[newSockIp]=_sock
        print('ipSocket.size:'+str(len(self.ipSocket)))
        pass

    def saveDeviceStateChangeLog(self,_device,_deviceState):
        description="null"
        if not self.mysqlTool.saveDeviceState(self.workshop,_device,str(_deviceState),description):
            self.outLog("save log to mysql server error!"+_device+' '+_deviceState)
        pass

    def outLog(self,logMsg):
        time=QDate.currentDate().toString('yyyy-MM-dd')+str('.log')
        log = Logger()
        log.outputLog('log/'+time,logMsg)
        pass

    def process_unknownWorkmode_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.UNKNOWN_WORKMODE)
        pass

    def process_calculate_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.CALCULATE)
        pass

    def process_stop_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.STOP)
        pass

    def process_pause_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.PAUSE)
        pass

    def process_ota_check_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.OTA)
        pass

    def process_monitor_check_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.MONITOR)
        pass

    def process_idle_check_msg(self,_device):
        self.stateMachine.changeState(self.devices[_device],DeviceState.IDLE)
        pass

    def stopPlayDeviceAlarmSound(self,_device):
        if self.alarmingDevice==_device and self.isPlayingAlarmSound:
            self._alarmThread.isRunning():
                self._alarmThread.terminate()
                self.isPlayingAlarmSound=False
        pass

    def playAlarmSound(self,_device):
        ###loop play alarm device###
        if self.devices[_device].state!=DeviceState.PAUSE and self.devices[_device].state!=DeviceState.STOP:
            if _device in self.waitPlayAlarmDevice:
                self.waitPlayAlarmDevice.remove(_device)
            if len(self.waitPlayAlarmDevice)!=0 and not self.isPlayingAlarmSound:
                self.playAlarmSound(self.waitPlayAlarmDevice[0])
            return
        
        ###new alarm device###
        print("new alarm device "+_device)
        if self.isPlayingAlarmSound:
            if _device not in self.waitPlayAlarmDevice:
                self.waitPlayAlarmDevice.append(_device)
            return
        else:
            if _device in self.waitPlayAlarmDevice:
                self.waitPlayAlarmDevice.remove(_device)
            # print(_device+" play alarm sound")
            self.__playSound(_device)
        pass

    def __playSound(self,_device):
        self._alarmThread=SoundPlayerThread(_device,3)
        self._alarmThread.playEnd.connect(self.playAlarmSoundEnd)
        self._alarmThread.start()
        self.isPlayingAlarmSound=True
        self.alarmingDevice=_device
        pass

    def playAlarmSoundEnd(self,_device):
        self.isPlayingAlarmSound=False
        print("play alarm sound end!"+_device)

    def processDeviceStateChanged(self,_device,_state):
        print(_device+" state changed")

        self.updateDeviceState.emit(_device,_state)
        self.saveDeviceStateChangeLog(_device,_state)
        if _state==DeviceState.PAUSE or _state==DeviceState.STOP:
            self.playAlarmSound(_device)
        elif _state==DeviceState.MONITOR:
            self.stopPlayDeviceAlarmSound(_device)
        pass

    def preProcessMsgFromDevice(self,msg,sockIp):
        #print("msg:"+msg)
        isMsgValid=True
        _device=''
        _validMsg=''

        _msgs=msg.split(':')
        if len(_msgs)==2:
            _device=_msgs[0]
            _validMsg=_msgs[1].replace("\n","")

            ######## update robot socket ##########
            if _device in self.onlineDeviceIp.keys():
                ### the connected robot use the new ip to connect server ###
                if sockIp != self.onlineDeviceIp[_device]:
                    if self.onlineDeviceIp[_device] in self.ipSocket.keys():
                        self.ipSocket[self.onlineDeviceIp[_device]].close()
                        self.ipSocket.pop(self.onlineDeviceIp[_device])
                    else:
                        self.outLog("error self.onlineDeviceIp[_device] in self.ipSocket.keys() "+sockIp+' '+_device)
                elif _device in self.devices.keys():
                    self.onlineDeviceIp[_device]=sockIp
                    self.devices[_device].ip=sockIp
                elif _device not in self.devices.keys():
                    isMsgValid=False
            else:
                # isMsgValid=False
                # self.outLog('receivd a error msg device not in onlineDeviceIp:'+msg)
                self.onlineDeviceIp[_device]=sockIp
        else:
            isMsgValid=False
            self.outLog('receivd a error msg len!=2:'+msg)
        return isMsgValid,_device,_validMsg


    def processMsgFromDevice(self,msg,sockIp):
        isMsgValid,_device,_validMsg=self.preProcessMsgFromDevice(msg,sockIp)
        if not isMsgValid:
            return

        if _device in self.devices.keys():
            self.devices[_device].ip=sockIp
            self.isCheckDeviceOnline[_device]=True
            if _validMsg=='stop':
                self.process_stop_msg(_device)
            elif _validMsg=='pause':
                self.process_pause_msg(_device)
            elif _validMsg=='ota_check':
                self.process_ota_check_msg(_device)
            elif _validMsg=='monitor_check':
                self.process_monitor_check_msg(_device)
            elif _validMsg=='idle_check':
                self.process_idle_check_msg(_device)
            elif _validMsg=='unknown_check':
                self.process_unknownWorkmode_msg(_device)
            else:
                self.outLog("receive a invalid msg:"+msg)
        else:
            self.outLog("receive a invalid msg:"+msg)
        pass

    def getMonitoringDevice(self):
        _monitoringDevices=[]
        for _device in self.devices.keys():
            _state=self.devices[_device].state
            if _state!=DeviceState.IDLE and \
                 _state!=DeviceState.OFFLINE and \
                      _state!=DeviceState.OTA and \
                          _state!=DeviceState.UNKNOWN_WORKMODE:
                _monitoringDevices.append(_device)
        return _monitoringDevices
        pass

    def getCalculatingDevice(self):
        _calculatingDevices=[]
        for _device in self.devices.keys():
            if self.devices[_device].state==DeviceState.CALCULATE:
                _calculatingDevices.append(_device)
        return _calculatingDevices

    def getOtaDevice(self):
        _otaDevices=[]
        for _device in self.devices.keys():
            if self.devices[_device].state==DeviceState.OTA:
                _otaDevices.append(_device)
        return _otaDevices

if __name__ == '__main__':
    server=MonitorServer()
    server.run()
