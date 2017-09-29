import numpy as np

from itertools import count
from collections import defaultdict

from util import *

class Tough_Mesh():
    """
    A container class for all the mesh objects. 
    Not super-neccessary since only one is loaded into memory at a time, but helped keep track with order-shuffling.
    Calls the routines below upon init to fill in its members. Will shuffle itself--overwriting mesh order--before
    returning from init.
    """
    def __init__(self, mname,cname=None,iname=None,del_groups=None ):
        self.centers, self.names,orig_index2name, self.groups, self.group_key, self.conne \
            = load_tough_mesh(mname, False if cname else True) # None evaluates False
        # TODO: The new filtering features breaks connections. Need to filter those too
        if del_groups:
            newcenters = []
            newnames = {}
            newgroups = []
            i = 0
            del_keys = [ self.group_key[g] for g in del_groups ]
            for c,n,g in zip(self.centers,orig_index2name,self.groups):
                #for grp in del_groups:
                #    if self.group_key[grp] == g:
                #        continue
                if g in del_keys:
                    continue
                newcenters.append(c)
                newnames[n] = i
                newgroups.append(g)
                i+=1
            self.centers = np.vstack(newcenters)
            self.names = newnames
            self.groups = np.array(newgroups,dtype=np.intc)
            
        if cname:
            self.corners,self.elems, self.corner_index2names = load_tough_corners(cname)
            self.corner_names = { n:i for i,n in enumerate(self.corner_index2names) }
            # We need to filter out cells that aren't in the mesh to deal with
            # holes that we've dug ourselves into:
            self.elems,self.corner_names = filter_by_names(self.names, self.corner_names,self.elems)
            self.centers,newnames = filter_by_names(self.corner_names, self.names,self.centers)
            self.groups, newnames = filter_by_names(self.corner_names, self.names,self.groups)
            self.names = newnames
        else:
            self.corners,self.elems, self.corner_names = None,None, None
            
        if iname:
            name2index,index2name = load_tough_incon(iname, len(list(self.names.keys())[0]))

            # WRONG STILL THE LOOP WON'T PRESERVE ORDER
            #index2name,name2index=filter_by_names(self.names, name2index,index2name, vstack=False)
            # This one will
            itr=0
            newindex2name = list(range(len(self.names)))
            newname2index = {}
            for n in index2name:
                if n in self.names:
                    newindex2name[itr]=n
                    newname2index[n] = itr
                    itr+=1
                
            index2name = newindex2name
            name2index = newname2index
            
            old2new = make_shuffler( index2name, self.names )
            self.centers = shuffle(old2new, self.centers)
            #self.names = shuffle(old2new, self.names)
            self.names = name2index
            self.groups = shuffle(old2new, self.groups).flatten()
            
            if self.conne is not None:
                translate(old2new, self.conne)
            if self.elems != None:
                if self.corner_names == None:
                    self.elems = shuffle(old2new, self.elems)
                else:
                    corners2new = make_shuffler( index2name, self.corner_names)
                    self.elems = shuffle(corners2new, self.elems)
            # AT THIS POINT, self.elems is in the same order as self.centers, following self.names
            
        else:
            # Shuffle the corners to match the original ordering, if it won't be shuffled with iname
            #name2index = { n:i for i,n in enumerate(self.names) }

            if self.elems != None and self.corner_names != None:
                index2name = range(len(self.names))
                for k,i in self.names.iteritems():
                    index2name[i] = k
                corners2orig = make_shuffler( index2name, self.corner_names )
                self.elems = shuffle( corners2orig, self.elems)

                
    def Generate_Pseudo_Corners(self,xmin,xmax,ymin,ymax):
        " For 2D, make a simple 2D mesh for FEM/Flac "
        # First, do we actually need to make them?
        if self.corners:
            return
        # Loop over the element centers and make a grid
        xs = set()
        ys = set()
        if self.centers.shape[1] == 3:
            for l in self.centers:
                xs.add(l[0])
                ys.add(l[2])
        else:
            for l in self.centers:
                xs.add(l[0])
                ys.add(l[1])
                
        xc = np.array(list(xs))
        yc = np.array(list(ys))
        xc.sort()
        yc.sort()
        # Generate corners based on the cell centers
        def corners(a,start=0.0):
            o = np.zeros((a.size+1,))
            o[0]=start
            # o[0] = a[0]-0.5*(a[1]-a[0])
            for i in range(1,a.size+1):
                o[i] = 2.0*(a[i-1]-o[i-1])+o[i-1]
            return o
        xl = corners(xc, start=xmin)
        yl = corners(yc[range(yc.size-1,-1,-1)], start=ymin)#[range(yc.size,-1,-1)]

        # Make the 2D grid of centers
        self.corners = np.empty( (len(xl)*len(yl), 2), dtype=np.double )
        for i,y in enumerate(yl):
            self.corners[i*len(xl):(i+1)*len(xl),0] = xl[:]
            self.corners[i*len(xl):(i+1)*len(xl),1] = y

        # Generate the elements
        self.elems = np.empty( ((len(xl)-1)*(len(yl)-1), 4 ), dtype=np.intc )
        idx = lambda i,j : j*(len(xl))+i
        for j in range(len(yl)-1):
            for i in range(len(xl)-1):
                self.elems[j*(len(xl)-1) + i,:] = \
                  ( idx(i,j), idx(i+1,j), idx(i+1,j+1), idx(i,j+1) )


                
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
    cell_index2names = []
    cell_groups = []
    keygen = count()
    group_key = defaultdict( lambda : next(keygen) )
    conne = []

    namelength = -1
    f = open(fname,"r")
    next(f) # Eat the ELEME header
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
        cell_index2names.append(name)
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
            l=next(f)

        # Read in connections
        for l in f:
            if not l.strip() or l[0]=="<" or l[0] == ">" or l[0] == "+": break
            conne.append( np.array( [cell_names[l[0:namelength]],
                                      cell_names[l[namelength:2*namelength]] ] ,
                                    dtype=np.intc ) )

        conne = np.vstack( conne )
    
    f.close()
    return cell_centers, cell_names, cell_index2names, cell_groups, group_key, conne


def load_tough_corners(fname):
    """
    Load the mesh of the domain; discared by default. Use VTK_output = .TRUE. to obtain from MeshMaker_V2
    
    fname shoud be the CORNERS file
    """
    ndim = 3
    verts = {}
    cells = []
    elemnames = []
    f = open(fname,"r")
    enum = -1
    elem = []
    for l in f:
        if l[0:3]==">>>":
            continue
        sp = l.split()
        if len(sp) > ndim+1:
            cells.append( elem )
            elem = []
            enum = enum+1 #int(sp[-1])
            elemnames.append(sp[-1])
        verts[int(sp[ndim])] = np.array(sp[:ndim],dtype=np.double)
        elem.append( int(sp[ndim]) )
    cells.append( elem )# Push the last elem that wasn't triggered
    cells.pop(0) # Frist loop fringe case
    f.close()
    
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
    for i,v in enumerate(cells):
        npcells[i,:] = [vertskey[j] for j in v]
    return npverts, npcells, elemnames

    
def load_tough_incon(fname, namelength=-1):
    """
    Read the inconn file to determine node ordering.
    This routine neglects the intial data; see XXX() in XXX.py
    
    fname should be the INCONN file
    """
    incon = open(fname,"r")
    next(incon)
    name2index = {}
    index2name = []
    itr = 0
    # namelength = 8 # TODO: AD-HOC
    while True:
        l = next(incon)
        if namelength == -1:
            namelength = l.find(" ")
        if l[0] == "<" or l[0]==":" or l[0]=='+': break
        name = l[0:namelength]
        name2index[name] = itr
        index2name.append( name )
        itr+=1
        next(incon)
    incon.close()
    return name2index, index2name
