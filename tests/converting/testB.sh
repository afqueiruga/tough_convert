#!/bin/sh
python ../../toughp-proc/toughp-convert.py MESH --corners CORNERS --vtk foo_mesh.vtk
python ../../toughp-proc/toughp-convert.py MESH --vtk foo_dual.vtk
