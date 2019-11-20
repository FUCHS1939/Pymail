#!/usr/bin/python
# coding:utf-8
# Created by: PyQt5 UI code generator 5.13.1
# WARNING! All changes made in this file will be lost!
"""
Created on Fri Nov 15 14:42:02 2019
@author: fuchs1939
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import re
import zmail

class TheSendMailWindow(QtWidgets.QMainWindow):

    send_dict_account = {
        "USERNAME": "",
        "PASSWORD": ""
    }

    def __init__(self):
        super(TheSendMailWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(667, 490)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        Form.setFont(font)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 131, 31))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 431, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("example@gmail.com")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 90, 231, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("标题")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 101, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 101, 31))
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 150, 651, 281))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlaceholderText("正文")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 440, 181, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.toSendMail)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 440, 181, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.process)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "发送新邮件"))
        self.label.setText(_translate("Form", "收信人"))
        self.label_2.setText(_translate("Form", "标题"))
        self.label_3.setText(_translate("Form", "内容"))
        self.pushButton.setText(_translate("Form", "发送"))
        self.pushButton_2.setText(_translate("Form", "取消"))
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.textEdit.clear()

    def toSendMail(self):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        mail = {
            "subject": "",  # 标题
            "content_text": "",  # 内容
        }
        recipients = self.lineEdit.text()
        if (re.match(pattern, recipients) == None):
            QMessageBox.warning(self, "警告", "请注意邮箱格式", QMessageBox.Yes)
            self.lineEdit.setFocus()
        else:
            mail["subject"] = self.lineEdit_2.text()
            if mail["subject"].isspace() or len(mail["subject"]) == 0:
                QMessageBox.warning(self, "警告", "标题不能为空", QMessageBox.Yes)
                self.lineEdit_2.setFocus()
            else:
                mail["content_text"] = self.textEdit.toPlainText()
                if (mail["content_text"].isspace() or len(mail["content_text"]) == 0):
                    QMessageBox.warning(self, "警告", "内容不能为空", QMessageBox.Yes)
                    self.textEdit.setFocus()
                else:
                    server = zmail.server(self.send_dict_account["USERNAME"], self.send_dict_account["PASSWORD"])
                    try:
                        server.send_mail(recipients, mail, auto_add_from=True, auto_add_to=True)
                    except:
                        QMessageBox.warning(self, "警告", "发送失败", QMessageBox.Yes)
                        self.lineEdit.setFocus()
                    else:
                        QMessageBox.warning(self, "提示", "发送成功", QMessageBox.Yes)
                        self.hide()

    def process(self):
        self.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sendmailWindow = QtWidgets.QMainWindow()
    ui = TheSendMailWindow()
    ui.setupUi(sendmailWindow)
    sendmailWindow.show()
    sys.exit(app.exec_())