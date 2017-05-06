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

squidconf = "/etc/squid3/squid.conf"


dir_="/etc/squid3"
squid = "squid.conf"
log = "Log.log"
file_ = ".%s" % squid
ip_ = os.popen("ifconfig |grep addr | awk '{print $2}' |grep addr").readlines()
ips = []
for i in ip_:
	i=i.split(':')
	ip=i[-1].strip()
	if ip and ip != '127.0.0.1':
		ips.append(ip)

if not ips:
	sys.exit('No valid ips found.')
else: pass

quit = False
arg = ""
proxy = '3128'
try:
	arg = sys.argv[-1].strip()
	proxy = sys.argv[-2].strip()
	if arg == '-p' and proxy.isdigit():
		if os.path.isfile(squidconf):
			http_port = os.popen("cat %s |grep http_port" % squidconf).read().strip()
			os.system("sed -i 's/%s/http_port %s/g' %s" % (http_port, proxy, squidconf))
			os.system("service squid3 restart")
			for ip in ips:
				print "%s:%s" % (ip, proxy)
			quit = True
			sys.exit()
		else:
			sys.exit("%s does not exists." % squidconf)
		sys.exit()
	else: pass
except: pass

if quit:
	sys.exit()
else: pass

if os.path.isfile(log): # test if log.log exists
	os.remove(log); # remove log.log file
else: pass

conf = os.popen("cat .squid.conf").readlines()
for i in conf:
	i=i.strip()
	if i:
		if re.search('IPADDRESS', i):
			cnt = 1
			for myip in ips:
				i_="acl ip%s myip %s" % (cnt, myip)
				write_to_file(".squid2.conf", i_)
				i_="tcp_outgoing_address %s ip%s" % (myip, cnt)
				write_to_file(".squid2.conf", i_)
				cnt += 1
		else:
			if re.search('http_port', i) and proxy.isdigit():
				write_to_file(".squid2.conf", "http_port %s" % proxy)
			else:
				write_to_file(".squid2.conf", i)	

commands="""
rm spi
mv /etc/squid3/squid.conf /etc/squid3/squid.conf.orig
mv ".squid2.conf" /etc/squid3/squid.conf
chmod a-w /etc/squid3/squid.conf*
touch /etc/squid3/squid_passwd
chown proxy /etc/squid3/squid_passwd
initctl show-config squid3 
"""

if os.path.isfile(file_):
	append_conf = os.popen("cat '%s'" % file_).readlines()
else: sys.exit('File %s does not exists!' % file_);

user = os.popen('whoami').read().strip(); #get the current user
list_of_users = []; # initializing list
adduser = ""
pwd = ""
curr_dir = os.getcwd().strip()

if arg == '-w':
	admin_passwd = getpass.getpass(prompt='Enter your administrative password: ').strip()
else:
	admin_passwd = ""

if user != 'root' and admin_passwd:
	test_login=os.popen("./.myssh.exp %s" % admin_passwd).read()
	if not re.search('Welcome', test_login):
		sys.exit('Invalid password!')
	else: pass
else: pass

while True: # Repeat the process
	adduser = sys.argv[1].strip()
	pwd = sys.argv[2].strip()
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
			break
		else: pass

if admin_passwd:	
	os.system("./.runexpect.exp %s %s %s" % (adduser, pwd, admin_passwd)); #install spi
else:
	os.system("./.runexpect2.exp %s %s" % (adduser, pwd)); #install spi
for i in commands.split('\n'): # split commands
	if admin_passwd:
		outp=os.popen("./.command.exp %s %s" % (admin_passwd, i)).read()
	else:
		outp=os.popen("./.command2.exp %s" % i).read()
	if re.search('command', outp) and i:
		write_to_file(log, (date_time() + ' %s Failure to execute.' % i))
	else:
		if i: 
			write_to_file(log, (date_time() + ' %s successfully executed.' % i))

if os.path.isfile("/etc/squid3/%s.conf" % squid):
	write_to_file(log, (date_time() + ' %s successfully copied a backup.' % squid))
else: pass

outp = os.popen("sudo service squid3 restart").read(); # restart squid

if re.search('start', outp):
	write_to_file(log, (date_time() + ' Squid successfully running.'))
else: write_to_file(log, (date_time() + '  Failure to run squid.'))

if os.path.isfile(log):
	os.system('clear'); # clear print display
	print 'Check the log file Log.log.'
else: print 'Log file: %s not found' % log; # print if file not found

if ips:
	print "Newly added ip(s) is / are:"
	for i in ips:
		write_to_file(log, "Newly added ip:port:user:passwd %s:%s:%s:%s" % (i, '3128', adduser, pwd))
		print "%s:%s:%s:%s" % (i, proxy, adduser, pwd)
else: pass
