import os
import json
from signals import S
from PyQt4 import QtCore, QtNetwork

#in milliseconds
READ_TIMEOUT=10000
CONNECTION_TIMEOUT=10000

BROADCAST_INTERVAL=1000
SCAN_INTERVAL=3000

#in bytes
PACKET_SIZE=1024

# FIXED TCP PORT
TCP_PORT=13373
# FIXED UDP PORT
UDP_PORT=13374

KEY='HailHydra'

class NetworkInterface():
    """ Generic class for network connections """
    def __init__(self):
        self.connection = None

        S.SEND_MSG.connect(self.sendMsg)
        S.SEND_FILE.connect(self.sendFile)

    def readData(self):
        instream = QtCore.QDataStream(self.connection)
        instream.setVersion(QtCore.QDataStream.Qt_4_0)

        if self.connection.bytesAvailable() < 4:
            return

        # Reading blocksize
        blockSize = instream.readUInt32()

        # Checking if the inputstream matches the blocksize
        if self.connection.bytesAvailable() < blockSize:
            return

        # Detecting the data type
        header_bytes = instream.readString()
        header = json.loads(str(header_bytes, encoding='utf-8'))

        if(header['TYPE']=='MSG'):
            S.MSG_RECV.emit(header)

        elif(header['TYPE']=='FILE'):
            actual_bytes=header['SIZE']
            recv_bytes=0

            # Storing file in default location
            new_path = QtCore.QDir.homePath() + '/LanChat/'
            if not QtCore.QDir(new_path).exists():
                QtCore.QDir(QtCore.QDir.homePath()).mkdir('LanChat')

            S.FILE_INIT.emit(header)

            file=open(new_path+header['NAME'],"wb")

            self.connection.waitForReadyRead(-1)

            # Writing raw bytes to file
            while(True):
                S.PROGRESS_UPD.emit('DOWNLOAD', (recv_bytes/actual_bytes)*100)

                bytes_remain=self.connection.bytesAvailable()
                if (bytes_remain==0):
                    break

                recv_bytes=recv_bytes+bytes_remain
                content=instream.readRawData(bytes_remain)
                file.write(content)

                if(recv_bytes==actual_bytes):
                    break

                self.connection.waitForReadyRead(READ_TIMEOUT)

            file.close()
            if(actual_bytes==recv_bytes):
                S.PROGRESS_UPD.emit('DOWNLOAD', 100)

                header['PATH']=new_path
                S.FILE_RECV.emit(header)
            else:
                print('Error occured')

    def sendMsg(self,msg):
        if (msg==''):
            return

        # Array of bytes to hold the data
        block = QtCore.QByteArray()

        # Datastream
        outstream = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstream.setVersion(QtCore.QDataStream.Qt_4_0)

        # Inserting space to write the block size
        outstream.writeUInt32(0)

        # Message
        header={'TYPE':'MSG','MSG':msg}
        header_bytes=bytes(json.dumps(header),encoding='utf-8')
        outstream.writeString(header_bytes)

        # Writing block size at the beginning of stream
        outstream.device().seek(0)
        outstream.writeUInt32(block.size() - 4)

        # Writing data to socket
        self.connection.write(block)

    def sendFile(self, filepath):
        if (filepath==''):
            return

        S.PROGRESS_UPD.emit('UPLOAD', 0)

        # Array of bytes to hold the data
        block = QtCore.QByteArray()

        # Datastream
        outstream = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstream.setVersion(QtCore.QDataStream.Qt_4_0)

        # Inserting space to write the block size
        outstream.writeUInt32(0)

        # Header for file
        filename = os.path.split(filepath)[-1]

        actual_bytes=os.path.getsize(filepath)
        send_bytes=0

        header={'TYPE':'FILE',
                'NAME':filename,
                'SIZE':actual_bytes}

        header_bytes=bytes(json.dumps(header),encoding='utf-8')
        outstream.writeString(header_bytes)

        outstream.device().seek(0)
        outstream.writeUInt32(block.size() - 4)

        # Writing header for file
        self.connection.write(block)

        # Raw bytes of the file
        f = open(filepath, "rb")
        try:
            byte = f.read(PACKET_SIZE)
            while byte != b'':
                S.PROGRESS_UPD.emit('UPLOAD', (send_bytes/actual_bytes)*100)

                block.clear()
                outstream.device().seek(0)
                outstream.writeRawData(byte)

                self.connection.waitForBytesWritten(-1)
                self.connection.write(block)

                byte = f.read(PACKET_SIZE)
                send_bytes=send_bytes+PACKET_SIZE
        finally:
            f.close()

        S.PROGRESS_UPD.emit('UPLOAD', 100)
        S.FILE_SENT.emit()

class Server(NetworkInterface):
    """ Class definition for the TCP server """
    def __init__(self):
        NetworkInterface.__init__(self)

        self.tcpServer = QtNetwork.QTcpServer()
        self.udpSocket= QtNetwork.QUdpSocket()

        self.timer = QtCore.QTimer()

    # Send a perodic broadcast for discovery
    def broadcast(self):
        self.timer.start(BROADCAST_INTERVAL)
        self.timer.timeout.connect(self.sendDatagram)

    # Datagram to send
    def sendDatagram(self):
        # Code for broadcasting in network
        self.udpSocket.writeDatagram(KEY,QtNetwork.QHostAddress(QtNetwork.QHostAddress.Broadcast),UDP_PORT)

    # Waiting for a TCP connection
    def listen(self):
        # Listening to a specific port
        if not self.tcpServer.listen(port=TCP_PORT):
            print('Error occured')

        # Function is called when new connection is available
        self.tcpServer.newConnection.connect(self.newconnection)

    def newconnection(self):
        if(self.connection):
            return

        # Stops the UPD broadcast
        self.timer.stop()

        # Saves the socket connection
        self.connection = self.tcpServer.nextPendingConnection()

        # Remote terminal ipaddress
        peerAddress = self.connection.peerAddress().toString()

        S.DEVICE_CONNECTED.emit(peerAddress)

        # Codes to execute when connection is dropped
        self.connection.disconnected.connect(self.close)
        self.connection.disconnected.connect(S.DISCONNECTED.emit)

        # Function to run when data to read is available
        self.connection.readyRead.connect(self.readData)

    # Closes socket and server if disconnected
    def close(self):
        if (self.connection):
            self.connection.close()
            self.connection=None
        self.tcpServer.close()

class Client(NetworkInterface):
    """ Class definition for TCP client """
    def __init__(self):
        NetworkInterface.__init__(self)

        self.connection = QtNetwork.QTcpSocket()
        self.udpSocket = QtNetwork.QUdpSocket()

        self.hostlist = []

        self.timer1 = QtCore.QTimer()

    def findHosts(self):
        self.udpSocket.bind(UDP_PORT)
        self.udpSocket.readyRead.connect(self.recvDatagram)

        # Timer to emit hostlist
        self.timer1.start(SCAN_INTERVAL)
        self.timer1.timeout.connect(self.emitHosts)

        S.CONNECT_HOST.connect(self.connect)

    def recvDatagram(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            key=str(datagram, encoding='ascii')
            strHost=host.toString()
            if(key==KEY):
                if(strHost not in self.hostlist):
                    self.hostlist.append(strHost)

    def emitHosts(self):
        # Sending a copy of list
        S.HOST_LIST.emit(self.hostlist.copy())
        self.hostlist.clear()

    def connect(self, host):
        self.timer1.stop()

        self.connection.connectToHost(host, TCP_PORT)

        # Code to run when connection is established
        if(self.connection.waitForConnected(CONNECTION_TIMEOUT)):
            S.DEVICE_CONNECTED.emit(host)

            # Function to run when data to read is available
            self.connection.readyRead.connect(self.readData)

            # Codes to execute when connection is dropped
            self.connection.disconnected.connect(self.close)
            self.connection.disconnected.connect(S.DISCONNECTED.emit)

        # Code to run when connection timeout
        else:
            self.close()
            S.NO_CONNECTION.emit()

    # Closes socket if disconnected
    def close(self):
        self.connection.close()

class NetworkThread(QtCore.QThread):
    """Defining a thread to be used for networking"""
    def __init__(self):
        QtCore.QThread.__init__(self)
        
        self.running = False
        self.mode = None
    
    # Runs in main thread 
    def startThread(self,mode):
        self.mode = mode
        self.start()        
    
    # Runs in seperate thread    
    def run(self):
        # Network objects are created within this thread only
        self.running = True

        if (self.mode == 'CLIENT'):
            client = Client()

            # Finds hosts in the network
            client.findHosts()

        elif(self.mode == 'SERVER'):
            server = Server()

            # Broadcast datagram to everyone
            server.broadcast()

            # Listen for incoming TCP connection
            server.listen()

        # Event loop to prevent thread from terminating
        self.exec_()

    def quit(self):
        self.running = False
        QtCore.QThread.quit(self)

if __name__ == '__main__':
    print('Nothing to run')
else:
    networkThread = NetworkThread()
