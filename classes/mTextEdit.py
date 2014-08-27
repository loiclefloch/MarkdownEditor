import sys
from PyQt4 import QtCore, QtGui

class mTextEdit(QtGui.QTextEdit):
  def __init__(self,parent):
    QtGui.QTextEdit.__init__(self, parent)

  def keyPressEvent(self, event):
    # Shift + Tab is not the same as trying to catch a Shift modifier and a tab Key.
    # Shift + Tab is a Backtab!!
    if event.key() == QtCore.Qt.Key_Backtab:
      self.unindent()
    elif event.key() == QtCore.Qt.Key_Tab:
      self.indent()
    else:
      return QtGui.QTextEdit.keyPressEvent(self, event)

  def indent(self):
    tab = "\t"
    cursor = self.textCursor()

    if cursor.hasSelection() == True:
      start = cursor.selectionStart()
      end = cursor.selectionEnd()
      while cursor.position() < end:
        cursor.movePosition(cursor.StartOfLine)
        cursor.insertText(tab)
        cursor.movePosition(cursor.Down)
      cursor.movePosition(end)
    else:
      cursor.insertText(tab)

  def unindent(self):
    cursor = self.textCursor()

    if cursor.hasSelection() == True:
      start = cursor.selectionStart()
      end = cursor.selectionEnd()
      while cursor.position() < end:
        self.removeTab(cursor)
        cursor.movePosition(cursor.Down)
      cursor.movePosition(end)
    else:
      self.removeTab(cursor)

  def removeTab(self, cursor):
    cursor.movePosition(cursor.StartOfLine)
    c = self.toPlainText().at(cursor.position())
    # little trick because == "\t" doesn't work. so we use unicode id
    if c.unicode() == 9:
        cursor.deleteChar()
