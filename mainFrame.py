# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainFrame.ui'
#
# Created: Tue Jan 20 01:14:21 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainFrame(object):
    def setupUi(self, mainFrame):
        mainFrame.setObjectName(_fromUtf8("mainFrame"))
        mainFrame.resize(640, 569)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Downloads/lanchat.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainFrame.setWindowIcon(icon)
        self.mainLayout = QtGui.QWidget(mainFrame)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.mainLayout)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chatTitle = QtGui.QLabel(self.mainLayout)
        self.chatTitle.setMinimumSize(QtCore.QSize(622, 15))
        self.chatTitle.setMaximumSize(QtCore.QSize(16777215, 15))
        self.chatTitle.setObjectName(_fromUtf8("chatTitle"))
        self.verticalLayout_2.addWidget(self.chatTitle)
        self.chatWindow = QtGui.QTextBrowser(self.mainLayout)
        self.chatWindow.setMinimumSize(QtCore.QSize(622, 344))
        self.chatWindow.setAcceptDrops(False)
        self.chatWindow.setAcceptRichText(True)
        self.chatWindow.setOpenExternalLinks(False)
        self.chatWindow.setOpenLinks(False)
        self.chatWindow.setObjectName(_fromUtf8("chatWindow"))
        self.verticalLayout_2.addWidget(self.chatWindow)
        self.sendText = QtGui.QLineEdit(self.mainLayout)
        self.sendText.setMinimumSize(QtCore.QSize(622, 27))
        self.sendText.setMaximumSize(QtCore.QSize(16777215, 27))
        self.sendText.setObjectName(_fromUtf8("sendText"))
        self.verticalLayout_2.addWidget(self.sendText)
        self.horizontalLayout_1 = QtGui.QHBoxLayout()
        self.horizontalLayout_1.setObjectName(_fromUtf8("horizontalLayout_1"))
        self.sendButton = QtGui.QPushButton(self.mainLayout)
        self.sendButton.setMinimumSize(QtCore.QSize(500, 27))
        self.sendButton.setMaximumSize(QtCore.QSize(16777215, 27))
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.horizontalLayout_1.addWidget(self.sendButton)
        self.browseButton = QtGui.QPushButton(self.mainLayout)
        self.browseButton.setMinimumSize(QtCore.QSize(114, 27))
        self.browseButton.setMaximumSize(QtCore.QSize(114, 27))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_1.addWidget(self.browseButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.downloadFrame = QtGui.QWidget(self.mainLayout)
        self.downloadFrame.setObjectName(_fromUtf8("downloadFrame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.downloadFrame)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.downloadLabel = QtGui.QLabel(self.downloadFrame)
        self.downloadLabel.setObjectName(_fromUtf8("downloadLabel"))
        self.verticalLayout_3.addWidget(self.downloadLabel)
        self.downloadProgress = QtGui.QProgressBar(self.downloadFrame)
        self.downloadProgress.setProperty("value", 24)
        self.downloadProgress.setTextVisible(False)
        self.downloadProgress.setObjectName(_fromUtf8("downloadProgress"))
        self.verticalLayout_3.addWidget(self.downloadProgress)
        self.horizontalLayout_2.addWidget(self.downloadFrame)
        self.uploadFrame = QtGui.QWidget(self.mainLayout)
        self.uploadFrame.setObjectName(_fromUtf8("uploadFrame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.uploadFrame)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.uploadLabel = QtGui.QLabel(self.uploadFrame)
        self.uploadLabel.setObjectName(_fromUtf8("uploadLabel"))
        self.verticalLayout_4.addWidget(self.uploadLabel)
        self.uploadProgress = QtGui.QProgressBar(self.uploadFrame)
        self.uploadProgress.setProperty("value", 24)
        self.uploadProgress.setTextVisible(False)
        self.uploadProgress.setObjectName(_fromUtf8("uploadProgress"))
        self.verticalLayout_4.addWidget(self.uploadProgress)
        self.horizontalLayout_2.addWidget(self.uploadFrame)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        mainFrame.setCentralWidget(self.mainLayout)

        self.retranslateUi(mainFrame)
        QtCore.QObject.connect(self.sendText, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.sendButton.click)
        QtCore.QMetaObject.connectSlotsByName(mainFrame)

    def retranslateUi(self, mainFrame):
        mainFrame.setWindowTitle(_translate("mainFrame", "LanChat", None))
        self.chatTitle.setText(_translate("mainFrame", "Chat with %user", None))
        self.sendButton.setText(_translate("mainFrame", "Send", None))
        self.browseButton.setText(_translate("mainFrame", "Files...", None))
        self.downloadLabel.setText(_translate("mainFrame", "Downloading", None))
        self.uploadLabel.setText(_translate("mainFrame", "Uploading", None))

import res_rc
