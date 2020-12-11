# Ziphyr

Ziphyr is an on-the-fly zip archiving applied on a streamed file source, with optional on-the-fly encryption.

![GitHub](https://img.shields.io/github/license/quarkslab/ziphyr)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/quarkslab/ziphyr/Python%20Tox/master)
![PyPI](https://img.shields.io/pypi/v/ziphyr)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ziphyr)

## Features

* Disclaimer: *the zip-native cryptography is unsecure*
* Streamed file turned into a streamed zip
* Can be used password-less for a non-encrypted zip stream
* Or with a password to apply on-the-fly zipcrypto to the stream
* Retro-compatibility for py35 with writable ZipInfo port

## Install

```console
    $ pip install ziphyr
```

## Usage

```python
   from ziphyr import Ziphyr

   # init the Ziphyr object
   z = Ziphyr(b'infected')
   # z = Ziphyr() for crypto-less usage

   # prepare it for a specific file, from path or metadata directly
   z.from_filepath(filepath)

   # consume the generator to get the encrypted ziped chunk
   for k in z.generator(source):
       pass
```

## Test

```console
   $ python -m unittest -v tests/*.py
```

## Contributing

Contributions are welcome and are always greatly appreciated. Every little bit helps and credit will always be given. You can contribute in many ways:
* reporting a bug
* submitting feedback
* helping fix bugs
* implementing new features
* writting better documentation

Remember that before submitting a pull request, you should if relevant include tests and update documentation.

## Credits and references

### zip-related

* [Python 3 zipfile](https://docs.python.org/3/library/zipfile.html>)
* [PKWARE's .ZIP File Format Specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)

### Underlying works

The following works served as sources of inspiration or examples for implementation.

* [devthat/zipencrypt](https://github.com/devthat/zipencrypt) (*MIT license*)
* [Ivan Ergunov's zipfile_generator](https://repl.it/@IvanErgunov/zipfilegenerator>) (*MIT license*)

### Cookiecutter

This package was kickstarted with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
