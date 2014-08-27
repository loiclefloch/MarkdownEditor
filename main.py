#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, signal
from PyQt4 import QtGui
from classes.mainWindow import MainWindow
from classes.Model import Model
from classes.Controller import Controller

# handle ctrl+c on terminal
def sigint_handler(*args):
  QtGui.QApplication.quit()

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    app = QtGui.QApplication(sys.argv)
    view = MainWindow()
    model = Model(view)
    controller = Controller(view, model)
    model.set_mtheme(model.mtheme["path"])
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

