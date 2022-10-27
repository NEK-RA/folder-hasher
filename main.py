#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

# parse arguments of script - https://docs.python.org/3/library/argparse.html
# work with paths  - https://docs.python.org/3/library/pathlib.html
# read file in binary format - https://docs.python.org/3/library/io.html
# hashing - https://docs.python.org/3/library/hashlib.html

# function which returns concrete hashing algorithm
# depending on passed value
# made to let user choose target hashing algorithm
# currently made without match-case to make script work in older versions
def get_hasher(method):
  if method == 'sha1':
    return hashlib.sha1()
  elif method == 'sha256':
    return hashlib.sha256()
  else:
    return hashlib.md5()

# file hashing function
# take required hashing algorithm, open target file for reading in binary mode
# returning hash value in format similar to seen by using md5sum and etc
# need to edit path to avoid listing unnecessary parts of filepaths
def hash_file(path, method):
  hashing = gethasher(method)
  with open("main.py","rb") as source:
    file = source.read()
    hashing.update(file)
    result = hashing.hexdigest()
    return f"{result}  {path.resolve()}"

def recursive_childs(path,level=0):
  paths = []
  files = []
  folders = []
  if path.is_dir():
    for item in list(path.iterdir()):
      if item.is_file():
        files.append(item)
      else:
        folders.append(item)
  else:
    files.append(path)
  if len(files):
    paths.append(
      dict(
        depth=level,
        tasks=files
      )
    )
    
  deeper = []
  for item in folders:
    deeper = recursive_childs(item,level+1)
    for deepitem in deeper:
      if len(deepitem['tasks']):
        paths.append(deepitem)
  # print(deeper)
  # print(paths)
  return paths
    


path = Path("/usr/share/wallpapers")
# path = Path("/usr/lib/dpkg/methods/apt")
# path = Path("/usr/lib/dpkg/")
sets = recursive_childs(path)
for each in sets:
  print(each)
  for task in each["tasks"]:
    print(task)
  print("\n")
#print( hashfile(path,"sha1") )
