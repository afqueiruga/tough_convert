tough\_convert
=============

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1164418.svg)](https://doi.org/10.5281/zenodo.1164418)

A utility for converting tough mesh files and outputs into other common visualization formats.

Alejandro Francisco Queiruga and Matthew Reagan

Lawrence Berkeley National Lab, 2016

Overview
--------

tough\_convert is utility for converting input and output formats for the TOUGH family of codes (TOUGH2, TOUGH+, etc.) into formats usable by other scientific visualization packages. The primary purpose is to create VTK or silo data files to render simulation results using ParaView or VisIt. Meshes can either be rendered as a centroid-connection graph, useful for visually verifying connectivity, or as a standard volumetric mesh using additional information output by MeshMaker. Concatenation and reordering of parallel TOUGH output formats is supported. Rock types can be filtered out to improve visualization clarity. tough\_ convert can also generate equivalent 2D meshes in Flac3D or gmsh formats to easily couple a TOUGH simulation to a geomechanics module that requires a one-to-one mesh correspondence.

tough-convert can do the following:

1. Output raw meshes as VTK files, Silo files, and FLAC3D meshes using MeshMaker's CORNERS output.
2. Output the dual-graph representation (cell-face-cell) used by tough as VTK and Silo
3. Output simulation data from PlotDataElem in VTK and Silo formats
4. Support reordering of the mesh according to a TOUGH inconn file to associate with output files and
produce appropriate meshes for TOUGH-FLAC.

Requirements
------------

This is a tool for use with TOUGH+ or TOUGH2. MeshMaker is needed to generate cell corners. Connection visualization is
possible without the corners.

- Python 2.7 or 3.0
- numpy

For silo output:

- libsilo
- pyvisfile

Usage
-----

See tough-convert.py --help. An example usage for TOUGH+ formatted output is
```bash
python /path/to/tough-convert/main.py MESH --data Plot_Data_Elem --order SAVE --vtk outs/viz.vtk
```
(note the directory `outs/` must exist.)

License and Citing
------------------

Copyright (c) 2015-2017, Alejandro Francisco Queiruga and Matt Reagan.

This work is released under the three-clause BSD License. See the file LICENSE for the full text.

If you use this utility in your work, please cite this repository with the following key:
```latex
@misc{toughconvert2016,
  author = {A. F. Queiruga and M. T. Reagan},
  title = {tough-convert},
  year = {2016},
  publisher = {Bitbucket},
  journal = {Bitbucket repository},
  howpublished = {https://bitbucket.org/afqueiruga/tough-convert/}
}
```

Acknowledgements
----------------

This software was developed under the TOUGH development grant titled "3-D Volume Rendering of TOUGH meshes and simulation outputs".
