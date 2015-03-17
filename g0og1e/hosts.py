#!usr/bin/env python
# check and update google hosts from specific URL
# written in python version 2.7.6
# works for python version 2.7+, but not python 3
# by zzj.99@hotmail.com
# last updated in 2015/03

import urllib2      # for opening url, python2 grammar
import os           # for interacting with OS
import shutil       # for coping files
import re           # for regular expression
import datetime     # for recording time of updated hosts
import tempfile     # for temporary file
import ctypes       # for windows
import collections  # for OrderedDict

# check if user is admin, required for changing the hosts file
try:
    is_admin = (os.getuid() == 0)
except AttributeError:
    is_admin = (ctypes.windll.shell32.IsUserAnAdmin() != 0)

if (not is_admin):
    if (os.name == 'nt'): # Windows
        exit("You need to run this script as administrator.")
    else: # Linux or MacOS
        exit("You need to run this script as root or use 'sudo'.")

# hosts path according to operating system
hosts=""
if (os.name == 'nt'): # Windows
    hosts = 'C:\Windows\System32\Drivers\etc\hosts'
else: # Linux or MacOS
    hosts = '/etc/hosts'

""" function that creates an ordered dictionary from hosts file """
def create_hosts_dict(hosts_file):
    hosts_dict = collections.OrderedDict() # ordered dictionary
    f = open(hosts_file,"r")    
    for line in f:
        pattern = re.match(r"^\s*(\d+\.\d+\.\d+\.\d+)\s+(.*)\s*",line)
        if (pattern):
            hosts_dict[pattern.group(2)] = pattern.group(1)

    return hosts_dict

""" function for updating hosts """
def update_hosts():
    # Websites that contain hosts, in case the selected one is unavailable
    # http://freedom.txthinking.com/hosts
    # http://www.360kb.com/kb/2_122.html
    hosts_url = "http://freedom.txthinking.com/hosts"

    # try to reach the URL for updating hosts
    try:
        response = urllib2.urlopen(hosts_url, timeout=5)
        now = datetime.datetime.now()
        temp_hosts = tempfile.mktemp()
        f_hosts = open(temp_hosts, "w")
        for i, line in enumerate(response):            
            line = re.sub(r"<[^>]*>", "", line)  # remove html tags
            line = re.sub(r"&nbsp;", " ", line)  # replace &nbsp; to white space
            ip = re.match(r"^\s*\d+\.\d+\.\d+\.\d+", line) # ip
            comment = re.match(r"^\s*#",line) # comments
            if (ip or comment):
                f_hosts.write(line)

        f_hosts.close()
        
        # make a backup for hosts
        date = now.strftime("%Y%m%d")
        hosts_bak = "hosts."+ date
        shutil.copyfile(hosts, hosts_bak)
        print "old hosts is copied to current directory as ", hosts_bak
        
        # update hosts dictionary ( key is name, value is ip )
        hosts_dict = create_hosts_dict(hosts)
        new_dict = create_hosts_dict(temp_hosts)
        hosts_dict.update(new_dict)

        # open file for writing hosts 
        hosts_file = open(hosts, "w")

        # write update information
        info = "# based on " + hosts_url + "\n# last update: " + date + "\n"
        hosts_file.write(info) 
        
        # write hosts from hosts dictionary
        for name, ip in hosts_dict.items():
            line = ip + "  " + name + "\n"
            hosts_file.write(line)
        hosts_file.close()
        print "hosts updated! see ",hosts

    except urllib2.URLError, e:
        print ("Can't reach the URL for updating hosts!")

    return

""" check if google ip exists and works, if not, update hosts """
def check_and_update_hosts():
    print "checking current hosts ..."
    # try to get the ip address for "www.google.com" in current hosts file
    hosts_file = open(hosts, "r")
    googleip=""
    for line in hosts_file:
        # look for line contain google ip, ignore case
        match = re.match(r"^\s*(\d+\.\d+\.\d+\.\d+)\s+www.google.com\s*$", line, re.I)
        if (match):
            googleip = match.group(1)

    hosts_file.close()

    # if google ip is found in hosts file
    if (googleip):
        print "google ip found: ", googleip
        # check if current google ip works
        google_url = "http://" + googleip
        try:
            response = urllib2.urlopen(google_url, timeout=5)
            print "google ip still works, need not update :-)"
        except urllib2.URLError, e:
            print "url error, try to update hosts ..."
            update_hosts()

    else:
        print "google ip not found, try to update hosts ..."
        update_hosts()

    return

# run script to check and update hosts
check_and_update_hosts()
