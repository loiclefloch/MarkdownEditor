import os
from . import mFile

class directory:
    def __init__(self, path):
        self.path = path
        self.files_list = list()

    """
        extension: with or without dot. Return the list with just
        files with this extension
    """
    def read(self, extension = None):
        lst = sorted(os.listdir((self.path)))
        files = sorted(f for f in os.listdir(self.path)
                if os.path.isfile(os.path.join(self.path, f)))

        for file in files:
            f = mFile.mFile(self.path + file)
            self.files_list.append(f)

        if extension:
          if extension[0] != '.':
            extension = '.' + extension
          l = list()
          for f in self.files_list:
            if f.extension() and f.extension() == extension:
              l.append(f)
          self.files_list = l

        return self.files_list

    def close(self):
        i = 0
        for f in self.files_list:
            f.close()

    def dump(self):
      if not self.files_list:
        print("[LIST EMPTY]")
      for f in self.files_list:
        print (f.getPath())
