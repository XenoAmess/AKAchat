# -*- coding:utf-8 -*-
import tkinter
import tkinter.filedialog
import datetime
import time
import socket
import threading

from Listener import * 
import ipaddress

# import ClientData
VERSION = '0.20'
system_color = 'skyblue'
local_user_name = '本机'
local_user_color = 'black'

class ChatFrame(tkinter.Frame):
    def __init__(self, data_center):
        self.data_center = data_center
        self.user_name = local_user_name
        self.user_color = local_user_color
    def start_window(self):
        self.root = self.createWindow()
        tkinter.Frame.__init__(self, self.root)
        self.grid(row=0, column=0, sticky="nsew")
        self.createFrame()
        self.mainloop()

    def createWindow(self):
        root = tkinter.Tk()
    #     filename = tkinter.filedialog.askopenfilename(title="Open File",initialdir='E:/')
    #     print(filename)
        root.title('AKA' + VERSION)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.geometry('320x480')  # 设置了主窗口的初始大小960x540 800x450 640x360    
        return root
    
    def createFrame(self):
#         label_frame_top = tkinter.LabelFrame(self)
        # label_frame_top.pack()

        label_frame_center = tkinter.LabelFrame(self)
        label_frame_center.pack(fill="both", expand=1)

        text_frame = tkinter.LabelFrame(label_frame_center)
        text_frame.pack(fill="both", expand=1)
        
        button_frame = tkinter.LabelFrame(text_frame)
        button_frame.pack(fill="both", expand=0)
        
        file_frame = tkinter.LabelFrame(label_frame_center)
        file_frame.pack(fill="y", expand=0)

#         self.text_frame_l = tkinter.Label(text_frame, text="文件路径：", width=10)
#         self.text_frame_l.pack(fill="none", expand=0, side=tkinter.LEFT)




        self.button_clear = tkinter.Button(button_frame, text="清除", command=self.clear)
        self.button_clear.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)
        
#         self.button_input = tkinter.Button(button_frame, text="输入", command=self.sendMessage)
#         self.button_input.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)
        
        self.button_see = tkinter.Button(button_frame , text="关注", command=self.seeFromIP)
        self.button_see.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)
        
        self.button_ignore = tkinter.Button(button_frame , text="忽略", command=self.ignoreFromIP)
        self.button_ignore.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)

        self.button_setname = tkinter.Button(button_frame , text="换名", command=self.setname)
        self.button_setname.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)
        
        self.button_setcolor = tkinter.Button(button_frame , text="换色", command=self.setcolor)
        self.button_setcolor.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)
        
        self.button_setcolor = tkinter.Button(button_frame , text="文件", command=self.sendFile)
        self.button_setcolor.pack(fill="both", expand=1, side=tkinter.LEFT, anchor=tkinter.SW)
        

        ##########文本框与滚动条
        self.text_dialog_sv = tkinter.Scrollbar(text_frame, orient=tkinter.VERTICAL)  # 文本框-竖向滚动条
        self.text_dialog_sh = tkinter.Scrollbar(text_frame, orient=tkinter.HORIZONTAL)  # 文本框-横向滚动条

        self.text_dialog = tkinter.Text(text_frame, yscrollcommand=self.text_dialog_sv.set,
                                          xscrollcommand=self.text_dialog_sh.set)  # 设置滚动条-不换行
        
        self.text_input = tkinter.Text(text_frame, height=4)




        # 滚动事件
        self.text_dialog_sv.config(command=self.text_dialog.yview)
        self.text_dialog_sh.config(command=self.text_dialog.xview)

        # 布局
        button_frame.pack(fill="x", expand=0, side=tkinter.BOTTOM, anchor=tkinter.SW)
        self.text_input.pack(fill="x", expand=0, side=tkinter.BOTTOM, anchor=tkinter.SW)
        self.text_dialog_sv.pack(fill="y", expand=0, side=tkinter.RIGHT, anchor=tkinter.N)
        self.text_dialog_sh.pack(fill="x", expand=0, side=tkinter.BOTTOM, anchor=tkinter.N)
        self.text_dialog.pack(fill="both", expand=1, side=tkinter.LEFT)
        
        
        # 绑定事件
        self.text_dialog.bind("<Control-Key-a>", self.selectAll)
        self.text_dialog.bind("<Control-Key-A>", self.selectAll)
        self.text_input.bind('<Return>', self.sendMessage)
        
        
        self.text_dialog.configure(state="disabled")
        
        ##########文本框与滚动条end



#         label_frame_bottom = tkinter.LabelFrame(self)
        # label_frame_bottom.pack()

#         pass

    # 文本全选
    def selectAll(self, event):
        self.text_dialog.tag_add(tkinter.SEL, "1.0", tkinter.END)
        # self.text_dialog.mark_set(tkinter.INSERT, "1.0")
        # self.text_dialog.see(tkinter.INSERT)
        return 'break'  # 为什么要return 'break'

    # 文本清空
    def clear(self):
        self.text_dialog.configure(state="normal")
        self.text_dialog.delete(0.0, tkinter.END)
        self.text_dialog.configure(state="disabled")
    
    # 发送按钮事件
    def sendMessage(self, event=0):
#         speaker_name = local_user_name
#         speaker_color = local_user_color
        string_words = self.text_input.get(0.0, tkinter.END)
#         self.putsMessage(string_words, speaker_name, speaker_color)
        self.putsMessage(string_words, speaker_name=self.user_name, speaker_color=self.user_color)
        self.text_input.delete(0.0, tkinter.END)
        
        self.data_center.send_message(string_words)
        return 'break'
    
    def putsMessage(self, string_words , speaker_name=local_user_name, speaker_color=local_user_color, speaker_ip='localhost'):
        self.text_dialog.tag_config(speaker_color, foreground=speaker_color)
        if(len(string_words) > 1):
            self.text_dialog.configure(state="normal")
#             print(len(self.text_input.get(0.0, END)))
            # 在聊天内容上方加一行 显示发送人及发送时间
            msgcontent = speaker_ip + ' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + speaker_name + ':\n' 
            self.text_dialog.insert(tkinter.END, msgcontent, speaker_color)
            self.text_dialog.insert(tkinter.END, string_words + '\n', speaker_color)
            self.text_dialog.see(tkinter.END)
            self.text_dialog.configure(state="disabled")
    
    def seeFromIP(self):
#         self.client_list.add()
        string_input = self.text_input.get(0.0, tkinter.END)[:-1]
        
        self.text_dialog.configure(state="normal")
        self.text_dialog.tag_config(system_color, foreground=system_color)
        
        try:
            ipaddress.ip_address(string_input)
            help_string = '您已经成功添加好友' + string_input + '。如果他也添加你为好友的话，你们俩就能看见对方说的话啦。\n'
            self.text_dialog.insert(tkinter.END, help_string, system_color)
            self.data_center.client_list.add(string_input)
        except:
            help_string = string_input + '不是一个合法的IP地址。\n'
            self.text_dialog.insert(tkinter.END, help_string, system_color)
        finally:
            self.text_dialog.configure(state="disabled")
            self.text_input.delete(0.0, tkinter.END)
        
    def ignoreFromIP(self):
        string_input = self.text_input.get(0.0, tkinter.END)[:-1]
        self.text_dialog.configure(state="normal")
        self.text_dialog.tag_config(system_color, foreground=system_color)
        try:
            self.data_center.client_list.remove(string_input)
            help_string = '您已经成功删除好友' + string_input + '。\n'
            self.text_dialog.insert(tkinter.END, help_string, system_color)
        except KeyError:
            help_string = '您的好友列表里本来就没有' + string_input + '。\n'
            self.text_dialog.insert(tkinter.END, help_string, system_color)
        finally:  
            self.text_dialog.configure(state="disabled")
            self.text_input.delete(0.0, tkinter.END)

        
    def setname(self):
        string_input = self.text_input.get(0.0, tkinter.END)[:-1]
        self.user_name = string_input
        self.text_dialog.tag_config(system_color, foreground=system_color)
        self.text_dialog.configure(state="normal")
        self.text_dialog.insert(tkinter.END, '用户名字成功变更为' + self.user_name + '\n', system_color)
        self.text_dialog.configure(state="disabled")
        self.text_input.delete(0.0, tkinter.END)
#         return 'break'
    def setcolor(self):
        string_input = self.text_input.get(0.0, tkinter.END)[:-1]
        self.text_dialog.configure(state="normal")
        try:
            self.text_dialog.tag_config(string_input, foreground=string_input)
            self.text_dialog.insert(tkinter.END, '用户颜色成功变更为' + string_input + '\n', string_input)
            self.user_color = string_input
        except tkinter.TclError:
            self.text_dialog.tag_config(system_color, foreground=system_color)
            help_string = '然而这并不是合法的颜色呀\n你可以使用一个字符串，指定红色，绿色和蓝色十六进制数字的比例。例如，“＃FFF”是白色的，“＃000000”是黑色的，“＃000fff000”是纯绿色，和“＃00FFFF”是纯青色（绿加蓝）.\n您还可以使用任何本地定义的标准颜色名称。如，white”，“black”，“red”，“green”，“blue”，“skyblue”，“cyan”,“yellow”，“magenta”等.\n'
            self.text_dialog.insert(tkinter.END, help_string, system_color)
            
        finally:
            self.text_dialog.configure(state="disabled")
            self.text_input.delete(0.0, tkinter.END)
#         return 'break'
    def sendFile(self):
        string_input = self.text_input.get(0.0, tkinter.END)[:-1]
        self.text_dialog.tag_config(system_color, foreground=system_color)
        self.text_dialog.configure(state="normal")
        try:
            self.data_center.send_file(string_input)
            self.text_dialog.insert(tkinter.END, '文件发送成功.\n', system_color)
        except:
            help_string = '文件发送失败.请确认输入框内的文件路径是否完全且合法,并且该路径是否对应一个存在的文件.这里提供一个成功的案例:\nc:\\\\1.zip\n'
            self.text_dialog.insert(tkinter.END, help_string, system_color)
              
        finally:
            self.text_dialog.configure(state="disabled")
            self.text_input.delete(0.0, tkinter.END)
    def acceptFile(self, file_name, sender_IP):
        self.text_dialog.tag_config(system_color, foreground=system_color)
        
        self.text_dialog.configure(state="normal")
        
        self.text_dialog.insert(tkinter.END, '您从' + sender_IP + '处收到一个名为' + file_name + '的文件.\n', system_color)
              
        self.text_dialog.configure(state="disabled")
        
        
    
if __name__ == "__main__":
    cha = ChatFrame();
