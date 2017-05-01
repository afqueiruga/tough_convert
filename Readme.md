tough\_convert
=============

A utility for converting tough mesh files and outputs into other common visualization formats.

Lawrence Berkeley National Lab, 2016

Overview
--------

tough\_convert is utility for converting input and output formats for the TOUGH family of codes (TOUGH2, TOUGH+, etc.) into formats usable by other scientific visualization packages. The primary purpose is to create VTK or silo data files to render simulation results using ParaView or VisIt. Meshes can either be rendered as a centroid-connection graph, useful for visually verifying connectivity, or as a standard volumetric mesh using additional information output by MeshMaker. Concatenation and reordering of parallel TOUGH output formats is supported. Rock types can be filtered out to improve visualization clarity. tough\_ convert can also generate equivalent 2D meshes in Flac3D or gmsh formats to easily couple a TOUGH simulation to a geomechanics module that requires a one-to-one mesh correspondence.

Requirements
------------

This is a tool for use with TOUGH+. MeshMaker is needed to generate cell corners (connection visualization is
possible without the corners.)

- Python 2.7 (3.0 support is a TODO)
- numpy

For silo output:

- libsilo
- pyvisfile

Usage
-----

See tough\_convert.py --help

tough_convert can do the following:

1. Output raw meshes as VTK files, Silo files, and FLAC3D meshes using MeshMaker's CORNERS output.
2. Output the dual-graph representation (cell-face-cell) used by tough as VTK and Silo
3. Output simulation data from PlotDataElem in VTK and Silo formats
4. Support reordering of the mesh according to a TOUGH inconn file to associate with output files and
produce appropriate meshes for TOUGH-FLAC.

License
-------

TBD

Acknowledgements
----------------

This software was developed under the TOUGH development grant titled "3-D Volume Rendering of TOUGH meshes and simulation outputs".
