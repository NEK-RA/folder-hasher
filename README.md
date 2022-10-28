# folder-hasher

Calculate hashes for all files in the folder (including nested folders) with
specifying depth, method and if absolute paths to files should be used or not.

Depends only on python runtime and openssl

# Usage

`python3 hasher.py --method METHOD --depth DEPTH --absolute /absolute/or/relative/path`

Shortcuts:

- `--method` = `-m`
- `--depth` = `-d`
- `--absolute` = `-a`

### Method

Method is which hashsums do you want to calculate - md5, sha1 and etc. Amount of available methods is requested from python runtime, so probably it may differ depending on version / platform / architecture / anything else.

Related link to python docs: https://docs.python.org/3/library/hashlib.html#hash-algorithms

For example in my `Python 3.8.10` for `Ubuntu 20.04` there are available:

- ripemd160
- md4
- md5
- md5-sha1
- sha1
- sha224
- sha256
- sha384
- sha512
- sha512_224
- sha512_256
- sha3_224
- sha3_256
- sha3_384
- sha3_512
- blake2b
- blake2s
- sm3
- shake_128
- shake_256
- whirlpool

### Depth

Depth is for specifying where hashfiles should be placed. Lets imagine that we have `template` folder with next tree view:

```
template
├── README.md
├── package-lock.json
├── package.json
├── src
│   ├── app
│   │   ├── handlers
│   │   │   ├── bot
│   │   │   │   ├── index.ts
│   │   │   │   └── info.ts
│   │   │   └── index.ts
│   │   ├── helpers
│   │   │   └── name.ts
│   │   └── server
│   │       ├── bot.ts
│   │       ├── env.ts
│   │       ├── express.ts
│   │       ├── index.ts
│   │       └── routes.ts
│   ├── index.ts
│   ├── src.sha1
│   └── src.whirlpool
└── tsconfig.json
```

With `--depth 0` (default) we will get `template/template.md5` file with content like this:

```
d2a7d21a911629e8c84bb2b6693cb929  .env
47c3c56f9ae310aed20dd16a7a961ee0  .env.example
3896d84c246040135f72cce2cc9db64b  .gitignore
...
a39bb438535e38480e80db61af6faf23  src/app/server/routes.ts
```

With `--depth 1` we will get `template/template.md5` with hashsums for `readme`,`package-json` and `tsconfig.json` files. 

But also going one level deeper we'll found also `template/src/src.md5` which contain hashes for all files inside `src` folder including nested folders and files.

With max depth for this example, equal to 4: each folder will contain it's own `foldername.algorithm` with hashsums only for files which are located in it, without content of nested folders.

### Absolute paths

This option let you choose if you want to see `src/index.ts` or `/home/user/projects/node/template/src/index.ts` (from the example above)

# Why

Firstly was written for friend, but I guess somebody else may find it useful :)

# What's next

- [ ] Make ability to verify files via hashsums by something like `-c path` (`--check path`)
- [ ] Think a bit later about it and see if anything may be improved
