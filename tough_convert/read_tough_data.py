import numpy as np
import re

from .util import *
from .matcher import match_point_clouds

def load_plot_data_elem(fname, nameorder=None, X=None, order_by_points=False):
    """
    Read a Plot_Data_Elem file and spit out the time series value step-by-step.
    returns a generator over the time step values so that it can throw away data.

    fname should be Plot_Data_Elem
    """
    print("Reading step 0...")
    fh = open(fname,"r")

    # Read the keys
    keys = next(fh).split()[2:]
    fields = [ [] for k in keys ]
    globalidx = None
    globalnames = []
    # Read the first timestep block
    next(fh) # Eat the zone block
    for l in fh:
        if not l.strip() or l[0:4]=="ZONE": break
        sp = re.sub(r"([^Ee])([-+])",r"\1 \2", l).split()
        try:
            if len(sp)==len(keys):
                for s,d in zip(sp,fields):
                    d.append(float(s))
            else:
                # THEORY: I don't need to shuffle now, I just need to skip sp[1] not in nameorder
                # Because I already shuffled in TMesh.__init__
                # Ah, but nope it's a different order in the parallel Plot_Data_Elem
                n = sp[1]
                if n in nameorder:
                    for s,d in zip(sp[-len(keys):],fields):
                        d.append(float(s))
                    #globalidx.append(int(sp[0])-1)
                    globalnames.append(sp[1])
        except:
            print("Had trouble with this line:")
            print(sp)
            raise


    if not order_by_points and len(globalnames) and (not nameorder is None):
        print("Name information found in plot_data_elem, using that.")
        globalidx = np.zeros(len(globalnames), dtype = np.intc)
        globalidx[:] = -1
        i=0
        # for i,n in enumerate(globalnames):
            # globalidx[i] = nameorder[n]
        for n in globalnames:
            try:
                globalidx[i] = nameorder[n]
                i+=1
            except KeyError:
                pass
    elif order_by_points:
        # Compact format
        print("Generating a correspondence between the mesh and plot_data_elem")
        if not X is None:
            keyidx = { k:i for i,k in enumerate(keys) }
            if 'x' in keyidx and 'y' in keyidx and 'z' in keyidx:
                Y = np.empty((len(fields[0]),3),dtype=np.double)
                Y[:,0] = fields[keyidx['x']]
                Y[:,1] = fields[keyidx['y']]
                Y[:,2] = fields[keyidx['z']]
            else:
                Y = np.empty((len(fields[0]),2),dtype=np.double)
                try:
                    Y[:,0] = fields[keyidx['x']]
                except KeyError:
                    Y[:,0] = fields[keyidx['r']]
                try:
                    Y[:,1] = fields[keyidx['z']]
                except KeyError:
                    Y[:,1] = fields[keyidx['y']]
            globalidx = match_point_clouds(X,Y)
    else:
        print("Using mesh ordering or specified order file")
    if not globalidx is None:
        for i,d in enumerate(fields):
            fields[i] = np.empty(len(nameorder), dtype=np.double)
            acopy = np.array(d)
            for j in range(len(acopy)):
                fields[i][globalidx[j]] = acopy[j]
    else:
        for i,d in enumerate(fields):
            fields[i] = np.array(d, dtype=np.double)

    # Yield the first time step
    print("done.")
    yield { k:d for k,d in zip(keys,fields) }

    # Now we keep going, but using the preallocated ndarrays
    while True:
        # Chew through till the next zone block.
        # If we run out of file, then we're done.
        while True:
            try:
                l = next(fh)
                if l[0:4]=="ZONE": break
            except StopIteration:
                fh.close()
                raise StopIteration()
        print("Reading step...")
        # Refill the preallocated arrays
        i=0

        while i<len(fields[0]):
            l = next(fh)
            sp = re.sub(r"([^Ee])([-+])",r"\1 \2",l).split()
            if len(sp)==len(keys):
                for s,d in zip(sp,fields):
                    if not globalidx is None:
                        d[globalidx[i]] = float(s)
                    else:
                        d[i] = float(s)
            else:
                if (not nameorder is None) and not sp[1] in nameorder:
                    continue
                for s,d in zip(sp[-len(keys):],fields):
                    if not globalidx is None:
                        d[globalidx[i]] = float(s)
                    else:
                        d[i] = float(s)
            i+=1
        # Yield this set of time step values
#        fields[globalidx] = fields[:]

        yield { k:d for k,d in zip(keys,fields) }
