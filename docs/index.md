## Features
* Disclaimer: the zip-native cryptography is unsecure
* Streamed file turned into a streamed zip
* Optional zipcrypto applied on-the-fly on the stream
* Retro-compatibility for py35 with writable ZipInfo port

![GitHub](https://img.shields.io/github/license/quarkslab/ziphyr)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/quarkslab/ziphyr/Python%20Tox/master)
![PyPI](https://img.shields.io/pypi/v/ziphyr)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ziphyr)

## Package

### Install

```console
    $ pip install ziphyr
```

### Usage

```python
   from ziphyr import Ziphyr

   # init the Ziphyr object
   z = Ziphyr(b'infected')
   # z = Ziphyr() for crypto-less usage

   # prepare it for a specific file
   # from path or metadata directly
   z.from_filepath(filepath)

   # consume the generator to get
   # the encrypted ziped chunk
   for k in z.generator(source):
       pass
```

### Test

```console
   $ python -m unittest -v tests/*.py
```

## Technical details

```console
ziphyr
├── ziphyr
│   ├── Ziphyr
│   └── PKCryptoZipInfo
├── stream
│   ├── ZiphyrStream
│   └── _gen_crc
├── retro
│   ├── RetroZipFile
│   ├── _ZipWriteFile
│   ├── RetroZipInfo
│   └── retro_from_file
└── utils
    └── file_iterable
```

## Shout-outs

* [Python 3 zipfile](https://docs.python.org/3/library/zipfile.html>)
* [PKWARE's .ZIP File Format Specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
* [devthat/zipencrypt](https://github.com/devthat/zipencrypt) (*MIT license*)
* [Ivan Ergunov's zipfile_generator](https://repl.it/@IvanErgunov/zipfilegenerator>) (*MIT license*)
