# coding=utf-8

import pygame
# from playsound import playsound
# from pydub import AudioSegment
# from pydub.playback import play
import PyQt5
from PyQt5.Qt import QApplication, QWidget, QPushButton, QThread
from PyQt5.QtCore import pyqtSignal,QUrl
from PyQt5 import QtMultimedia
import time

class SoundPlayerThread(QThread):
    playEnd=pyqtSignal(str)
    def __init__(self,_device):
        super().__init__()
        self.alarmDevice=_device

    def run(self):

        # sound_file = 'xe_line1_robot1.wav'
        sound_file = './alarmSound/test.mp3'


        pygame.mixer.init()
        pygame.mixer.music.load(sound_file) 
        pygame.mixer.music.set_volume(0.5) 
        pygame.mixer.music.play()


        # sound = AudioSegment.from_file(sound_file, format="wav")
        # play(sound) 


        # sound_file = 'test.mp3'

        # sound = PyQt5.QtMultimedia.QSoundEffect()
        # sound.setSource(PyQt5.QtCore.QUrl.fromLocalFile(sound_file))
        # sound.setLoopCount(PyQt5.QtMultimedia.QSoundEffect.Infinite)
        # sound.setVolume(100)
        # sound.play()
        
        # url = PyQt5.QtCore.QUrl.fromLocalFile(sound_file)
        # self.content = PyQt5.QtMultimedia.QMediaContent(url)
        # self.player = PyQt5.QtMultimedia.QMediaPlayer()
        # self.player.setMedia(self.content)
        # print(self.player.isMetaDataAvailable())
        # self.player.setMuted(False)
        # self.player.setVolume(50.0)
        # self.player.play()
        # time.sleep(2)
        # time.sleep(30)


        # _alarmSoundPath="./alarmSound/"+self.alarmDevice+".wav"
        # print("alarm sound path:"+_alarmSoundPath)
        # playsound(_alarmSoundPath)

        self.playEnd.emit(self.alarmDevice)
        pass


if __name__=="__main__":
    print("fuck")
    test=SoundPlayerThread('test')
    test.start()