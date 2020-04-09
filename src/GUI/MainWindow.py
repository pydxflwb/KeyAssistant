from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor, QFont
import sys, os, json
from PyQt5.QtWidgets import *
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from GUI import InfoRequestWidget, CentralWidget, OneKey
import Functions.get_curricular_data as data
from selenium import webdriver


class MainWindow(QMainWindow):

    def __init__(self, file, timefile, pic_dir):
        super().__init__()

        self.initUI(file, timefile, pic_dir)

    def initUI(self, file, timefile, pic_dir):
        self.setWindowTitle("KeyAssitant")
        self.setWindowIcon(QIcon(pic_dir))
        self.file1 = file
        self.file2 = timefile
        self.pic = pic_dir

        self.CentralWidget = CentralWidget.CentralWidget(self.file1, self.file2, self.pic)
        self.fileflag = self.insertCurri(self.file1, self.file2)
        self.setCentralWidget(self.CentralWidget)
        self.Signal_connectC = self.CentralWidget.signal_ConnectCentral
        self.Signal_connectC.connect(self.judgeConnectMain)

        # Info Request
        self.infoReq = InfoRequestWidget.InfoRequestWidget()
        self.infoReq.signal_returnText.connect(self.getInputData)
        self.Dock_InfoReq = QDockWidget('课程信息访问', self)
        self.Dock_InfoReq.setWidget(self.infoReq)
        self.Dock_InfoReq.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.Dock_InfoReq.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.Dock_InfoReq)
        self.Dock_InfoReq.close()

        self.oneKey = OneKey.OneKeyWidget(self.file1, self.file2, self.pic)
        self.Dock_OneKey = QDockWidget('一键上课模块', self)
        self.Dock_OneKey.setWidget(self.oneKey)
        self.Dock_OneKey.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.Dock_OneKey.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.Dock_OneKey)
        self.Dock_OneKey.close()

        if not self.fileflag:
            self.Dock_InfoReq.show()
            QMessageBox.warning(self, "尚未发现个人信息", "请填写jaccount登录查询存储课程信息",
                                QMessageBox.Yes)

        self.action_OneKey = QAction(QIcon("../settings/key.png"), "&一键上课界面", self)
        self.action_OneKey.setShortcut('Ctrl+O')
        self.action_OneKey.triggered.connect(self.Dock_OneKey.show)
        self.action_OneKey.triggered.connect(self.oneKey.fresh)

        self.action_InfoRequest = QAction(QIcon("../settings/table.png"), "&获取课表信息", self)
        self.action_InfoRequest.setShortcut('Ctrl+R')
        self.action_InfoRequest.triggered.connect(self.Dock_InfoReq.show)

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea,self.toolbar)
        self.toolbar.addAction(self.action_InfoRequest)
        self.toolbar.addAction(self.action_OneKey)
        self.toolbar.setStyleSheet(""" QToolBar {border: 2px outset gray;}  """)

    def getInputData(self, ilist):
        with open(setting_file, 'r') as f:
            self.datastring = json.load(f)
        f.close()
        try:
            if ilist[2] == 0:
                webbrowser = webdriver.Chrome()
            elif ilist[2] == 1:
                webbrowser = webdriver.Firefox()
            new_url = data.browser_access_monitor(webbrowser, self.datastring['kbcx_url'],
                                         self.datastring['sjtu_captcha_url'], self.datastring['sjtu_excepted_url'],
                                              ilist[0], ilist[1])
            data1 = data.get_curricular(webbrowser, self.datastring['url1'], 10)
            data.store_curricular_data(data1, file1)
            data.create_time_json(file1, file2)
            self.Dock_InfoReq.close()
            self.fileflag = self.insertCurri(self.file1, self.file2)
        except:
            QMessageBox.warning(self, "获取失败", "账户错误或网络超时，请重新填写", QMessageBox.Yes)

    def insertCurri(self, file1, file2):
        try:
            self.CentralWidget.insertCurri(file1, file2)
            return True
        except FileNotFoundError:
            QMessageBox.warning(self, "File Not Found!", "未找到设置文件！ ", QMessageBox.Yes)
            return False

    def judgeConnectMain(self, flag):
        if flag:
            Reply = QMessageBox.information(self, "Connected", "已连接，点击Yes自动关闭程序",
                                        QMessageBox.Yes| QMessageBox.No, QMessageBox.No)
            if Reply == QMessageBox.Yes:
                self.close()
        else:
            QMessageBox.warning(self, "Error: Timeout or Occupied!", "连接失败，可能原因是:\n1.网络连接时间过长，请在Z"
                                                                     "oom启动后重新点击连接\n2.当前Zoom已经打开了一个"
                                                                     "会议", QMessageBox.Yes)


if __name__ == "__main__":
    setting_file = "../settings/setting.json"
    try:
        with open(setting_file, 'r') as f:
            datastring = json.load(f)
        f.close()
    except FileNotFoundError:
        datastring = {"currifile":'settings/curricular.json', "timefile":'settings/time_setting.json',
                      "pic_dir":'settings/1.png','kbcx_url':'http://kbcx.sjtu.edu.cn/jaccountlogin',
                      'sjtu_captcha_url':"https://jaccount.sjtu.edu.cn/jaccount/captcha",
                      'url1':"http://kbcx.sjtu.edu.cn/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default",
                      'sjtu_excepted_url':"http://kbcx.sjtu.edu.cn/xtgl/index_initMenu.html"
        }
        with open(setting_file, 'w') as f:
            f.write(json.dumps(datastring))
        f.close()

    app = QApplication(sys.argv)
    file1 = datastring['currifile']
    file2 = datastring['timefile']
    pic_dir = datastring['pic_dir']
    win = MainWindow(file1, file2, pic_dir)
    win.setGeometry(300, 100, 750, 450)
    win.show()
    sys.exit(app.exec_())
