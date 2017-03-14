#!/usr/bin/env python
# -*- utf8-encoding -*-

import os

# Append data on existing file
def write_to_file(filename, text):
	with open(filename, mode='a+') as outfile:
		outfile.write("%s\n" % text)
		outfile.close()

dir_="/etc/squid3"
commands="""
apt-get update
apt-get install expect # Install expect
apt-get install squid # Install squid
cp squid.conf squid.conf.orig
service squid3 restart
initctl show-config squid3 # Start squid at boot
"""
user = os.popen('users').read().strip(); #get the current user
if re.search(" ", user): # check if user have space in between
	user=user.split() # split it by space
	user=user[0] # get user at index zero
else: pass

if os.path.isdir(dir_): # test if directory exists
	os.chdir(dir_); # cd directory

	for i in commands.split('\n'):
		print i
else: 
	print 'Directory %s does not exists!' % dir_;
	sys.exit(); # quit script
