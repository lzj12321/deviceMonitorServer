from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class DeviceDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceDialog, self).__init__(parent)

        self.resize(759, 434)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(280, 20, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(50, 130, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 180, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(50, 230, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(50, 280, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(400, 280, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(400, 130, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(400, 180, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(400, 230, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(170, 129, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 180, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(170, 230, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(170, 280, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(510, 280, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self)
        self.lineEdit_6.setGeometry(QtCore.QRect(510, 130, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self)
        self.lineEdit_7.setGeometry(QtCore.QRect(510, 180, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self)
        self.lineEdit_8.setGeometry(QtCore.QRect(510, 230, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.label.setText("设备信息")
        self.label_2.setText("设备序列号")
        self.label_3.setText("设备名称")
        self.label_4.setText("生产型号")
        self.label_5.setText("生产数量")
        self.label_6.setText("工作模式")
        self.label_7.setText("MAC地址")
        self.label_8.setText("IP地址")
        self.label_9.setText("固件版本")



        self.setWindowTitle('debug')
        self.pushbutton=QPushButton(self)
        self.pushbutton.setVisible(True)
        self.pushbutton.setGeometry(50,20,100,100)
        self.pushbutton.setText('test')
        self.pushbutton.setVisible(False)


        self.pushbutton.clicked.connect(self.test)
    
    def setDevice(self,_name):
        self._name=_name
        self.setWindowTitle(_name)

    def dataIni(self,_serial,_model,_num,_state,_mac,_ip,_version):
        _nullData="null"
        self.deviceSerial=_serial
        # self.deviceName=_name
        self.productModel=_model
        self.productNum=_num
        self.state=_state
        self.macAddress=_mac
        self.ip=_ip
        self.firmWareVersion=_version

        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText(self.deviceSerial)

        # self.lineEdit_2.setReadOnly(True)
        # self.lineEdit_2.setText(self.deviceName)

        self.lineEdit_3.setText(self.productModel)

        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setText(str(self.productNum))

        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_5.setText(str(self.state))

        self.lineEdit_6.setReadOnly(True)
        self.lineEdit_6.setText(self.macAddress)

        self.lineEdit_7.setReadOnly(True)
        if self.ip!="":
            self.lineEdit_7.setText(self.ip)
        else:
            self.lineEdit_7.setText(_nullData)

        self.lineEdit_8.setReadOnly(True)
        self.lineEdit_8.setText(str(self.firmWareVersion))

        pass

    def uiIni(self):
        pass

    def test(self):
        self.testSignal.emit(self._name)
        # print(self._name)

