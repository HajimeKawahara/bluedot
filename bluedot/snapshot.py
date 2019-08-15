#!/usr/bin/python
import pylab
import matplotlib.pyplot as plt
import rossli
import geometry
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
from makeinput import LibRadtran
from bluedotclass import PlanetGeometry
from bluedotclass import PlanetColor
from bluedotclass import PlanetData
import cloudmodel as clm
import plotgeo as plg

def compute_snapshot(pdata,pgeo,pcol,inpdir="INP"):

    gpc,mcd = gg.initgg(pdata,pcol)
    fisox, fvolx, fgeox, landfx=gg.set_gsurface_brdf(pgeo, pcol, mcd)
    fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask=gg.set_gsurface_clouds_vi(pdata,pgeo,gpc)
#    plg.plotall(fisox, fvolx, fgeox, landfx, fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask, cmap=plt.cm.jet)

    others=[fisox, fvolx, fgeox, landfx, fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask]

    #radall = []
    radallcl=[]
    radallcs=[]
    fclall=[]
    ipixarr = []
    ereo=[]

    wgfile = inpdir+"/wgf.txt"
    for ipix in range(0, pgeo.npix):
#    for ipix in range(2247, 2248):
        pgeo.ipix=ipix
        if pgeo.VI:
            print(ipix, "/", pgeo.npix)
            ipixarr.append(ipix)
            ereo.append(np.dot(pgeo.eR, pgeo.eO)[0])

            inputfile = inpdir+"/tmp" + str(ipix)+"cs.INP"
            inputfilec= inpdir+"/tmp" + str(ipix)+"cl.INP"
            wcfile = inpdir+"/WC" + str(ipix)+".DAT"

            librad = LibRadtran(inputfile, wcfile, wgfile)
            libradc = LibRadtran(inputfilec, wcfile, wgfile)

            librad.default(pdata.default_input)
            libradc.default(pdata.default_input)

            librad.solver("fdisort2")
            libradc.solver("fdisort2")
            librad.pseudospherical()
            libradc.pseudospherical()

            librad.angles(pgeo.sza, pgeo.vza, pgeo.aza)
            libradc.angles(pgeo.sza, pgeo.vza, pgeo.aza)
            
            # LAND or OCEAN?
            if landfx[ipix] > 0.5:
                librad.rossli(fisox[ipix], fvolx[ipix], fgeox[ipix])
                libradc.rossli(fisox[ipix], fvolx[ipix], fgeox[ipix])
                print("Ross-Li parameters:")
                print(fisox[ipix], fvolx[ipix], fgeox[ipix])
            else:
                librad.ocean()
                libradc.ocean()
                print("Ocean")


            #SET WAVE LENGTH GRID
            wavegrid=pcol.wavegrid
            librad.savewg(wavegrid)                
            libradc.savewg(wavegrid)                
            # Clear Sky
            lamb, radcs = librad.uvspec()
            # Cloudy Sly
            if meanwpxd[ipix]>0.0:
                z,LWC,R_eff=clm.thin_profile(meanwpxd[ipix],meantauxd[ipix],cthx[ipix])
                libradc.savewc(z,LWC,R_eff)                
                lamb, radcl = libradc.uvspec()
                fcln=fcl[ipix]
                fclall.append(fcln)
                radallcl.append(radcl)
                radallcs.append(radcs)
                #radall.append((1.0-fcln)*np.array(radcs)+fcln*np.array(radcl))
                print("****** CLOUDY!!",fcl[ipix])
            else:
                print("****** CLEAR SKY!!",fcl[ipix])
                fclall.append(0.0)
                radallcl.append(np.zeros(len(radcs)))
                radallcs.append(radcs)
                #radall.append(np.array(radcs))

    print("End snapshot.")

    return ipixarr, ereo, lamb, others, radallcl, radallcs, fclall


def notcompute_snapshot(pdata,pgeo,pcol,inpdir="INP"):

    gpc,mcd = gg.initgg(pdata,pcol)
    fiso, fvol, fgeo = brdf_modis.get_BRDF_parameters(pgeo.jd, pcol.ispec, mcd)
#    fisox, fvolx, fgeox, landfx=gg.set_gsurface_brdf(pgeo, pcol, mcd)
#    fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask=gg.set_gsurface_clouds_vi(pdata,pgeo,gpc)

    return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generating a snapshot.')
    parser.add_argument('-d',default=[0.0],nargs=1, help='day', type=float)
    args = parser.parse_args()
    increment=args.d[0]
    pgeo = PlanetGeometry()
    pgeo.jd=pgeo.jd+increment ### solar day for prograde = 1d
    pdata = PlanetData()
    pcol = PlanetColor(1)

