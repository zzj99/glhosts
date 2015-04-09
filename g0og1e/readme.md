Files
------
The scripts in this folder are used to update hosts for g0og1e from specific URLs.
The python version script is strongly recommended, as the shell script version is just a demo for test.

* hosts.py - python2 script, works for Windows, Linux and MacOS.

* hosts.sh - shell script, works for Linux and MacOS. 

Usage
------
To use hosts.py, please make sure you have installed python 2.7.6+ (but NOT 3.x). Just run 'python hosts.py' in the command line with Administrator or root privilege.
In Windows, it is recommended to run the script as Administrator with a batch file, e.g. 'hosts.bat', which contains

       python disk:\path\to\hosts.py

To use hosts.sh, please make sure your hosts DONOT contain google contents, such as 'xx.xx.xx.xx www.google.com'

Acknowledgement
------
The author thank [360kb](http://www.360kb.com/kb/2_122.html) and [txthinking](https://github.com/txthinking/google-hosts) and all the people who share the knowledge for accessing g0og1e very much for their great internet spirit.
