import argparse
import hashlib
import pathlib

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


hashing = gethasher("sha256")
with open("main.py","rb") as source:
    data = source.read()
    hashing.update(data)
    result = hashing.hexdigest()
    print(f"{result} - main.py")
