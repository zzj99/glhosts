#!usr/bin/env python
# check and update google hosts from specific URL
# written in python version 2.7.6
# works for python version 2.7+, but not python 3
# by zzj.99@hotmail.com
# last updated in 2015/04

import urllib2      # for opening url, python2 grammar
import os           # for interacting with OS
import shutil       # for coping files
import re           # for regular expression
import datetime     # for recording time of updated hosts
import tempfile     # for temporary file
import ctypes       # for windows
import collections  # for OrderedDict

""" function that creates an ordered dictionary from hosts file """
def create_dict(hosts_file):
    new_dict = collections.OrderedDict() # ordered dictionary
    f = open(hosts_file,"r")    
    for line in f:
        match = re.match(r"^\s*(\d+\.\d+\.\d+\.\d+)\s+(.*)\s*",line)
        if (match):
            new_dict[match.group(2)] = match.group(1)
    f.close()
    return new_dict

""" try to find the desired IP address """
def find_ip(hosts, name):
    f = open(hosts, "r")
    ip = ""
    pattern = "^\s*(\d+\.\d+\.\d+\.\d+)\s+" + name + "\s*$"
    for line in f:
        match = re.match(pattern, line, re.I)
        if (match):
            ip = match.group(1)
    f.close()
    return ip

""" check if ip works """
def check_ip(ip):
    print "checking current hosts ..."
    # if ip is found in hosts file
    if (ip):
        # check if current ip works
        url = "http://" + ip
        try:
            response = urllib2.urlopen(url, timeout=5) 
            bWork = True
        except urllib2.URLError, e:
            bWork = False
    else:
        bWork = False

    return bWork

""" download hosts from specific URL """
def download_hosts(hosts_url):
    print "Now downloading hosts from ", hosts_url
    try:
        response = urllib2.urlopen(hosts_url, timeout=5)
        temp_hosts = tempfile.mktemp()
        f = open(temp_hosts, "w")
        for line in response:            
            line = re.sub(r"<[^>]*>", "", line)  # remove html tags
            line = re.sub(r"&nbsp;", " ", line)  # replace &nbsp; to white space
            ip = re.match(r"^\s*\d+\.\d+\.\d+\.\d+", line) # ip
            comment = re.match(r"^\s*#",line) # comments
            if (ip or comment):
                f.write(line)
        f.close()
    except urllib2.URLError, e:
        print "Can't reach the URL for updating hosts!"

    return temp_hosts

""" write values in hosts_dict into hosts file"""
def write_hosts(hosts, hosts_dict, hosts_url):
    # make a backup for hosts
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    hosts_bak = "hosts."+ date
    shutil.copyfile(hosts, hosts_bak)
    print "Old hosts is saved to current directory as ", hosts_bak
    
    # update hosts dictionary ( key is name, value is ip )
    print "Updating hosts ..."
    # open file for writing hosts 
    f = open(hosts, "w")
    
    # write update information
    info = "# based on " + hosts_url + "\n# last update: " + date + "\n"
    f.write(info) 
    
    # write hosts from hosts dictionary
    for name, ip in hosts_dict.items():
        line = ip + "  " + name + "\n"
        f.write(line)
    f.close()
    return

""" update hosts with specific URL """
def update_hosts(hosts, hosts_url):
    # try to download hosts from specific URL
    temp_hosts = download_hosts(hosts_url)
    # check if downloaded hosts works
    if (temp_hosts):
        new_dict = create_dict(temp_hosts)
	works = check_ip(new_dict["www.google.com"])
	if (works):
            hosts_dict = create_dict(hosts)
            hosts_dict.update(new_dict)
            write_hosts(hosts, hosts_dict, hosts_url)
	    succeed = True
            print "Congratulations! Please see updated hosts in ", hosts
	else:
	    print "Unfortunately the downloaded ip doesn't work :-("
	    succeed = False
    else:
	print "Unfortunately the URL can not be reached at this time :-("
	succeed = False
    
    return succeed

""" main routine, update hosts if need, change url if failed """
def check_update():
    # check if user is admin, for modifing the hosts file
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

    # if no hosts file, create it
    if (not os.path.isfile(hosts)):
	f=open(hosts,'w')
	f.close()
    
    ip = find_ip(hosts, "www.google.com")
    works = check_ip(ip)
    if (works):
	print "Congratulations, current ip still works :-)"
    else:
	urls = ["http://www.360kb.com/kb/2_122.html", \
		"http://freedom.txthinking.com/hosts"]
	succeed = False
	iurl = 0
	while ((not succeed) and (iurl < len(urls)) ):
	    succeed = update_hosts(hosts, urls[iurl])
	    iurl += 1
    
    return

# default usage
if __name__ == '__main__':
    check_update()
