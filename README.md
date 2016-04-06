Description
------
The simple python script in this folder is used to update hosts for g0og1e from specific URLs, works for Linux, MacOS and Windows.
Please **backup** your `hosts` file before using it.

Path for hosts file

* Windows: `C:\Windows\System32\Drivers\hosts`

* Linux / Mac : `/etc/hosts`

Usage
------
Make sure you have installed python 2.7.6+ (but NOT 3.x). Then run the script with Administrator or root (sudo) privilege.

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

中文描述
-----
这个简单的脚本通过好人们的网址复制hosts，不包成功，用之前最好先备份你的hosts，路径见上面。

由于要修改系统文件hosts，你需要用管理员身份运行`python hosts.py`。

感谢互联网！好人一生平安！
