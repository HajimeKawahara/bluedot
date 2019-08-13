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
from makemovie import PlanetMovie
import makemovie as mm
import healpy as hp
import argparse
import shutil

def read_solar_flux(filename):
    data=np.loadtxt(filename)
    wavsl=data[:,0]
    fluxsl=data[:,1]
    return wavsl, fluxsl

def get_irradiance(wavsl,fluxsl,upper,lower):
    i=np.searchsorted(wavsl,upper)
    j=np.searchsorted(wavsl,lower)
    return np.mean(fluxsl[j:i+1])
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='playback movie')
    parser.add_argument('-m',action='store_true', help='generate maps')
    parser.add_argument('-f',default=["none.pickle"],nargs=1, help='pickle file', type=str)
    parser.add_argument('-i',default=[1,10],nargs=2, help='PM IDs for start to end', type=int)
    parser.add_argument('-x',action='store_true', help='display')
    
    args = parser.parse_args()
    pfile=args.f[0]
    pmov=mm.loadpmov(pfile)
    lc=[]
    lccs=[]
    lccl=[]
    lccsf=[]
    
    jd=[]
    fcl=[]
    wavsl,fluxsl=read_solar_flux("/home/kawahara/sotica/bluedot/data/solar_flux/kurudz_1.0nm.dat")
#    for idPM in range(args.i[0],args.i[1]+1):
    for idPM in range(args.i[0],args.i[1]+1,8): #for debug
        print(idPM)
        pmov.setPMid(idPM)
        pgeo = pmov.pgeo
        pdata = pmov.pdata
        pcol = pmov.pcol
        irrad_solar=get_irradiance(wavsl,fluxsl,pcol.upper,pcol.lower)

        jd.append(pmov.jd)
        dOmega=4.0*np.pi/pgeo.npix #sr

        ###READING DATA
        data=np.load(pmov.inpdir+"/rads.npz")
        #fisox, fvolx, fgeox, landfx, fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask
        others=data["arr_3"]
        fisox, fvolx, fgeox, landfx, fclx, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask=others   

        #data: ipixarr, ereo, lamb, others, radallcl, radallcs, fclall
        ipixarr=data["arr_0"]
        ereo=np.array(data["arr_1"])

        radwvcs=np.array(data["arr_5"])
        radwvcl=np.array(data["arr_4"])        
        if np.shape(radwvcs)[1]==np.shape(radwvcl)[1]:
            nlamb=np.shape(radwvcs)[1]
        else:
            sys.exit("INCONSISTENT DATA")
            
        fclall=np.zeros(pgeo.npix)
        fclall[ipixarr]=data["arr_6"]
        radcs=np.zeros(pgeo.npix)
        radcs[ipixarr]=np.nansum(radwvcs,axis=1)/nlamb*ereo
        radcl=np.zeros(pgeo.npix)
        radcl[ipixarr]=np.nansum(radwvcl,axis=1)/nlamb*ereo
        radcs[radcs<0.0]=0.0


        ####force to zero if fcl < 0:
        fclall[fclall<0.0]=0.0
        ############################

        rad=radcs*(1.0-fclall)+fclall*radcl
        lc.append(np.nansum(rad)*dOmega)
        lccs.append(np.nansum(radcs*(1.0-fclall))*dOmega)
        lccl.append(np.nansum(radcl*fclall)*dOmega)
        lccsf.append(np.nansum(radcs)*dOmega)
        fcl.append(np.median(data["arr_6"]))

        if args.x:
            ereoarr=np.zeros(pgeo.npix)
            ereoarr[ipixarr]=ereo

#            hp.mollview(radcs,title="radcs",flip="geo",cmap=plt.cm.pink)
            hp.mollview(radcl,title="radcl",flip="geo",cmap=plt.cm.pink)

#            hp.mollview(ereoarr,title="radcs",flip="geo",cmap=plt.cm.CMRmap,min=0.0,max=np.pi)
            hp.graticule(color="orange")
            plt.savefig("tmp/"+str(idPM)+".png")



        if args.m:
            print(irrad_solar)
            hp.mollview(np.pi*rad/irrad_solar,title="BRDF",flip="geo",cmap=plt.cm.pink)
            hp.graticule(color="orange")
#            plt.savefig("brdfexample.pdf", bbox_inches="tight", pad_inches=0.0)
            hp.mollview(np.pi*radcs*(1.0-fclall)/irrad_solar,title="clear sky (BRDF)",flip="geo",cmap=plt.cm.pink,min=0.0)
            hp.graticule(color="orange")
            hp.mollview(np.pi*radcl*fclall/irrad_solar,title="cloud sky (BRDF)",flip="geo",cmap=plt.cm.pink,min=0.0)
            hp.graticule(color="orange")
            hp.mollview(fclall,title="cloud fraction",flip="geo",cmap=plt.cm.pink,min=0.0)
            hp.graticule(color="orange")
            plt.show()
 
    np.savetxt("lc"+str(pcol.ispec)+".txt",np.array([jd,lc,lccs,lccl,lccsf]).T)#reflectivity

    sys.exit()
    fig=plt.figure()
    ax=fig.add_subplot(311)
    ax.plot(jd,fcl,label="cloud fraction")
    plt.legend()
    ax=fig.add_subplot(312)
    ax.plot(jd,lc,label="LC")
    ax.plot(jd,lccl,label="cl")
    plt.legend()
    ax=fig.add_subplot(313)
    ax.plot(jd,np.array(lccs),label="cs")
    plt.legend()
    plt.show()



