#!/usr/bin/python3

from classes.mFile import mFile
from classes.directory import directory

if __name__ == "__main__" :
  d = directory("/home/loic/shared/")
  files = d.read(".sql")
  d.dump()
  d.close()
