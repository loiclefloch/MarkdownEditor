#!/usr/bin/python3

from classes.mFile import mFile
from classes.directory import directory

if __name__ == "__main__" :
  d = directory("/home/loic/shared/cours/")
  files = d.read()
#  for file in files:
#    print(file.content())
  d.close()
