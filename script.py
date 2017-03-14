#!/usr/bin/env python
# -*- utf8-encoding -*-

import os
import re
from time import gmtime, strftime
import sys

# date and time
def date_time():
	return strftime("%Y-%m-%d %H:%M:%S", gmtime()); # return data with Year-month-day Hour-minute-second
# Append data on existing file
def write_to_file(filename, text):
	with open(filename, mode='a+') as outfile:
		outfile.write("%s\n" % text)
		outfile.close()

dir_="/etc/squid3"
squid = "squid.conf"
commands="""
apt-get update
apt-get install expect # Install expect
apt-get install squid # Install squid
apt-get install apache2-utils
cp squid.conf squid.conf.orig
chmod a-w squid.conf.orig
touch /etc/squid3/squid_passwd
chown proxy /etc/squid3/squid_passwd
initctl show-config squid3 # Start squid at boot
"""
append_conf="""
forwarded_for off
request_header_access Allow allow all
request_header_access Authorization allow all
request_header_access WWW-Authenticate allow all
request_header_access Proxy-Authorization allow all
request_header_access Proxy-Authenticate allow all
request_header_access Cache-Control allow all
request_header_access Content-Encoding allow all
request_header_access Content-Length allow all
request_header_access Content-Type allow all
request_header_access Date allow all
request_header_access Expires allow all
request_header_access Host allow all
request_header_access If-Modified-Since allow all
request_header_access Last-Modified allow all
request_header_access Location allow all
request_header_access Pragma allow all
request_header_access Accept allow all
request_header_access Accept-Charset allow all
request_header_access Accept-Encoding allow all
request_header_access Accept-Language allow all
request_header_access Content-Language allow all
request_header_access Mime-Version allow all
request_header_access Retry-After allow all
request_header_access Title allow all
request_header_access Connection allow all
request_header_access Proxy-Connection allow all
request_header_access User-Agent allow all
request_header_access Cookie allow all
request_header_access All deny all
auth_param basic program /usr/lib/squid3/basic_ncsa_auth /etc/squid3/squid_passwd
acl ncsa_users proxy_auth REQUIRED
http_access allow ncsa_users
"""
user = os.popen('users').read().strip(); #get the current user
os.chdir(dir_); # cd directory
list_of_users = []; # initializing list
adduser = ""
pwd = ""
log = "log.log";

while True: # Repeat the process
	client_ip = raw_input("Enter client's IP: ") 
	adduser = raw_input("Client's user: "); # asking for new username
	pwd = raw_input("Client's password: "); # asking for new password
	ask = raw_input("Do you want to add more <Y/n>").strip(); # Asking to continue
	if ask.lower() != 'y': # if ask var is not equal to Y or y
		break
	else: pass

	if ( not adduser or not pwd ): # test if user and or password is not empty
		print "User and or password should not be empty."; # display an error
	else:
		list_of_users.append(([adduser, pwd])); #insert user and password
print list_of_users
sys.exit()

if re.search(" ", user): # check if user have space in between
	user=user.split() # split it by space
	user=user[0] # get user at index zero
else: pass

if os.path.isfile(log): # test if log.log exists
	os.remove(log); # remove log.log file
else: pass

if os.path.isdir(dir_): # test if directory exists
	for i in commands.split('\n'): # split commands
		os.system(i); # execute commands
	if os.path.isfile("%s.conf" % squid):
		write_to_file('log.log', (date_time() + ' %s successfully copied a backup.' % squid))

	# iterate append_conf
	for i in append_conf.split("\n"):
		check = os.popen("cat %s |grep '%s'" % (squid, i)).read().strip()
		if not check: # if null or empty
			write_to_file(squid, i); # writing into conf file
	os.system("service squid3 restart"); # restart squid
else: 
	print 'Directory %s does not exists!' % dir_;
	sys.exit(); # quit script

