# -*- coding:utf-8 -*-

import threading
import socket

HOST = 34525
HOST_FILE = HOST + 1
BUFSIZE = 1024
FBUFSIZE = BUFSIZE * 4


class FileReader(threading.Thread):
    def __init__(self, client, listener, client_ip):
        threading.Thread.__init__(self)
        self.client = client
        self.listener = listener
        self.client_ip = client_ip        
        
    def run(self):
        file_data_from_socket = self.client.recv(BUFSIZE)
        string_massage = bytes.decode(file_data_from_socket, 'utf-8')
            
        string_file_name = self.listener.data_center.translate_message(string_massage=string_massage, speaker_ip=self.client_ip)
        
        file = open(string_file_name, 'wb')
        
        file_data_from_socket = self.client.recv(FBUFSIZE)      
        while (file_data_from_socket):  
                file.write(file_data_from_socket)  
                file_data_from_socket = self.client.recv(FBUFSIZE)  
        file.close()
#         print(self.client)
        self.listener.data_center.chat_frame.acceptFile(file_name=string_file_name, sender_IP=self.client_ip[0])
        self.client.close()

class FileSender(threading.Thread):
    def __init__(self, data_center, client_ip, buffer_massage, file_path):
        self.data_center = data_center
        self.client_ip = client_ip
        self.buffer_massage = buffer_massage
        self.file_path = file_path
        threading.Thread.__init__(self)
        
    def run(self):
        self.filesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.filesock.connect((self.client_ip, HOST_FILE))
        self.filesock.send(self.buffer_massage)
#         
        file_constent = open(self.file_path, 'rb').read()
        self.filesock.sendall(file_constent)
        self.filesock.close()
        

class Sender(threading.Thread):
    def __init__(self, data_center, client_ip, buffer_massage):
        self.data_center = data_center
        self.client_ip = client_ip
        self.buffer_massage = buffer_massage
        threading.Thread.__init__(self)
        

        
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.client_ip, HOST))
        self.sock.send(self.buffer_massage)
        self.sock.close()

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client, listener, client_ip):
        threading.Thread.__init__(self)
        self.client = client
        self.listener = listener
        self.client_ip = client_ip

        
    def run(self):
        string_massage = '';
        chat_data_from_socket = self.client.recv(BUFSIZE)
        while(chat_data_from_socket):
            string = bytes.decode(chat_data_from_socket, 'utf-8')
            string_massage += string
            chat_data_from_socket = self.client.recv(BUFSIZE)
            
#         print(self.client_ip)
        self.listener.data_center.translate_message(string_massage=string_massage, speaker_ip=self.client_ip)
        self.client.close()
#         print("close:", self.client.getpeername())
        
#     def readline(self):
#         rec = self.inputs.readline()
#         if rec:
#             string = bytes.decode(rec, 'utf-8')
#             if len(string)>2:
#                 string = string[0:-2]
#             else:
#                 string = ' '
#         else:
#             string = False
#         return string

# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, data_center , listener_type):
        threading.Thread.__init__(self)
        self.listener_type = listener_type
        self.thread_stop = False
        self.data_center = data_center
        if (listener_type == 0):
            self.port = HOST
        elif(listener_type == 1):
            self.port = HOST_FILE
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(0)
        
    def run(self):
        print('' + str(self.listener_type) + '形监听线程开始.')
        while True:
            if(self.thread_stop == True):
                self.sock.close()
                return
            client, cltadd = self.sock.accept()
            
            if(cltadd[0] not in self.data_center.client_list):
                print('从' + cltadd[0] + '收到一条信息,但是因为他没有在你的好友列表中,所以该信息被舍弃.')
                continue
            
            if(self.listener_type == 0):
#                 如果是chat_listener
                Reader(client=client, client_ip=cltadd , listener=self).start()
                cltadd = cltadd
                print('从' + cltadd[0] + '收到一条信息')
            elif(self.listener_type == 1):
                FileReader(client=client, client_ip=cltadd , listener=self).start()
                cltadd = cltadd
                print('从' + cltadd[0] + '收到一条文件传输信息')
            
#     def stop(self):
#         self.kill_received = True
    def stop(self):  
        self.thread_stop = True 

if __name__ == "__main__":
    lst = Listener(HOST)  # create a listen thread
    lst.start()  # then start
