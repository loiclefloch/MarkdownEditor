#!/bin/python

class FileException(Exception):
  def __init__(self, msg=""):
    self.msg = msg

  def __str__(self):
    return self.msg

  def error(self):
    return self.msg
