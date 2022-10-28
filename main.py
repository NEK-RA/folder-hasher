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
  hashing = get_hasher(method)
  # open target file for reading in binary mode
  with path.open(mode="rb") as source:
    file = source.read()
    hashing.update(file)
    result = hashing.hexdigest()
    # returning hash value in format similar to produced by md5sum and etc (hash, 2 spaces, filename)
    # need to edit path to files to avoid listing unnecessary parts of filepaths (start/file instead of /home/user/downloads/start/file)
    # the idea for now is to pass starting point path to hash_file function
    return result
    
# function to collect list of files for which hashsum should be calculated
# it create list of dicts with raw tasks
# later this list of raw tasks will be processed in hash_tasks function
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

def final_preparation(path,start,level,absolute):
  levels = str(path).split("/")
  index = levels.index(start)
  cut = None
  # checking if paths on required level are folders, not files
  # (actually if it's not the last element of path)
  # and selecting place to split by this
  if(index+1 != len(levels)-1):
    cut = index+1+level
  else:
    cut = index+1
  # getting part which will be folder where hashfile should be located
  hashfile = "/".join(levels[:cut])
  # adding folder name one more time, as it will be hashfile name actually
  # extension will be added to it in hash_tasks function, right before writing hashes to file
  hashfile += f"/{levels[cut-1]}"
  # relative path to file, which should be written to hashfile
  # if absolute=true, then absolute path will be kept for file
  # otherwise relative will be used
  relative = ""
  if absolute:
    relative = str(path)
  else:
    relative = "/".join(levels[cut:])
  # returning path too, as it will be used to pass to hash function
  return (hashfile, relative, path)
  

def hash_tasks(tasksets,startpath,method,absolute):
  final_tasks = dict()
  for taskset in tasksets:
    for task in taskset["tasks"]:
      hashfile, relative, path = final_preparation(task,startpath,taskset["depth"],absolute)
      if hashfile not in final_tasks.keys():
        final_tasks[hashfile] = [dict(name=relative,fullpath=path)]
      else:
        final_tasks[hashfile].append(dict(name=relative,fullpath=path))

  for key in final_tasks.keys():
    content = ""
    hashfilepath = f"{key}.{method}"
    for file in final_tasks[key]:
      checksum = hash_file(file["fullpath"],method)
      content += f"{checksum}  {file['name']}\n"
    print(f"\n\nGoing to write into {hashfilepath} next content:\n{content}")

# pathstr = "/usr/share/wallpapers"
# pathstr = "/usr/lib/dpkg/methods/apt"
# pathstr = "/usr/lib/dpkg/"
pathstr = "~/deta-template"
if "~" in pathstr:
  pathstr = pathstr.replace("~",str(Path.home()))
path = Path(pathstr).resolve()
sets = recursive_childs(path,3)
print(f"Hashing folder: {pathstr}\nAlgorithm: md5\nUsing depth: 3\nUsing absolute paths: False")
hash_tasks(sets, path.name, "md5",True)
#print( hashfile(path,"sha1") )
