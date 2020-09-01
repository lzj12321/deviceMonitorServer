from playsound import playsound
from PyQt5.Qt import QApplication, QWidget, QPushButton, QThread
from PyQt5.QtCore import pyqtSignal

class SoundPlayerThread(QThread):
    playEnd=pyqtSignal(str)
    def __init__(self,_device):
        super().__init__()
        self.alarmDevice=_device

    def run(self):
        print("play "+self.alarmDevice+" alarm sound!")
        playsound("test.wav")
        self.playEnd.emit(self.alarmDevice)
        # print("alarm sound end!")
        pass