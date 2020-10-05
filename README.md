# GDHSXY
广东财经大学华商学院WiFi认证小工具-Windows GUI

# 环境依赖
基于Python3.8
requests、re、time、ping3、pytesseract
PIL (easy_install Pillow)

* Python安装第三方库的方法：
使用pip命令进行安装，以安装requests库为例：

pip install requests

# 使用说明
修改个人校园网账户信息
修改Login_in.py文件中对应校园网登录信息的变量的值：

# =========请修改以下校园网登陆信息==========
# 1.校园网账号：
id = '1825010xxxx'
# 2.校园网密码：
password = '123456789'
# 3.校园网ip地址：
wlan_user_ip = '172.27.xxx.xx'
# 4.设备mac地址：
mac = 'A8-xx-xx-xx-xx-xx'
# ======================================
为获取设备mac地址与宿舍墙上端口所分配的ip地址，可ssh连接路由器后使用以下命令：

ifconfig 

# 添加周期性任务（定时任务）
cron命令可以周期性地执行任务，使用前先确定crond进程是否启动，可通过以下命令查看：

ps -ef|grep crond
如未启动，可通过以下命令启动、重启 ：

/sbin/service crond start
/sbin/service crond restart
编辑时程表，输入命令后选择自己最熟悉的文本编辑器即可：

crontab -e
时程表格式如下，根据实际情况修改定时参数以及脚本路径并保存即可：

0 6-12/3 * 12 * /usr/bin/backup   
# 在 12 月内, 每天的早上 6 点到 12 点，每隔 3 个小时 0 分钟执行一次 /usr/bin/backup

20 0-23/2 * * * echo "haha"
# 每月每天的午夜 0 点 20 分, 2 点 20 分, 4 点 20 分....执行 echo "haha"

其他说明
本脚本仅供学习交流，严禁任何形式的商用。
