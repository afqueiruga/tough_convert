import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tough_convert",
    version = "1.0",
    author = "Alejandro Francisco Queiruga and Matthew Reagan",
    description = "A utility for converting TOUGH mesh files and outputs into other common visualization formats.",
    license = "BSD 3-clause",
    keywords = "",
    packages=['tough_convert'],
    #test_suite='test',
    long_description=read('Readme.md'),
    classifiers=[],
    entry_points = {
        'console_scripts' : ['tough_convert = tough_convert.main:main']
    },
)
