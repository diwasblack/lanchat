import os
import sys

from PyQt4 import QtCore, QtGui
from mainFrame import Ui_mainFrame
from waitingFrame import Ui_waitingDialog

import values as V

from signals import S
from misc import *

# Import everything along with the network thread
from network import *

class mainFrame(QtGui.QMainWindow):
    """Desigining the main window of the app"""
    def __init__(self):
        # Setting up the main window GUI
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_mainFrame()
        self.ui.setupUi(self)
        self.ui.downloadFrame.hide()
        self.ui.uploadFrame.hide()

        # Binding the ui elements' signals to their respective slots
        self.ui.sendButton.released.connect(self.sendButtonClicked)
        self.ui.browseButton.released.connect(self.browseButtonClicked)

        # Binding various signals to their respective slots
        S.MSG_RECV.connect(self.msgReceived)
        S.FILE_INIT.connect(self.fileTransferInit)
        S.FILE_RECV.connect(self.fileReceived)
        S.FILE_SENT.connect(self.fileSent)
        S.PROGRESS_UPD.connect(self.progressUpdate)
        S.DISCONNECTED.connect(self.deviceDisconnected)

    def deviceDisconnected(self):
        # Message displayed when the guest terminal drops the connection
        msg = "Connection Terminated. Do you want to quit?"
        self.close()
        
        # Terminating thread
        networkThread.quit()
        
        reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.No:
            self.ui.chatWindow.clear()
            V.waitingWindow.show()

    def progressUpdate(self, Job, Value):
        # Update the progress bar when any upload or download jobs are running
        if Job == 'DOWNLOAD':
            ProgressBar = self.ui.downloadProgress
        elif Job == 'UPLOAD':
            ProgressBar = self.ui.uploadProgress
        else:
            return

        ProgressBar.setValue(Value)

    def msgReceived(self, msgHeader):
        # Display a received message on the chat window
        outputBuffer = encodeOutput(msgHeader, 'TEXT')
        self.ui.chatWindow.append(outputBuffer)

    def fileTransferInit(self, msgHeader):
        # Alerting the program before attempting to save a received file
        # Message displayed on browseButtonClicked method
        self.ui.uploadLabel.setText("Downloading " + msgHeader['NAME'])
        self.ui.downloadFrame.show()

        printEvent("File Transfer Initiated")

    def fileReceived(self, msgHeader):
        # Display a file received acknowledgement on the chat window
        outputBuffer = encodeOutput(msgHeader, 'FILE')
        self.ui.chatWindow.append(outputBuffer)
        self.ui.downloadLabel.clear()
        self.ui.downloadFrame.hide()

    def fileSent(self):
        # Update GUI after file is sent
        printEvent("File Sent")
        self.ui.sendButton.setEnabled(True)
        self.ui.browseButton.setEnabled(True)

        self.ui.uploadLabel.clear()
        self.ui.uploadFrame.hide()

    def sendButtonClicked(self):
        # Preparing the message and sending it to the networking thread for transmission
        inputBuffer = encodeInput(self.ui.sendText.text(), 'TEXT')
        self.ui.chatWindow.append(inputBuffer)

        S.SEND_MSG.emit(self.ui.sendText.text())

        self.ui.sendText.clear()

    def browseButtonClicked(self):
        # Get the path of file to be sent
        filePath = str(QtGui.QFileDialog.getOpenFileName())

        # Returns if the filepath returned is null
        if (filePath == ''):
            return

        # Preparing the file info to display and send to the networking thread
        fileName = os.path.split(filePath)[-1]
        inputBuffer = encodeInput(fileName, 'FILE')

        self.ui.chatWindow.append(inputBuffer)

        S.SEND_FILE.emit(filePath)

        # Updating the GUI
        self.ui.sendButton.setEnabled(False)
        self.ui.browseButton.setEnabled(False)

        self.ui.uploadLabel.setText("Uploading " + fileName)
        self.ui.uploadFrame.show()

class waitingFrame(QtGui.QDialog):
    """Defining the loading frame"""
    def __init__(self):
        # Setting up the main window GUI
        QtGui.QDialog.__init__(self)
        self.ui = Ui_waitingDialog()
        self.ui.setupUi(self)

        # Binding the ui elements' signals to their respective slots
        self.ui.deviceListBox.itemSelectionChanged.connect(self.deviceListBoxSelectionChanged)
        self.ui.okButton.released.connect(self.okButtonClicked)

        # Binding various signals to their respective slots
        S.NO_CONNECTION.connect(self.clientTimeOut)
        S.DEVICE_CONNECTED.connect(self.deviceConnected)
        S.HOST_LIST.connect(self.getConnectedHosts)

    def show(self):
        msg = "Do you want to host a connection or search for an active device?"
        hostButton = QtGui.QPushButton('Host')
        searchButton = QtGui.QPushButton('Search')
        reply = QtGui.QMessageBox()

        reply.setText(msg)
        reply.addButton(searchButton, QtGui.QMessageBox.RejectRole)
        reply.addButton(hostButton, QtGui.QMessageBox.AcceptRole)

        if reply.exec_() == QtGui.QMessageBox.Accepted:
            MODE = 'SERVER'
            QtGui.QMessageBox.warning(self, 'Warning', 'Please select Search on other device', QtGui.QMessageBox.Ok)
        else:
            MODE = 'CLIENT'
            QtGui.QMessageBox.warning(self, 'Warning', 'Please select Host on other device', QtGui.QMessageBox.Ok)

        printEvent("Set user as " + MODE)
        
        # Starting network thread
        networkThread.startThread(MODE)
        self.populateFrame(MODE)

        QtGui.QDialog.show(self)

    def populateFrame(self, MODE):
        # Populating waiting frame
        if MODE == 'CLIENT':
            self.ui.selectingFrame.show()
        else:
            self.ui.selectingFrame.hide()

        self.adjustSize()

        printEvent("Populating WaitingFrame")

    def deviceListBoxSelectionChanged(self):
        # Updating GUI whenever selection is changed
        if self.ui.deviceListBox.currentIndex == -1:
            self.ui.okButton.setEnabled(False)
        else:
            self.ui.okButton.setEnabled(True)

        printEvent("deviceListBoxSelectionChanged")

    def getConnectedHosts(self, hosts):
        # Updating the list with available hosts
        if self.ui.deviceListBox.currentItem() is not None:
            currentItemValue = self.ui.deviceListBox.currentItem().text()
        else:
            currentItemValue = None

        sortedHosts = sorted(hosts)
        self.ui.deviceListBox.clear()

        self.ui.deviceListBox.addItems(sortedHosts)

        if currentItemValue is not None:
            for host in hosts:
                if host == currentItemValue:
                    printEvent('Old host found')
                    currentIndex = hosts.index(host)
                    self.ui.deviceListBox.setCurrentRow(currentIndex)

        printEvent(hosts)

    def okButtonClicked(self):
        # Connecting the device with host
        currentItem = self.ui.deviceListBox.currentItem()
        if currentItem == None:
            return

        host = self.ui.deviceListBox.currentItem().text()
        self.ui.deviceListBox.clear()
        S.CONNECT_HOST.emit(host)
        self.hide()

    def deviceConnected(self, peer):
        # Launching the main window of the app
        V.GUEST = peer
        V.mainWindow.ui.chatTitle.setText("Chatting with " + V.GUEST)
        V.mainWindow.show()
        self.hide()
        printEvent("Guest Connected")

    def clientTimeOut(self):
        # Cleaning up if no connection is established
        networkThread.quit()
        MODE = 'SERVER'
        self.populateFrame(MODE)
        printEvent("Client time out")

"""Initialising the main classes"""
V.mainWindow = mainFrame()
V.waitingWindow = waitingFrame()

if __name__ == '__main__':
    V.waitingWindow.show()
    sys.exit(V.app.exec_())
