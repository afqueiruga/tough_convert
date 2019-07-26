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
    def hunt_for_start_of_block():
        try:
            while True:
                l = fh.next()
                if l[:13] == " ELEM.  INDEX":
                    return l
        except StopIteration:
            fh.close()
            raise StopIteration()
    def read_elem_block(firsttime=False):
        keys = hunt_for_start_of_block().split()[2:]
        print(keys)
        fields = [ np.zeros(Nelem,dtype=np.double) for k in keys ]
        i=0
        while True:
            # Check out the line
            l = next(fh)
            # Skip junk inside of the block
            if len(l)<=3 or l[1:6]=='ELEM.' or l[1:6]=='     ':
                continue
            # read the pesky element name
            name = l[1:6]
            # Split the pesky data
            sp = re.sub(r"([^Ee])([-+])",r"\1 \2", l[6:]).split()[1:]
            # print sp
            # sp = range(len(keys))
            lda = 13
            off = 12
            for j in range(len(keys)):
                try:
                    # sp[j] = float(l[ (off+j*lda) : (off+(j+1)*lda) ])
                    sp[j] = float(sp[j])
                except ValueError:
                    print(sp[j]) #"Value error:", l[ (off+j*lda) : (off+(j+1)*lda) ]
                    sp[j] = 0.0
            # Save data
            if firsttime:
                read_elem_block.globalnames.append(name)
                for s,d in zip(sp,fields):
                    d[i]=s #float(s)
            else:
                for s,d in zip(sp,fields):
                    d[read_elem_block.globalidx[i]] = s #float(s)
            # Loop logic
            i += 1
            if i >= Nelem:
                break
        if firsttime:
            # Shuffle the data
            if read_elem_block.globalnames and nameorder:
                read_elem_block.globalidx = np.zeros(len(read_elem_block.globalnames), dtype = np.intc)
                read_elem_block.globalidx[:] = -1
                for i,n in enumerate(read_elem_block.globalnames):
                    read_elem_block.globalidx[i] = nameorder[n]
            for i,d in enumerate(fields):
                fields[i] = np.array(d, dtype=np.double)
                if read_elem_block.globalnames and nameorder:
                    for j in range(len(fields[i])):
                        fields[i][read_elem_block.globalidx[j]] = d[j]
        return {k:d for k,d in zip(keys,fields)}

    # Persistent data in the namespace of the subroutine
    read_elem_block.globalidx = []
    read_elem_block.globalnames = []

    block1 = read_elem_block(firsttime=True)
    block2 = read_elem_block(firsttime=False)
    block1.update(block2)
    yield block1
    
    while True:
        block1 = read_elem_block()
        block2 = read_elem_block()
        block1.update(block2)
        yield block1
        

