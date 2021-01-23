import sys
from PyQt5.QtWidgets import QDialog, QApplication, QLabel
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5 import Qt


class Login(QDialog):

    def __init__(self):
        super(Login, self).__init__()
        loadUi("LoginPage.ui",self)
        self.login.clicked.connect(self.loginfun)
        self.password_note.setHidden(True)
        self.closewindow.clicked.connect(lambda: self.close())
        self.minmizewindow.clicked.connect(lambda: self.showMinimized())
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.Fpassword.mousePressEvent = self.forgetpass
        self.show()

        def moveWindow(e):
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.Header.mouseMoveEvent = moveWindow



    def forgetpass(self,eve):
        print('dsd')

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()


    def windowFilePath(self):
        print('hello!')

    def loginfun(self):
        username = self.username.text()
        password = self.password.text()

        if  username == "" and password =="":
            self.password_note.setHidden(False)





app=QApplication(sys.argv)
mainwindow=Login()
sys.exit(app.exec_())

