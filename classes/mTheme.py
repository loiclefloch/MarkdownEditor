import os, json

class mTheme():

  def __init__(self, model, filepath):
    self.filepath = filepath
    self.MODEL = model
    self.mtheme = {
      'h1': "",
      'h2': "",
      'h3': "",
      'h4': "",
      'h5': "",
      'h6': "",
      'bold': "",
      'italic': "",
      'link': "",
      'code': "",
      'anchor': "",
      'quotes': "",
      'html': ""
    }

  def load(self):
    try:
      result = self.MODEL.get_file_content(self.filepath)
    except Exception:
      self.MODEL.VIEW.runError("Error", "File does not exists: " + self.filepath)
      return None

    try:
      data = json.loads(result)
    except ValueError:
      self.MODEL.VIEW.runError("Error", "Json file is broken: " + self.filepath)
      return None

    for tag in self.mtheme.keys():
      if tag in data and type(data) is not None:
        self.mtheme[tag] = data[tag]
    return self.mtheme
