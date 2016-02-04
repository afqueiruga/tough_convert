import argparse

from meshmakerinputs import *
from vtk_writer import *

def main():
    parser = argparse.ArgumentParser(description='Convert TOUGH meshes and data output to common formats')

    parser.add_argument("MESH")
    parser.add_argument("CORNERS")
    parser.add_argument("--order",nargs=1)
    parser.add_argument("--data",nargs="+")
    parser.add_argument("--vtk",nargs="+")
    parser.add_argument("--silo",nargs="+")
    parser.add_argument("--flac3d",nargs="+")
    
    ag = parser.parse_args()
    print ag
    # Read in Mesh components
    cells = load_tough_mesh(ag.MESH)
    corners,elems = load_tough_corners(ag.CORNERS)

    # Flac3D doesn't need data to be read in:
    print ag.flac3d
    print ag.data
    print ag.vtk
    print ag.silo
    # Read in optional data fields: determine if a timestep loop needs to be taken for memory effeciency
    
    # Output formats
    
if __name__=="__main__":
    main()
