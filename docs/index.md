## Features
* Streamed file turned into a streamed zip
* zipcrypto applied on-the-fly on the stream
* retro-compatibility for py35 with writable ZipInfo port

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
│   └── retro_from_file
└── utils
    └── file_iterable
```

## Shout-outs

* [Python 3 zipfile](https://docs.python.org/3/library/zipfile.html>)
* [PKWARE's .ZIP File Format Specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
* [devthat/zipencrypt](https://github.com/devthat/zipencrypt) (*MIT license*)
* [Ivan Ergunov's zipfile_generator](https://repl.it/@IvanErgunov/zipfilegenerator>) (*MIT license*)
