# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waitingFrame.ui'
#
# Created: Tue Jan 20 21:38:04 2015
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

class Ui_waitingDialog(object):
    def setupUi(self, waitingDialog):
        waitingDialog.setObjectName(_fromUtf8("waitingDialog"))
        waitingDialog.resize(320, 272)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(waitingDialog.sizePolicy().hasHeightForWidth())
        waitingDialog.setSizePolicy(sizePolicy)
        waitingDialog.setMinimumSize(QtCore.QSize(320, 0))
        waitingDialog.setMaximumSize(QtCore.QSize(320, 293))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/lanchat.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        waitingDialog.setWindowIcon(icon)
        waitingDialog.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(waitingDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.progressBar = QtGui.QProgressBar(waitingDialog)
        self.progressBar.setMinimumSize(QtCore.QSize(302, 23))
        self.progressBar.setMaximumSize(QtCore.QSize(302, 23))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_2.addWidget(self.progressBar)
        self.selectingFrame = QtGui.QWidget(waitingDialog)
        self.selectingFrame.setMinimumSize(QtCore.QSize(302, 225))
        self.selectingFrame.setMaximumSize(QtCore.QSize(302, 225))
        self.selectingFrame.setObjectName(_fromUtf8("selectingFrame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.selectingFrame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.deviceListBox = QtGui.QListWidget(self.selectingFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceListBox.sizePolicy().hasHeightForWidth())
        self.deviceListBox.setSizePolicy(sizePolicy)
        self.deviceListBox.setMaximumSize(QtCore.QSize(302, 192))
        self.deviceListBox.setAlternatingRowColors(True)
        self.deviceListBox.setObjectName(_fromUtf8("deviceListBox"))
        self.verticalLayout.addWidget(self.deviceListBox)
        self.okButton = QtGui.QPushButton(self.selectingFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setMinimumSize(QtCore.QSize(302, 27))
        self.okButton.setMaximumSize(QtCore.QSize(302, 27))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.verticalLayout.addWidget(self.okButton)
        self.verticalLayout_2.addWidget(self.selectingFrame)

        self.retranslateUi(waitingDialog)
        QtCore.QObject.connect(self.deviceListBox, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), self.okButton.click)
        QtCore.QMetaObject.connectSlotsByName(waitingDialog)

    def retranslateUi(self, waitingDialog):
        waitingDialog.setWindowTitle(_translate("waitingDialog", "Setting up connection", None))
        self.deviceListBox.setSortingEnabled(True)
        self.okButton.setText(_translate("waitingDialog", "Ok", None))

import res_rc
