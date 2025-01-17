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
from PyQt5.QtWidgets import QWidget,QApplication, QInputDialog, QLineEdit,QLabel,QFrame,QTextEdit,QMessageBox,QPushButton,QDialog
import sys
from monitorServer import MonitorServer
from yamlTool import Yaml_Tool
from deviceState import DeviceState,MonitorState
from PyQt5.QtGui import QPixmap
from deviceDialog import DeviceDialog
import copy


class myButton(QPushButton):
    clickedButton=pyqtSignal(str)
    def __init__(self):
        super(myButton,self).__init__()
        self.clicked.connect(self.clickedMy)
        pass

    def clickedMy(self):
        self.clickedButton.emit(self.objectName())


class GUI(QWidget):
    def __init__(self):
        super(GUI,self).__init__()
        self.getObjectNames()
        self.labelArray=[]
        self.checkboxArray=[]
        self.deviceLabelIni()

        labelFontSize=30
        labelWidth=160
        labelHeight=70
        
        self.label_33 = QtWidgets.QLabel(self)
        self.label_33.setGeometry(QtCore.QRect(300, 100, 1600, 125))
        font = QtGui.QFont()
        font.setPointSize(90)
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
        self.textEdit.setVisible(False)
        self.textEdit.setObjectName("textEdit")
        self.label_34 = QtWidgets.QLabel(self)
        self.label_34.setGeometry(QtCore.QRect(50, 70, 300, 180))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self)
        
        deviceLabel_x=50
        self.label_35.setGeometry(QtCore.QRect(deviceLabel_x, 545, labelWidth, labelHeight))
        font = QtGui.QFont()
        font.setPointSize(labelFontSize)
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setAlignment(QtCore.Qt.AlignCenter)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self)
        self.label_36.setGeometry(QtCore.QRect(deviceLabel_x, 440, labelWidth, labelHeight))
        font = QtGui.QFont()
        font.setPointSize(labelFontSize)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setAlignment(QtCore.Qt.AlignCenter)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self)
        self.label_37.setGeometry(QtCore.QRect(deviceLabel_x, 650, labelWidth, labelHeight))
        font = QtGui.QFont()
        font.setPointSize(labelFontSize)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setAlignment(QtCore.Qt.AlignCenter)
        self.label_37.setObjectName("label_37")

        self.label_38 = QtWidgets.QLabel(self)
        self.label_38.setGeometry(QtCore.QRect(deviceLabel_x, 755, labelWidth, labelHeight))
        font = QtGui.QFont()
        font.setPointSize(labelFontSize)
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
        self.setUiBg()

    def deviceLabelIni(self):
        labelWidth=180
        labelHeight=70
        label_y=230
        label_x=30
        label_x_gap=25
        label_y_gap=35
        
        objectIndex=0
        for i in range(0,40):
            _label=myButton()
            _label.setParent(self)
            self.labelArray.append(_label)
            if i%5==0:
                label_y=230
                label_x=label_x+labelWidth+label_x_gap
                _label.setText(str(int(i/5+1))+'拉')
                _label.setEnabled(False)
                _label.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:rgb(78,255,255)}"
                    "QPushButton{border:2px}"
                    "QPushButton{border-radius:20px}"
                    "QPushButton{padding:2px 4px}")
            else:
                _label.setObjectName(self.monitorDevices[objectIndex])
                objectIndex+=1
                ##_label.setStyleSheet("background-color:yellow")
               # _label.setStyleSheet("QPushButton{color:black}"
               #     "QPushButton{background-color:yellow}"
               #     "QPushButton{border:2px}"
                #    "QPushButton{border-radius:20px}"
               #     "QPushButton{padding:2px 4px}")
                _label.setText("离线")
                _label.clickedButton.connect(self.deviceButtonClicked)

            label_y=label_y+labelHeight+label_y_gap
            font = QtGui.QFont()
            font.setPointSize(30)
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
        self.label_35.setStyleSheet("QLabel{color:black}"
                                  "QLabel{background-color:rgb(78,255,255)}"
                                  "QLabel{border:2px}"
                                  "QLabel{border-radius:20px}"
                                  "QLabel{padding:2px 4px}")
        self.label_36.setText(_translate("MainWindow", "A号手"))
        self.label_36.setStyleSheet("QLabel{color:black}"
                                  "QLabel{background-color:rgb(78,255,255)}"
                                  "QLabel{border:2px}"
                                  "QLabel{border-radius:20px}"
                                  "QLabel{padding:2px 4px}")
        self.label_37.setText(_translate("MainWindow", "C号手"))
        self.label_37.setStyleSheet("QLabel{color:black}"
                                  "QLabel{background-color:rgb(78,255,255)}"
                                  "QLabel{border:2px}"
                                  "QLabel{border-radius:20px}"
                                  "QLabel{padding:2px 4px}")
        self.label_38.setText(_translate("MainWindow", "超声波"))
        self.label_38.setStyleSheet("QLabel{color:black}"
                                  "QLabel{background-color:rgb(78,255,255)}"
                                  "QLabel{border:2px}"
                                  "QLabel{border-radius:20px}"
                                  "QLabel{padding:2px 4px}")


    def addRunMessage(self,msg):
        self.textEdit.append(QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')+' : '+msg)
        pass

    def runMonitorServer(self):
        self.monitorServer=MonitorServer()
        self.monitorServer.appendRunMsg.connect(self.addRunMessage)
        self.monitorServer.updateDeviceState.connect(self.updateDeviceLabel)
        self.monitorServer.run()

    def getObjectNames(self):
        paramPath="configure.yaml"
        confirmConfigureFile=QFile(paramPath)
        if not confirmConfigureFile.exists():
            QMessageBox.critical(self,'Critical','配置文件丢失！')
            exit(0)

        yamlTool=Yaml_Tool()
        params=yamlTool.getValue(paramPath)
        self.monitorDevices=[]
        for _device in params['devices'].keys():
            self.monitorDevices.append(_device)

    def updateDeviceLabel(self,_device,_state):
        lableBgColor='gray'
        if _state==DeviceState.OFFLINE:
            lableBgColor='yellow'
            self.findChild(QPushButton,_device).setText("离线")
        elif _state==DeviceState.MONITOR:
            lableBgColor='green'
            self.findChild(QPushButton,_device).setText("监控")
        elif _state==DeviceState.STOP:
            lableBgColor='red'
            self.findChild(QPushButton,_device).setText("停止")
        # elif _state==DeviceState.CALCULATE:
        #     lableBgColor='blue'
        #     self.findChild(QPushButton,_device).setText("统计")
        elif _state==DeviceState.PAUSE:
            lableBgColor='red'
            self.findChild(QPushButton,_device).setText("中止")
        elif _state==DeviceState.OTA:
            lableBgColor='blue'
            self.findChild(QPushButton,_device).setText("OTA")
        elif _state==DeviceState.UNKNOWN_WORKMODE:
            lableBgColor='red'
            self.findChild(QPushButton,_device).setText("未知")
        elif _state==DeviceState.IDLE:
            lableBgColor='gray'
            self.findChild(QPushButton,_device).setText("空闲")
        else:
            lableBgColor='dark'

        if self.runMode==MonitorState.MONITOR_STATE:
            #self.findChild(QPushButton,_device).setStyleSheet("background-color:rgb(78,255,255)")
            self.setDeviceButtonStyle(self.findChild(QPushButton,_device),lableBgColor)
        pass
    
    def setDeviceButtonStyle(self,deviceButton,color):
        if color=="yellow":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:yellow}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{border:2px}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton{padding:2px 4px}")
        elif color=="red":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:red}"
                    "QPushButton{border:2px}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton{padding:2px 4px}")
        elif color=="gray":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:gray}"
                    "QPushButton{border:2px}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{padding:2px 4px}")
        elif color=="green":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:green}"
                    "QPushButton{border:2px}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{padding:2px 4px}")
        elif color=="blue":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:blue}"
                    "QPushButton{border:2px}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{padding:2px 4px}")
        elif color=="dark":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:dark}"
                    "QPushButton{border:2px}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton{padding:2px 4px}")
        elif color=="lightBlue":
            deviceButton.setStyleSheet("QPushButton{color:black}"
                    "QPushButton{background-color:rgb(78,155,255)}"
                    "QPushButton:hover{color:rgb(150,200,200)}"
                    "QPushButton{border:2px}"
                    "QPushButton{border-radius:0px}"
                    "QPushButton{padding:2px 4px}")
            
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

    def editButtonIni(self):
        _buttonWidth=180
        _buttonHeight=70

        self.otaButton=QPushButton(self)
        self.clearButton=QPushButton(self)
        self.confirmButton=QPushButton(self)
        self.monitorButton=QPushButton(self)
        # self.calculateButton=QPushButton(self)

        self.otaButton.clicked.connect(self.otaButtonClicked)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        self.confirmButton.clicked.connect(self.confirmButtonClicked)
        self.monitorButton.clicked.connect(self.monitorButtonClicked)
        # self.calculateButton.clicked.connect(self.calculateButtonClicked)

        self.otaButton.setText("OTA")
        self.clearButton.setText("CLEAR")
        self.confirmButton.setText("CONFIRM")
        self.monitorButton.setText("MONITOR")
        # self.calculateButton.setText("CALCULATE")

        buttonY=930
        buttonX=520
        # self.calculateButton.setGeometry(buttonX-200,buttonY,_buttonWidth,_buttonHeight)
        self.otaButton.setGeometry(buttonX,buttonY,_buttonWidth,_buttonHeight)
        buttonX+=220
        self.monitorButton.setGeometry(buttonX,buttonY,_buttonWidth,_buttonHeight)
        buttonX+=220
        self.clearButton.setGeometry(buttonX,buttonY,_buttonWidth,_buttonHeight)
        buttonX+=220
        self.confirmButton.setGeometry(buttonX,buttonY,_buttonWidth,_buttonHeight)
        _buttons=[]
        _buttons.append(self.otaButton)
        _buttons.append(self.monitorButton)
        _buttons.append(self.clearButton)
        _buttons.append(self.confirmButton)
        # _buttons.append(self.calculateButton)
        self.setbuttonStyleSheet(_buttons)

    def showDeviceDialog(self,_device):
        _deviceDialog=DeviceDialog(self)
        _deviceDialog.setDevice(_device)
        self.state=DeviceState.OFFLINE
        _deviceDialog.dataIni(
            self.monitorServer.devices[_device].deviceSerial,\
            # self.monitorServer.devices[_device].name,\
            self.monitorServer.devices[_device].productModel,\
            self.monitorServer.devices[_device].productNum,\
            self.monitorServer.devices[_device].state,\
            self.monitorServer.devices[_device].macAddress,\
            self.monitorServer.devices[_device].ip,\
            self.monitorServer.devices[_device].firmWareVersion)
        _deviceDialog.show()
        pass

    def deviceButtonClicked(self,_device):
        if self.runMode==MonitorState.MONITOR_STATE:
            self.showDeviceDialog(_device)
            return

        if _device in self.choosingOtaList and self.runMode==MonitorState.CHOOSING_OTA_STATE:
            self.choosingOtaList.remove(_device)
            self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'gray')
            return
        # if _device in self.choosingCalculateList and self.runMode==MonitorState.CHOOSING_CALCULATE_STATE:
        #     self.choosingCalculateList.remove(_device)
        #     self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'gray')
        #     return
        if _device in self.choosingMonitorList and self.runMode==MonitorState.CHOOSING_MONITOR_STATE:
            self.choosingMonitorList.remove(_device)
            self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'gray')
            return
            
        if self.runMode==MonitorState.CHOOSING_OTA_STATE:
            self.choosingOtaList.append(_device)
        elif self.runMode==MonitorState.CHOOSING_MONITOR_STATE:
            self.choosingMonitorList.append(_device)
        # elif self.runMode==MonitorState.CHOOSING_CALCULATE_STATE:
        #     self.choosingCalculateList.append(_device)
        self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'lightBlue')
        pass

    def setbuttonStyleSheet(self,_buttons):
        for _button in _buttons:
            font = QtGui.QFont()
            font.setPointSize(25)
            font.setBold(True)
            font.setWeight(87)
            _button.setFont(font)
            _button.setStyleSheet("QPushButton{color:black}"
                                  "QPushButton:hover{color:rgb(150,200,200)}"
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
            self.monitorServer.setDeviceToMonitorState(self.choosingMonitorList)
            self.choosingMonitorList.clear()
            pass
        elif self.runMode==MonitorState.CHOOSING_OTA_STATE:
            print(self.choosingOtaList)
            self.monitorServer.setDeviceToOtaState(self.choosingOtaList)
            self.choosingOtaList.clear()
            pass
        # elif self.runMode==MonitorState.CHOOSING_CALCULATE_STATE:
        #     print(self.choosingCalculateList)
        #     self.monitorServer.setDeviceToMonitorState(self.choosingCalculateList)
        #     self.choosingCalculateList.clear()
        self.runMode=MonitorState.MONITOR_STATE
        self.updateAllDeviceLabel()
        pass

    def clearButtonClicked(self):
        print('clear button clicked')
        self.runMode=MonitorState.MONITOR_STATE
        self.updateAllDeviceLabel()
        pass

    def otaButtonClicked(self):
        print('ota button clicked')
        self.choosingOtaList=copy.deepcopy(self.monitorServer.getOtaDevice())
        self.runMode=MonitorState.CHOOSING_OTA_STATE
        for _device in self.monitorServer.devices.keys():
            if _device not in self.choosingOtaList:
                self.findChild(QPushButton,_device).setStyleSheet('background:gray')
            else:
                self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'lightBlue')
        pass

    def monitorButtonClicked(self):
        print('monitor button clicked')
        self.choosingMonitorList=copy.deepcopy(self.monitorServer.getMonitoringDevice())
        self.runMode=MonitorState.CHOOSING_MONITOR_STATE
        for _device in self.monitorServer.devices.keys():
            if _device not in self.choosingMonitorList:
                self.findChild(QPushButton,_device).setStyleSheet('background:gray')
            else:
                self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'lightBlue')
        pass

    # def calculateButtonClicked(self):
    #     self.choosingCalculateList=copy.deepcopy(self.monitorServer.getCalculatingDevice())
    #     self.runMode=MonitorState.CHOOSING_CALCULATE_STATE
    #     for _device in self.monitorServer.devices.keys():
    #         if _device not in self.choosingCalculateList:
    #             self.findChild(QPushButton,_device).setStyleSheet('background:gray')
    #         else:
    #             self.setDeviceButtonStyle(self.findChild(QPushButton,_device),'lightBlue')

    def updateAllDeviceLabel(self):
        for _device in self.monitorDevices:
            self.updateDeviceLabel(_device,self.monitorServer.devices[_device].state)

    def setUiBg(self):
        window_pale = QtGui.QPalette() 
        window_pale.setBrush(self.backgroundRole(),   QtGui.QBrush(QtGui.QPixmap("timg.jpg"))) 
        self.setPalette(window_pale)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    runGui=GUI()
    runGui.showFullScreen()
    #runGui.show()
    sys.exit(app.exec_())
