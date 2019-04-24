# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(536, 316)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.description = QtWidgets.QLabel(self.centralwidget)
        self.description.setObjectName("description")
        self.verticalLayout.addWidget(self.description)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chatroom_list_label = QtWidgets.QLabel(self.centralwidget)
        self.chatroom_list_label.setObjectName("chatroom_list_label")
        self.horizontalLayout.addWidget(self.chatroom_list_label)
        self.chatroom_list = QtWidgets.QComboBox(self.centralwidget)
        self.chatroom_list.setEnabled(False)
        self.chatroom_list.setObjectName("chatroom_list")
        self.chatroom_list.addItem("")
        self.chatroom_list.setItemText(0, "")
        self.chatroom_list.addItem("")
        self.chatroom_list.addItem("")
        self.chatroom_list.addItem("")
        self.chatroom_list.addItem("")
        self.horizontalLayout.addWidget(self.chatroom_list)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setObjectName("button")
        self.horizontalLayout_2.addWidget(self.button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "微信群聊成员导出助手"))
        self.description.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">用法：</span></p><p><span style=\" font-size:14pt; font-weight:600;\">1.点击登录按钮扫描二维码登录。</span></p><p><span style=\" font-size:14pt; font-weight:600;\">2.在下拉列表中选择要导出的群聊。</span></p><p><span style=\" font-size:14pt; font-weight:600;\">3.点击导出即可。导出的文件在当前目录下的output.xlsx。</span></p><p><br/></p><p><span style=\" font-size:14pt; font-weight:600;\">注意：可能需提前将要导出的群聊保存到通讯录。</span></p></body></html>"))
        self.chatroom_list_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">选择群聊</span></p></body></html>"))
        self.chatroom_list.setItemText(1, _translate("MainWindow", "COM4"))
        self.chatroom_list.setItemText(2, _translate("MainWindow", "COM5"))
        self.chatroom_list.setItemText(3, _translate("MainWindow", "COM6"))
        self.chatroom_list.setItemText(4, _translate("MainWindow", "COM7"))
        self.button.setText(_translate("MainWindow", "登录"))


