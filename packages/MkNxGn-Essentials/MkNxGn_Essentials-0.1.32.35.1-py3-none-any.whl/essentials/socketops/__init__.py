import struct, socket, threading, json, os, pickle
from essentials import tokening

def SocketDownload(sock):
    try:
        data = b""
        payload_size = struct.calcsize(">L")
        while True:
            while len(data) < payload_size:
                data += sock.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += sock.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            xData = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            return xData
    except:
        raise ConnectionError("Connection Error")

def SocketUpload(sock, data):
    try:
        data = pickle.dumps(data, 0)
        size = len(data)
        sock.sendall(struct.pack(">L", size) + data)
    except:
        raise ConnectionError("Connection Error")

def HostServer(HOST, PORT, connections=5):
    PORT = int(os.getenv('PORT', PORT))
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen(connections)
    return sock

def ConnectorSocket(HOST, PORT):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    return clientsocket


class Socket_Server_Host:
    def __init__(self, HOST, PORT, on_connection_open, on_data_recv, connections=5, on_connection_close=False, daemon=True):
        """Host your own Socket server to allows connections to this computer.

        Args:
            HOST (:obj:`str`): Your hosting IP Address for this server.
            PORT (:obj:`int`): Which port you'd like to host this server on.
            on_connection_open (:obj:`def`): The function to call when you get a new connection.
            on_data_recv (def): The function to call when you receive data from a connection.
            connections (:obj:`int`, optional): How many connections to allow at one time.
            on_connection_close (:obj:`def`, optional): The function to call when a connection is closed.
            daemon (:obj:`bool`, optional): If you'd like the server to close when the python file closes or is interrupted. 
        """
        self.on_connection_open = on_connection_open
        self.on_connection_close = on_connection_close
        self.on_data_recv = on_data_recv
        self.HOST = HOST
        self.PORT = PORT
        self.connections = {}
        self.running = True
        self.server = HostServer(HOST, PORT, connections)
        self.broker = threading.Thread(target=self.ConnectionBroker, daemon=daemon)
        self.broker.start()

    def ConnectionBroker(self):
        while self.running:
            conn, addr = self.server.accept()
            conID = tokening.CreateToken(12, self.connections)
            connector = Socket_Server_Client(conn, addr, conID, self.on_data_recv, on_close=self.on_connection_close)
            self.connections[conID] = connector
            self.on_connection_open(connector)

    def Shutdown(self):
        self.running = False
        for con in self.connections:
            self.connections[con].shutdown()
        self.connections = {}

    def CloseConnection(conID):
        self.connections[conID].shutdown()
        del self.connections[conID]

class Socket_Server_Client:

    def __init__(self, socket, addr, conID, on_data, on_close):
        self.socket = socket
        self.addr = addr
        self.conID = conID
        self.on_data = on_data
        self.on_close = on_close
        self.running = True
        self.data_Recv = threading.Thread(target=self.__data_rev__, daemon=True)
        self.data_Recv.start()

    def shutdown(self):
        try:
            self.on_close(self)
        except:
            pass
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        

    def send(self, data, is_json=True):
        if self.running == False:
            raise ConnectionResetError("No Connection")
        if is_json:
            data = json.dumps(data)
        try:
            SocketUpload(self.socket, data)
        except:
            self.shutdown()

    def __data_rev__(self):
        while self.running:
            try:
                data = SocketDownload(self.socket)
            except:
                self.shutdown()
                return
            try:
                data = json.loads(data)
            except:
                pass
            self.on_data(data, self)


class Socket_Connector:

    def __init__(self, HOST, PORT, on_data_recv):
        self.running = True
        self.HOST = HOST
        self.PORT = PORT
        self.socket = ConnectorSocket(HOST, PORT)
        self.on_data_recv = on_data_recv
        self.data_Recv = threading.Thread(target=self.__data_rev__, daemon=True)
        self.data_Recv.start()

    def send(self, data, is_json=True):
        if self.running == False:
            raise ConnectionResetError("No Connection")
        if is_json:
            data = json.dumps(data)
        try:
            SocketUpload(self.socket, data)
        except:
            self.shutdown()

    def shutdown(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def __data_rev__(self):
        while self.running:
            try:
                data = SocketDownload(self.socket)
            except:
                self.shutdown()
                return
            try:
                data = json.loads(data)
            except:
                pass
            self.on_data_recv(data)