#!/usr/bin/python

from PyQt4 import QtGui, QtCore
import getpass # for getuser

from . import logger
from classes.fileFactory import FileFactory
from classes.Exceptions import FileException
from . import Constants

class NewFileWindow(QtGui.QDialog):

  def __init__(self, parent=None):
    super(NewFileWindow, self).__init__(parent)
    self.initUI()
    self._want_to_close = False

  def initUI(self):
    # window design
    self.resize(350, 400)
    self.setWindowTitle("new File")

    # labels
    title = QtGui.QLabel('Title')
    author = QtGui.QLabel('Author')
    comment = QtGui.QLabel('Comment')

    # widgets
    self.titleEdit = QtGui.QLineEdit()
    self.authorEdit = QtGui.QLineEdit(getpass.getuser())
    self.commentEdit = QtGui.QTextEdit()
    okButton = QtGui.QPushButton("Create !")
    cancelButton = QtGui.QPushButton("Cancel")

    # events
    okButton.clicked.connect(self.okEvent)
    cancelButton.clicked.connect(self.cancelEvent)

    # grid
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(title, 1, 0)
    grid.addWidget(self.titleEdit, 1, 1)

    grid.addWidget(author, 2, 0)
    grid.addWidget(self.authorEdit, 2, 1)

    grid.addWidget(comment, 3, 0)
    grid.addWidget(self.commentEdit, 3, 1, 2, 1)

    grid.addWidget(okButton, 5, 1)
    grid.addWidget(cancelButton, 5, 0)

    self.setLayout(grid)

  def okEvent(self):
    title = self.titleEdit.text()
    author = self.authorEdit.text()
    comment = self.commentEdit.toPlainText()
    filename = title.strip()

    if title and author:
      logger.info("create new task")
      fileFactory = FileFactory(Constants.DIR)
      try:
        f = fileFactory.createFile(filename, title, author, comment)
        return
      except FileException as e:
        msgError = e.error()
    elif not title:
      msgError = "Title must not be empty"
    else:
      msgError = "Author must not be empty"
    QtGui.QMessageBox.critical(self, "Attention", msgError)

  def cancelEvent(self):
    logger.info("Cancel !")
    self._want_to_close = True
    self.close()

  def closeEvent(self, event):
    if self._want_to_close:
      super(NewFileWindow, self).closeEvent(event)
    else:
      event.ignore()
    logger.info("Close NewFileWindow")

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Escape:
      logger.info("press echap")
#      self.cancelEvent()
    else:
      logger.info("key press")

