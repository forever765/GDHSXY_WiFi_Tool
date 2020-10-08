#Author: forever765
#v0.1，2020-09-27，初版
#v0.2，2020-10-05，加入自动认证

import os
import re
import time
import json
import ping3
import base64
import socket
import tkinter
import requests
import threading
import subprocess
import webbrowser
import pytesseract
import tkinter.messagebox
from PIL import Image
from io import BytesIO
from tkinter import ttk
from tkinter import IntVar
from tkinter import StringVar

class HSXY_WiFi(tkinter.Frame):
    def __init__(self, master=None):
        ### Change me ###
        self.wlanacip = '183.56.17.66'
        self.username = '改成你自己的账户名'
        self.password = base64.b64encode(b'改成你自己的密码').decode('ascii')
        ### Change me ###

        tkinter.Frame.__init__(self, master)
        self.Window_Base_Setting()
        self.focus='yes'
        #动态刷新Label
        self.Dynamic_Display()
        #加载按钮
        self.Button()
        #动态-every 0.5s-检查焦点
        self.Check_Focus()
          
    def Window_Base_Setting(self):
        #bg_image = tkinter.PhotoImage(file ="D:\\Script\\bg.gif")
        #x = tkinter.Label (image = bg_image)
        #x.grid(row = 6, column = 0)
        width = 400
        height = 150
        screenwidth = window.winfo_screenwidth() 
        screenheight = window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
        window.geometry(alignstr)
        window.title("广财华商WiFi连接工具   By: forever765")
        #window.iconbitmap(r'D:\Script\hsxy.ico')
        window.configure(bg='#66c0ff')
        window.attributes("-topmost", True)
        window.resizable(False, False)

    def Dynamic_Display(self):
        #动态显示段
        #动态-时间
        self.now = StringVar()
        self.Time = tkinter.Label(window, textvariable=self.now)
        self.Time.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.Update_Time()
        window.grid_columnconfigure(1, weight=1)

        #动态-本机IP
        self.ip = StringVar()
        self.ipaddr = tkinter.Label(window, textvariable=self.ip)
        self.ipaddr.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        self.Get_IP()

        #动态-当前SSID
        self.ssid = StringVar()
        self.ssid_label = tkinter.Label(window, textvariable=self.ssid)
        self.ssid_label.grid(row=0, column=6, padx=2, pady=2, sticky="e")
        self.Get_SSID()

        #动态-AC连通性
        self.ac = StringVar()
        self.ac_stat = tkinter.Label(window, textvariable=self.ac, fg="green")
        self.ac_stat.grid(row=1, column=6, padx=2, pady=2, sticky="e")
        self.Ping_AC()

        #动态-粗略检测Internet连通性
        self.i = StringVar()
        self.i_stat = tkinter.Label(window, textvariable=self.i, fg="green")
        self.i_stat.grid(row=2, column=6, padx=2, pady=2, sticky="e")
        self.Ping_Internet()

        #按需刷新-验证码识别结果-Label
        self.captcha_result = StringVar()
        self.captcha_result.set('未开始自动认证')
        self.captcha_result_lable = tkinter.Label(window, textvariable=self.captcha_result)
        self.captcha_result_lable.grid(row=3, column=0, padx=2, pady=2, sticky="w")

    def Button(self):
        #按钮段
        B = ttk.Button(window, text="连接HSXY_Young", command = self.Connect_WiFi)
        B.grid(row=1, column=0, padx=2, pady=2, sticky="w")

        C = ttk.Button(window, text ="重启无线网卡", command = self.Reset_NIC)
        C.grid(row=2, column=0, padx=2, pady=2, sticky="w")

        D = ttk.Button(window, text ="手动合成URL", command = self.Generate_URL)
        D.grid(row=1, column=1, padx=2, pady=2)

        E = ttk.Button(window, text ="检查联网状态", command = self.Check_Real_Status_Base)
        E.grid(row=2, column=1, padx=2, pady=2)

        Auto_Auth_Bottom = ttk.Button(window, text ="自动认证", command = self.Auto_Auth)
        Auto_Auth_Bottom.grid(row=4, column=1, padx=2, pady=2)

    def Update_Time(self):
        if self.focus == 'yes':   
            self.now.set(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.th_time = threading.Timer(1.0, self.Update_Time)
        self.th_time.setDaemon(True)
        self.th_time.start()

    def Ping_AC(self):
        if self.focus == 'yes':
            try:
                ping_ac_r = ping3.ping('125.88.59.131')
            except:
                self.ac_stat.configure(fg="red")
                self.ac.set('AC连通性：failed')
            else:
                if ping_ac_r == 0:
                    self.ac_stat.configure(fg="red")
                    self.ac.set('AC连通性：failed')
                else:
                    self.ac_stat.configure(fg="green")
                    self.ac.set('AC连通性：ok')
        self.th_pingac = threading.Timer(1.0, self.Ping_AC)
        self.th_pingac.setDaemon(True)
        self.th_pingac.start()

    def Ping_Internet(self):
        if self.focus == 'yes':
            try:
                ping_internet_r = ping3.ping('223.5.5.5')
            except:
                self.i_stat.configure(fg="red")
                self.i.set('Internet：failed')
            else:
                if ping_internet_r == 0 or ping_internet_r == None:
                    self.i_stat.configure(fg="red")
                    self.i.set('Internet：failed')
                else:
                    self.i_stat.configure(fg="green")
                    self.i.set('Internet：ok')
        self.th_pingi = threading.Timer(1.0, self.Ping_Internet)
        self.th_pingi.setDaemon(True)
        self.th_pingi.start()

    def Get_SSID(self):
        if self.focus == 'yes':
            try:
                #结果会有SSID和BSSID，排除BSSID
                ssid_raw = (os.popen('netsh wlan show interfaces | findstr SSID | findstr /V BSSID')).read()
                self.curr_ssid = ssid_raw.split(':')[1].replace(' ','').replace('\n','')
                #旧方案
                #ssid_raw = (os.popen('netsh wlan show interfaces | findstr "配置文件"')).read()
                #self.ssid = ssid_raw.split('\n')[1].split(' ')[20]
            except:
                self.ssid.set('SSID：未连接')
                self.ssid_label.configure(fg="red")
            else:
                if self.curr_ssid == None:
                    self.ssid.set('SSID：未连接')
                    self.ssid_label.configure(fg="red")
                #自己的手机热点
                elif self.curr_ssid == 'dog':
                    self.ssid.set('SSID：手机热点')
                    self.ssid_label.configure(fg="green")
                else:
                    self.ssid.set('SSID：' + self.curr_ssid)
                    self.ssid_label.configure(fg="green")
        self.th_getssid = threading.Timer(1.0, self.Get_SSID)
        self.th_getssid.setDaemon(True)
        self.th_getssid.start()

    def Get_IP(self):
        if self.focus == 'yes':
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8',80))
                self.ipaddr = s.getsockname()[0]
            except:
                self.ip.set('本机IP：IP获取失败！')
            else:
                self.ip.set('本机IP：'+self.ipaddr)
                return(self.ipaddr)
        self.th_getip = threading.Timer(1.0, self.Get_IP)
        self.th_getip.setDaemon(True)
        self.th_getip.start()

    def Connect_WiFi(self):
        try:
            connect = os.popen('netsh wlan connect name=HSXY_Young')
            connect_r = connect.read()
        except Exception as e:
            tkinter.messagebox.showinfo( "结果", "WiFi连接失败，未知异常！"+e)
        else:
            if '没有无线接口' in connect_r:
                tkinter.messagebox.showinfo( "结果", "WiFi连接失败，网卡接口丢失！")
            elif '成功' in connect_r:
                tkinter.messagebox.showinfo( "结果", "WiFi HSXY-Young连接成功！")
            else:
                tkinter.messagebox.showinfo( "结果", "连接异常："+connect_r)

    def Reset_NIC(self):
        try:
            close_nic = os.popen('netsh interface set interface WLAN disabled')
            tkinter.messagebox.showinfo( "执行结果", close_nic.read())
            time.sleep(1)
            open_nic = os.popen('netsh interface set interface WLAN enabled')
            tkinter.messagebox.showinfo( "执行结果", open_nic.read())
        except Exception as e:
            tkinter.messagebox.showinfo( "执行结果", "网卡重启失败！\n"+e)
            return 444
        else:
            tkinter.messagebox.showinfo( "执行结果", "重启无线网卡完成！")
            return 0

    def Check_Real_Status_Base(self):
        th_chk_real_base=threading.Thread(target=self.Check_Real_Status)
        th_chk_real_base.setDaemon(True)
        th_chk_real_base.start()

    def Check_Real_Status(self):
        try:
            r = requests.get('https://www.baidu.com', timeout=2)
        except:
            tkinter.messagebox.showinfo( "结果", "网络未通！")
        else:
            if r.status_code == 200:
                tkinter.messagebox.showinfo( "结果", "已经联网！")
            else:
                tkinter.messagebox.showinfo( "结果", "网络未通！")

    def Generate_URL(self):
        base_url = 'http://125.88.59.131:10001/qs/index_gz.jsp?wlanacip=' + self.wlanacip + '&wlanuserip=' + self.ipaddr
        webbrowser.open(base_url)

    def Check_Focus(self):
        if window.focus_get() == None:
            self.focus = 'no'
        else:
            self.focus = 'yes'
        self.th_chk_f = threading.Timer(0.5, self.Check_Focus)
        self.th_chk_f.setDaemon(True)
        self.th_chk_f.start()

    def Get_JSID(self):
        #建立统一session
        self.session = 	requests.Session()
        Auto_URL = 'http://125.88.59.131:10001/qs/index_gz.jsp?wlanacip=' + self.wlanacip + '&wlanuserip=' + self.ipaddr
        Get_Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',}
        JSID_Return = self.session.get(url=Auto_URL, headers=Get_Headers, timeout=5)
        #print(JSID_Return.headers)
        try:
            js_id = JSID_Return.headers['Set-Cookie'].split('=')[1]
        except:
            print('返回响应有误，未获取到JSESSIONID')
            self.session.close()
            return(444)
        else:
            if js_id == '':
                tkinter.messagebox.showerror( "未知错误", "未获取到JSESSIONID")
                self.session.close()
                return(444)
            else:
                jsid = js_id.replace('; path','')
                return(jsid)
                #print('JSID= ',self.jsid)

    def Parse_Captcha(self):
        pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
        TimeStamp_13 = int(round(time.time() * 1000))
        Code_URL = 'http://125.88.59.131:10001/common/image_code.jsp?time=' + str(TimeStamp_13)
        #获取验证码图片
        code_img = (self.session.get(Code_URL)).content
        #新建Image对象，读取图片
        image = Image.open(BytesIO(code_img))
        #转灰度图像
        image = image.convert('L')
        #image.show()
        try:
            self.Captcha_Result = pytesseract.image_to_string(image)
        except Exception as e:
            print('pytesseract执行出错：',e)
        #干掉验证码中识别错误的空格、特殊符号
        self.Captcha_Result = self.Captcha_Result.strip()
        self.Captcha_Result = self.Captcha_Result.replace(' ','').replace('-','')

        if len(self.Captcha_Result) == 4:
            print('验证码识别成功：',self.Captcha_Result)
            self.captcha_result.set('验证码识别结果：'+self.Captcha_Result)
            self.captcha_result_lable.configure(fg="green")
            return(0)
        elif self.Captcha_Result == ' ':
            #OCR失败
            self.Parse_Captcha()
        else:
            print(self.Captcha_Result,', 解析验证码失败，重试中')
            self.Parse_Captcha()

    def Auto_Auth(self):
        #Auth_URL = 'http://125.88.59.131:10001/qs/index_gz.jsp?wlanacip='+ self.wlanacip +'&wlanuserip='+self.ipaddr
        Auth_URL = 'http://125.88.59.131:10001/ajax/login'
        #获取JSID
        JSID_R = self.Get_JSID()
        if JSID_R == 444:
            tkinter.messagebox.showerror( "执行结果", "JSID获取失败，取消认证！")
        else:
            #获取JSID成功后，解析验证码
            if self.Parse_Captcha() == 0:
                Post_Headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Content-Length': '108',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie': 'JSESSIONID=' + JSID_R,
                    'DNT': '1',
                    'Host': '125.88.59.131:10001',
                    'Origin': 'http://125.88.59.131:10001',
                    'Pragma': 'no-cache',
                    'Referer': Auth_URL,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                Post_Data = {
                    'wlanuserip': self.ipaddr,
                    'wlanacip': self.wlanacip,
                    'username': self.username,
                    'password': self.password,
                    'code': self.Captcha_Result,
                }

                #开始认证
                try:
                    print('go')
                    EndResult = self.session.post(url=Auth_URL, headers=Post_Headers, data=Post_Data, timeout=5) 
                except Exception as e:
                    #print('认证请求出错：',e)
                    tkinter.messagebox.showerror( "执行结果", '认证请求出错：'+e)
                else:
                    FinalR = json.loads(EndResult.text)
                    RCode = FinalR['resultCode']
                    RInfo = FinalR['resultInfo']
                    if RCode == 0:
                        tkinter.messagebox.showinfo( "执行结果", "认证成功！")
                    elif RCode == 11063000:
                        tkinter.messagebox.showerror( "执行结果", "认证失败：验证码错误！")
                    elif RCode == 13002000:
                        tkinter.messagebox.showinfo( "执行结果", "已经认证，请勿重复认证！")
                    elif RCode == 13017000:
                        tkinter.messagebox.showinfo( "执行结果", "帐号状态为暂停")
                    else:
                        tkinter.messagebox.showinfo( "执行结果", "认证失败，原因：" + RInfo)

if __name__ == "__main__":
    window=tkinter.Tk()
    HSXY_WiFi(master=window)
    #开始主界面死循环
    window.mainloop()
