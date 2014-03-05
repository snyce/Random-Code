#!/usr/bin/python

# Get all of the licenses and display the information
#
#

from ontapi.NaServer import *
from ontapi.NaElement import *

filer = NaServer('filer.filerdomain.com')
filer.setAdminUser('user', 'password')

### the below is absolutely unnecessary###
#lic = ['code', 'count', 'expiration-timestamp', 'installation-timestamp',\
#	  'is-demo', 'is-expired', 'is-licensed', 'is-site', 'length',\
#	  'node-count', 'platform', 'service', 'storage-count']

cmd = NaElement('license-list-info')
results = filer.invokeElem(cmd)

items = results.getChildByName('licenses')
for item in items.getChildren():
	license = item.getChildContent("code")
	service = item.getChildContent("service")
	if license == None:
		pass
	else:
		print "%-15s ==> %15s" % (service,license)
