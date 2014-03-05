#!/usr/bin/python

from ontapi.NaServer import *
from ontapi.NaElement import *

filer = NaServer('filer.filerdomain.com')
filer.setAdminUser('user', 'password')

cmd = NaElement('qtree-list')
results = filer.invokeElem(cmd)
qtree_info = ['id', 'oplocks', 'owning-vfiler', 'qtree', 'security-style'\
			  'status', 'volume']

qtrees = results.getChildByName('qtrees')
for qtree in qtrees.getChildren():
		for i in qtree_info:
			item = qtree.getChildContent(i)
			print "%-10s\t %10s %10s" % (i,'==>',item)
