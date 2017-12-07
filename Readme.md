tough-convert
=============

A utility for converting tough mesh files and outputs into other common visualization formats.

Alejandro Francisco Queiruga and Matthew Reagan

Lawrence Berkeley National Lab, 2016

tough-convert can do the following:

1. Output raw meshes as VTK files, Silo files, and FLAC3D meshes using MeshMaker's CORNERS output.
2. Output the dual-graph representation (cell-face-cell) used by tough as VTK and Silo
3. Output simulation data from PlotDataElem in VTK and Silo formats
4. Support reordering of the mesh according to a TOUGH inconn file to associate with output files and
produce appropriate meshes for TOUGH-FLAC.

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

See tough-convert.py --help. An example usage for TOUGH+ formatted output is
```bash
python /path/to/tough-convert/main.py MESH --data Plot_Data_Elem --order SAVE --vtk outs/viz.vtk
```
(note the directory `outs/` must exist.)

License and Citing
------------------

License TBD

If you use this utility in your work, please cite this repository with the following key:
```latex
{

}
```
Acknowledgements
----------------

Developed under TOUGH development grant XXXX
