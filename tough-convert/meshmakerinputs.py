import numpy as np

from itertools import count
from collections import defaultdict
class Tough_Mesh():
    def __init__(self):
        pass
    
def load_tough_mesh(fname, read_conne = False):
    """
    Loads the dual-mesh graph (cell-cell) that TOUGH uses directly
    It's stored as three tables:
    Name-to-index dictionary
    cell-centers packed and ordered by index
    cell properties packed and ordered by index
    index-to-index connection graph

    fname should be the MESH file
    """

    cell_centers = []
    cell_names = {}
    cell_groups = []
    keygen = count()
    group_key = defaultdict( lambda : keygen.next() )
    conne = []
    
    f = open(fname,"r")
    f.next() # Eat the ELEME header
    itr = 0
    for l in f:
        if not l.strip() or l[0:5]=="CONNE": break # The end of the ELEME block

        name = l[0:5]
        x,y,z = l[50:60],l[60:70],l[70:80]
        if not y.strip():
            X = np.array([ x,z ], dtype=np.double)
        else:
            X = np.array([ x,y,z ], dtype=np.double)
        group = l[15:20]
        cell_centers.append(X)
        
        cell_names[name] = itr 
        cell_groups.append(group_key[group])
        itr += 1
    cell_centers = np.vstack( cell_centers )
    cell_groups = np.array(cell_groups,np.intc)
    # Is that all we wanted?
    if read_conne:
        # Chew to the CONNE block
        while True:
            if l[0:5]=="CONNE":
                break
            l=f.next()

        # Read in connections
        for l in f:
            if not l.strip() or l[0]=="<" or l[0] == ">": break
            conne.append( np.array( [cell_names[l[0:5]], cell_names[l[5:10]] ] , dtype=np.intc ) )

        conne = np.vstack( conne )
    
    f.close()
    return cell_centers, cell_names, cell_groups, group_key, conne


def load_tough_corners(fname):
    """
    Load the mesh of the domain; discared by default. Use VTK_output = .TRUE. to obtain from MeshMaker_V2
    
    fname shoud be the CORNERS file
    """
    ndim = 3
    verts = {}
    cells = {}
    f = open(fname,"r")
    enum = -1
    elem = []
    for l in f:
        if l[0:3]==">>>": break
        sp = l.split()
        verts[int(sp[ndim])] = np.array(sp[:ndim],dtype=np.double)
        if len(sp) > ndim+1:
            cells[enum] = elem
            elem = []
            enum = int(sp[-1])
        elem.append( int(sp[ndim]) )
    cells[enum] = elem # Push the last elem that wasn't triggered
    cells.pop(-1) # Frist loop fringe case
    f.close()
    
    # Densify dictionaries in np arrays
    npverts = np.empty((len(verts),ndim),dtype=np.double)
    for i,v in verts.iteritems():
        npverts[i-1,:] = v
    npcells = np.empty((len(cells),len(cells[1])),dtype=np.intc)
    for i,v in cells.iteritems():
        npcells[i-1,:] = [j-1 for j in v]
    return npverts, npcells

    
def load_tough_incon(fname):
    """
    Read the inconn file to determine node ordering.
    This routine neglects the intial data; see XXX() in XXX.py
    
    fname should be the INCONN file
    """
    incon = open(fname,"r")
    incon.next()
    orderdict = {}
    itr = 1
    while True:
        l = incon.next()
        if l[0] == "<" or l[0]==":": break
        name = l[0:5]
        orderdict[name] = itr
        itr+=1
        incon.next()
    incon.close()
    return orderdict
