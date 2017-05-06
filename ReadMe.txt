Pre-requisite:
1. Install expect
   $ sudo apt-get install expect
   
Run the program
1. Launch Terminal
2. Type the command
       $ git clone https://github.com/catchwhale/squid-ubuntu
3. Browse the checkout files i.e 
       $ cd ~/Download/squid_ubuntu
4. Run any of the ff command
       $ ./script.py <USERNAME> <PASSWORD> <PORT>       IF USING ADMIN PASSWORD
       $ ./script.py <USERNAME> <PASSWORD>              IF USING ADMIN PASSWORD WITH DEFAULT PORT NUMBER 3128
       $ ./script.py <USERNAME> <PASSWORD> <PORT> -w    IF WITHOUT SPECIFYING PASSWORD
       $ ./script.py <USERNAME> <PASSWORD> -w           IF WITHOUT SPECIFYING PASSWORD WITH DEFAULT PORT NUMBER 3128
5. When using OS with ADMINISTRATIVE PASSWORD, 
      supply it and hit enter button to proceed
6. When asking for new user and password provide it
7. When asking to repeat the process in step no 5 to 6, Type 'n' to proceed with the next stage
or hit enter to repeat the process
8. Done

Notes: 
	1 Log.log file will be created name Log.log.
	2. When adding new User and or password, 
	      it should not contain space " " or not empty.
	3. Never move or alter the script.py file or transfer to another folder.
	4. You can transfer the script.py python file together with its folder and its hidden dependency files.


To uninstall squid:
    1. sudo apt-get remove apache2-util squid
    2. sudo apt-get autoremove
    2. sudo rm /etc/squid3/squid.*

How to update existing port number:
	1. At your terminal, browse script folder
		i.e cd ~/Download/squid-ubuntu
	2. ./script -p <PORT NUMBER>

