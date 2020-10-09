# GDHSXY_WiFi_Tool
广东财经大学华商学院WiFi认证小工具，可自动获取当前IP和SSID，自动进行WiFi认证
基于Python3.8 tkinter的Windows GUI小工具，界面丑


# 环境依赖
1、Python3.8

2、requests、re、time、ping3、pytesseract、PIL (easy_install Pillow)

* Python安装第三方库的方法：
使用pip命令进行安装，以安装requests库为例：

pip install requests

3、验证码识别插件tesseract（如tesseract-ocr-w64-setup-v5.0.0.20190623.exe）
下载地址：https://digi.bib.uni-mannheim.de/tesseract/
安装最新的x64版本到D:\Tesseract-OCR


# 可编译为exe使用
1. 先安装pyinstaller
pip install pyinstaller

2. 编译
pyinstaller WiFi_Tool.py --hidden-import IntVar --hidden-import StringVar --hidden-import ttk --hidden-import Image --hidden-import BytesIO -w

3、[可选] 创建系统计划任务，解锁电脑自动运行本程序
触发器选择【工作站解锁时】，操作为启动上面编译出来的exe

# 使用说明
修改个人校园网账户信息
WiFi_Tool.py文件中对应校园网登录信息的变量的值：

#=========请修改以下校园网登陆信息==========
1. 校园网账号：
self.username = 'xxxxxxx'

2. 校园网密码：
self.password = '123456789'


# 其他说明
本脚本仅供学习交流，严禁任何形式的商用。
