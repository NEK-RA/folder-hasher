import hashlib

hashing = hashlib.md5()
with open("main.py","rb") as source:
    data = source.read()
    hashing.update(data)
    result = hashing.hexdigest()
    print(f"{result} - main.py")
