from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from DownloadTube import YouTubeDownloader

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(200,200,500,500)
        self.setWindowTitle('DownloadTube')
        self.InitUI()
        self.main = YouTubeDownloader()
        self.quality = 'low'


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
        verdict = ""
        verdict, video_updated_title,video_file_name,audio_file_name = self.main.Main(type,link,self.quality)
        self.quality = 'low'
        if(verdict == True):
            self.label2.setText('Status: Download Successful')
            self.label2.adjustSize()
        elif(verdict == False):
            self.label2.setText('Status: Download Failed')
            self.label2.adjustSize()

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
