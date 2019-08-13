#!/usr/bin/python
import os
import sys
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generating shell files for movies')
    parser.add_argument(
        '-i', nargs=2, default=[0,10], help="numbers", type=int)
    parser.add_argument(
        '-f', nargs=1, default=["temp.pickle"], help="pickle", type=str)
    parser.add_argument(
        '-j', nargs=1, default=["1"], help="exe tag", type=str)
    parser.add_argument(
        '-n', nargs=1, default=[1], help="the number of threads", type=int)
    parser.add_argument(
        '-e',action='store_true', help='emulate movies (without uvspec)')

    args = parser.parse_args()
    n=args.n[0]
    ncom=args.i[1]-args.i[0]+1

    if n > 1:
        g = open("exe"+args.j[0]+".exe","w")

    for j in range(0,n):
        if n==1:
            efile = args.j[0]+".exe"
        else:
            efile = args.j[0]+"_"+str(j)+".exe"
            g.write("./"+efile+" > exelog"+str(j)+' &'+"\n")
            
        if args.e:
            print("***************")
            print("EMULATE MOVIES.")
            print("***************")
            com = "python ../makemovie.py -e -i "
        else:
            com = "python ../makemovie.py -i "
        f = open(efile,"w")
        for i in range(args.i[0],args.i[1]+1):
            ii=i+j*ncom
            if args.e:
                f.write(com+str(ii)+" -f "+args.f[0]+"\n")                
            else:
                f.write(com+str(ii)+" -f "+args.f[0]+" > log"+str(ii)+"\n")
        f.close()

    if n > 1:
        g.close()

