#!/bin/bash
# @brief   check if google hosts is available, if not, update hosts 
# @usage   (chmod +x *.sh for the first time) sudo ./hosts.sh 
# @author  zzj.99@hotmail.com 
# @date    2015/3/4

# Make sure only root can run this script
if [[ "$(id -u)" != "0" ]]; then
	echo " Sorry, you must be 'root' or use 'sudo' to run this script." 
	exit 1
fi
# detect OS of the user
platform="unknown"
hostsfile=''
unamestr=$(uname)
if [[ "$unamestr" == "Linux" ]]; then
	platform="linux"
	hostsfile='/etc/hosts'
elif [[ "$unamestr" == "Darwin" ]]; then
	platform="mac"
	hostsfile='/etc/hosts'
else
	#unknown OS
	echo " Sorry, this script is only available on Linux/Mac OS." 
	exit 1
fi

# function for updating hosts
updatehosts()
{
	# download the html file
	hostspage="http://www.360kb.com/kb/2_122.html"
	if [[ "${platform}" == 'linux' ]]; then
		echo " try to download hosts from ${hostspage} using wget ..."
		wget -t 2 -T 2 ${hostspage} -O hosts.html 1>/dev/null 2>&1
	elif [[ "${platform}" == 'mac' ]]; then
		echo " try to download hosts from ${hostspage} using curl ..."
		curl -m 5 --retry-delay 2 --retry 2 -o hosts.html ${hostspage} 1>/dev/null 2>&1
	else
		echo ' Sorry, this script is only available on Linux/Mac'
		exit 1
	fi

	# make a backup file
	hostsbak=hosts.$(date +%Y%m%d%H)
	echo " Old hosts is saved as ${hostsbak}, please check it if update fails."
	cp ${hostsfile} ${hostsbak}

	# grab #google lines from html file
	# and remove html tags, replace html white space to white space
	sed -n -e '/^[\t ]*#google.*hosts/,/^[\t ]*#google.*hosts.*end/p' hosts.html | \
		sed -e 's/<[^>]*>//g; s/\&nbsp;/ /g' > google_hosts

	# remove #google lines in old hosts
	sed -e '/^[\t ]*#google.*hosts/,/^[\t ]*#google.*hosts.*end/d' ${hostsfile} > old_hosts

	# combine to get new hosts
	cat old_hosts google_hosts > ${hostsfile} 

	# clean temporary files
	rm hosts.html google_hosts old_hosts

	# compare the new hosts and the old one
	if [[ -n $(diff ${hostsbak} ${hostsfile}) ]]; then
		echo -e " hosts updated!\n"
	else
		echo -e " The hosts on source page is same as current hosts file, please try again later or change the source page.\n"
	fi
}

# start to check hosts
echo 'checking hosts ...'

# if hosts doesn't exist, generate a new one
if [[ ! -e ${hostsfile} ]]; then
	echo "${hostsfile} doesn't exist, we will generate it."
	echo '' > ${hostsfile}
fi

# get the ip address for www.google.com in current hosts
googleip=$(sed -n -e 's/^\([^#]*\)www\.google\.com[\t ]*$/\1/p' ${hostsfile})

# check if google ip address exists
if [[ -n $googleip ]]; then
	echo "google ip found in hosts: $googleip"

	# check if current google ip is available 
	# by downloading the index.html of google with default tool of OS
	if [[ "$platform" == "linux" ]]; then 
		wget -t 2 -T 2 $googleip -O g.html 1>/dev/null 2>&1
	elif [[ "$platform" == "mac" ]]; then
		curl -m 5 --retry-delay 2 --retry 2 -o g.html $googleip 1>/dev/null 2>&1
	fi

	# check if g.html is empty
	if [[ -s g.html ]]; then
		echo " Safe, google ip is still available!"
		rm g.html
		exit 
	else
		echo " google ip is unavailable now, trying to update ..."
		rm g.html
		updatehosts
	fi
else
	echo ' google ip not found in hosts, trying to update ...'
	updatehosts
fi
