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

    fields = [ [] for k in keys ]
    globalidx = []
    globalnames = []
    
    for i in xrange(Nelem):
        l = fh.next()
        sp = re.sub(r"([^Ee])([-+])",r"\1 \2", l).split()
        if len(sp) != len(keys):
            continue
        print sp


    raise StopIteration()
        
