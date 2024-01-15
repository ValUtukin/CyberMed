# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\PyCharmProjects\PyQt_withHub\CyberMed\src\PyQT-version\UIs\PreSavedMoves.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1346, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.current_script_label = QtWidgets.QLabel(self.centralwidget)
        self.current_script_label.setGeometry(QtCore.QRect(10, 10, 151, 31))
        self.current_script_label.setObjectName("current_script_label")
        self.script_file_path_label = QtWidgets.QLabel(self.centralwidget)
        self.script_file_path_label.setGeometry(QtCore.QRect(170, 10, 561, 31))
        self.script_file_path_label.setStyleSheet(" background-color: white; border-bottom-style: solid; "
                                                  "border-bottom-width: 1px;")
        self.script_file_path_label.setObjectName("script_file_path_label")
        self.open_script_file_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_script_file_btn.setGeometry(QtCore.QRect(740, 10, 75, 31))
        self.open_script_file_btn.setObjectName("open_script_file_btn")
        self.load_script_file_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_script_file_btn.setGeometry(QtCore.QRect(820, 10, 75, 31))
        self.load_script_file_btn.setObjectName("load_script_file_btn")
        self.move_script_label = QtWidgets.QLabel(self.centralwidget)
        self.move_script_label.setGeometry(QtCore.QRect(10, 50, 721, 91))
        self.move_script_label.setStyleSheet("border-style: solid;border-color: rgb(0, 0, 0);border-width: 1px;\n"
                                             "background-color: white; text-align: justify; text-justify: inter-word;")
        self.move_script_label.setObjectName("move_script_label")
        self.send_full_sequence_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_full_sequence_btn.setGeometry(QtCore.QRect(510, 150, 101, 31))
        self.send_full_sequence_btn.setObjectName("send_full_sequence_btn")
        self.send_next_command_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_next_command_btn.setGeometry(QtCore.QRect(620, 150, 111, 31))
        self.send_next_command_btn.setObjectName("send_next_command_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1346, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.current_script_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Currently used script file:</span></p></body></html>"))
        self.script_file_path_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">TextLabel</span></p></body></html>"))
        self.open_script_file_btn.setText(_translate("MainWindow", "Open..."))
        self.load_script_file_btn.setText(_translate("MainWindow", "Load"))
        self.move_script_label.setText(_translate("MainWindow", "Text"))
        self.send_full_sequence_btn.setText(_translate("MainWindow", "Send Full Sequence"))
        self.send_next_command_btn.setText(_translate("MainWindow", "Send Next Command"))
