from os.path import sep

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Warning(QDialog):

    def __init__(self, msg):
        super(Warning, self).__init__()
        loadUi(sep.join(['gui', 'interfaces', 'Warning.ui']), self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.setWindowModality(Qt.ApplicationModal)
        self.i_ok.clicked.connect(lambda: self.close())
        self.i_message.setText(msg)
        self.i_message.setAlignment(Qt.AlignCenter)
        self.show()

