path = "system/ServerFiles/"

def make_file(filename, command):
  file = open(path + filename, command)
  file.close()

def remove_file(filename):
  import os
  if os.path.exists(path + filename):
    os.remove(path + filename)

