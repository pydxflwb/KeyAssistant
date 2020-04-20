# OneKey.py
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, sys, json
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
import webbrowser
import Functions.get_curricular_data as data
import Functions.zoom_signin as zoom


# OneKeyWidget Definition
class OneKeyWidget(QWidget):
    def __init__(self, file, timefile, pic_dir):
        super(OneKeyWidget, self).__init__()
        self.initUI(file, timefile, pic_dir)

    def initUI(self, file, timefile, pic_dir):
        self.setWindowTitle("OneKeyWindow")
        self.setWindowIcon(QIcon("../settings/key.png"))
    # Layouts
        self.Layout = QVBoxLayout()
        self.oneLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()

    # Top Row -- Time Labels in oneLayout
        self.timelabel1 = QLabel('')
        self.timelabel2 = QLabel('')
        self.timelabel1.setFont(QFont('FangSong', 16, 63))
        self.timelabel2.setFont(QFont('FangSong', 12))
        # Use Timer to Update Time
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.showtime)
        self.timer1.start(1000)     # per second
        self.oneLayout.addWidget(self.timelabel1)
        self.oneLayout.addWidget(self.timelabel2)
        # Layout Instantiation to be Put in a Larger Layout
        self.timeline = QWidget()
        self.timeline.setLayout(self.oneLayout)

    # A Button with A Gif Picture
        self.gifbutton1 = GIFButton("./fufufbm.gif")
        self.gifbutton1.setFixedSize(QSize(156, 156))
        self.gifbutton1.clicked.connect(self.connectToZoom)
        # A Layout is added to Provide a HCenter Location
        self.middleLayout.addWidget(self.gifbutton1)
        self.middleWidget = QWidget()
        self.middleWidget.setLayout(self.middleLayout)

    # Bottom -- A Label with Classname
        self.currilabel = QLabel('')
        self.currilabel.setFont(QFont('FangSong', 16))
        self.currilabel.setAlignment(Qt.AlignHCenter)

        self.file = file
        self.timefile = timefile
        self.picdir = pic_dir
        self.currishow()
        # Add a 30 sec Timer to Update Classname
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.currishow)
        self.timer2.start(30000)    # per 30 seconds

    # Total Layout
        self.Layout.addWidget(self.timeline)
        self.Layout.addWidget(self.middleWidget)
        self.Layout.addWidget(self.currilabel)
        self.setLayout(self.Layout)

    def showtime(self):
        # A Function to Show Nowtime
        self.nowtime = datetime.datetime.now().strftime('%H:%M:%S %A ')
        self.nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
        self.timelabel1.setText(self.nowtime)
        self.timelabel2.setText(self.nowdate)

    def currishow(self):
        # A Function to Show Nowclass
        self.nowhour = datetime.datetime.now().hour
        self.nowmin = datetime.datetime.now().minute
        self.nowweekday = datetime.datetime.now().isoweekday()

        # Functional Code
        try:
            self.returndata = zoom.showcurri_now(self.file, self.timefile, self.nowweekday, [self.nowhour, self.nowmin])
            self.returndata = self.returndata[0]
            if self.returndata == '':
                self.returndata = "暂时无课"
        except:
            self.returndata = "无课程信息，请获取"
        self.currilabel.setText(self.returndata)
        
    def connectToZoom(self):
        # Call Zoom Connetion and Display a Return Message
        self.connect_flag = zoom.signin_nowtime(self.picdir, self.file, self.timefile, self.nowweekday, [self.nowhour, self.nowmin])
        self.judgeConnect()

    def judgeConnect(self):
        # Subfunction to Deal with Return Value
        if self.connect_flag == 0:
            # 0 -- No class
            QMessageBox.information(self, "No Class Now!", "现在没有要上的课哦！", QMessageBox.Yes)
        elif self.connect_flag == 1:
            # 1 -- Connected
            Reply = QMessageBox.information(self, "Connected", "已连接，点击Yes自动关闭程序",
                                        QMessageBox.Yes| QMessageBox.No, QMessageBox.No)
            if Reply == QMessageBox.Yes:
                self.close()
        elif self.connect_flag == -1:
            # -1 -- Failed
            QMessageBox.warning(self, "Error: Timeout or Occupied!", "连接失败，可能原因是:\n1.网络连接时间过长，请在Z"
                                                                     "oom启动后重新点击连接\n2.当前Zoom已经打开了一个"
                                                                     "会议", QMessageBox.Yes)
        else:
            # Else -- Error
            reply = QMessageBox.critical(self, "Error Occured", "发生了一个未知错误！请重启程序\n发现问题？联系开发者\n"
                                                       "肖 鹏宇\tpydxflwb@sjtu.edu.cn\n"
                                                       "或在github.com/pydxflwb/KeyAssistant上提交issue"
                                                                "\n点击Help去提交issue并关闭程序",
                                 QMessageBox.Yes|QMessageBox.Help)
            if reply == QMessageBox.Yes:
                self.close()
            else:
                # To Github
                webbrowser.open('github.com/pydxflwb/KeyAssistant/issues')
                self.close()

    def fresh(self):
        # To Fresh
        self.currishow()
        

class GIFButton(QPushButton):
    # A Subclass of QPushButton
    def __init__(self, gif, ):
        super().__init__()
        # When .gif Frame Changes, Repaint Pixmap -- to Use .gif as Button
        self.movie = QMovie(gif)
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.movie.frameChanged.disconnect(self.repaint)

    def paintEvent(self, event):
        # To Repaint a Pixmap When Mouse Move in
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(0,0, self.width(), self.height(), currentFrame)

    def enterEvent(self, event):
        self.movie.frameChanged.connect(self.repaint)

    def leaveEvent(self, event):
        self.movie.frameChanged.disconnect(self.repaint)


# Test
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
