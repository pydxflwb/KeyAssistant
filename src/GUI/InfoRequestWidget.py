from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class InfoRequestWidget(QWidget):
    # pyqtSignals to connect widgets
    signal_returnText = pyqtSignal(list)    # to get username and password

    def __init__(self):
        super(InfoRequestWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # Layout
        self.Layout = QVBoxLayout()

        # Input Lines
        self.UserName = SingleInputWidget("Username")
        self.PassWord = SingleInputWidget("Password")
        # self.PassWord.Edit.setEchoMode(2)
        self.Layout.addWidget(self.UserName)
        self.Layout.addWidget(self.PassWord)

        # Combobox
        self.comboLayout = QHBoxLayout()
        self.BrLabel = QLabel("Browser")
        self.BrLabel.setFont(QFont("Consolas", 9))
        self.Browser = QComboBox(self)
        self.Browser.setFont(QFont("Consolas", 9))
        self.Browser.addItem(' ')
        self.Browser.addItem('Chrome')
        self.Browser.addItem('Firefox')
        self.Browser.addItem('Edge')
        self.Browser.addItem('IE')
        self.comboLayout.addWidget(self.BrLabel)
        self.comboLayout.addWidget(self.Browser)
        self.Br = QWidget()
        self.Br.setLayout(self.comboLayout)
        self.Layout.addWidget(self.Br)

        # Buttons
        self.nextButton = QPushButton("Next")
        self.nextButton.setFont(QFont("Consolas", 9))
        self.nextButton.clicked.connect(self.next)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFont(QFont("Consolas", 9))
        self.cancelButton.clicked.connect(self.close)

        # Buttons Layout
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.nextButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.buttonSpace = QWidget()
        self.buttonSpace.setLayout(self.buttonLayout)
        self.Layout.addWidget(self.buttonSpace)

        # Main Layout Setting(s)
        self.setLayout(self.Layout)

    # Functions
    def next(self):         # Function for Next Button
        username = self.UserName.returnText()
        password = self.PassWord.returnText()
        if username and password:
            returnText = []
            returnText.append(username)
            returnText.append(password)
            self.signal_returnText.emit(returnText)
            self.close()
        else:
            QMessageBox.warning(self, 'Invalid Input !',
                        "No username or password",
                        QMessageBox.Yes)


# A Self-Defined Input Widget Template (More arguments excepted)
class SingleInputWidget(QWidget):
    def __init__(self, label):
        super(SingleInputWidget, self).__init__()
        self.initUI(label)

    def initUI(self, label):
        self.Layout = QHBoxLayout()
        self.Label = QLabel(label)
        self.Label.setFont(QFont("Consolas", 9))
        self.Edit = QLineEdit(self)
        self.Edit.setFont(QFont("Consolas", 9))
        self.Layout.addWidget(self.Label)
        self.Layout.addWidget(self.Edit)
        self.setLayout(self.Layout)

    def returnText(self):
        return self.Edit.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = InfoRequestWidget()
    win.setGeometry(300, 100, 305, 105)
    win.show()
    sys.exit(app.exec_())