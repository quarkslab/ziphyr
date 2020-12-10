======
Ziphyr
======


.. image:: https://img.shields.io/pypi/v/ziphyr.svg
        :target: https://pypi.python.org/pypi/ziphyr

.. image:: https://img.shields.io/travis/quarkslab/ziphyr.svg
        :target: https://travis-ci.com/quarkslab/ziphyr

.. image:: https://readthedocs.org/projects/ziphyr/badge/?version=latest
        :target: https://ziphyr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Ziphyr is an on-the-fly zipcrypto archiving applied on a streamed file source.


* Free software: Apache Software License 2.0
* Documentation: https://ziphyr.readthedocs.io.

Features
--------

* Streamed file turned into a streamed zip
* zipcrypto applied on-the-fly on the stream

Install
-------

To install Ziphyr, run this command in your terminal:

.. code-block:: console

    $ pip install ziphyr

Usage
-----

.. code-block:: python

   from ziphyr import Ziphyr

   # init the Ziphyr object
   z = Ziphyr(b'infected')

   # prepare it for a specific file, from path or metadata directly
   z.from_filepath(filepath)

   # consume the generator to get the encrypted ziped chunk
   for k in z.generator(source):
       pass

Test
----

.. code-block:: console

   $ python -m unittest -v tests/*.py

Credits and references
----------------------

Underlying works
^^^^^^^^^^^^^^^^
The following works served as sources of inspiration or examples for implementation.

* `devthat/zipencrypt <https://github.com/devthat/zipencrypt>`_ (*MIT license*)
* `Ivan Ergunov's zipfile_generator <https://repl.it/@IvanErgunov/zipfilegenerator>`_ (*MIT license*)

Cookiecutter
^^^^^^^^^^^^
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

zip-related
^^^^^^^^^^^
- `Python 3 zipfile <https://docs.python.org/3/library/zipfile.html>`_
- `PKWARE's .ZIP File Format Specification <https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT>`_
