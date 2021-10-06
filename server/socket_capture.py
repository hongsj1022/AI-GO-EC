import socket
import cv2
import numpy
from select import *
from _thread import *
import queue
import threading

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


class BufferlessSocketCapture:
    def __init__(self, port, isCenter=False):
        self.HOST = ''
        self.PORT = port
        self.isCenter = isCenter

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socketList = []
        self.q = queue.Queue()

        self.thr = threading.Thread(target=self._socket_bind)
        self.thr.daemon = True
        self.thr.start()

        self.socket_connection = False


    def _reader(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = '2'
                client_socket.send(message.encode())

                length = recvall(client_socket, 16)
                stringData = recvall(client_socket, int(length))
                data = numpy.frombuffer(stringData, dtype='uint8')
                decimg = cv2.imdecode(data, 1)
                if self.isCenter:
                    cv2.imwrite('/home/aigo/detect/image.jpg', decimg)
                if not self.q.empty():
                    try:
                        self.q.get_nowait()
                    except queue.Empty:
                        pass
                self.q.put(decimg)

            except ConnectionResetError as e:
                print('connection error')
                break
        client_socket.close()
    
    def isConnected(self):
        return self.socket_connection

    def read(self):
        return True, self.q.get()


    def _socket_bind(self):
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        self.socketList.append(self.server_socket)

        while True:
            try:
                read_socket, _, _ = select(self.socketList, [], [], 1)
                for sock in read_socket:
                    if sock == self.server_socket:
                        client_socket, addr = self.server_socket.accept()
                        self.socket_connection = True
                        print(addr)
                        start_new_thread(self._reader, (client_socket, ))            
            
            except KeyboardInterrupt:
                break

        self.server_socket.close()
