tough-convert
=============

A utility for converting tough mesh files and outputs into other common visualization formats.

Lawrence Berkeley National Lab, 2016

Requirements
------------

- Python 2.7 (3.0?)
- numpy
For silo output:
- libsilo
- pyvisfile
To generate inputs:
- MeshMaker
To generate ordering and input data:
- TOUGH+

Usage
-----

See tough-convert.py --help

tough-convert can do the following:

1) Output raw meshes as VTK files, Silo files, and FLAC3D meshes using MeshMaker's CORNERS output.
2) Output the dual-graph representation (cell-face-cell) used by tough as VTK and Silo
3) Output simulation data from PlotDataElem in VTK and Silo formats
4) Support reordering of the data according to a TOUGH inconn file

License
-------

TBD

Acknowledgements
----------------

Developed under TOUGH development grant XXXX
