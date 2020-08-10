# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget,QApplication, QInputDialog, QLineEdit,QLabel,QFrame,QTextEdit,QMessageBox,QPushButton
import sys
from monitorServer import MonitorServer
from yamlTool import Yaml_Tool
from robotState import RobotState,MonitorState
from PyQt5.QtGui import QPixmap
import copy


class myButton(QPushButton):
    clickedButton=pyqtSignal(str)
    def __init__(self):
        super(myButton,self).__init__()
        self.clicked.connect(self.clickedMy)
        pass

    def clickedMy(self):
        # self.clickedButton.emit('test')
        self.clickedButton.emit(self.objectName())


class GUI(QWidget):
    test123=pyqtSignal(str)
    def __init__(self):
        super(GUI,self).__init__()
        self.getObjectNames()
        self.labelArray=[]
        self.checkboxArray=[]
        self.deviceLabelIni()
        
        self.label_33 = QtWidgets.QLabel(self)
        self.label_33.setGeometry(QtCore.QRect(300, 10, 701, 101))
        font = QtGui.QFont()
        font.setPointSize(45)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setStyleSheet("color: rgb(0, 85, 255);")
        self.label_33.setAlignment(QtCore.Qt.AlignCenter)
        self.label_33.setObjectName("label_33")
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(330, 460, 750, 250))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        # self.textEdit.setVisible(False)
        self.textEdit.setObjectName("textEdit")
        self.label_34 = QtWidgets.QLabel(self)
        self.label_34.setGeometry(QtCore.QRect(30, 10, 200, 120))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self)
        self.label_35.setGeometry(QtCore.QRect(50, 265, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setAlignment(QtCore.Qt.AlignCenter)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self)
        self.label_36.setGeometry(QtCore.QRect(50, 205, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setAlignment(QtCore.Qt.AlignCenter)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self)
        self.label_37.setGeometry(QtCore.QRect(50, 325, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setAlignment(QtCore.Qt.AlignCenter)
        self.label_37.setObjectName("label_37")

        self.label_38 = QtWidgets.QLabel(self)
        self.label_38.setGeometry(QtCore.QRect(50, 385, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setAlignment(QtCore.Qt.AlignCenter)
        self.label_38.setObjectName("label_37")


        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.logoIni()
        self.dataIni()
        self.editButtonIni()
        self.runMonitorServer()
        self.updateAllDeviceLabel()

    def deviceLabelIni(self):
        labelWidth=100
        labelHeight=40
        label_y=80
        label_x=50
        
        objectIndex=0
        for i in range(0,40):
            _label=myButton()
            _label.setParent(self)
            self.labelArray.append(_label)
            if i%5==0:
                label_y=80
                label_x=label_x+labelWidth+20
                _label.setText(str(int(i/5+1))+'拉')
                _label.setEnabled(False)
                _label.setStyleSheet("background-color:rgb(78,255,255)")
            else:
                _label.setObjectName(self.monitorDevices[objectIndex])
                objectIndex+=1
                _label.setStyleSheet("background-color:gray")
                _label.setText("离线")
                _label.clickedButton.connect(self.deviceButtonClicked)

            label_y=label_y+labelHeight+20
            font = QtGui.QFont()
            font.setPointSize(17)
            font.setBold(True)
            font.setWeight(75)
            _label.setFont(font)
            _label.setGeometry(label_x,label_y,labelWidth,labelHeight)
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_33.setText(_translate("MainWindow", "新厂E车间终测机械手状态"))
        self.label_34.setText(_translate("MainWindow", "pi icon"))
        self.label_35.setText(_translate("MainWindow", "B号手"))
        self.label_36.setText(_translate("MainWindow", "A号手"))
        self.label_37.setText(_translate("MainWindow", "C号手"))
        self.label_38.setText(_translate("MainWindow", "超声波"))

    def alterRobotState(self,robotNumber,state):
        pass

    def addRunMessage(self,msg):
        self.textEdit.append(QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')+' : '+msg)
        pass

    def runMonitorServer(self):
        self.monitorServer=MonitorServer()
        self.monitorServer.appendRunMsg.connect(self.addRunMessage)
        self.monitorServer.updateRobotState.connect(self.updateRobotLabel)
        self.monitorServer.monitoringRobot=self.monitorDevices
        self.monitorServer.run()

    def getObjectNames(self):
        paramPath="configure.yaml"
        confirmConfigureFile=QFile(paramPath)
        if not confirmConfigureFile.exists():
            QMessageBox.critical(self,'Critical','配置文件丢失！')
            exit(0)

        yamlTool=Yaml_Tool()
        params=yamlTool.getValue(paramPath)
        self.monitorDevices=params['robot'].split(',')

    def updateRobotLabel(self,_robot):
        lableBgColor='background:gray'
        if self.monitorServer.robotState[_robot]==RobotState.OFFLINE:
            lableBgColor='background:yellow'
            self.findChild(QPushButton,_robot).setText("离线")
        elif self.monitorServer.robotState[_robot]==RobotState.ONLINE:
            lableBgColor='background:green'
            self.findChild(QPushButton,_robot).setText("正常")
        elif self.monitorServer.robotState[_robot]==RobotState.STOP:
            lableBgColor='background:red'
            self.findChild(QPushButton,_robot).setText("停止")
        elif self.monitorServer.robotState[_robot]==RobotState.PAUSE:
            lableBgColor='background:red'
            self.findChild(QPushButton,_robot).setText("中止")
        elif self.monitorServer.robotState[_robot]==RobotState.OTA:
            lableBgColor='background:blue'
            self.findChild(QPushButton,_robot).setText("OTA")

        if self.runMode==MonitorState.MONITOR_STATE:
            self.findChild(QPushButton,_robot).setStyleSheet(lableBgColor)

        if _robot not in self.monitorServer.monitoringRobot and _robot not in self.monitorServer.otaStateRobots:
            self.findChild(QPushButton,_robot).setStyleSheet("background-color:gray")
        pass

    def logoIni(self):
        print('logoIni')
        self.logPixMap=QPixmap('PI_LOGO.png')
        self.fitPixMap=self.logPixMap.scaled(self.label_34.width(),
                                             self.label_34.height(),
                                             Qt.IgnoreAspectRatio,
                                             Qt.SmoothTransformation)
        self.label_34.setPixmap(self.fitPixMap)
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        choose = QMessageBox.question(self, 'Question', '确认关闭程序？', QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if choose == QMessageBox.No:
            a0.ignore()

    def changeLabelStylesheet(self,_label,_text,_flag):
        _label.setText(_text)
        pass

    def editButtonIni(self):
        _buttonWidth=100
        _buttonHeight=50

        self.otaButton=QPushButton(self)
        self.clearButton=QPushButton(self)
        self.confirmButton=QPushButton(self)
        self.monitorButton=QPushButton(self)


        self.otaButton.clicked.connect(self.otaButtonClicked)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        self.confirmButton.clicked.connect(self.confirmButtonClicked)
        self.monitorButton.clicked.connect(self.monitorButtonClicked)

        self.otaButton.setText("OTA")
        self.clearButton.setText("CLEAR")
        self.confirmButton.setText("CONFIRM")
        self.monitorButton.setText("MONITOR")

        self.otaButton.setGeometry(50,500,_buttonWidth,_buttonHeight)
        self.monitorButton.setGeometry(200,500,_buttonWidth,_buttonHeight)
        self.clearButton.setGeometry(50,600,_buttonWidth,_buttonHeight)
        self.confirmButton.setGeometry(200,600,_buttonWidth,_buttonHeight)
        _buttons=[]
        _buttons.append(self.otaButton)
        _buttons.append(self.monitorButton)
        _buttons.append(self.clearButton)
        _buttons.append(self.confirmButton)
        self.setbuttonStyleSheet(_buttons)
    
    def deviceButtonClicked(self,_device):
        # print(_str+' clicked')
        if self.runMode==MonitorState.MONITOR_STATE:
            return

        if _device in self.choosingOtaList and self.runMode==MonitorState.CHOOSING_OTA_STATE:
            self.choosingOtaList.remove(_device)
            print('remove ota '+_device)
            self.findChild(QPushButton,_device).setStyleSheet('background-color:gray') 
            return
        if _device in self.choosingMonitorList and self.runMode==MonitorState.CHOOSING_MONITOR_STATE:
            self.choosingMonitorList.remove(_device)
            print('remove monitor '+_device)
            self.findChild(QPushButton,_device).setStyleSheet('background-color:gray')
            return
            
        if self.runMode==MonitorState.CHOOSING_OTA_STATE:
            self.choosingOtaList.append(_device)
            print('add ota '+_device)
        elif self.runMode==MonitorState.CHOOSING_MONITOR_STATE:
            self.choosingMonitorList.append(_device)
            print('add monitor '+_device)
        self.findChild(QPushButton,_device).setStyleSheet('background-color:rgb(78,155,255)')
        pass

    def setbuttonStyleSheet(self,_buttons):
        for _button in _buttons:
            font = QtGui.QFont()
            font.setPointSize(15)
            font.setBold(True)
            font.setWeight(75)
            _button.setFont(font)
            _button.setStyleSheet("QPushButton{color:black}"
                                  "QPushButton:hover{color:red}"
                                  "QPushButton{background-color:rgb(78,255,255)}"
                                  "QPushButton{border:2px}"
                                  "QPushButton{border-radius:10px}"
                                  "QPushButton{padding:2px 4px}")
    def dataIni(self):
        self.runMode=MonitorState.MONITOR_STATE
        self.choosingOtaList=[]
        self.choosingMonitorList=[]

    def confirmButtonClicked(self):
        print('confirm button clicked')
        if self.runMode==MonitorState.MONITOR_STATE:
            return
        elif self.runMode==MonitorState.CHOOSING_MONITOR_STATE:
            print(self.choosingMonitorList)
            self.monitorServer.setRobotToMonitorState(self.choosingMonitorList)
            self.choosingMonitorList.clear()
            pass
        elif self.runMode==MonitorState.CHOOSING_OTA_STATE:
            print(self.choosingOtaList)
            self.monitorServer.setRobotToOtaState(self.choosingOtaList)
            self.choosingOtaList.clear()
            pass
        self.runMode=MonitorState.MONITOR_STATE
        self.updateAllDeviceLabel()
        pass

    def clearButtonClicked(self):
        print('clear button clicked')
        self.runMode=MonitorState.MONITOR_STATE
        self.choosingMonitorList=copy.deepcopy(self.monitorServer.monitoringRobot)
        self.choosingOtaList=copy.deepcopy(self.monitorServer.otaStateRobots)
        self.updateAllDeviceLabel()
        pass

    def otaButtonClicked(self):
        print('ota button clicked')
        self.choosingMonitorList=copy.deepcopy(self.monitorServer.monitoringRobot)
        self.choosingOtaList=copy.deepcopy(self.monitorServer.otaStateRobots)
        # self.choosingOtaList.clear()
        # self.choosingMonitorList.clear()
        self.runMode=MonitorState.CHOOSING_OTA_STATE
        for _robot in self.monitorServer.robotState.keys():
            if _robot not in self.choosingOtaList:
                self.findChild(QPushButton,_robot).setStyleSheet('background:gray')
            else:
                self.findChild(QPushButton,_robot).setStyleSheet('background-color:rgb(78,155,255)')
        pass

    def monitorButtonClicked(self):
        print('monitor button clicked')
        self.choosingMonitorList=copy.deepcopy(self.monitorServer.monitoringRobot)
        self.choosingOtaList=copy.deepcopy(self.monitorServer.otaStateRobots)
        # self.choosingOtaList.clear()
        # self.choosingMonitorList.clear()
        self.runMode=MonitorState.CHOOSING_MONITOR_STATE
        for _robot in self.monitorServer.robotState.keys():
            if _robot not in self.choosingMonitorList:
                self.findChild(QPushButton,_robot).setStyleSheet('background:gray')
            else:
                self.findChild(QPushButton,_robot).setStyleSheet('background-color:rgb(78,155,255)')

        pass

    def updateAllDeviceLabel(self):
        for _robot in self.monitorServer.robotState.keys():
            self.updateRobotLabel(_robot)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    runGui=GUI()
    runGui.show()
    sys.exit(app.exec_())
