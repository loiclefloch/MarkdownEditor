import sys, os, markdown
from PyQt4 import QtGui, QtCore

from classes.directory import directory
from classes.mFile import mFile
from classes.htmlWindow import HtmlWindow
from classes.markdownWindow import MarkdownWindow
import Constants

class Controller():
  def __init__(self, view, model):
    self.VIEW = view
    self.CONTROLLER = self
    self.MODEL = model

    self.VIEW.tabs.connect(self.VIEW.tabs, QtCore.SIGNAL("currentChanged(int)"),self.tabChangedSlot)
    self.VIEW.tabs.connect(self.VIEW.tabs, QtCore.SIGNAL("tabCloseRequested(int)"),self.tabCloseRequestedSlot)
    self.VIEW.helpAction.triggered.connect(self.open_help)
    self.VIEW.saveAction.triggered.connect(self.save_file)
    self.VIEW.previewHtmlAction.triggered.connect(self.preview_html)
    self.VIEW.exportAsHtmlAction.triggered.connect(self.export_as_html)
    self.VIEW.themesMapper.mapped['QString'].connect(self.change_theme)
    self.VIEW.mthemesMapper.mapped['QString'].connect(self.change_mtheme)

    # shortcuts
    #nextTab = QtGui.QKeySequence(QtGui.KeyUp, None, None, self.next_tab)

    # init files
    d = directory(Constants.DIR)
    files = d.read(".cours")
    for file in files:
        self.addFile(file)
    d.close()

  """
    :param file: mFile
  """
  def addFile(self, file):
    doc_ix = self.MODEL.is_document_present(file.filename())
    # if document already open
    if doc_ix != -1:
        self.VIEW.change_active_tab(self.MODEL.get_active_tab())
    else:
        self.MODEL.append_doc(file.filename())
    textEdit = self.VIEW.add_tab(file.filename())
    textEdit.setPlainText(QtCore.QString(file.content()))
    textEdit.connect(textEdit, QtCore.SIGNAL("textChanged()"), self.renderInput)

  @QtCore.pyqtSlot()
  def save_file(self):
    filename = self.MODEL.get_document_title()
    filepath = Constants.DIR + filename + ".cours"
    try:
        self.MODEL.write_file_content(filepath, self.VIEW.get_current_document_content())
    except Exception:
        self.VIEW.runError("Error", "Can't save " + filepath)
    self.VIEW.update_status("File saved")
    self.VIEW.saveAction.setDisabled(True)

  @QtCore.pyqtSlot(int)
  def tabChangedSlot(self, argTabIndex):
      self.VIEW.update_status(self.MODEL.get_active_tab_name())

  @QtCore.pyqtSlot(int)
  def tabCloseRequestedSlot(self, argTabIndex):
    self.MODEL.remove_tab(argTabIndex)
    self.VIEW.remove_tab(argTabIndex)

  @QtCore.pyqtSlot()
  def open_help(self):
    f = mFile(Constants.HELP_FILE)
    #self.html_overview(f.filename(), f.content())
    self.markdown_overview(f.filename(), f.content())
    f.close()

  @QtCore.pyqtSlot()
  def preview_html(self):
    html = self.VIEW.get_current_document_content()
    title = self.MODEL.get_document_title() + " (Overview)"
    self.html_overview(title, html)

  @QtCore.pyqtSlot()
  def renderInput(self):
    self.VIEW.saveAction.setDisabled(False)

  @QtCore.pyqtSlot(str, str)
  def export_as_html(self):
    html_document = self.get_html(self.VIEW.get_current_document_content())
    filename = QtGui.QFileDialog.getSaveFileName(None, "Save file", Constants.DEFAULT_DIR_EXPORT, ".html")
    if filename:
      self.MODEL.write_file_content(filename, html_document)
      self.VIEW.update_status("File exported correctly on " + filename)
      return True
    return False # if no filename

  def next_tab(self):
    print("dqwdwq")

  @QtCore.pyqtSlot(str, str)
  def html_overview(self, title, html):
    html_document = self.get_html(html)
    self.window = HtmlWindow(title, html_document, self.MODEL)
    self.window.show()

  @QtCore.pyqtSlot(str, str)
  def markdown_overview(self, title, content):
    self.window = MarkdownWindow(title, content, self.MODEL)
    self.window.show()

  def get_html(self, html):
    html_document = "<!doctype html><html><body>"
    html_document += "<style type=\"text/css\">" + self.MODEL.css + "</style>"
    html_document += markdown.markdown(html)
    html_document += "</body></html>"

    return html_document

  def change_theme(self, themepath):
    self.MODEL.set_css(themepath)

  def change_mtheme(self, themepath):
    self.MODEL.set_mtheme(themepath)
