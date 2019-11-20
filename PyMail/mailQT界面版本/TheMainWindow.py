#!/usr/bin/python
# coding:utf-8
# Created by: PyQt5 UI code generator 5.13.1
# WARNING! All changes made in this file will be lost!
"""
Created on Fri Nov 15 14:42:02 2019
@author: fuchs1939
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QStringListModel
import zmail
from TheSendMailWindow import *


class TheMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(TheMainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(977, 586)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(0, 0, 291, 561))
        self.listView.setObjectName("listView")
        self.listView.clicked.connect(self.clickedlist)
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setGeometry(QtCore.QRect(300, 0, 681, 561))
        self.webEngineView.setObjectName("webEngineView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 977, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action.triggered.connect(self.process)
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_2.triggered.connect(self.process2)
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_3.triggered.connect(self.process3)

        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.action_3)
        self.menu_3.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mail"))
        self.menu.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "账号"))
        self.action.setText(_translate("MainWindow", "退出登录"))
        self.action_2.setText(_translate("MainWindow", "刷新邮箱内容"))
        self.action_3.setText(_translate("MainWindow", "发送新邮件"))

    def process3(self):
        self.ui_second = TheSendMailWindow()
        self.ui_second.show()

    def process2(self):
        global mainServer
        list = []
        mainServer = zmail.server(TheSendMailWindow.send_dict_account["USERNAME"], TheSendMailWindow.send_dict_account["PASSWORD"])
        getmail_list = mainServer.get_mails(start_index=1, end_index=mainServer.stat()[0])
        for i in range(len(getmail_list)):
            list.append(getmail_list[i]["subject"])
        listModel = QStringListModel()
        listModel.setStringList(list)
        self.listView.setModel(listModel)

    def process(self):
        append = QtWidgets.QApplication.instance()
        append.quit()

    def clickedlist(self, qModelIndex):
        mail = mainServer.get_mail(qModelIndex.row()+1)
        str = mail["content_html"][0]
        self.webEngineView.setHtml(str)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = TheMainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())