from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *
import sys, time
import json
import src.Functions.get_curricular_data as data
curri_label = ['课程信息', '课程时间', 'Zoom会议信息', '自动打开时间' ]


# 课程列表模式
class CurricularWidget1(QWidget):
    signal_TableRow = pyqtSignal(int)
    def __init__(self):
        super(CurricularWidget1, self).__init__()
        self.initUI()

    def initUI(self):
        self.Layout = QHBoxLayout()
        self.auto_scroll = True
        self.tablewidget = QTableWidget()
        self.tablewidget.setColumnCount(4)
        self.tablewidget.setFont(QFont('YouYuan', 11))
        # 表头
        self.tablewidget.setHorizontalHeaderLabels(curri_label)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)   # Resize to Contents
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)     # Select Rows
        QTableWidget.resizeRowsToContents(self.tablewidget)
        QTableWidget.resizeColumnsToContents(self.tablewidget)
        self.Layout.addWidget(self.tablewidget)
        self.setLayout(self.Layout)

        # 表格自适应伸缩
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # ResizeToContents
        self.tablewidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 表格禁止编辑
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 选择行
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        #双击事件
        self.tablewidget.doubleClicked.connect(self.curriDoubleClicked)
        self.lastRow = None

    # Insert Operations
    def insertRow(self, current_row, curri_data):
        for i in range(4):
            temp = QTableWidgetItem(curri_data[i])
            self.tablewidget.setItem(current_row, i, temp)

    def insertCurri(self, curri_info):
        curri_num = len(curri_info)
        for i in range(curri_num):
            current_row = self.tablewidget.rowCount()
            self.tablewidget.insertRow(current_row)
            self.insertRow(current_row, curri_info[i])

    def curriDoubleClicked(self, index):
        if int(index.row()) != self.lastRow:
            self.signal_TableRow.emit(int(index.row()))
            self.lastRow = int(index.row())

    def clear(self):
        self.tablewidget.clearContents()
        self.tablewidget.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pkt_table = CurricularWidget1()
    file1 = '../settings/curricular.json'
    file2 = '../settings/time_setting.json'

    curri = data.change_DataStyle_List(file1, file2)
    pkt_table.insertCurri(curri)
    pkt_table.show()
    sys.exit(app.exec_())
