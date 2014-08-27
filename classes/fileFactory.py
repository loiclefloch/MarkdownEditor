#!/usr/bin/python

import os

from . import mFile
from . import logger
from classes.Exceptions import FileException

class FileFactory:

  def __init__(self, path):
    self.path = path

  def openFile(self, filename):
      filepath = self.getFilePath(filename)
      logger.info("FileFactory: open " + filepath)
      return mFile.mFile(filepath)

  # create a new .cours file
  def createFile(self, filename, title, author = "", comment = ""):
    filepath = self.getFilePath(filename)
    if os.path.isfile(filepath):
      raise FileException("File exists")
    print("FileFactory: create " + filepath)
    f = mFile.mFile(filepath)
    f.saveContent(title + author + comment)
    return f

  def getFilePath(self, filename):
    fileName, fileExtension = os.path.splitext(filename)
    ext = ".cours"
    if not fileExtension:
      filename = filename + ext
    return self.path + filename
