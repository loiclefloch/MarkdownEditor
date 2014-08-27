import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView

class HtmlWindow(QtGui.QDialog):

  def __init__(self, title, content, model, parent=None):
    super(HtmlWindow, self).__init__(parent)
    self.title = title
    self.content = content
    self.MODEL = model
    self.initUI()

  def initUI(self):
    self.resize(850, 700)
    self.setWindowTitle(self.title)

    hbox = QtGui.QHBoxLayout()

    preview = QWebView()
    preview.setContent("<style>"+ self.MODEL.css +"</style>" + self.content)
    hbox.addWidget(preview)

    self.setLayout(hbox)


  def closeEvent(self, event):
    self.close()
