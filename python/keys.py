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

if __name__ == "__main__":
  d = diskwalk(udir)
  print "Walking directories...\n"
  for file in d.enumPaths():
    print file
