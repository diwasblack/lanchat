import time
import values as V

def clientConnected():
    if V.waitingWindow.isVisible():
        V.waitingWindow.hide()

    V.mainWindow.show()

def printEvent(*args):
    Message = ''
    for arg in args:
        Message = Message + str(arg) + ' '
    print(time.strftime("%H:%M:%S - ", time.localtime()) + "EVENT: " + Message)

def obtainActiveDevices():
    printEvent("obtainActiveDevices")

def encodeInput(DisplayString, MsgType):
    if MsgType == 'TEXT':
        Buffer = '<font color="#102046"><b>You: </b></font>' + (DisplayString + '<br>')
    elif MsgType == 'FILE':
        Buffer = '<font color="#102046"><b>You sent a file: </b></font>' + (DisplayString + '<br>')
    return Buffer


def encodeOutput(DisplayDict, MsgType):
    if MsgType == 'TEXT':
        Buffer = '<font color="#a51842"><b>'+V.GUEST+': </b></font>' + (DisplayDict['MSG'] + '<br>')
    elif MsgType == 'FILE':
        fileName = DisplayDict['NAME']
        filePath = DisplayDict['PATH']
        fullPath = filePath + fileName
        Buffer = '<font color="#a51842"><b>'+V.GUEST+' sent a file: </b></font>' + ('<a>' + fileName + '</a><br>')
    return Buffer
