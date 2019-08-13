#!/usr/bin/python
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
from read_isccp import GPC
from bluedotclass import PlanetColor
from bluedotclass import PlanetGeometry
from bluedotclass import PlanetData
from read_hdf_MCD import ModisMCD


def initgg(pdata,pcol):
    print("* Init MCD (MODIS)")
    mcd=ModisMCD()
    mcd.load_fmean(pdata.modismeanpath(pcol))
    mcd.load_mcdpathlist(pdata.mcdpath)
    mcd.load_ldmask()
    mcd.set_grid()

    print("* Init GPC (ISCPP)")
    gpc=GPC()
    gpc.set_path(pdata.d1path)
    gpc.load_anc()
    gpc.load_gpclist()

    return gpc, mcd


def set_gsurface(pdata, pgeo, pcol, mcd):

    # READ ISCCP
    phi, theta, galt, cth, meantc, meantau, meanwp, meanpc, ctp, ntot, ncloud, surfaceclass, datearr = read_isccp.read_gpc(gpc,pdata.wrappath)

    galtx = resamp_healpix.step_by_healpix(galt, theta, phi, pgeo.nside)
    cthx = resamp_healpix.step_by_healpix(cth, theta, phi, pgeo.nside)
    ntotx = resamp_healpix.step_by_healpix(ntot, theta, phi, pgeo.nside)
    ncloudx = resamp_healpix.step_by_healpix(ncloud, theta, phi, pgeo.nside)
    meantauxd = resamp_healpix.step_by_healpix(meantau, theta, phi, pgeo.nside)

    #set UTC
    utcstr = Time(datetime(datearr[0], datearr[1], datearr[2], datearr[3], 0, 0))
    ttime=Time(utcstr, format='iso', scale='utc')
    jd=ttime.jd

    # read MODIS at UTC
    fiso, fvol, fgeo = brdf_modis.get_BRDF_parameters(pgeo.jd, pcol.ispec, mcd)
    # resampling
    fisox = resamp_healpix.step_by_healpix(
        fiso.flatten(), thetam.flatten(), phim.flatten(), pgeo.nside)
    fvolx = resamp_healpix.step_by_healpix(
        fvol.flatten(), thetam.flatten(), phim.flatten(), pgeo.nside)
    fgeox = resamp_healpix.step_by_healpix(
        fgeo.flatten(), thetam.flatten(), phim.flatten(), pgeo.nside)
    landfx = resamp_healpix.step_by_healpix(
        ldmask.flatten(), thetam.flatten(), phim.flatten(), pgeo.nside)

    return utcstr, jd, fisox, fvolx, fgeox, galtx, cthx, ntotx, ncloudx, meantauxd, landfx

def set_gsurface_brdf(pgeo, pcol, mcd):
    #set UTC

    # read MODIS at UTC
    fiso, fvol, fgeo = brdf_modis.get_BRDF_parameters(pgeo.jd, pcol.ispec, mcd)    # resampling
    fisox = resamp_healpix.step_by_healpix(
        fiso.flatten(), mcd.thetam.flatten(), mcd.phim.flatten(), pgeo.nside)
    fvolx = resamp_healpix.step_by_healpix(
        fvol.flatten(), mcd.thetam.flatten(), mcd.phim.flatten(), pgeo.nside)
    fgeox = resamp_healpix.step_by_healpix(
        fgeo.flatten(), mcd.thetam.flatten(), mcd.phim.flatten(), pgeo.nside)
    landfx = resamp_healpix.step_by_healpix(
        mcd.ldmask.flatten(), mcd.thetam.flatten(), mcd.phim.flatten(), pgeo.nside)

    return fisox, fvolx, fgeox, landfx

    

def get_vimask(pgeo):
    vimask = []
    j=0
    for ipix in range(0, pgeo.npix):
        pgeo.ipix=ipix
        if pgeo.VI:
            vimask.append(True)
            j=j+1
        else:
            vimask.append(False)
    print("VI fraction=",np.float(j)/pgeo.npix)
    vimask=np.array(vimask)
    return vimask


def set_gsurface_clouds(pdata,pgeo,gpcfile):
    # READ ISCCP MEAB TAU ONLY
    phi, theta, galt, cth, meantc, meantau,  meanwp, meanpc, ctp, ntot, ncloud, surfaceclass, datearr = read_isccp.read_gpc(gpcfile, pdata.wrappath)

    ntotx = resamp_healpix.step_by_healpix(ntot, theta, phi, pgeo.nside)
    ncloudx = resamp_healpix.step_by_healpix(ncloud, theta, phi, pgeo.nside)
    fcl=ncloudx/list(map(float, ntotx))   #cloud fraction
    
    meantauxd = resamp_healpix.step_by_healpix(meantau, theta, phi, pgeo.nside,False)
    galtx = resamp_healpix.step_by_healpix(galt, theta, phi, pgeo.nside,False) #ground height
    cthx = resamp_healpix.step_by_healpix(cth, theta, phi, pgeo.nside,False)   #cloud top height
    
    #set UTC
    utcstr = Time(datetime(datearr[0], datearr[1], datearr[2], datearr[3], 0, 0))
    ttime=Time(utcstr, format='iso', scale='utc')
    jd=ttime.jd
    print("Time in GPC=",utcstr)
    print("JD in GPC=",jd)

    return fcl, meantauxd, cthx

def set_gsurface_clouds_vi(pdata,pgeo,gpc):

    #TIME SELECTION
    isel=np.searchsorted(gpc.gpcjd,pgeo.jd)
    distance=(np.abs(gpc.gpcjd[isel-2:isel+2]-pgeo.jd))
    iselp=np.array([isel-2,isel-1,isel,isel+1])
    prind=np.argsort(distance)
    isel_priority=iselp[prind] #order 

    #closest
    gpcfile=gpc.gpcfile[isel_priority[0]] 
    print("Closest GPC file=",gpcfile)
    phi, theta, galt, cth, meantc, meantau, meanwp, meanpc, ctp, ntot, ncloud, surfaceclass, datearr = read_isccp.read_gpc(gpcfile, pdata.wrappath)
    ntotx = resamp_healpix.step_by_healpix(ntot, theta, phi, pgeo.nside)
    ncloudx = resamp_healpix.step_by_healpix(ncloud, theta, phi, pgeo.nside)
    fcl=ncloudx/list(map(float, ntotx))   #cloud fraction

    galtx = resamp_healpix.step_by_healpix(galt, theta, phi, pgeo.nside,False) #ground height
    cthx = resamp_healpix.step_by_healpix(cth, theta, phi, pgeo.nside,False)   #cloud top height
    
    iselmapt = np.ones(pgeo.npix,dtype=np.float)*isel_priority[0]
    meantauxd = resamp_healpix.step_by_healpix(meantau, theta, phi, pgeo.nside,False)
    iselmapw = np.ones(pgeo.npix,dtype=np.float)*isel_priority[0]
    meanwpxd = resamp_healpix.step_by_healpix(meanwp, theta, phi, pgeo.nside,False)

    vimask=get_vimask(pgeo)

    maskt=(meantauxd<0.0)*vimask
    maskw=(meanwpxd<0.0)*vimask

    for j in range(1,len(isel_priority)):
        gpcfile=gpc.gpcfile[isel_priority[j]] 
        phi, theta, galt, cth, meantc, meantau, meanwp, meanpc, ctp, ntot, ncloud, surfaceclass, datearr = read_isccp.read_gpc(gpcfile, pdata.wrappath)
        #mean tau
        meantautmp = resamp_healpix.step_by_healpix(meantau, theta, phi, pgeo.nside,False)
        meantauxd[maskt] = meantautmp[maskt]
        maskt=(meantauxd<0.0)*vimask
        #mean wp
        meanwptmp = resamp_healpix.step_by_healpix(meanwp, theta, phi, pgeo.nside,False)
        meanwpxd[maskw] = meanwptmp[maskw]
        maskw=(meanwpxd<0.0)*vimask

        iselmapt[maskt] = isel_priority[j]
        iselmapw[maskw] = isel_priority[j]


    # extrapolation        
    maskt=(meantauxd<0.0)*vimask
    maskw=(meanwpxd<0.0)*vimask

    iselmapt[maskt] = None
    iselmapw[maskw] = None

    # extraporate by neibours 
    pixorder = np.array(range(0, pgeo.npix))

    # tau
    nullpix = pixorder[maskt]
    nnull = len(nullpix)
    nullang = hp.pix2ang(pgeo.nside, nullpix)
    px4 = (hp.get_all_neighbours(pgeo.nside, nullang[0], nullang[1])).T
    for jpix in range(0, nnull):
        val = np.nanmedian(meantauxd[px4[jpix]])
        ipix = nullpix[jpix]
        meantauxd[ipix] = val
    # WP
    nullpix = pixorder[maskw]
    nnull = len(nullpix)
    nullang = hp.pix2ang(pgeo.nside, nullpix)
    px4 = (hp.get_all_neighbours(pgeo.nside, nullang[0], nullang[1])).T
    for jpix in range(0, nnull):
        val = np.nanmedian(meanwpxd[px4[jpix]])
        ipix = nullpix[jpix]
        meanwpxd[ipix] = val


    return fcl, meantauxd, cthx, meanwpxd, iselmapt, iselmapw, vimask




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generate globe')
#    parser.add_argument('-i', nargs=1, default=["template.INP"], help="template input file", type=str)
    args = parser.parse_args()
    
