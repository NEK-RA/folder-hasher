#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

# parse arguments of script - https://docs.python.org/3/library/argparse.html
# work with paths  - https://docs.python.org/3/library/pathlib.html
# read file in binary format - https://docs.python.org/3/library/io.html
# hashing - https://docs.python.org/3/library/hashlib.html
# list of available hashing algorithms for current python interpretter - hashlib.algorithms_available

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
def hash_file(path, method):
  # take required hashing algorithm
  hashing = gethasher(method)
  # open target file for reading in binary mode
  with open("main.py","rb") as source:
    file = source.read()
    hashing.update(file)
    result = hashing.hexdigest()
    # returning hash value in format similar to produced by md5sum and etc (hash, 2 spaces, filename)
    # need to edit path to files to avoid listing unnecessary parts of filepaths (start/file instead of /home/user/downloads/start/file)
    # the idea for now is to pass starting point path to hash_file function
    return f"{result}  {path.resolve()}"
    
# function to collect list of files for which hashsum should be calculated
def recursive_childs(path,depth,level=0):
  # final list of tasks - dict(depth=number, tasks=[list,of,paths])
  paths = []
  # lists for current folder
  files = []
  folders = []
  # checking current path for content if it's a folder
  if path.is_dir():
    # walk through folder content and checking which entries are files and folders
    for item in list(path.iterdir()):
      if item.is_file():
        files.append(item)
      else:
        folders.append(item)
  # if not a folder then just add path to hash tasks
  else:
    files.append(path)
  # checking if we need to go deeper
  if len(folders):
    deeper = []
    for item in folders:
      # recursively collecting childs for nested folders and so on
      deeper = recursive_childs(item,depth,level+1)
      for deepitem in deeper:
        # checking if nested tasks are not empty
        if len(deepitem['tasks']):
          # if current nested level is below specified depth
          # then each folder have it own separate tasks
          if level < depth:
            paths.append(deepitem)
          # if level is equal or deeper than specified depth
          # then all nested paths should be inside of tasks for this level
          else:
            files.extend(deepitem["tasks"])
          

  # adding files from current folder
  if len(files):
    paths.insert(
      0,
      dict(
        depth=level,
        tasks=files
      )
    )
  # returning list of tasks in current folder
  
  return paths
    
def hash_tasks(tasksets):
  for taskset in tasksets:
    print(taskset)
    print("\n")

# pathstr = "/usr/share/wallpapers"
# pathstr = "/usr/lib/dpkg/methods/apt"
pathstr = "/usr/lib/dpkg/"
if "~" in pathstr:
  pathstr = pathstr.replace("~",str(Path.home()))
path = Path(pathstr).resolve()
sets = recursive_childs(path,0)
hash_tasks(sets)
#print( hashfile(path,"sha1") )
