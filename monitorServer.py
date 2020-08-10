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
        self.robotState={}
        self.onlineRobotIp={}
        self.ipSocket={}
        self.workshop=self.params['workshop']
        self._robots=self.params['robot'].split(',')
        for _robot in self._robots:
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

    def processMsgFromRobot(self,msg,sockIp):
        print('msg:'+msg)
        # self.outLog(msg)
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

            _robotState=RobotState.ONLINE
            if _robotFlag in self.robotOnlineCheckFlag.keys():
                self.robotOnlineCheckFlag[_robotFlag]=True
                if _validMsg=='check':
                    _robotState=RobotState.ONLINE
                elif _validMsg=='stop':
                    _robotState=RobotState.STOP
                elif _validMsg=='pause':
                    _robotState=RobotState.PAUSE
                elif _validMsg=='anfang':
                    _robotState=RobotState.ANFANG
                elif _validMsg=='catchError':
                    _robotState=RobotState.CATCH_ERROR
                elif _validMsg=='hipot':
                    _robotState=RobotState.HIPOT
                if self.robotState[_robotFlag]!=_robotState:
                    self.saveRobotStateChangeLog(_robotFlag,_validMsg)
                    self.robotState[_robotFlag]=_robotState
                    self.updateRobotState.emit(_robotFlag)
                    self.addRunMessage(_robotFlag+':'+_validMsg)
                    self.outLog(_robotFlag+' alter robot state to '+_validMsg)
            else:
                self.outLog('receivd a error msg:'+msg)
        else:
            self.outLog('receivd a error msg:'+msg)
        pass

if __name__ == '__main__':
    server=monitorServer()
    server.run()