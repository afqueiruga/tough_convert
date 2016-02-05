#!/bin/sh
python ../../tough-convert/main.py MESH --corners CORNERS --vtk foo_mesh.vtk
python ../../tough-convert/main.py MESH --vtk foo_dual.vtk
