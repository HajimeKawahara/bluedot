#!/usr/bin/python
import pylab
import matplotlib.pyplot as plt
import os
import sys
import datetime
from makeinput import LibRadtran
from bluedotclass import PlanetGeometry
from bluedotclass import PlanetColor
from bluedotclass import PlanetData
import pickle
import numpy as np
from pathlib import Path
import snapshot as ss
import generate_globe as gg

import argparse

class PlanetMovie:
    
    def __init__(self,ispec):
        print("Setting PlanetMovie...")
        self.date=datetime.datetime.now()
        self.pmid=0
        self.pgeo=PlanetGeometry()
        self.pcol=PlanetColor(ispec)
        self.pdata=PlanetData()
        self.jdlist=[]
        
    def setPMid(self,pmid):
        if pmid <= len(self.jdlist):
            self.pmid = pmid
            pmidst = '{0:05d}'.format(pmid)
            self.inpdir="INP"+pmidst
            self.jd=self.jdlist[pmid-1]
            p=Path(self.inpdir)
            p.mkdir(parents=False, exist_ok=True)
        else:
            print("INVALID PM id. From 1 to "+str(len(jdlist)))
            
def savepmov(pfile,pmov):
    with open(pfile, 'wb') as f:
        pickle.dump(pmov, f)

def loadpmov(pfile):
    with open(pfile, 'rb') as f:
        pmov = pickle.load(f)
    return pmov
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generating a snapshot.')
    parser.add_argument('-p',action='store_true', help='generate pickle.')
    parser.add_argument('-f',default=["test.pickle"],nargs=1, help='pickle file', type=str)
    parser.add_argument('-i',default=[0],nargs=1, help='PM ID. if 0 set pmov.', type=int)
    parser.add_argument('-s',default=[1],nargs=1, help='spectral ID.', type=int)
    parser.add_argument('-e',action='store_true', help='emulate movie (without uvspec)')


    args = parser.parse_args()
    pfile=args.f[0]
    ispec=args.s[0]
    if args.p:
        print("Set Planet Movie. Pickle file=",pfile)
        pmov=PlanetMovie(ispec)
        pmov.pgeo.inc=45.0/180.0*np.pi
        pmov.pgeo.Thetaeq=90.0/180.0*np.pi
        #pmov.jdlist=pmov.pgeo.jd0+np.arange(0.0,1.0,1.0/8.0) #daily
        pmov.jdlist=pmov.pgeo.jd0  - 79.0 + np.arange(0.0,365.0,1.0/8.0)#annual
        savepmov(pfile,pmov)
        sys.exit()

    if args.i[0] <= 0:
        sys.exit()
        
    pmov=loadpmov(pfile)
    pmov.setPMid(args.i[0])
    pgeo = pmov.pgeo
    pgeo.jd=pmov.jd
    pdata = pmov.pdata
    pcol = pmov.pcol
    print("ispec=",pcol.ispec)
    print("JD=",pmov.jd)

    if args.e:
        print("***************")
        print("EMULATE MOVIES.")
        print("***************")
        ss.notcompute_snapshot(pdata,pgeo,pcol,pmov.inpdir)
        print("===============")
    else:
        ipixarr, ereo, lamb, others, radallcl, radallcs, fclall=ss.compute_snapshot(pdata,pgeo,pcol,pmov.inpdir)
        print("END snapshot")
        np.savez(pmov.inpdir+"/rads.npz", ipixarr, ereo, lamb, others, radallcl, radallcs, fclall)
        print("Save rads.")
        np.savez(pmov.inpdir+"/otherinfo.npz", others)
        
