import Constants
import os, json
from PyQt4 import QtGui, QtCore

from . import MarkdownHighlighter
from directory import directory
from mTheme import mTheme

class Model():

  def __init__(self, view):
    self.VIEW = view
    self.TABS = [ { "path": "" } ]
    self.THEMES = []
    self.MTHEMES = []
    self.themeContent = None

    self.theme = self.get_from_config("theme")
    if not self.theme or type(self.theme) != dict:
      self.theme = {"path":Constants.DEFAULT_CSS_PATH, "name": Constants.DEFAULT_CSS_NAME}


    self.mtheme = self.get_from_config("mtheme")
    if not self.mtheme or type(self.mtheme) != dict:
      self.mtheme = {"path":Constants.DEFAULT_MTHEME_PATH, "name": Constants.DEFAULT_MTHEME_NAME}

    self.load_css()
    self.load_themes()
    self.load_mthemes()

  def get_filename(self, filepath):
    path = str(filepath)
    t = path.split("/")
    return t[ len(t) - 1 ]

  def get_file_folder(self, filepath):
    path = filepath
    t = path.split("")
    str = ""
    for i in range(len(t) - 1):
      str = str + t[i] + "/"
    return str

  def is_document_present(self, filepath):
    for i in range(len(self.TABS)):
      if self.TABS[i]['path'] == filepath:
        return i
    return -1

  def append_doc(self, filepath):
    if len(filepath) != 0:
      self.TABS.append({ "path":filepath })

  def get_document_title(self):
    return self.TABS[self.get_active_tab()]['path']

  def get_active_tab(self):
    return self.VIEW.tabs.currentIndex() + 1

  def get_active_tab_name(self):
    return self.TABS[self.get_active_tab()]['path']

  def get_file_content(self, filepath):
    try:
      f = open(filepath, "r")
      return f.read()
    except Exception:
      raise Exception()

  def write_file_content(self, filepath, data):
    f = open(filepath, "w")
    f.write(str(data))
    f.close()

  def remove_tab(self, index):
    self.TABS.pop(index)

  def load_css(self):
    extension = ".css"
    themepath = self.theme["path"]
    try:
      self.css = self.get_file_content(themepath)
    except Exception:
      self.VIEW.runError("Error", "Unable to load theme: " + self.theme + " on " + themepath)

  def set_css(self, themepath):
    for theme in self.THEMES:
      if theme["path"] == themepath:
        self.theme = theme
        break
    self.load_css()
    self.save_in_config("theme", self.theme)
    self.VIEW.update_status("Load theme: " + self.theme["name"])

  def set_mtheme(self, themepath):
    for theme in self.MTHEMES:
      if theme["path"] == themepath:
        self.mtheme = theme
        break

    theme = mTheme(self, self.mtheme["path"])
    self.themeContent = theme.load()
    if not self.themeContent:
      self.VIEW.runError("Error", "Unable to load Markdown theme " + self.mtheme["path"])
      return

    # we apply theme on each tab
    tabs = self.VIEW.tabs
    i = 0
    while i < tabs.count():
      tab = tabs.widget(i)
      if not tab:
        print ("No tab")
        return
      textEdit = tab.findChildren(QtGui.QTextEdit)[0]
      if not textEdit:
        print("No text edit")
        return
      i = i + 1
      self.VIEW.highlighter = MarkdownHighlighter.MarkdownHighlighter(textEdit, self.themeContent)

    self.VIEW.update_status("Load Markdown theme: " + self.mtheme["name"])
    self.save_in_config("mtheme", self.mtheme)

  def load_themes(self):
    dir = directory(Constants.CSS_DIR)
    files = dir.read()
    for f in files:
      style = { "name": f.filename(), "path": f.getPath() }
      self.THEMES.append(style)
    dir.close()
    if not self.THEMES:
      self.VIEW.runError("Error", "Can't load themes...")
      return False
    for theme in self.THEMES:
      checked = False
      if theme["path"] == self.theme["path"]:
        checked = True
      action = self.VIEW.add_theme_to_menu(theme["name"], theme["path"], checked)
      action.triggered.connect(self.VIEW.themesMapper.map)

  def load_mthemes(self):
    dir = directory(Constants.MTHEMES_DIR)
    files = dir.read()
    for f in files:
      theme = { "name": f.filename(), "path": f.getPath() }
      self.MTHEMES.append(theme)
    dir.close()
    if not self.MTHEMES:
      self.VIEW.runError("Error", "Can't load Markdown themes...")
      return False
    for theme in self.MTHEMES:
      checked = False
      if theme["path"] == self.mtheme["path"]:
        checked = True
      action = self.VIEW.add_mtheme_to_menu(theme["name"], theme["path"], checked)
      action.triggered.connect(self.VIEW.mthemesMapper.map)

  def get_from_config(self, key):
    try:
      result = self.get_file_content(Constants.CONFIG_FILE)
    except Exception:
      self.VIEW.runError("Error", "Unable to load configuration file: " + Constants.CONFIG_FILE)
      return None
    try:
      data = json.loads(result)
    except ValueError:
      self.VIEW.runError("Error", "Config file broken. Json can't be decode")
    if key in data and type(data) is not None:
      return data[key]
    else:
      return None

  def save_in_config(self, key, value):
    try:
      result = self.get_file_content(Constants.CONFIG_FILE)
    except Exception:
      self.VIEW.runError("Error", "Unable to load configuration file: " + Constants.CONFIG_FILE)
      return None
    try:
      data = json.loads(result)
    except ValueError:
      self.VIEW.runError("Error", "Config file broken. Json can't be decode")
    data[key] = value
    self.write_file_content(Constants.CONFIG_FILE, json.dumps(data))
