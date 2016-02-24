def silo_write_meshfile(fname, X, elems):
    try:
        from pyvisfile.silo import SiloFile, IntVector, DB_ZONETYPE_BEAM, DB_NODECENT, DB_ZONECENT, DBOPT_CYCLE, DBOPT_DTIME, DBOPT_TIME, DB_CLOBBER
    except ImportError:
        print "Need PyVisFile to write silo files. Use vtk for now."
        raise
    import numpy as np

    silo = SiloFile(fname, mode=DB_CLOBBER)
    
    pair_edges = elems
    zonelist_name = "foo_zonelist"
    nodelist = IntVector()
    nodelist.extend( int(i) for i in pair_edges[:,0:2].flat)
    shapetypes = IntVector()
    shapetypes.append(DB_ZONETYPE_BEAM)
    shapesizes = IntVector()
    shapesizes.append(2)
    shapecounts = IntVector()
    shapecounts.append(len(pair_edges))
    silo.put_zonelist_2(zonelist_name, len(pair_edges), 2, nodelist,
                            0,0, shapetypes, shapesizes, shapecounts)
    silo.put_ucdmesh("foo", [],
                     np.asarray(X.T,order="C"), len(pair_edges),
                     zonelist_name, None)
    silo.close()
