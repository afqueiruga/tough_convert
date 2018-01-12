import argparse

def main():
    parser = argparse.ArgumentParser(description='Cat together output from parallel meshmaker')
    parser.add_argument("Outfile",type=str)
    parser.add_argument("Infiles",type=str,nargs='+')
    arg=parser.parse_args()

    
    fo = open(arg.Outfile,"w")
    for I in arg.Infiles:
        fi = open(I,"r")
        for l in fi:
            if not l[0] in '<>' :
                fo.write(l)
        fi.close()
    fo.close()
    
if __name__=="__main__":
    main()
