#!/usr/bin/env python

from ontapi.NaServer import *
from ontapi.NaElement import *

#### non-prod filer ####
filer = NaServer('filer.filerdomain.com')
filer.setAdminUser('user', 'password')

def get_perf_objects(filer):
    cmd = NaElement('perf-object-list-info')
    res = filer.invokeElem(cmd)
    items = res.getChildByName('objects')
    objects = []
    for item in items.getChildren():
        name = item.getChildContent('name')
        objects.append(name)
        # Debug code
        # print "Name of perf is %s" % (name)
    return objects

outside_list =  get_perf_objects(filer)

def get_perf_instance_info(outside_list, filer):
    cmd = NaElement('perf-object-instance-list-info')
    res = filer.invokeElem(cmd)
    items = res.getChildByName('instances')
    if outside_list == 'fcp':
        for item in items.getChildren():
            name = item.getChildContent('item')
            print "Name of instance is %s" % (name)
    else:
        print "Not gonna work!\n"

#get_perf_objects(filer)
#get_perf_instance_info(filer)
