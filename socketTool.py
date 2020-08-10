from PyQt5 import QtNetwork
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from  PyQt5.QtNetwork import QTcpSocket

class Socket(QObject):
    receivedMsg=pyqtSignal(str,str)
    # disconnectedServer=pyqtSignal(str)

    def __init__(self):
        super(Socket,self).__init__()
        pass

    def setSocket(self,sock):
        self.sock=sock
        self.sockIp= sock.peerAddress().toString().split(':')[-1]
        # self.sock.disconnected.connect(self.disconnectedFromServer)
        self.sock.readyRead.connect(self.readMsg)

    def setDescriptor(self,descriptor):
        self.descriptor=descriptor

    def readMsg(self):
        # print('read msg111111111')
        msg=str(self.sock.readLine(),encoding='utf-8')
        self.receivedMsg.emit(msg,self.sockIp)
        return msg

    def sendMsg(self,msg):
        msg+='\n'
        self.sock.write(msg.encode('utf-8'))

    def disconnectedFromServer(self):
        self.close()
        # self.disconnectedServer.emit(self.descriptor)
        pass

    def close(self):
        self.sock.close()



