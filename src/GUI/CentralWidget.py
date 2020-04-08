from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.GUI import CurricularWidget
import sys, json
import src.Functions.get_curricular_data as data
import src.Functions.zoom_signin as zoom


class CentralWidget(QWidget):

    def __init__(self, file1, file2):
        super().__init__()
        self.initUI(file1, file2)

    def initUI(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        # Layout
        self.Layout = QVBoxLayout()
        self.CurriWidget = CurricularWidget.CurricularWidget1()
        self.Layout.addWidget(self.CurriWidget)
        self.DetailWidget = DetailCurriWidget(file1, file2)
        self.Layout.addWidget(self.DetailWidget)
        self.setLayout(self.Layout)
        self.Signal_showdetail = self.CurriWidget.signal_TableRow
        self.Signal_showdetail.connect(self.showCurriDetail)

        self.insertCurri(file1, file2)
        self.Signal_timeedit= self.DetailWidget.signal_EditTime
        self.Signal_timeedit.connect(self.refresh)

    def insertCurri(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.curri = data.change_DataStyle_List(file1, file2)
        self.CurriWidget.insertCurri(self.curri)

    def showCurriDetail(self, row):
        self.DetailWidget.freshDetail(row, self.file1, self.file2)

    def refresh(self, row):
        self.CurriWidget.clear()
        self.insertCurri(self.file1, self.file2)
        self.showCurriDetail(row)


class DetailCurriWidget(QWidget):
    signal_EditTime = pyqtSignal(int)

    def __init__(self, file1, file2):
        super(DetailCurriWidget, self).__init__()
        self.initUI(file1, file2)

    def initUI(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.Layout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.title = QLabel('课程详情')
        self.title.setFont(QFont('YouYuan', 12))
        self.leftLayout.addWidget(self.title)

        # Details
        self.classdata = QTextBrowser()
        self.classdata.setFont(QFont('Fang Song', 10))
        self.leftLayout.addWidget(self.classdata)

        # TimeSetting
        self.smallBlockLayout1 = QHBoxLayout()
        self.startLabel = QLabel('开始时间')
        self.startEdit = QDateTimeEdit(QTime.currentTime())
        self.smallBlockLayout1.addWidget(self.startLabel)
        self.smallBlockLayout1.addWidget(self.startEdit)
        self.smallBlock1 = QWidget()
        self.smallBlock1.setLayout(self.smallBlockLayout1)

        self.smallBlockLayout2 = QHBoxLayout()
        self.endLabel = QLabel('结束时间')
        self.endEdit = QDateTimeEdit(QTime.currentTime())
        self.smallBlockLayout2.addWidget(self.endLabel)
        self.smallBlockLayout2.addWidget(self.endEdit)
        self.smallBlock2 = QWidget()
        self.smallBlock2.setLayout(self.smallBlockLayout2)
        self.button1 = QPushButton("修改时间")
        self.button1.clicked.connect(self.change_time)

        self.rightLayout.addWidget(self.smallBlock1)
        self.rightLayout.addWidget(self.smallBlock2)
        self.rightLayout.addWidget(self.button1)

        self.leftW = QWidget()
        self.leftW.setLayout(self.leftLayout)
        self.rightW = QWidget()
        self.rightW.setLayout(self.rightLayout)
        self.Layout.addWidget(self.leftW)
        self.Layout.addWidget(self.rightW)
        self.setLayout(self.Layout)
        self.row = 0
        # self.freshDetail(0, '../Functions/curricular.json', '../Functions/time_setting.json')

    def freshDetail(self, row, filename, timefilename):
        self.row = row
        with open(filename, 'r') as f:
            raw_curri = json.load(f)
        f.close()
        with open(timefilename, 'r') as tif:
            raw_time = json.load(tif)
        tif.close()
        details = raw_curri[row]
        times = raw_time[row]
        daylist = ['一', '二', '三', '四', '五', '六', '日']
        self.detailString = details[0]+' '+details[1]+"\n"+details[2]+' 学分:'+details[5]+'\n时间:周'\
                            +daylist[int(details[3])-1]+details[4]
        self.stTime = times[2]
        self.edTime = times[3]
        self.classdata.setText(self.detailString)
        self.startEdit.setTime(QTime(int(self.stTime[0]), int(self.stTime[1]), 0))
        self.endEdit.setTime(QTime(int(self.edTime[0]), int(self.edTime[1]), 0))

    def change_time(self):
        self.editStaTime = self.startEdit.time()
        self.editEndTime = self.endEdit.time()
        self.editSta = [self.editStaTime.hour(), self.editStaTime.minute()]
        self.editEnd = [self.editEndTime.hour(), self.editEndTime.minute()]
        with open(self.file2, 'r') as tif:
            raw_time = json.load(tif)
        tif.close()
        raw_time[self.row][2] = self.editSta
        raw_time[self.row][3] = self.editEnd
        with open(self.file2, 'w') as tiif:
            tiif.write(json.dumps(raw_time))
        tiif.close()
        self.signal_EditTime.emit(self.row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file01 = '../settings/curricular.json'
    file02 = '../settings/time_setting.json'
    win = CentralWidget(file01, file02)
    win.show()
    sys.exit(app.exec_())