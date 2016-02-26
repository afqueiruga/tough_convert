import numpy as np
import re

def load_plot_data_elem(fname):
    """
    Read a Plot_Data_Elem file and spit out the time series value step-by-step.
    returns a generator over the time step values so that it can throw away data.

    fname should be Plot_Data_Elem
    """

    fh = open(fname,"r")

    # Read the keys
    keys = fh.next().split()[2:]
    fields = [ [] for k in keys ]
    
    # Read the first timestep block
    fh.next() # Eat the zone block
    for l in fh:
        if not l.strip() or l[0:4]=="ZONE": break
        sp = re.sub(r"([^Ee])([-+])",r"\1 \2", l).split()
        try:
            if len(sp)==len(keys):
                for s,d in zip(sp,fields):
                    d.append(float(s))
            else:
                for s,d in zip(sp[-len(keys):],fields):
                    d.append(float(s))
        except:
            print "Had trouble with this line:"
            print sp
            raise
                
    # Compact format
    for i,d in enumerate(fields):
        fields[i] = np.array(d, dtype=np.double)

    # Yield the first time step
    yield { k:d for k,d in zip(keys,fields) }

    # Now we keep going, but using the preallocated ndarrays
    while True:
        # Chew through till the next zone block.
        # If we run out of file, then we're done.
        while True:
            try:
                l = fh.next()
                if l[0:4]=="ZONE": break
            except StopIteration:
                fh.close()
                raise StopIteration()

        # Refill the preallocated arrays
        for i in xrange(len(fields[0])):
            sp = re.sub(r"([^Ee])([-+])",r"\1 \2",fh.next()).split()
            if len(sp)==len(keys):
                for s,d in zip(sp,fields):
                    d[i] = float(s)
            else:
                for s,d in zip(sp[-len(keys):],fields):
                    d[i] = float(s)
        # Yield this set of time step values
        yield { k:d for k,d in zip(keys,fields) }
