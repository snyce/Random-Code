#!/usr/bin/env python

from ontapi.NaServer import *
from ontapi.NaElement import *

#### non-prod filer ####
filer = NaServer('filer.filerdomain.com')
filer.setAdminUser('user', 'password')

def get_perf_objects(filer):
    print "Filer %s\n" % filer
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
print "\nThis is the list of objects:\n"
print outside_list
print "\nEnd list of objects \n"

def get_perf_instance_info(filer, outside_list):
    print "Filer => %s\n" % (filer)
    print "\nList:\n"
    print outside_list
    #cmd = NaElement('perf-object-instance-list-info')
    cmd = NaElement('perf-object-get-instances')
    res = filer.invokeElem(cmd)
    perf_objs = res.getChildByName('instances')
    for i in perf_objs.getChildren():
        print i
    #for objs in perf_objs.getChildren():
    #    for iter in outside_list:
    #        perf_inst = objs.getChildContent(iter)
    #        print "%-25s \t==> %25s" % (iter,perf_inst)

get_perf_instance_info(filer, outside_list)
