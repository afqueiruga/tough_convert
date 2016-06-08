import numpy as np

def filter_by_names(filter_names, data_names, data, vstack=True):
    newdata = []
    newnames = {}
    for n in filter_names:
        try:
            newdata.append(data[data_names[n]] )
            newnames[n] = len(newdata)-1
        except KeyError:
            pass
    if len(newnames) != len(data_names):
        print "Element-mismatch: Had to prune ", len(data_names)-len(newnames), "Entries"
    #print newelems
    if vstack:
        newdata = np.vstack(newdata)
    return newdata, newnames
