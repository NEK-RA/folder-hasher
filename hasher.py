#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path
from os import sep

# parse arguments of script - https://docs.python.org/3/library/argparse.html
# work with paths  - https://docs.python.org/3/library/pathlib.html
# read file in binary format - https://docs.python.org/3/library/io.html
# hashing - https://docs.python.org/3/library/hashlib.html
# list of available hashing algorithms for current python interpretter - hashlib.algorithms_available
# os.sep is platform specific separator for paths, which is "/" on linux/unix and "\\" on windows

# file hashing function
def hash_file(path, method):
  print(f"Calculating hashsum for {path}")
  # take required hashing algorithm
  hashing = hashlib.new(method)
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
  levels = str(path).split(sep)
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
  hashfile = sep.join(levels[:cut])
  # adding folder name one more time, as it will be hashfile name actually
  # extension will be added to it in hash_tasks function, right before writing hashes to file
  hashfile += f"{sep}{levels[cut-1]}"
  # relative path to file, which should be written to hashfile
  # if absolute=true, then absolute path will be kept for file
  # otherwise relative will be used
  relative = ""
  if absolute:
    relative = str(path)
  else:
    relative = sep.join(levels[cut:])
  # returning path too, as it will be used to pass to hash function
  return (hashfile, relative, path)
  
# function where raw tasks are processed into final stage and then hashed
def hash_tasks(tasksets,startpath,method,absolute):
  # dict used to avoid hashfile paths duplication
  final_tasks = dict()
  # iterating through raw tasks
  for taskset in tasksets:
    # iterating through file for current raw task
    for task in taskset["tasks"]:
      # preparing hashfile path, path which will be shown in hashfile
      # and absolute path to file, which will be actually used in hashing function
      hashfile, relative, path = final_preparation(task,startpath,taskset["depth"],absolute)
      # if hashfile not yet appeared while processing tasks, then add it and related task
      # else just append prepared elements to list of tasks for this hashfile
      if hashfile not in final_tasks.keys():
        final_tasks[hashfile] = [dict(name=relative,fullpath=path)]
      else:
        final_tasks[hashfile].append(dict(name=relative,fullpath=path))
  # iterating through hashfile paths
  for key in final_tasks.keys():
    # all strings will firstly be written into content variable
    # so later will be just one writing to file
    content = ""
    # adding method as extension of hashfile
    hashfilepath = f"{key}.{method}"
    for file in final_tasks[key]:
      # calculating hashsum and addint to the end of current hashfile
      checksum = hash_file(file["fullpath"],method)
      content += f"{checksum}  {file['name']}\n"
    # when all hashsums were calculated, writing them to file
    with open(hashfilepath,"w") as result:
      result.write(content)

# entrypoint after processing the arguments, may be used if script imported somewhere
def hasher(pathstr,method="md5",depth=0,absolute=False):
  # summary
  print(f"Hashing folder: {pathstr}\nAlgorithm: {method}\nUsing depth: {depth}\nUsing absolute paths: {absolute}")
  # replacing ~ with actual $HOME path
  if "~" in pathstr:
    pathstr = pathstr.replace("~",str(Path.home()))
  # resolving absolute path for case if relative was provided
  path = Path(pathstr).resolve()
  # check if path doesn't exist
  if not path.exists():
    exit(f"ERROR: Path {path} does not exist")
  # if depth specified as negative, it should be replaced by 0
  if depth < 0:
    depth = 0
  # gathering all files in this folder
  sets = recursive_childs(path,depth)
  # check if method is available
  if method not in hashlib.algorithms_available:
    exit(f"ERROR: Hashing algorithm {method} is not available in current python interpreter")
  # hash the folder  
  hash_tasks(sets, path.name, method, absolute)
  
if __name__=="__main__":
  shortinfo="""
  Calculate hashes for all files in the folder (including nested folders) with specifying depth, method and if absolute paths to files should be used or not
  """
  methodinfo = "Hashing algorithm (default: md5)"
  depthinfo = "Depth for placing hashfiles, using name of this folder with hash suffix, like: myfolder.md5 (default: 0 - inside specified folder)"
  absinfo = "Option to write absolute paths to files into hashfile, or not. By default relative paths will be used."
  pathinfo = "Path to folder which content should be hashed"
  
  parser = argparse.ArgumentParser(description=shortinfo)

  parser.add_argument("-m","--method", dest="method", type=str, default="md5", choices=hashlib.algorithms_available, help=methodinfo)
  parser.add_argument("-d","--depth", dest="depth", type=int, default=0, help=depthinfo)
  parser.add_argument("-a", "--absolute", dest="absolute", action="store_true", help=absinfo)
  parser.add_argument('path', metavar='path', type=str, help='path to file or folder')

  args = parser.parse_args()
  hasher(args.path, args.method, args.depth, args.absolute)
