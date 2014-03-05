#!/usr/bin/env python

import os
import argparse
import hashlib
import sys
from time import sleep
from os.path import getsize

if not sys.argv[1:]:
  udir = os.getcwd()
else:
  udir = sys.argv[1]

print "User specified directory is: %s" % (udir)

class diskwalk(object):
  def __init__(self,path):
    self.path = path

  def enumPaths(self):
    path_collection = []
    for dirpath, dirnames, filenames in os.walk(self.path):
      for file in filenames:
        fullpath = os.path.join(dirpath,file)
        path_collection.append(fullpath)
    return path_collection

  def enumFiles(self):
    file_collection = []
    for dirpath, dirnames, filenames in os.walk(self.path):
      for file in filenames:
        file_collection.append(file)

    return file_collection

def create_checksum(path):
  fp = open(path)
  checksum = hashlib.md5()
  while True:
    buffer = fp.read(8192)
    if not buffer:break
    checksum.update(buffer)
  fp.close()
  checksum = checksum.digest()
  return checksum


def findDupes(path = udir):
  dup = []
  record = {}
  d = diskwalk(path)
  files = d.enumPaths()
  for file in files:
    compound_key = (getsize(file),create_checksum(file))
    if compound_key in record:
      dup.append(file)
    else:
      record[compound_key] = file
  return dup

if __name__ == "__main__":
  dupes = findDupes()
  print "Walking directories...\n"
  for dup in dupes:
    print "Duplicate: %s" % (dup)
    #os.remove(dup)
