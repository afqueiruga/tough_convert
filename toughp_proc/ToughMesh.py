import numpy as np

from itertools import count
from collections import defaultdict

class Tough_Mesh():
    """
    A container class for all the mesh objects. 
    Not super-neccessary since only one is loaded into memory at a time, but helped keep track with order-shuffling.
    Calls the routines below upon init to fill in its members. Will shuffle itself--overwriting mesh order--before
    returning from init.
    """
    def __init__(self, mname,cname=None,iname=None ):
        """
        Load a mesh from some files
        """
        self.centers, self.names, self.groups, self.group_key, self.conne \
            = load_tough_mesh(mname, False if cname else True) # None evaluates False
        if cname:
            self.corners,self.elems = load_tough_corners(cname)
        else:
            self.corners,self.elems = None,None
            
        if iname:
            name2index,index2name = load_tough_incon(iname, len(self.names.keys()[0]))

            old2new = make_shuffler( index2name, self.names )
            self.centers = shuffle(old2new, self.centers)
            #self.names = shuffle(old2new, self.names)
            self.names = name2index
            self.groups = shuffle(old2new, self.groups)
            if self.conne != None: translate(old2new, self.conne)
            if self.elems != None: self.elems = shuffle(old2new, self.elems)

    def FindElements(self , fltr):
        """
        Return a list of elements that satisfy the function fltr( x[name] )
        Does an O(n) search.
        """
        matches = []
        for n,idx in self.names.iteritems(): # TODO: Bad loop. Loop in center order.
            if fltr(self.centers[idx]):
                matches.append(n)
        return matches
    
def make_shuffler(new2name, name2old):
    new2old = np.empty( (len(new2name),) , dtype=np.intc)
    #from IPython import embed
    #embed()
    for new,name in enumerate(new2name):
        new2old[new] = name2old[name]
    old2new = np.empty( new2old.shape, dtype=np.intc )
    for i,v in enumerate(new2old):
        old2new[v] = i
    return old2new

def shuffle(old2new, oldarr):
    newarr = np.empty(oldarr.shape,oldarr.dtype)
    newarr[ old2new ] = oldarr[ : ]
    return newarr

def translate(old2new, arr):
    for j,v in enumerate(arr):
        arr[j] = old2new[ v ] # NEED TO FLIP THIS

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

    namelength = -1
    f = open(fname,"r")
    f.next() # Eat the ELEME header
    itr = 0
    for l in f:
        if not l.strip(): continue
        if l[0:5]=="CONNE": break # The end of the ELEME block

        # We need to figure out how long element names are
        if namelength == -1:
            namelength = l.find(" ")
            if namelength<5: namelength = 5
        
        name = l[0:namelength]
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
    
    # Conditionally read connections
    if read_conne:
        # Chew to the CONNE block
        while True:
            if l[0:5]=="CONNE":
                break
            l=f.next()

        # Read in connections
        for l in f:
            if not l.strip() or l[0]=="<" or l[0] == ">" or l[0] == "+": break
            conne.append( np.array( [cell_names[l[0:namelength]],
                                      cell_names[l[namelength:2*namelength]] ] ,
                                    dtype=np.intc ) )

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
        if l[0:3]==">>>":
            
            continue
        sp = l.split()
        verts[int(sp[ndim])] = np.array(sp[:ndim],dtype=np.double)
        if len(sp) > ndim+1:
            cells[enum] = elem
            elem = []
            enum = enum+1 #int(sp[-1])
        elem.append( int(sp[ndim]) )
    cells[enum] = elem # Push the last elem that wasn't triggered
    cells.pop(-1) # Frist loop fringe case
    f.close()
    # from IPython import embed
    # embed()
    # Densify dictionaries in np arrays
    npverts = np.empty((len(verts),ndim),dtype=np.double)
    # First, we need to make a new translation map, because they're read in
    # in the original TOTAL BLOCK order, before carving
    vertskey = {}
    for newk,(i,v) in enumerate(verts.iteritems()):
        vertskey[i] = newk
    for i,v in verts.iteritems():
        npverts[vertskey[i],:] = v
    npcells = np.empty((len(cells),len(cells[1])),dtype=np.intc)
    for i,v in cells.iteritems():
        npcells[i-1,:] = [vertskey[j] for j in v]
    return npverts, npcells

    
def load_tough_incon(fname, namelength=-1):
    """
    Read the inconn file to determine node ordering.
    This routine neglects the intial data; see XXX() in XXX.py
    
    fname should be the INCONN file
    """
    incon = open(fname,"r")
    incon.next()
    name2index = {}
    index2name = []
    itr = 0
    # namelength = 8 # TODO: AD-HOC
    while True:
        l = incon.next()
        if namelength == -1:
            namelength = l.find(" ")
        if l[0] == "<" or l[0]==":": break
        name = l[0:namelength]
        name2index[name] = itr
        index2name.append( name )
        itr+=1
        incon.next()
    incon.close()
    return name2index, index2name
