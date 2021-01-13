from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from DownloadTube import YouTubeDownloader
import threading
import time


thread_track={}

def DownloadTubeCallThreadFunction(type,link,quality,my_window_object):
    try:
        verdict, video_updated_title,video_file_name,audio_file_name = my_window_object.main.Main(type,link,quality)
        if(verdict == True):
            my_window_object.label2.setText('Status: Download Successful')
            my_window_object.label2.adjustSize()
        elif(verdict == False):
            my_window_object.label2.setText('Status: Download Failed')
            my_window_object.label2.adjustSize()
    except Exception as e:
        print(e)
        my_window_object.label2.setText('Status: Error Occurred')
        my_window_object.label2.adjustSize()
    global thread_track
    thread_track.clear()

class MyThread (threading.Thread):
   def __init__(self, threadID,type,link,quality,my_window_object):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.type = type
      self.link = link
      self.quality = quality
      self.my_window_object = my_window_object

      global thread_track

   def run(self):
      print ("Starting ",self.threadID)
      DownloadTubeCallThreadFunction(self.type,self.link,self.quality,self.my_window_object)
      print ("Exiting ", self.threadID)


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(200,200,500,500)
        self.setWindowTitle('DownloadTube')
        self.InitUI()
        self.main = YouTubeDownloader()
        self.quality = 'low'
        self.thread_count = 0


    def InitUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('URL: ')
        self.label.move(20,10)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Audio')
        self.b1.clicked.connect(lambda : self.clickType('audio'))
        self.b1.move(20,100)


        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText('Video')
        self.b2.clicked.connect(lambda : self.clickType('video'))
        self.b2.move(120,100)

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(50, 10)
        self.textbox.resize(400,30)

        self.low = QtWidgets.QPushButton(self)
        self.low.setText('Low')
        self.low.clicked.connect(lambda : self.outputQuality('low'))
        self.low.move(20,60)

        self.medium = QtWidgets.QPushButton(self)
        self.medium.setText('Medium')
        self.medium.clicked.connect(lambda : self.outputQuality('medium'))
        self.medium.move(120,60)

        self.high = QtWidgets.QPushButton(self)
        self.high.setText('High')
        self.high.clicked.connect(lambda : self.outputQuality('high'))
        self.high.move(220,60)

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText('Status: ')
        self.label2.move(20,300)

    def clickType(self,type):
        link = self.textbox.text()

        self.label2.setText('Status: Download Being Processed')
        self.label2.adjustSize()
        print("Status: Download Being Processed")


        self.thread_count = self.thread_count + 1

        thread1 = MyThread(self.thread_count,type,link,self.quality,self)
        self.quality = 'low'
        thread1.start()
        global thread_track
        thread_track[self.thread_count] = thread1
        print('active thread count = ',threading.activeCount())


    def outputQuality(self,q):
        self.quality = q

    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
for t in thread_track:
    thread_track[i].join()
