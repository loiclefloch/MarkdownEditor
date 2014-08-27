import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView

from . import MarkdownHighlighter

class MarkdownWindow(QtGui.QDialog):

  def __init__(self, title, content, model, parent=None):
    super(MarkdownWindow, self).__init__(parent)
    self.title = title
    self.content = content
    self.MODEL = model
    self.initUI()

  def initUI(self):
    self.resize(550, 700)
    self.setWindowTitle(self.title)

    hbox = QtGui.QHBoxLayout()

    preview = QtGui.QTextEdit()
    #preview.
    preview.setPlainText(self.content)
    MarkdownHighlighter.MarkdownHighlighter(preview)
    hbox.addWidget(preview)

    self.setLayout(hbox)

  def closeEvent(self, event):
    self.close()
