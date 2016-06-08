def gmsh_write_mesh(fname, X,elems):
    """
    Write a simple gmsh file. 

    This is an ad hoc feature! Only 2D elements from a structured grid supported.
    A better mesher is needed for anything serious.
    """
    fh = open(fname,"w")
    fh.write("$MeshFormat\n2.2 0 8\n&EndMeshFormat\n")

    fh.write("$Nodes\n")
    fh.write("{0}\n".format(X.shape[0]))
    for i,l in enumerate(X):
      fh.write("{0} {1} {2} 0.0\n".format(1+i,*l))
    fh.write("$EndNodes\n")

    etype = 3 # 4-node quad
    fh.write("$Elements\n")
    fh.write("{0}\n".format(elems.shape[0]))
    for i,e in enumerate(elems):
        fh.write("{0} {1} 2 0 0".format(i+1,etype))
        for v in e: fh.write(" {0}".format(v+1))
        fh.write("\n")
    fh.write("$EndElements\n")
    fh.close()
