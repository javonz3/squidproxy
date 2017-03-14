#!/usr/bin/env python
# -*- utf8-encoding -*-

import os
import re
from time import gmtime, strftime
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
cp squid.conf squid.conf.orig
service squid3 restart
initctl show-config squid3 # Start squid at boot
"""
user = os.popen('users').read().strip(); #get the current user
os.chdir(dir_); # cd directory
list_of_users=[]
adduser=""
pwd=""
while True:
	adduser = raw_input('Enter new user: ')
	pwd = raw_input("Enter User's password: ")
	ask = raw_input("Do you want to add more <Y/n>").strip()
	if ask.lower() != 'y':
		break
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

if os.path.isdir(dir_): # test if directory exists
	for i in commands.split('\n'): # split commands
		os.system(i); # execute commands
	if os.path.isfile("%s.conf" % squid):
		write_to_file('log.log', (date_time() + ' %s successfully copied a backup.' % squid))
else: 
	print 'Directory %s does not exists!' % dir_;
	sys.exit(); # quit script

