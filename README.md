Description
------
The simple python script in this folder is used to update hosts for g0og1e from specific URLs, works for Linux, MacOS and Windows.
Please **backup** your `hosts` file before using it.

这个简单的脚本从好人们的网址里提取地址，不包成功，用之前最好先备份你的hosts。

* Windows path: `C:\Windows\System32\Drivers\hosts`
* Linux / Mac : `/etc/hosts`

Usage
------
Make sure you have installed python 2.7.6+ (but NOT 3.x). Then run the script with Administrator or root (sudo) privilege.

由于要修改系统文件，你需要用管理员身份在命令行中输入以下命令：

* Linux / Mac  

```shell
python hosts.py   # as root, or: sudo python hosts.py
```

* Windows 

```shell
python hosts.py   # as Administrator
```
In Windows, it is recommended to run the script as Administrator with a batch file, e.g. 'hosts.bat', which contains the above command and path to the script file.

Acknowledgement
------
The author thank all the people who share the knowledge for accessing g0og1e very much for their great internet spirit.

感谢分享！好人一生平安！
