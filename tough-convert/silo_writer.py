def silo_write_meshfile(fname, X, elems):
    try:
        from pyvisfile.silo import SiloFile, IntVector, DB_ZONETYPE_BEAM, DB_ZONETYPE_HEX, \
            DB_NODECENT, DB_ZONECENT, DBOPT_CYCLE, DBOPT_DTIME, DBOPT_TIME, DB_CLOBBER
    except ImportError:
        print("Need PyVisFile to write silo files. Use vtk for now.")
        raise
    import numpy as np

    silo = SiloFile(fname, mode=DB_CLOBBER)

    # TODO: Check to see if it should be connections or bricks
    zonelist_name = "foo_zonelist"
    nodelist = IntVector()
    nodelist.extend( int(i) for i in elems[:,:].flat)
    shapetypes = IntVector()
    if elems.shape[1]==2:
        shapetypes.append(DB_ZONETYPE_BEAM)
    elif elems.shape[1]==8:
        shapetypes.append(DB_ZONETYPE_HEX)
    shapesizes = IntVector()
    shapesizes.append(elems.shape[1])
    shapecounts = IntVector()
    shapecounts.append(len(elems))
    silo.put_zonelist_2(zonelist_name, len(elems), 2, nodelist,
                            0,0, shapetypes, shapesizes, shapecounts)
    silo.put_ucdmesh("foo", [],
                     np.asarray(X.T,order="C"), len(elems),
                     zonelist_name, None)
    silo.close()
    print("Wrote file "+fname)

def silo_write_datafile(fname,mname,cycle=0, time=0, nodefields={}, cellfields={}):
    try:
        from pyvisfile.silo import SiloFile, IntVector, DB_ZONETYPE_BEAM,\
            DB_NODECENT, DB_ZONECENT, DBOPT_CYCLE, DBOPT_DTIME, DBOPT_TIME, DB_CLOBBER
        from pyvisfile.silo import DBObjectType as DBOBjectType
    except ImportError:
        print("Need PyVisFile to write silo files. Use vtk for now.")
        raise
    import numpy as np
    silo = SiloFile(fname, mode=DB_CLOBBER)
    silo.put_multimesh('foo', [(mname+":foo",DBOBjectType.DB_UCDMESH)])
    def putvar(n,fo,LOC):
        if len(f.shape)==1 or f.shape[1]==1:
            silo.put_ucdvar1("node_"+n,"foo",
                             np.asarray(f.T,order="C",dtype=np.double),
                             LOC, {DBOPT_CYCLE:cycle,DBOPT_DTIME:float(time),DBOPT_TIME:float(time)})
        elif f.shape[1]==2:
            silo.put_ucdvar("node_"+n,"foo", [n+"x",n+"y"],
                            np.asarray(f.T,order="C",dtype=np.double),
                            LOC, {DBOPT_CYCLE:cycle,DBOPT_DTIME:float(time),DBOPT_TIME:float(time)})
        else:
            silo.put_ucdvar("node_"+n,"foo", [n+"x",n+"y",n+"z"],
                            np.asarray(f.T,order="C",dtype=np.double),
                            LOC,  {DBOPT_CYCLE:cycle,DBOPT_DTIME:float(time),DBOPT_TIME:float(time)})
   
    for n,f in nodefields.iteritems():
        putvar(n,f,DB_NODECENT)
    for n,f in cellfields.iteritems():
        putvar(n,f,DB_ZONECENT)

    silo.close()
    print("Wrote file "+fname)
