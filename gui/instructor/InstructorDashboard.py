from functools import partial

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QColor
from gui import Login, Warning
from gui.instructor.Session import Session
from gui.instructor.ViewReports import ViewReports
from modules.DBHelper import DBHelper


class InstructorDashboard(QDialog):

    def __init__(self, UUID):
        super(InstructorDashboard, self).__init__()
        uic.loadUi("gui/interfaces/InstructorDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.connect_widgets()
        self.UUID = UUID

        self.i_save_recheck.clicked.connect(self.save_attendance)
        # self.i_save.clicked.connect(self.save)
        self.db = DBHelper()
        self.view_reports = ViewReports(self)
        self.session = Session(self)
        self.disable_btn(self.i_end_session)
        self.show()

    def connect_widgets(self):
        self.connect_header()
        self.connect_side_widgets()

    def connect_header(self):
        self.i_header.mouseMoveEvent = self.move_window
        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.clicked.connect(self.logout)

    def connect_side_widgets(self):
        self.connect_view_reports()
        self.i_start_session.clicked.connect(partial(self.goto, self.i_choices, self.i_start_session_sec))
        self.i_end_session.clicked.connect(partial(self.goto, self.i_choices, self.i_end_session_sec))

    def connect_view_reports(self):
        self.i_view_reports.clicked.connect(partial(self.goto, self.i_choices, self.i_view_report_sec))
        self.i_view_reports.clicked.connect(partial(self.goto, self.i_stacked_widget, self.i_courses))
        self.i_view_reports.clicked.connect(partial(self.i_title.setText, "View Reports - Courses"))

    @staticmethod
    def goto(parent_widget, widget):
        parent_widget.setCurrentWidget(widget)

    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def end_session(self):
        self.i_choices.setCurrentWidget(self.i_end_session_sec)

    def save_attendance(self):
        print('save attendance test')

    def enable_btn(self, btn):
        btn.setEnabled(True)
        self.i_end_session.setStyleSheet("QPushButton {border-radius: 25px;background-color: "
                                         "#38DBD0;color:#ffffff}QPushButton:hover {background-color: "
                                         "#23b2a8; color: rgb(255, 255, 255);} QPushButton:pressed { background-color: #38DBD0; }")

    def disable_btn(self, btn):
        btn.setEnabled(False)
        btn.setStyleSheet("QPushButton {border-radius: 25px;background-color: "
                          "#727272;color:#ffffff}QPushButton:hover {background-color: "
                          "#23b2a8; color: rgb(255, 255, 255);} QPushButton:pressed { background-color: #38DBD0; }")

    def logout(self):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)
