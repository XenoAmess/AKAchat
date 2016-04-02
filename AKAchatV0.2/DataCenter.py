# -*- coding:utf-8 -*-

import threading
import socket
from ChatFrame import *
from Listener import *
import struct
import os


PACKKEY_SWITCH = '!i1020s'
PACKKEY_CHAT = '!i50si50si908s'
# 用户名长度,用户名,用户颜色长度,用户颜色,聊天信息长度,聊天信息
PACKKEY_FILE = '!i1016s'
# 文件名长度,文件名



class DataCenter():
    def __init__(self):
        self.client_list = set()
        self.listener = Listener(data_center=self, listener_type=0)
        self.listener.start()
        self.fileListener = Listener(data_center=self, listener_type=1)
        self.fileListener.start()
        self.chat_frame = ChatFrame(self)
        self.chat_frame.start_window()
        
    def translate_message(self, string_massage, speaker_ip=('未知来源', 0)):
        
        
        string_massage = string_massage.ljust(BUFSIZE)
        message_buffer = bytes(string_massage, "utf-8")
        message_buffer = message_buffer[0:BUFSIZE]
        
        message_type, message_content = struct.unpack(PACKKEY_SWITCH, message_buffer)
          
        if (message_type == 0):
            # 先闲置吧
            pass
        elif(message_type == 1):
            # 聊天信息包
            len_name, buffer_speaker_name, len_color, buffer_speaker_color, len_words, buffer_string_words = struct.unpack(PACKKEY_CHAT, message_content)
            
            
            speaker_name = str(buffer_speaker_name, "utf-8")
            speaker_color = str(buffer_speaker_color, "utf-8")
            string_words = str(buffer_string_words, "utf-8")
              
            speaker_name = speaker_name[:len_name]
            speaker_color = speaker_color[:len_color]
            string_words = string_words[:len_words]
            self.chat_frame.putsMessage(string_words=string_words, speaker_name=speaker_name, speaker_color=speaker_color, speaker_ip=speaker_ip[0])
        elif(message_type == 2):
            len_file_name, buffer_file_name = struct.unpack(PACKKEY_FILE, message_content)
            string_file_name = str(buffer_file_name, "utf-8")
            string_file_name = string_file_name[:len_file_name]
            return string_file_name
        
    def send_message(self, string_words): 
        buffer_user_name = bytes(self.chat_frame.user_name, encoding="utf8")
        buffer_user_color = bytes(self.chat_frame.user_color, encoding="utf8")
        buffer_words = bytes(string_words, encoding="utf8")
        message_content = struct.pack(PACKKEY_CHAT, len(self.chat_frame.user_name), buffer_user_name, len(self.chat_frame.user_color), buffer_user_color, len(string_words), buffer_words)
        message_buffer = struct.pack(PACKKEY_SWITCH, 1, message_content)
        
#         buffer_massage = bytes(buffer_massage, encoding="utf8")
        
        for client_ip in self.client_list:
            self.send_massage_to_somebody(message_buffer, client_ip)
            
    def send_massage_to_somebody(self, buffer_massage, client_ip):
        Sender(data_center=self, client_ip=client_ip, buffer_massage=buffer_massage).start()
        
        
    def send_file(self, string_file_path): 
        string_file_name = os.path.basename(string_file_path)
        len_file_name = len(string_file_name)
        buffer_file_name = bytes(string_file_name, encoding="utf8")
        
        message_content = struct.pack(PACKKEY_FILE, len_file_name, buffer_file_name)
        message_buffer = struct.pack(PACKKEY_SWITCH, 2, message_content)
        
#         buffer_massage = bytes(buffer_massage, encoding="utf8")

        for client_ip in self.client_list:
            self.send_file_to_somebody(buffer_massage=message_buffer, client_ip=client_ip, file_path=string_file_path)
            
    def send_file_to_somebody(self, buffer_massage, client_ip, file_path):
        FileSender(data_center=self, client_ip=client_ip, buffer_massage=buffer_massage, file_path=file_path).start()
        
        

data_center = DataCenter()
data_center.listener.stop()


