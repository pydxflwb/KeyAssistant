import datetime
import src.Functions.get_curricular_data as data
import src.Functions.zoom_signin as zoom
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, json
import webbrowser


class OneKeyWidget(QWidget):
    def __init__(self, file, timefile, pic_dir):
        super(OneKeyWidget, self).__init__()
        self.initUI(file, timefile, pic_dir)

    def initUI(self, file, timefile, pic_dir):
        self.setWindowTitle("OneKeyWindow")
        self.setWindowIcon(QIcon("../settings/key.png"))
        self.Layout = QVBoxLayout()
        self.oneLayout = QHBoxLayout()
        self.OnekeyButton = QPushButton("一键上课")
        self.timelabel1 = QLabel('')
        self.timelabel2 = QLabel('')
        self.timelabel1.setFont(QFont('FangSong', 16, 63))
        self.timelabel2.setFont(QFont('FangSong', 12))
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.showtime)
        self.timer1.start(1000)     # per second
        self.oneLayout.addWidget(self.timelabel1)
        self.oneLayout.addWidget(self.timelabel2)
        self.timeline = QWidget()
        self.timeline.setLayout(self.oneLayout)

        self.zoombutton = QPushButton("一键上课")
        self.zoombutton.setFont(QFont('YouYuan',20, 75))
        self.zoombutton.clicked.connect(self.connectToZoom)

        self.currilabel = QLabel('')
        self.currilabel.setFont(QFont('FangSong', 16))
        self.file = file
        self.timefile = timefile
        self.picdir = pic_dir
        self.currishow()
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.currishow)
        self.timer2.start(30000)    # per 30 seconds

        self.Layout.addWidget(self.timeline)
        self.Layout.addWidget(self.zoombutton)
        self.Layout.addWidget(self.currilabel)
        self.setLayout(self.Layout)

    def showtime(self):
        self.nowtime = datetime.datetime.now().strftime('%H:%M:%S %A ')
        self.nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
        self.timelabel1.setText(self.nowtime)
        self.timelabel2.setText(self.nowdate)

    def currishow(self):
        self.nowhour = datetime.datetime.now().hour
        self.nowmin = datetime.datetime.now().minute
        self.nowweekday = datetime.datetime.now().isoweekday()
        self.returndata = zoom.showcurri_now(self.file, self.timefile, self.nowweekday, [self.nowhour, self.nowmin])
        self.returndata = self.returndata[0]
        if self.returndata == '':
            self.returndata = "暂时无课"

        self.currilabel.setText(self.returndata)

    def connectToZoom(self):
        self.connect_flag = zoom.signin_nowtime(self.picdir, self.file, self.timefile, self.nowweekday, [self.nowhour, self.nowmin])
        self.judgeConnect()

    def judgeConnect(self):
        if self.connect_flag == 0:
            QMessageBox.infomation(self, "No Currilum Now!", "现在没有要上的课哦！", QMessageBox.Yes)
        elif self.connect_flag == 1:
            Reply = QMessageBox.information(self, "Connected", "已连接，点击Yes自动关闭程序",
                                        QMessageBox.Yes| QMessageBox.No, QMessageBox.No)
            if Reply == QMessageBox.Yes:
                self.close()
        elif self.connect_flag == -1:
            QMessageBox.warning(self, "Error: Timeout or Occupied!", "连接失败，可能原因是:\n1.网络连接时间过长，请在Z"
                                                                     "oom启动后重新点击连接\n2.当前Zoom已经打开了一个"
                                                                     "会议", QMessageBox.Yes)
        else:
            reply = QMessageBox.critical(self, "Error Occured", "发生了一个未知错误！请重启程序\n发现问题？联系开发者\n"
                                                       "肖 鹏宇\tpydxflwb@sjtu.edu.cn\n"
                                                       "或在github.com/pydxflwb/KeyAssistant上提交issue"
                                                                "\n点击Help去提交issue并关闭程序",
                                 QMessageBox.Yes|QMessageBox.Help)
            if reply == QMessageBox.Yes:
                self.close()
            else:
                webbrowser.open('github.com/pydxflwb/KeyAssistant/issues')
                self.close()


if __name__ == "__main__":
    setting_file = "../settings/setting.json"
    try:
        with open(setting_file, 'r') as f:
            datastring = json.load(f)
    except FileNotFoundError:
        datastring = {"currifile": '../settings/curricular.json', "timefile": '../settings/time_setting.json',
                      "pic_dir": '../settings/1.png', 'kbcx_url': 'http://kbcx.sjtu.edu.cn/jaccountlogin',
                      'sjtu_captcha_url': "https://jaccount.sjtu.edu.cn/jaccount/captcha",
                      'url1': "http://kbcx.sjtu.edu.cn/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default",
                      'sjtu_excepted_url': "http://kbcx.sjtu.edu.cn/xtgl/index_initMenu.html"
                      }
        with open(setting_file, 'w') as f:
            f.write(json.dumps(datastring))
        f.close()

    app = QApplication(sys.argv)
    file1 = datastring['currifile']
    file2 = datastring['timefile']
    pic_dir = datastring['pic_dir']
    one = OneKeyWidget(file1, file2, pic_dir)
    one.show()
    sys.exit(app.exec_())
