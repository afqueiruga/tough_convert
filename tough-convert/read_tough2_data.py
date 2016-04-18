import numpy as np
import re

def load_tough2_output(fname, Nelem, Nconn, nameorder=None):
    """
    Read a TOUGH2 file and spit out the time series value step-by-step.
    The logic is tricky because of all of the extra junk between what we want.
    returns a generator over the time step values so that it can throw away data.

    No default filename.
    """
    print("Reading step 0...")
    fh = open(fname,"r")

    # Read the keys
    #keys = fh.next().split()[2:]
    #fields = [ [] for k in keys ]
    #globalidx = []
    #globalnames = []

    
    def hunt_for_start_of_block():
        try:
            while True:
                l = fh.next()
                if l[:13] == " ELEM.  INDEX":
                    return l
        except StopIteration:
            fh.close()
            raise StopIteration()

    keys = hunt_for_start_of_block().split()[2:]

    fields = [ np.zeros(Nelem,dtype=np.double) for k in keys ]
    
    globalidx = []
    globalnames = []

    # Read the first time step
    i=0
    while True:
        # Check out the line
        l = fh.next()
        # Skip junk inside of the block
        if len(l)<=3 or l[1:6]=='ELEM.':
            continue
        # read the pesky element name
        name = l[1:6]
        # Split the pesky data
        sp = re.sub(r"([^Ee])([-+])",r"\1 \2", l[6:]).split()
        # Save data
        globalnames.append(name)
        for s,d in zip(sp[1:],fields):
            d[i]=float(s)
        # Loop logic
        i += 1
        if i >= Nelem:
            break
    print globalnames
    # Shuffle the data
    if globalnames and nameorder:
        globalidx = np.zeros(len(globalnames), dtype = np.intc)
        globalidx[:] = -1
        for i,n in enumerate(globalnames):
            globalidx[i] = nameorder[n]
    for i,d in enumerate(fields):
        fields[i] = np.array(d, dtype=np.double)
        if globalnames and nameorder:
            for j in xrange(len(fields[i])):
                fields[i][globalidx[j]] = d[j]
    yield {k:d for k,d in zip(keys,fields)}
    # return
    while True:
        hunt_for_start_of_block()
        i=0
        while True:
            l = fh.next()
            if len(l)<=3 or l[1:6]=='ELEM.':
                continue
            name = l[1:6]
            sp = re.sub(r"([^Ee])([-+])",r"\1 \2", l[6:]).split()
            for s,d in zip(sp[1:],fields):
                d[globalidx[i]] = float(s)
            i += 1
            if i >= Nelem:
                break
        yield {k:d for k,d in zip(keys,fields)}

    # raise StopIteration()
        
