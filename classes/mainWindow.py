import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QTextEdit

from classes.newFileWindow import NewFileWindow as NewFileWindow
from . import logger
from . import Constants
from . import MarkdownHighlighter
from . import mTextEdit

from HorizontalTab import FingerTabBarWidget

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        _widget = QtGui.QWidget()
        self.initUI(_widget)

    """
        UI Initialization
    """
    def initUI(self, widget):

        hbox = QtGui.QHBoxLayout()

        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setTabBar(FingerTabBarWidget(width=130,height=25))
        self.tabs.setTabPosition(QtGui.QTabWidget.West)

        hbox.addWidget(self.tabs)

        widget.setLayout(hbox)

        self.setCentralWidget(widget)

        self.make_menu_bar()

        self.make_toolbar()

        # window design
        self.setWindowTitle(Constants.APPLICATION_NAME)
        self.setWindowIcon(QtGui.QIcon(Constants.ICON_APPLICATION))
        self.resize(1200, 900)
        self.showMaximized()
        self.center()

        # childs
        self.newFileWindow = NewFileWindow()

        self.update_status("Ready")

        self.show()

    def make_menu_bar(self):
      self.newFileAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_NEW_FILE), '&New file', self)
      self.newFileAction.setShortcut('Ctrl+N')
      self.newFileAction.setStatusTip('Create new file')
      self.newFileAction.triggered.connect(self.open_new_file_window)

      self.saveAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_SAVE_FILE), '&Save', self)
      self.saveAction.setDisabled(True)
      self.saveAction.setShortcut('Ctrl+S')
      self.saveAction.setStatusTip('Save file')

      self.exitAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_EXIT), '&Exit', self)
      self.exitAction.setShortcut('Ctrl+Q')
      self.exitAction.setStatusTip('Exit application')
      self.exitAction.triggered.connect(self.close)

      self.statusBar()

      menubar = self.menuBar()
      fileMenu = menubar.addMenu('&File')
      fileMenu.addAction(self.newFileAction)
      fileMenu.addAction(self.saveAction)
      fileMenu.addAction(self.exitAction)

      # action menu
      actionMenu = menubar.addMenu("&Actions")

      self.previewHtmlAction = QtGui.QAction(QtGui.QIcon(''), '&Preview', self)
      self.previewHtmlAction.setStatusTip('Preview')
      self.previewHtmlAction.setShortcut('Ctrl+P')

      self.exportAsHtmlAction =  QtGui.QAction(QtGui.QIcon(Constants.ICON_EXPORT), '&Export', self)
      self.exportAsHtmlAction.setStatusTip('Preview')
      self.exportAsHtmlAction.setShortcut('Ctrl+H')


      self.boldAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_BOLD), '&Bold', self)
      self.boldAction.setShortcut('Ctrl+B')
      self.boldAction.setStatusTip('Bold')
      self.boldAction.triggered.connect(self.text_make_bold)

      self.italicAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_ITALIC), '&Italic', self)
      self.italicAction.setShortcut('Ctrl+I')
      self.italicAction.setStatusTip('Italic')
      self.italicAction.triggered.connect(self.text_make_italic)

      self.quoteAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_QUOTE), '&Quote', self)
      self.quoteAction.setShortcut('Ctrl+G')
      self.quoteAction.setStatusTip('Quotes')
      self.quoteAction.triggered.connect(self.text_make_quote)

      self.codeAction = QtGui.QAction(QtGui.QIcon(Constants.ICON_CODE), '&Code', self)
      self.codeAction.setShortcut('Ctrl+K')
      self.codeAction.setStatusTip('Code')
      self.codeAction.triggered.connect(self.text_make_code)

      actionMenu.addAction(self.boldAction)
      actionMenu.addAction(self.italicAction)
      actionMenu.addAction(self.quoteAction)
      actionMenu.addAction(self.codeAction)
      actionMenu.insertSeparator(self.previewHtmlAction)
      actionMenu.addAction(self.previewHtmlAction)
      actionMenu.addAction(self.exportAsHtmlAction)

      # tools menu
      toolsMenu = menubar.addMenu("&Tools")

      self.themesMapper = QtCore.QSignalMapper(self)
      self.themesMenu = QtGui.QMenu('&Html themes', self)
      self.themesMenuAG = QtGui.QActionGroup(self, exclusive=True)

      self.mthemesMapper = QtCore.QSignalMapper(self)
      self.mthemesMenu = QtGui.QMenu('&Markdown themes', self)
      self.mthemesMenuAG = QtGui.QActionGroup(self, exclusive=True)

      self.aboutAction = QtGui.QAction(QtGui.QIcon(''), '&About', self)
      self.aboutAction.setStatusTip('About')
      self.aboutAction.triggered.connect(self.dialog_about)

      self.helpAction = QtGui.QAction(QtGui.QIcon(''), '&Help', self)
      self.helpAction.setShortcut('Ctrl+H')
      self.helpAction.setStatusTip('Help')

      toolsMenu.insertMenu(self.aboutAction, self.mthemesMenu)
      toolsMenu.insertMenu(self.aboutAction, self.themesMenu)
      toolsMenu.insertSeparator(self.aboutAction)
      toolsMenu.addAction(self.aboutAction)
      toolsMenu.addAction(self.helpAction)

    def make_toolbar(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAction)

        self.toolbar.addAction(self.boldAction)
        self.toolbar.addAction(self.italicAction)
        self.toolbar.addAction(self.quoteAction)
        self.toolbar.addAction(self.codeAction)

    # center the window on the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_theme_to_menu(self, name, path, checked = False):
      themeAction = QtGui.QAction('&' + str(name), self, checkable=True)
      themeAction.setChecked(checked)
      a = self.themesMenuAG.addAction(themeAction)
      self.themesMenu.addAction(a)
      self.themesMapper.setMapping(themeAction, str(path))
      return themeAction


    def add_mtheme_to_menu(self, name, path, checked = False):
      themeAction = QtGui.QAction('&' + str(name), self, checkable=True)
      themeAction.setChecked(checked)
      a = self.mthemesMenuAG.addAction(themeAction)
      self.mthemesMenu.addAction(a)
      self.mthemesMapper.setMapping(themeAction, str(path))
      return themeAction

    """
        Events
    """
    @QtCore.pyqtSlot()
    def open_new_file_window(self):
        self.newFileWindow.exec_()

    # event called when we went quit.
    @QtCore.pyqtSlot(int)
    def closeEvent(self, event):
      logger.info("quit")
      """ disable for tests.
        reply = QtGui.QMessageBox.question(self,
                'Message',
                "Are you sure to quit?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
      """

    @QtCore.pyqtSlot(str, int)
    def update_status(self, string, time=1500):
        self.statusBar().showMessage(string, time)

    """
        Tabs
    """

    def change_active_tab(self, index):
        self.tabs.setCurrentIndex(index)

    def add_tab(self, title):
        tab = QtGui.QWidget()
        self.tabs.addTab(tab, title)

        textEdit = mTextEdit.mTextEdit(self)

        self.highlighter = MarkdownHighlighter.MarkdownHighlighter(textEdit)

        font = QtGui.QFont()
        font.setFamily(Constants.EDIT_FONT)
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)

        #textEdit.setFont(font)
        textEdit.setGeometry(0, 0, 200, 200)
        textEdit.setTabStopWidth(10)

        tab_hbox = QtGui.QHBoxLayout()
        tab_hbox.addWidget(textEdit)

        tab.setLayout(tab_hbox)

        return textEdit

    def remove_tab(self, index):
        self.tabs.removeTab(index)

    def active_tab(self):
      return self.tabs.currentWidget()

    """
            Dialogs
    """
    def dialog_about(self):
        QtGui.QMessageBox.about(self, "About", "<b>Cours</b><br>version "+Constants.VERSION+"<br><br>Author: "+Constants.AUTHOR+"<br><br>License: "+Constants.LICENSE)

    """
        some functions
    """
    def get_current_document_content(self):
      textEdit = self.active_input()
      return unicode(textEdit.toPlainText())

    def set_document(self, content):
      textEdit = self.active_input()
      textEdit.setPlainText(QtCore.QString(content))

    def active_input(self):
      tabs = self.tabs
      if not tabs:
        return None
      return tabs.currentWidget().findChildren(QtGui.QTextEdit)[0]

    def runError(self, title, string):
      QtGui.QMessageBox.critical(self, title, string)

    def confirm(self, title, string):
        reply = QtGui.QMessageBox.question(self, title, string,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        return False



    """
    Text manipulation
    """
    def text_make_quote(self):
      textEdit = self.active_input()
      cursor = textEdit.textCursor()
      textSelected = cursor.selectedText()
      cursor.insertText("\n> "+textSelected)

    def text_make_bold(self):
      self.format_text("**")

    def text_make_italic(self):
      self.format_text("*")

    def text_make_code(self):
      self.format_text("`")

    def format_text(self, character):
      textEdit = self.active_input()
      cursor = textEdit.textCursor()
      textSelected = cursor.selectedText()
      cursor.insertText(character + textSelected + character)
      if len(textSelected) == 0:
        cursor.setPosition(cursor.position() - len(character))
        textEdit.setTextCursor(cursor)

