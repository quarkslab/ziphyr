#!/usr/bin/env python

"""The setup script."""

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='ziphyr',
    version='0.1.0',
    description="On-the-fly zipcrypto applied on streamed file source.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/quarkslab/ziphyr',
    author="irma-dev",
    author_email='irma-dev@quarkslab.com',
    license="Apache Software License 2.0",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[],
    include_package_data=True,
    keywords='ziphyr',
    packages=['ziphyr'],
    setup_requires=[],
    test_suite='tests',
    tests_require=[],
    zip_safe=False,
)
