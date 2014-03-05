#!/usr/bin/env python

from ontapi.NaServer import *
from ontapi.NaElement import *

filer = NaServer('<fqdn of server>')
filer.setAdminUser('<user>', '<password>')

cmd = NaElement('aggr-list-info')
results = filer.invokeElem(cmd)
aggvars = ['checksum-status', 'checksum-style', 'disk-count', 'files-total',\
			'files-used', 'has-local-root', 'has-partner-root', 'is-checksum-enabled',\
			'is-inconsistent', 'is-snaplock', 'mirror-status', 'name', 'plex-count',\
			'plexes', 'raid-size', 'raid-status', 'size-available', 'size-percentage-used',\
			'size-total', 'size-used', 'snaplock-type', 'state', 'type', 'uuid', 'volume-count',\
			'volume-count-striped-dv', 'volume-count-striped-mdv', 'volumes']

aggrs = results.getChildByName('aggregates')
for aggr in aggrs.getChildren():
		for i in aggvars:
			item = aggr.getChildContent(i)
			print "%-25s \t==> %25s" % (i,item)
