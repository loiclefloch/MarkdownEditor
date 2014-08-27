import os
import os.path

from os.path import basename
from . import logger

class mFile:
    def __init__(self, path):
      self.path = path
      #logger.info("open " + self.path)
      if os.path.exists(self.path):
        self.f = open(self.path, "r+")
      else:
        self.f = open(self.path, "w+")

    def close(self):
      self.f.close()
      #logger.info("close " + self.path)

    def getPath(self):
        return str(self.path)

    def saveContent(self, text):
        self.f.write(text)

    def content(self):
      return self.f.read()

    def extension(self):
      return os.path.splitext(self.path)[1]

    def filename(self):
      return os.path.splitext(basename(self.path))[0]
