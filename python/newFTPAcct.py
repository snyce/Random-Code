#!/usr/bin/env python

#############################################################################################################################
# This is revision 1 of the ftp account creation script																		#
# Todos: add better looping constructs to allow for multiple input chances													#
# Todos: don't know if it's necessary, but add the ability to add in MB not just GB, though seems like moot point.			#
# Todos: input colors, email script for NOC, string cmp on storage (test for in'ness) for valid storage disks				#
# OK: I have added colors but this takes away the portability as i'm using bash escape codes, tra laa la					#
# Going to make the colors more readable with vars \033[31m is less readable to most than RED								#
#############################################################################################################################

# Import necessary modules

import re			# for regular expressions
import subprocess	# for spawning shell subprocess
import time			# for wating and stuff
import sys			# for sys(tem) functions, mainly to exit out of errors cleanly
import os			# for os calls

# Define ANSI color codes for clarity

RED = "\033[31m"
LT_RED = "\033[1;31m"
GREEN = "\033[32m"
LT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
SQ_RST = "\033[0m"

# Going to define a default disk as I don't have the time not inclination to check which has the lowest quota
# if this needs to be changed it's easy enough and close enough to the top to notice

default_disk = "/storage010"

# Define Functions that are necessary to keep everything clean and tidy

# Get Disk information

def getDiskSize():
	print "*" * 60
	print "\n%sWould you like to print disk information?" % (RED)
	print "NOTE: Please DO NOT USE %s/storage006%s %sor%s %s/storage012%s" % (YELLOW, SQ_RST, LT_RED, SQ_RST, YELLOW, SQ_RST)
	print "%sNOTE: They do exist /storage006 belongs to VASG" % (SQ_RST)
	print "NOTE: and /storage012 is *emergency* space\n"
	print "*" * 60
	try:	
		# Get the option value to switch on (make sure to check for valid options)
		opt = raw_input("\033[32mPlease enter Y/N (case insensitive - no spaces):\033[0m ")
		# Take the option and figure out what to do (if yes get disk info, else skip)
		""" 
		getDiskSize() Ok so what's happening here, subprocess allows us to call a system process
		spawn system shell to run it, you can redirect stdin and stdout so we are
		taking the stdout from the previous process dfin which in our case is a df -hP
		to get the disks, then we're passing the stdout to the next subprocess named
		dfgrep1, grepping out the storage006, then passing the stdout to then next grep
		process and so on and so forth.  I have not found yet a better quicker way to do
		it
		"""
		if (opt == 'y' or opt == 'Y'):
			#OK I admit this is ghetto, and if something changes will throw off formatting
			dfin = subprocess.Popen(['df', '-hP'], stdout=subprocess.PIPE)
			dfgrep1 = subprocess.Popen(['grep', '-v', 'storage006'], stdin=dfin.stdout, stdout=subprocess.PIPE)
			dfgrep2 = subprocess.Popen(['grep', '-v', 'storage012'], stdin=dfgrep1.stdout, stdout=subprocess.PIPE)
			dfgrep3 = subprocess.Popen(['grep', 'storage'], stdin=dfgrep2.stdout, stdout=subprocess.PIPE)
			dfout = subprocess.Popen(['column', '-t'], stdin=dfgrep3.stdout)
			time.sleep(1)
		elif (opt == 'n' or opt == 'N'):
			print "%sI hope you know where to put the new account!%s" % (RED, SQ_RST)
			pass
		else:
			print "\n%sI'm sorry that's not a valid option!%s\n" % (RED, SQ_RST)
			print "I said 'Good Day!'\n"
			sys.exit(0)
	# If the user interrupts print custom message
	except(KeyboardInterrupt):
		keyboardMSG()

# Get Disk if specified

def getDiskLoc():
	try:
		# get the disk, making sure to sanitize input, if it doesn't have storage in it set default value
		dfcmd = subprocess.Popen(['df', '-hP'], stdout=subprocess.PIPE)
		dfgrep1 = subprocess.Popen(['grep', '-v', 'storage006'], stdin=dfcmd.stdout, stdout=subprocess.PIPE)
		dfgrep2 = subprocess.Popen(['grep', 'storage'], stdin=dfgrep1.stdout, stdout=subprocess.PIPE)
		dfawk = subprocess.Popen(['awk', '{ print $6}'], stdin=dfgrep2.stdout, stdout=subprocess.PIPE)
		disk_report = dfawk.stdout
		disks = ''.join(disk_report)

		print "%s" % (GREEN)
		disk = raw_input("Please Enter the Location (e.g. storage011):\033[0m ")
		# regular expression to check if storage is part of the name
		# could probably be optimized
		disk = re.sub("^/", '', disk)
		disk_chk = re.match("^storage\d{3}", disk)
		if not disk_chk:
			disk = default_disk
		elif disk not in disks:
			print "%s is not a valid disk" % (disk)
			sys.exit(0)
		else:
			if re.match("^/", disk):
				disk = disk
			else:
				disk = re.sub("^", "/", disk)
	except (KeyboardInterrupt):
		keyboardMSG()
	print "Disk is %s%s%s" % (YELLOW, disk, SQ_RST)
	return disk

# Get Account Name

def getAcctName():
	try:
		# Get the account username (Have to leave the ansi color codes in here for time being)
		# going to use replace to strip out spaces from the raw input, maybe ghetto but it works
		uname = raw_input("\033[32mPlease Enter the Username: \033[0m").replace(' ', '')
		# use routine to check username against passwd file for collisions
		checkUser(uname)
		# again have to leave the ansi color codes, until i can figure out a good way to do it with raw_input()
		requester = raw_input("\033[32mPerson who Requested the account: \033[0m")
		print "Requester is %s" % (requester)
		return uname, requester

	except (KeyboardInterrupt):
		keyboardMSG()

# Get Quota

def getQuota():
	print "*" * 75
	print "%sNOTE:%s %sIf the user wants higher than%s %s25G%s %sdefer to PDIT Engingeering%s" % (RED, SQ_RST, GREEN, SQ_RST, YELLOW, SQ_RST, GREEN, SQ_RST)
	print "%sNOTE:%s %sif they user needs a small account give them%s %s1G%s %sas the low end.%s" % (RED, SQ_RST, GREEN, SQ_RST, YELLOW, SQ_RST, GREEN, SQ_RST)
	print "*" * 75
	try:
		quota = raw_input("\033[32mPlease enter Quota\033[0m \033[31mdefault is 5G:\033[0m ")
		# compile this once cause we use it a couple of times, i know it's cached but what the hell, eh.
		numbers = re.compile('[^\d+?]')
		qnum = numbers.sub('', quota)
		if not qnum: 
			quota = "5G"
		else:
			# make sure the quota is numbers
			set_quota = numbers.sub('', quota)
			# if there are any 0's in the beginning strip them
			set_quota = re.sub('^0+', '', quota)
			# if there are any chars error out on them 
			parse_chars = re.search('[a-zA-Z]', set_quota)
			if parse_chars:
				print "%sPlease remove the %s character from the quota.%s" % (RED, parse_chars.group(0), SQ_RST)
				sys.exit(0)
			# cheap and easy way to make sure the quota isn't 3 digits (up to 99G)
			elif len(set_quota) > 2:
				print "%sPlease talk to engineering before setting such a large quota.%s" % (RED, SQ_RST)
				sys.exit(0)
			else:
				quota = re.sub("$", "G", set_quota)
		print "Quota = %s%s%s" % (RED, quota, SQ_RST)
		return quota	

	except (KeyboardInterrupt):
		keyboardMSG()
	
# Take all the information provided and setup the account

def createFTPAccount(uname, disk, requester, quota):
	print "\n"
	print "*" * 80
	print "Here is where the magic happens."
	print "Please check over your work before hitting yes!"
	print "*" * 80
	print "\n"
	print "Here is the information you entered:"
	print "%sAccount name%s = %s%s%s" % (GREEN, SQ_RST, YELLOW, uname, SQ_RST)
	print "%sDisk location%s = %s%s%s" % (GREEN, SQ_RST, YELLOW, disk, SQ_RST)
	print "%sRequester%s = %s%s%s" % (GREEN, SQ_RST, YELLOW, requester, SQ_RST)
	print "%sAnd quota is%s %s%s%s" % (GREEN, SQ_RST, YELLOW, quota, SQ_RST)
	acct_opt = raw_input("\033[1;33mDoes this look correct\033[0m \033[1;31m(Y/N):\033[0m ")

	try:
		if (acct_opt == 'y' or acct_opt == 'Y'):
		
			# Ok I KNOW some of this is ghetto fab and kludgey, so sue me
			# First lets create the user account
			# this i know is a ghetto fabulous kludge
			pub = "./pub/"
			ftp_dir = "ftp"
			
			# get the hostname programmatically
			hostname = os.getenv("HOSTNAME")

			# Here comes the ghettofab, there is probably a much easier more pythonic way of doing this
			homedir = (disk + "/" + ftp_dir + "/" + uname + "/" + pub)

			# Lets create the user account
			subprocess.Popen(['useradd', '-M', '-d', homedir, '-s', '/sbin/nologin', '-c', requester, '-g', 'ftponly', uname])
			print "User Account %s%s%s has been created." % (YELLOW,uname,SQ_RST)
			time.sleep(2)
			
			# Lets now setup the home dir
			tar_file = "/vault/FTP-skel.tar.gz"
			subprocess.Popen(['tar', '-x', '-z', '-f', tar_file, '-C', disk + "/" + ftp_dir + "/"])
			print "Skeleton dir %s%s%s has been uncompressed." % (YELLOW,tar_file,SQ_RST)
			time.sleep(2)
			
			# Now lets mv the dir to the username
			template_dir = (disk + "/" + ftp_dir + "/" + "tmpl")
			user_dir = (disk + "/" + ftp_dir + "/" + uname)

			subprocess.Popen(['mv', template_dir, user_dir])
			print "Skeleton dir %s%s%s has been moved to user dir %s%s%s." % (RED, template_dir, SQ_RST, RED, user_dir, SQ_RST)		
			time.sleep(2)

			# OK now chown the pub dir to uname + ":ftponly"
			subprocess.Popen(['chown', uname + ":ftponly", user_dir + "/" + pub])
			print "Directory Permissions have been set."
			print "User Account and Directory have been setup.\n"
			print "Please create a password entry in <password safe> and get ready to paste it in...\n"
			time.sleep(2)
			
			# Ok now we call passwd to set the password for the user account
			# here we use subprocess.call instead of Popen as we want to 
			# wait for passwd to return before moving on, else it gets ugly
			subprocess.call(['passwd', uname])
			print "Thanks for setting the password for %s%s%s. \n" % (YELLOW, uname, SQ_RST)
			time.sleep(2)

			# lets split the requester name up and only use the first name
			whole_name = requester.split()
			# whole_name[0] should contain the first file (which should be the first name)
			# Ok last but not least lets set the quota
			# again we want to wait for it to return before finishing up
			# Ok weird bug, with subprocess.call the quota get set on two diff filesystems, make it wait
			subprocess.call(['/root/bin/setquota', uname, quota])
			print "Quota has been set to %s%s%s, this should round out the account creation, thanks!\n" % (YELLOW, quota, SQ_RST)
			print "#" * 100
			print "%s" % (LT_RED)
			print "Please ftp to <ftp host> as %s%s%s%s and make sure you can login." % (YELLOW, uname, SQ_RST, LT_RED)
			print "\nPlease copy and paste the below text, as well as the password from <password safe> and \nsend in an encrypted email to %s.\n" % (requester)
			print "%s" % (SQ_RST)
			print "#" * 100

			# Lets just use the first name
			print "Greetings %s,\n" % (whole_name[0].capitalize())
			print "Your new FTP account is now ready.  You should be able to connect and transfer files using the following credentials:"
			print "hostname: %s" % (hostname)
			print "username: %s" % (uname)
			print "password: PASSWORD"
			print "quota: %s\n" % (quota)
			print "Please remember if you need to share the credentials do so either through encrypted email, or over the phone never in plain text email."
			print "Keep in mind, the FTP storage really shouldn't be used as a backup, or as permanent storage in any way. It should really just be to get"
			print "files out to people that are too large to email. Once it's confirmed that the vendor or whomever has received the files you're "
			print "transferring, delete it and you should be good.\n"
			print "To check your current disk usage, please visit <removed> %s" % (uname)
			print "Please let us know if we can be of further assistance."
			print "\nThanks,"

			print "#" * 80
			print "\nCopy this information into a comment on the ticket:\n"
			print "requester: %s" % (requester)
			print "hostname: %s" % (hostname)
			print "username: %s" % (uname)
			print "password: IN <password safe>"
			print "storage: %s" % (disk)
			print "directory: %s" % (user_dir)
			print "quota: %s\n" % (quota)
			print "To check your current disk usage, please visit <removed internal cgi>%s" % (uname)
			print "#" * 80
			print "\n"
			print "#" * 80
			print "Make sure to update the wiki http://wiki.somedomain.com/index.php/\nwith the account information"
			print "#" * 80

		elif (acct_opt == 'n' or acct_opt == 'N'):
			print "Exiting! Thanks for playing!\n"
			sys.exit(0)

	except (KeyboardInterrupt):
		keyboardMSG()

##################################
# Routines to check input		 #
##################################

# Check username

def checkUser(uname):
	# open /etc/passwd, READ ONLY
	password_file = open('/etc/passwd', 'r')
	# loop through each line and check against username
	for username in password_file:
		result = re.match(uname, username, re.IGNORECASE)
		# If we have a match exit
		if result:
			print "Username: %s%s%s already exists sorry!\n" % (RED,uname,SQ_RST)
			sys.exit(0)
	print "Username %s%s%s is OK!\n" % (YELLOW,uname,SQ_RST)

#################################
# Custom Exceptions				#
#################################

def keyboardMSG():
	print "\n\n"
	print "%s*" % (RED) * 40 
	print "You pressed %sCTRL+C exiting!%s" % (LT_RED, SQ_RST)
	print "%s*" % (RED) * 40 
	print "%s" % (SQ_RST)
	sys.exit(0)

######################################################
# Print Welcome message and disk size information    #
######################################################

print "\n"
print "#" * 60
print "\nWelcome to the FTP account creation script!\n"
print "#" * 60
print "\n"

# Show disks size
getDiskSize()

#########################################################################################
# After the disk sizes have been printed, get the username, disk location and quota     #
#########################################################################################

# get the username and account requester
gAcctName = getAcctName()

# get the disk storage location
gDisk = getDiskLoc()

# get quota information
gQuota = getQuota()

#############################################################################################
# After we've gotten all the appropriate information, lets go ahead and create the account  #
# set the password and quota																#
#############################################################################################

if __name__ == "__main__":
  createFTPAccount(gAcctName[0], gDisk, gAcctName[1], gQuota)
