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
4. Support reordering of the mesh according to a TOUGH incon file to associate with output files and
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

To install it,

```bash
python setup.py install --prefix=/path/to/opt/
```

The path will have to be in your python path, so make sure your environment is set up for a local install. It will install a scipt into `opt/bin` called `tough_convert` as well as an importable library `tough_convert` into site-packages.

Usage
-----

See `main.py --help`. An example usage for TOUGH+ formatted output is
```bash
tough_convert MESH --data Plot_Data_Elem --order SAVE --vtk outs/viz.vtk
```
(note the directory `outs/` must exist.)

tough\_convert can also be used from a Python API. It can be used to build an iteration over time snapshots for post processing,
```python
import tough_convert as tc
# Define the list of input files
data_root = "/home/user/tough/simulation/data/"
pde_nums = [1,3,8,15,16,17,20,22,25,32,33,37,47,54,55,61,65,66,67]
save_name = "SAVE_1"
datafiles = [ data_root+"/Plot_Data_Elem_{0}".format(i)
              for i in pde_nums ]
# Load a TOUGH configuration and register empty fields
TM = tc.Tough_Mesh(data_root+"/MESH",None,data_root+save_name,None)
# Loop over the data
for fname in datafiles:
    for t,step in enumerate(tc.load_plot_data_elem(fname)):
        print "--- File ",fname," step ",t
		r_array = step['r']
        z_array = step['z']
        for l in ['vol','p','T','S','trE','trSigma',
                      'trSigma_init','phi','dil']:
				  do_some_work(step['l'])
```
This workflow is particularly useful for performing one-way geomechanical analyses (using the Millstone geomechanical package, for instance) after running a very costly TOUGH flow simulation.

License and Citing
------------------

Copyright (c) 2015-2017, Alejandro Francisco Queiruga and Matt Reagan.

This work is released under the three-clause BSD License. See the file LICENSE for the full text.

If you use this utility in your work, please cite it through the Zenodo entry linked to this repository:
```latex
@article{toughconvert_2018,
  title={tough_convert: Version 1.0},
  DOI={10.5281/zenodo.1164418},
  publisher={Zenodo},
  author={Alejandro F Queiruga and Mattew T Reagan},
  year={2018},
  month={Feb}
  abstractNote={<p>tough_convert is utility for converting input and output formats for the TOUGH family of codes (TOUGH2, TOUGH+, etc.) into formats usable by other scientific visualization packages.</p>},
}
```

Acknowledgements
----------------

This software was developed under the TOUGH development grant titled "3-D Volume Rendering of TOUGH meshes and simulation outputs".
