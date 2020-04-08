from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor, QFont
import sys, time
from PyQt5.QtWidgets import *
from src.GUI import InfoRequestWidget, CentralWidget
import src.Functions.get_curricular_data as data

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("KeyAssitant")
        self.setWindowIcon(QIcon(""))

        # InfoRequest
        self.infoReq = InfoRequestWidget.InfoRequestWidget()
        self.infoReq.signal_returnText.connect(self.getInputData)
        self.CentralWidget = CentralWidget.CentralWidget()
        self.setCentralWidget(self.CentralWidget)
        self.OneKeyDock

    def getInputData(self, ilist):
        print(ilist)

    def insertCurri(self, file1, file2):
        curri = data.change_DataStyle_List(file1, file2)
        self.CentralWidget.insertCurri(curri)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    file1 = '../settings/curricular.json'
    file2 = '../settings/time_setting.json'
    win.insertCurri(file1,file2)
    win.setGeometry(300, 100, 750, 450)
    win.show()
    sys.exit(app.exec_())