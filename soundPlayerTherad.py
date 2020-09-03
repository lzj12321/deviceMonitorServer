# coding=utf-8

from pydub import AudioSegment
from pydub.playback import play
import PyQt5
from PyQt5.Qt import QApplication, QWidget, QPushButton, QThread
import time
import sys

class SoundPlayerThread(QThread):
    playEnd=pyqtSignal(str)
    def __init__(self,_device):
        super().__init__()
        self.alarmDevice=_device

    def run(self):
        _alarmSoundPath="./alarmSound/"+self.alarmDevice+".wav"
        sound = AudioSegment.from_file(_alarmSoundPath)
        play(sound) 
        time.sleep(1)
        self.playEnd.emit(self.alarmDevice)
        pass


if __name__=="__main__":
    print("fuck")
    test=SoundPlayerThread('test')
    test.start()