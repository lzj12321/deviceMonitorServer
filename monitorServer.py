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


class MonitorServer(QObject):
    appendRunMsg=pyqtSignal(str)
    updateRobotState=pyqtSignal(str)
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
        self.robotOnlineCheckFlag={}
        self.monitoringRobot=[]
        self.otaStateRobots=[]
        self.robotState={}
        self.onlineRobotIp={}
        self.ipSocket={}
        self.workshop=self.params['workshop']
        self._robots=self.params['robot'].split(',')
        for _robot in self._robots:
            self.monitoringRobot.append(_robot)
            self.robotOnlineCheckFlag[_robot]=False
            self.robotState[_robot]=RobotState.OFFLINE
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
            if _robot in self.otaStateRobots:
                continue
            if _robot in self.onlineRobotIp.keys():
                print('send ota msg to:'+_robot)
                self.ipSocket[self.onlineRobotIp[_robot]].sendMsg('ota')
                pass
            else:
                self.appendRunMsg.emit('cant set '+_robot+' into ota mode because it not online!')
        pass

    def setRobotToMonitorState(self,_monitorList):
        self.monitoringRobot=copy.deepcopy(_monitorList)
        for _robot in _monitorList:
            if _robot in self.onlineRobotIp.keys():
                self.ipSocket[self.onlineRobotIp[_robot]].sendMsg('monitor')
                print('send monitor msg to '+_robot)
            else:
                self.appendRunMsg.emit('cant set '+_robot+' into monitor model because it not on line!')
        pass

    def checkTimerTimeout(self):
        #### only detect offline time more than three times it will close the connection #########
        for _robot in self.robotOnlineCheckFlag.keys():
            if self.robotState[_robot]!=RobotState.OFFLINE:
                if not self.robotOnlineCheckFlag[_robot]:
                    self.appendRunMsg.emit(_robot+" offline!")
                    self.outLog(_robot+' alter robot state to offline!')
                    self.robotState[_robot]=RobotState.OFFLINE
                    self.saveRobotStateChangeLog(_robot,'offline')
                    self.updateRobotState.emit(_robot)
                    self.closeRobotConnection(_robot)

            ##remove the device from the ota or monitor list if it has disconnect from server##
                    # if _robot not in self.otaStateRobots:
                    #     self.otaStateRobots.remove(_robot)
                    # if _robot in self.monitoringRobot:
                    #     self.monitoringRobot.remove(_robot)
            self.robotOnlineCheckFlag[_robot]=False
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
        checkTimer.setInterval(60000)
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
        # prevStateElaspe=self.robotPrevStateStartTime[_robotFlag]
        if not self.mysqlTool.saveRobotState(self.workshop,_robotFlag,_robotState,description):
            self.outLog("save log to mysql server error!"+_robotFlag+' '+_robotState)
        pass

    def outLog(self,logMsg):
        time=QDate.currentDate().toString('yyyy-MM-dd')+str('.log')
        log = Logger()
        log.outputLog('log/'+time,logMsg)
        pass

    def process_unknownWorkmode_msg(self,_robotFlag):
        return RobotState.UNKNOWN_WORKMODE
        pass

    def process_stop_msg(self,_robotFlag):
        if _robotFlag in self.otaStateRobots:
            self.otaStateRobots.remove(_robotFlag)
        return RobotState.STOP
        pass

    def process_pause_msg(self,_robotFlag):
        if _robotFlag in self.otaStateRobots:
            self.otaStateRobots.remove(_robotFlag)
        return RobotState.PAUSE
        pass

    def process_ota_check_msg(self,_robotFlag):
        if _robotFlag not in self.otaStateRobots:
            self.otaStateRobots.append(_robotFlag)
        if _robotFlag in self.monitoringRobot:
            self.monitoringRobot.remove(_robotFlag)
        return RobotState.OTA
        pass

    def process_monitor_check_msg(self,_robotFlag):
        # if _robotFlag not in self.monitoringRobot:
            # self.monitoringRobot.append(_robotFlag)
        if _robotFlag in self.otaStateRobots:
            self.otaStateRobots.remove(_robotFlag)
        return RobotState.ONLINE
        # if self.robotState[_robotFlag]==RobotState.OTA:
            # _robotState=RobotState.ONLINE
        pass

    def process_idle_check_msg(self,_robotFlag):
        if _robot not in self.otaStateRobots:
            self.otaStateRobots.remove(_robotFlag)
        if _robot in self.monitoringRobot:
            self.monitoringRobot.remove(_robotFlag)
        return RobotState.IDLE
        pass

    def processMsgFromRobot(self,msg,sockIp):
        print('msg:'+msg)
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
            elif _robotFlag in self._robots:
                self.onlineRobotIp[_robotFlag]=sockIp
            else:
                self.outLog('receivd a error msg:'+msg)
                return

            _robotState=self.robotState[_robotFlag]
            if _robotFlag in self.robotOnlineCheckFlag.keys():
                self.robotOnlineCheckFlag[_robotFlag]=True
                if _validMsg=='stop':
                    _robotState=self.process_stop_msg(_robotFlag)
                elif _validMsg=='pause':
                    _robotState=self.process_pause_msg(_robotFlag)
                elif _validMsg=='ota_check':
                    _robotState=self.process_ota_check_msg(_robotFlag)
                elif _validMsg=='monitor_check':
                    _robotState=self.process_monitor_check_msg(_robotFlag)
                elif _validMsg=='idle_check':
                    _robotState=self.process_idle_check_msg(_robotFlag)
                elif _validMsg=='unknownWorkmode':
                    _robotState=self.process_unknownWorkmode_msg(_robotFlag)
                else:
                    self.outLog('receivd a error msg without valid msg:'+msg)
                    return
                if self.robotState[_robotFlag]!=_robotState:
                    self.saveRobotStateChangeLog(_robotFlag,_validMsg)
                    self.robotState[_robotFlag]=_robotState
                    self.updateRobotState.emit(_robotFlag)
                    self.addRunMessage(_robotFlag+':'+_validMsg)
                    self.outLog(_robotFlag+' alter robot state to '+_validMsg)
            else:
                self.outLog('receivd a error msg without valid robot:'+msg)
        else:
            self.outLog('receivd a error msg:'+msg)
        pass
    

if __name__ == '__main__':
    server=monitorServer()
    server.run()