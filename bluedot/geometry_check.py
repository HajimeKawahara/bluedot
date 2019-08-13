#!/usr/bin/python
import pylab
import matplotlib.pyplot as plt
import rossli
import read_hdf_MCD
import blue_calendar
import brdf_modis
import read_isccp
import resamp_healpix
import healpy as hp
import numpy as np
import argparse
from astropy.time import Time
import glob
from datetime import datetime
import time
import generate_globe as gg
import makeinput as mi
import iouvspec
import sys
from bluedotclass import PlanetGeometry
from bluedotclass import PlanetColor
from bluedotclass import PlanetData
from makeinput import LibRadtran
import cloudmodel as clm


def compute_snapshot_gc(pgeo, default_input, nband=1):
    radall = []
    j=0
    for ipix in range(0, pgeo.npix):
        pgeo.ipix=ipix
        if pgeo.VI:
#            print(ipix, "/", pgeo.npix)
            radall.append(1.0*np.ones(nband))
            j=j+1
        else:
            radall.append(np.zeros(nband))
    print("VI fraction=",np.float(j)/pgeo.npix)
    return radall


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generating a snapshot.')
#    parser.add_argument('-i', nargs=1, help='month', type=str)
    args = parser.parse_args()

    pgeo = PlanetGeometry()
    pgeo.jd=pgeo.jd#+0.5 ### solar day for prograde = 1d
    pdata = PlanetData()
    pcol = PlanetColor()

    default_input = "/home/kawahara/sotica/bluedot/input/template.INP"
    radall=compute_snapshot_gc(pgeo, default_input, nband=1801)
    srad = np.sum(radall, axis=1)

    gpc,mcd = gg.initgg(pdata,pcol)
    start = time.time()

    #### time match ####
    print("==================")
    isel=np.searchsorted(gpc.gpcjd,pgeo.jd)
    distance=(np.abs(gpc.gpcjd[isel-2:isel+2]-pgeo.jd))
    iselp=np.array([isel-2,isel-1,isel,isel+1])
    prind=np.argsort(distance)
    isel_priority=iselp[prind]
    print("==================")

    #####
#    fcl, meantauxd, cthx=gg.set_gsurface_clouds(pdata,pgeo,gpc.gpcfile[isel_priority[0]])
    fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask=gg.set_gsurface_clouds_vi(pdata,pgeo,gpc)

#    for i in range(0,len(meantauxd)):
#        print(meantauxd[i])
    elapsed_time = time.time() - start
    print(("set surface :{0}".format(elapsed_time)) + "[sec]")

    mask = (meantauxd < 0.0)
    taumap = np.copy(meantauxd)
    taumap[mask] = None

    mask = (meanwpxd < 0.0)
    wpmap = np.copy(meanwpxd)
    wpmap[mask] = None


    print("Median cloud fraction=",np.median(fcl))
    hp.mollview(srad, title="sum rad", flip="geo", cmap=plt.cm.pink, min=0.0)
#    hp.orthview(srad, title="sum rad", flip="geo", cmap=plt.cm.pink, min=0.0)
    hp.graticule(color="orange")
    hp.mollview(np.log10(taumap), title="mean log tau", flip="geo",
                cmap=plt.cm.coolwarm, min=-1, max=2)
    hp.graticule(color="orange")

    hp.mollview((wpmap), title="water path [g/m2]", flip="geo",
                cmap=plt.cm.coolwarm)
    hp.graticule(color="orange")

    hp.mollview(clm.derive_R_eff(wpmap,taumap), title="effective droplet radius [um]", flip="geo",
                cmap=plt.cm.coolwarm, min=0.0,max=30.0)
    hp.graticule(color="orange")

    hp.mollview(fcl, title="cloud fraction", flip="geo",
                cmap=plt.cm.coolwarm)
    hp.graticule(color="orange")
    hp.mollview(cthx, title="cloud top height", flip="geo",
                cmap=plt.cm.coolwarm)
    hp.graticule(color="orange")
    hp.mollview(iselmapt, title="selected index (tau)", flip="geo",
                cmap=plt.cm.coolwarm)
    hp.graticule(color="orange")

    hp.mollview(iselmapw, title="selected index (wp)", flip="geo",
                cmap=plt.cm.coolwarm)
    hp.graticule(color="orange")

    plt.show()
    
