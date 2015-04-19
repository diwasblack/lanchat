from PyQt4.QtCore import QObject, pyqtSignal

class signals(QObject):
    # Handles connection
    DEVICE_CONNECTED = pyqtSignal(str)
    NO_CONNECTION = pyqtSignal()
    DISCONNECTED = pyqtSignal()
    HOST_LIST = pyqtSignal(list)
    CONNECT_HOST = pyqtSignal(str)
    
    # Sending data
    SEND_MSG = pyqtSignal(str)
    SEND_FILE = pyqtSignal(str)
    
    # Receiving data 
    MSG_RECV = pyqtSignal(dict)
    FILE_INIT = pyqtSignal(dict)
    FILE_RECV = pyqtSignal(dict)
    
    # Uploading file
    FILE_SENT = pyqtSignal()
    PROGRESS_UPD = pyqtSignal(str,int)

S = signals()
