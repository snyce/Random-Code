#!/usr/bin/env python

#import the necessary modules
import re #for regular expressions - to match ip's
import sys #for parsing command line opts

# I need to probably make this more pythonic but am working on that...
# if file is specified on command line, parse, else ask for file
if sys.argv[1:]:
    print "File: %s" % (sys.argv[1])
    logfile = sys.argv[1]
else:
    logfile = raw_input("Please enter a file to parse, e.g /var/log/secure: ")
    print "File: %s" % (logfile)

try:
    # open the file
    file = open(logfile, "r")
    # create an empty list
    ips = []
    # read through the file
    for text in file.readlines():
       #strip off the \n
        text = text.rstrip()
       #this is probably not the best way, but it works for now
        regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', text)
        # if the regex is not empty and is not already in ips list append
        if regex is not None and regex not in ips:
            ips.append(regex)

    #loop through the list
    for ip in ips:
        #I know there is argument as to whether the string join method is pythonic
        addy = "".join(ip)
        if addy is not '':
            print "IP: %s" % (addy)
    #cleanup and close file
    file.close()
#catch any standard error (we can add more later)
except IOError, (errno, strerror):
    print "I/O Error(%s) : %s" % (errno, strerror)
