#!/usr/bin/python
# coding:utf-8
"""
Created on Tue Nov 12 21:15:38 2019
@author: fuchs1939
"""

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from TheMainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re
import zmail
from TheSendMailWindow import *

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 120)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 20, 200, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 50, 200, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(20, 24, 40, 12))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(20, 54, 40, 12))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)

        self.pushButton.clicked.connect(self.word_get)
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QMessageBox.warning(self, "提示", "在使用程序之前请确保你已经打开了邮箱的POP3和SMTP功能\n并且拥有用于POP3和SMTP客户端的授权密码", QMessageBox.Yes)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "登录"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "邮箱账号"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请注意不是邮箱密码"))
        self.label.setText(_translate("MainWindow", "帐号"))
        self.label_2.setText(_translate("MainWindow", "授权码"))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        self.pushButton_2.setText(_translate("MainWindow", "取消"))

    def word_get(self):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        TheSendMailWindow.send_dict_account["USERNAME"] = self.lineEdit.text()
        TheSendMailWindow.send_dict_account["PASSWORD"] = self.lineEdit_2.text()
        if re.match(pattern, TheSendMailWindow.send_dict_account["USERNAME"]) == None:
            QMessageBox.warning(self, "警告", "请检查邮箱账号格式！", QMessageBox.Yes)
            self.lineEdit.setFocus()
        else:
            server = zmail.server(TheSendMailWindow.send_dict_account["USERNAME"], TheSendMailWindow.send_dict_account["PASSWORD"])
            if server.smtp_able():
                if server.pop_able():
                    ui_first.show()
                    MainWindow.close()
                else:
                    QMessageBox.warning(self, "警告", "无法连接POP3服务，请检查邮箱账号和授权密码", QMessageBox.Yes)
                    self.lineEdit.setFocus()
            else:
                QMessageBox.warning(self, "警告", "无法连接SMTP服务，请检查邮箱账号和授权密码", QMessageBox.Yes)
                self.lineEdit.setFocus()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui_first = TheMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())