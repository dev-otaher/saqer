from sqlite3 import Error

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy, QPushButton
from qtpy import QtWidgets
from gui.Warning import Warning


class ViewReports:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")
        self.fill_courses()

    def connect_widgets(self):
        self.parent.i_courses_table.clicked.connect(self.fill_classes)
        self.parent.i_classes_table.clicked.connect(self.fill_report)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)
        # self.hide_first_column(self.parent.i_classes_table)
        # self.hide_first_column(self.parent.i_courses_table)

    def hide_first_column(self, table):
        table.setColumnHidden(0, True)
        table.setColumnHidden(0, True)

    def fill_courses(self):
        try:
            sql = '''
                    SELECT DISTINCT	course.id, course.code, course.title FROM class 
                    INNER JOIN course ON class.course_id == course.id 
                    WHERE instructor_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (self.parent.UUID,))
            courses = cur.fetchall()
            for course in courses:
                self.add_course(course)
        except Error as e:
            Warning(str(e))
            print(e)

    def add_course(self, course):
        self.parent.i_courses_table.insertRow(0)
        for i in range(3):
            self.parent.i_courses_table.setItem(0, i, QtWidgets.QTableWidgetItem(str(course[i])))

    def fill_classes(self, location: QModelIndex):
        try:
            row = location.row()
            course_id = self.parent.i_courses_table.item(row, 0).text()

            sql = '''
                    SELECT id, title, date, time FROM class 
                    WHERE course_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (course_id,))
            classes = cur.fetchall()

            self.reset_table(self.parent.i_classes_table)
            for c in classes:
                self.add_class(c)

            self.parent.goto(self.parent.i_stacked_widget, self.parent.i_classes)
            self.parent.i_title.setText("View Reports - Classes")
        except Error as e:
            Warning(str(e))
        except Exception as e:
            print(e)

    def add_class(self, c):
        self.parent.i_classes_table.insertRow(0)
        a = QtWidgets.QTableWidgetItem("Attendance")
        a.setForeground(QColor(56, 219, 208))
        self.parent.i_classes_table.setItem(0, 1, a)
        b = QtWidgets.QTableWidgetItem("Behaviour")
        b.setForeground(QColor(56, 219, 208))
        self.parent.i_classes_table.setItem(0, 2, b)

        self.parent.i_classes_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(c[0])))
        for i in range(3, 6):
            self.parent.i_classes_table.setItem(0, i, QtWidgets.QTableWidgetItem(c[i - 2]))

    def fill_report(self, location):
        try:
            row, column = location.row(), location.column()
            class_id = self.parent.i_classes_table.item(row, 0).text()
            if column == 1:
                sql = '''
                        SELECT student_id, status FROM attendance 
                        WHERE class_id=?;
                        '''
            elif column == 2:
                sql = '''
                        SELECT happy, sad, neutral FROM behavior 
                        WHERE class_id=?;
                        '''
            else:
                return

            cur = self.db_conn.cursor()
            cur.execute(sql, (class_id,))
            reports = cur.fetchall()

            if column == 1:
                self.reset_table(self.parent.i_attendance_table)
                for report in reports:
                    self.parent.i_attendance_table.insertRow(0)
                    self.parent.i_attendance_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(report[0])))
                    checkbox = QtWidgets.QCheckBox()
                    checkbox.setChecked(report[1])
                    self.parent.i_attendance_table.setCellWidget(0, 1, checkbox)
                self.parent.goto(self.parent.i_stacked_widget, self.parent.i_attendance)
            elif column == 2:
                self.reset_table(self.parent.i_behaviour_table)
        except Exception as e:
            print(e)

    def reset_table(self, table):
        table.clearContents()
        table.setRowCount(0)

    def save_data(self):
        try:
            sql = '''INSERT INTO attendence (student_id, status)
                            VALUES (?, ?)'''
            cur = self.db_conn.cursor()
            for r in range(self.parent.i_recheck_table.rowCount()):
                id = self.parent.i_recheck_table.item(r, 0).text()
                status = self.parent.i_recheck_table.cellWidget(r, 3).isChecked()
                cur.execute(sql, (id, status))
                self.db_conn.commit()
        except Error as e:
            Warning(str(e))
            print(e)
