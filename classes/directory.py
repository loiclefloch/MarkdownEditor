import os
from . import mFile

class directory:
    def __init__(self, path):
        self.path = path
#        self.dirp = opendir(path)
        self.files_list = list()

    def read(self):
        lst = sorted(os.listdir((self.path)))
        files = sorted(f for f in os.listdir(self.path)
                if os.path.isfile(os.path.join(self.path, f)))
        for file in files:
            f = mFile.mFile(self.path + file)
            self.files_list.append(f)
        return self.files_list

    def close(self):
        i = 0
        for f in self.files_list:
            f.close()
