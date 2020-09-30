import PyQt5
from PyQt5.Qt import QApplication, QWidget, QPushButton, QThread
from PyQt5.QtCore import pyqtSignal
from pydub import AudioSegment
from pydub.playback import play
import sys
import time


class SoundPlayerThread(QThread):
    playEnd=pyqtSignal(str)
    def __init__(self,_device,_playTime=1):
        super().__init__()
        self.alarmDevice=_device
        self.playTime=_playTime

    def run(self):
        _alarmsoundPath="./alarmSound/"+self.alarmDevice+".wav"
        sound = AudioSegment.from_file(_alarmsoundPath)
        while self.playTime>0:
            play(sound)
            time.sleep(1)
            self.playTime-=1

        self.playEnd.emit(self.alarmDevice)
        pass

if __name__=="__main__":
    test=SoundPlayerThread("xe_line3_robot3",3)
    test.start()
    print("test")
