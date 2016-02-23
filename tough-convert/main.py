import argparse

from meshmakerinputs import *
from vtk_writer import *
from read_tough_data import *

def main():
    parser = argparse.ArgumentParser(description='Convert TOUGH meshes and data output to common formats')
    parser.add_argument("MESH")
    parser.add_argument("--corners",type=str)
    parser.add_argument("--order",type=str)
    parser.add_argument("--data",type=str)
    parser.add_argument("--vtk", type=str)
    parser.add_argument("--silo", type=str)
    parser.add_argument("--flac3d", type=str)
    arg = parser.parse_args()
    
    # Read in Mesh components. Reading CONNE is not needed if CORNERS is supplied.
    #if arg.corners:
    #    cell_centers, cell_names, cell_groups, group_keys, _  = load_tough_mesh(arg.MESH)
    #    corners,elems = load_tough_corners(arg.corners)
    #else:
    #    cell_centers, cell_names, cell_groups, group_keys, conne = load_tough_mesh(arg.MESH, True)
    #if arg.order:
    #    order = load_tough_incon(arg.order)
        # Shuffle the mesh correspondingly
    TMesh = Tough_Mesh( arg.MESH, arg.corners, arg.order )

    
    print "Groups are output according to the following key: ", TMesh.group_key
    
    # We just want the meshes if there is no data.
    if arg.data == None:
        if arg.vtk:
            # Verify extension
            if arg.vtk[-4:]!=".vtk":
                arg.vtk += ".vtk"
            # Write either the real mesh or the dual-graph, depending on whether or not we were given corners
            if arg.corners:
                vtk_write_mesh(arg.vtk, TMesh.corners, TMesh.elems, cellfields={"Groups": TMesh.groups})
            else:
                vtk_write_mesh(arg.vtk, TMesh.centers, TMesh.conne,  nodefields={"Groups": TMesh.groups})
        if arg.silo:
            pass
    # Flac3D is indifferent to wether or not there is data:
    if arg.flac3d:
        pass

    
    # Take a time step loop for the data
    # We read in data and write it out one timestep at a time to minimize how much needs to be held in memory
    # The reader for plot data elem is an iterator to handle this.
    if arg.data:
        for t,step in enumerate(load_plot_data_elem(arg.data)):
            print "Processing step ",t
            if arg.vtk[-4:]!=".vtk":
                oname += "_{0}.vtk".format(t)
            else:
                oname = arg.vtk[:-4] +  "_{0}.vtk".format(t)
            if arg.corners:
                step.update({"Groups":TMesh.groups})
                vtk_write_mesh(oname, TMesh.corners,TMesh.elems, cellfields=step) # WRONG
            else:
                vtk_write_mesh(oname, TMesh.centers, TMesh.conne,  nodefields=step)
    
    
if __name__=="__main__":
    main()
