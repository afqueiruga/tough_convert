
def vtk_write_mesh(fname, X, elems, nodefields=None, cellfields=None):
    celltypekey = {
        1:1,
        2:3,
        3:5,
        4:9,
        #4:10,
        8:12}
    vecformatdict = {
        1:"{0} 0.0 0.0\n",
        2:"{0} {1} 0.0\n",
        3:"{0} {1} {2}\n"
        }
    vecfmt = vecformatdict[X.shape[1]]

    fh = open(fname,"w")
    fh.write("# vtk DataFile Version 2.0\nGraph connectivity\nASCII\n")
    fh.write("DATASET UNSTRUCTURED_GRID\n")
    
    fh.write("POINTS {0} double\n".format(X.shape[0]))
    for pt in X:
        fh.write(vecfmt.format(*pt))

    fh.write("\nCELLS {0} {1}\n".format(elems.shape[0],elems.shape[0]*(1+elems.shape[1])))
    # I assume they're all the same
    for el in elems:
        fh.write("{0} ".format(len(el))+" ".join([str(x) for x in el])+"\n")
    fh.write("\nCELL_TYPES {0}\n".format(elems.shape[0]))
    for el in elems:
        fh.write("{0}\n".format(celltypekey[elems.shape[1]]))

    # Node fields now
    if nodefields:
        fh.write("POINT_DATA {0}\n".format(X.shape[0]))
        for n,f in nodefields.iteritems():
            if len(f.shape)==1 or f.shape[1]==1:
                fh.write("SCALARS {0} double\n".format(n))
                fh.write("LOOKUP_TABLE default\n")
                for l in f:
                    fh.write(str(l)+"\n")
            else:
                fh.write("VECTORS {0} double\n".format(n))
                for l in f:
                    fh.write(vecfmt.format(*l))

    # Cell fields now
    
    fh.close()
