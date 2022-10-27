#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

# parse arguments of script - https://docs.python.org/3/library/argparse.html
# work with paths  - https://docs.python.org/3/library/pathlib.html
# read file in binary format - https://docs.python.org/3/library/io.html
# hashing - https://docs.python.org/3/library/hashlib.html

def gethasher(method):
  if method == 'sha1':
    return hashlib.sha1()
  elif method == 'sha256':
    return hashlib.sha256()
  else:
    return hashlib.md5()

def hashfile(path, method):
  hashing = gethasher(method)
  with open("main.py","rb") as source:
    file = source.read()
    hashing.update(file)
    result = hashing.hexdigest()
    print(f"{result} - {path.resolve()}")


path = Path("main.py")
hashfile(path,"sha1")
