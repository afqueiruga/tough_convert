import numpy as np

class Tough_Mesh():
    def __init__(self):
        pass
    
def load_tough_mesh(fname):
    """
    Loads the dual-mesh graph (cell-cell) that TOUGH uses directly
    It's stored as two tables
    
    fname should be the MESH file
    """
    # 

    cells = []

    f = open(fname,"r")
    f.next()
    
    f.close()
    
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
    cells.pop(-1) # Frist loop fringe case
    f.close()
    
    # Densify dictionaries in np arrays
    npverts = np.empty((len(verts),ndim),dtype=np.double)
    for i,v in verts.iteritems():
        npverts[i-1,:] = v
    
    return npverts, cells
    # from IPython import embed
    # embed()
    
def load_tough_inconn(fname):
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
