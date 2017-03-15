#!/usr/bin/env python
# -*- utf8-encoding -*-

import os
import re
from time import gmtime, strftime
import sys
import getpass

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
apt-get install squid
apt-get install apache2-utils
cp /etc/squid3/squid.conf /etc/squid3/squid.conf.orig
chmod 0777 /etc/squid3/squid.conf
chmod a-w /etc/squid3/squid.conf.orig
touch /etc/squid3/squid_passwd
chown proxy /etc/squid3/squid_passwd
initctl show-config squid3 
"""
file_ = "Ubuntu Suid Setup Proxy.txt"
if os.path.isfile(file_):
	append_conf = os.popen("cat '%s'" % file_).readlines()
else: sys.exit('File %s does not exists!' % file_);

user = os.popen('whoami').read().strip(); #get the current user
list_of_users = []; # initializing list
adduser = ""
pwd = ""
log = "log.log";
curr_dir = os.getcwd().strip()

admin_passwd = getpass.getpass(prompt='Enter your administrative password: ').strip()

test_login=os.popen("./myssh.exp %s" % admin_passwd).read()
if not re.search('Welcome', test_login):
	sys.exit('Invalid password!')
else: pass

while True: # Repeat the process
	adduser = raw_input("Enter your client's username: ").strip(); # asking for new username
	pwd = getpass.getpass(prompt="Enter your Client's password: ").strip(); # asking for new password
	if ( not adduser or not pwd or re.search(" ", adduser) or re.search(" ", pwd)): # test if user and or password is not empty
		print "User and or password should not be empty or not contains with space."; # display an error
	else:
		nclient = [ adduser, pwd ]
		for myuser in list_of_users:
			if adduser == myuser[0]:
			   nclient = []
			   print 'Client user: %s already exists!' % adduser
			   break 
			else:  pass
		if nclient:
			list_of_users.append(nclient); #insert user and password
		else: pass
	ask = raw_input("Do you want to add more type 'n' or hit enter to continue? ").strip(); # Asking to continue
	if ask.lower() == 'n': # if ask var is not equal to Y or y
		if len(list_of_users) == 0:
			print "It's not permitted to quit since no user was newly added."
		else: break
	else: pass

	
print "Please wait while configuring the device..."
# os.popen("./runexpect.exp %s" % admin_passwd).read(); #install spi
os.system("./runexpect.exp %s" % admin_passwd); #install spi
if os.path.isfile(log): # test if log.log exists
	os.remove(log); # remove log.log file
else: pass

# if os.path.isdir(dir_): # test if directory exists
	# os.chdir(dir_); # cd directory
for i in commands.split('\n'): # split commands
	if re.search('install', i):
		i=i.split()
		i=i[-1]
		os.chdir(curr_dir)
		# os.popen("./myexpect.exp %s %s" % (i, admin_passwd)).read()
		try:
			os.system("./myexpect.exp %s %s" % (i, admin_passwd))
		except: os.system("./myexpect.exp %s %s" % (i, admin_passwd))
	else:
		os.system("sudo %s" % i); # execute commands

if os.path.isfile("/etc/squid3/%s.conf" % squid):
	write_to_file('log.log', (date_time() + ' %s successfully copied a backup.' % squid))
else: pass
# iterate append_conf
os.chdir(dir_)
for i in append_conf:
	i=i.strip()
	if i:
		check = os.popen("cat /etc/squid3/%s |grep '%s'" % (squid, i)).read().strip()
		if not check: # if null or empty
			write_to_file(squid, i); # writing into conf file
		else: pass
	else: pass
os.chdir(curr_dir)
for i in list_of_users:
	outp = os.popen("./login.exp %s %s %s" % (i[0], i[1], admin_passwd)).read()
os.system("service squid3 restart"); # restart squid
# else: sys.exit('Directory %s does not exists!' % dir_); # quit script

