#!/usr/bin/python
import sys
import argparse
import matplotlib
import matplotlib.pyplot as plt
import pylab
import numpy as np
import healpy as hp
import time
import scipy.signal


def read_gpctxt(gpctxt):
    # read output of extractgpc.f90
    gdata = np.loadtxt(gpctxt, skiprows=4)
    phi = gdata[:, 0]/180.0*np.pi
    theta = (90.0-gdata[:, 1])/180.0*np.pi
    ndata = len(gdata)
    landf = np.mod(gdata[:, 2], 100)-1.0
    # extract the terrain as land=1 and ocean=0 coast=0.5
    maskcoast = (landf > 1.0)
    landf[maskcoast] = 0.5
    # day=1/night=0
    dnmask = (gdata[:, 2] > 100)
    daynight = np.ones(len(gdata[:, 2]))
    daynight[dnmask] = 0.0
    ntot = gdata[:, 3]
    ncloud = gdata[:, 4]
    ctp = gdata[:, 5]
    cth = gdata[:, 6]
    meanpc = gdata[:, 7]
    meantc = gdata[:, 8]
    meantau = gdata[:, 9]
    return phi, theta, landf, ntot, ncloud, daynight, ctp, cth, meanpc, meantc, meantau, ndata


def conv_healpix_form_test(phi, theta, landf, ntot, ncloud, daynight, ctp, cth, meanpc, meantc, meantau, ndata):
    nside = 16  # CHECK landf.fits if use value larger than 16
    npix = hp.nside2npix(nside)
    arr = np.zeros((npix, 8))
    numarr = np.zeros(npix)
    for idata in range(0, ndata):
        ipix = hp.ang2pix(nside, theta[idata], phi[idata])
        numarr[ipix] = numarr[ipix]+1
    mask = (numarr == 0)
    numarr[mask] = -1
    hp.write_map("num.fits", numarr[:])

    for idata in range(0, ndata):
        ipix = hp.ang2pix(nside, theta[idata], phi[idata])
#        arr[ipix,0]=landf[idata]+2.0*daynight[idata]+arr[ipix,0] #land, ocean1
        arr[ipix, 0] = landf[idata]+arr[ipix, 0]  # land, ocean1
        arr[ipix, 1] = ctp[idata]+arr[ipix, 1]
        arr[ipix, 2] = cth[idata]+arr[ipix, 2]
        arr[ipix, 3] = meanpc[idata]+arr[ipix, 3]
        arr[ipix, 4] = meantc[idata]+arr[ipix, 4]
        arr[ipix, 5] = meantau[idata]+arr[ipix, 5]
        arr[ipix, 6] = ntot[idata]+arr[ipix, 6]
        arr[ipix, 7] = ncloud[idata]+arr[ipix, 7]

    arr = arr/numarr[:, np.newaxis]
#    hp.write_map("land.fits", arr[:,0])
#    hp.write_map("ctp.fits", arr[:,1])
#    hp.write_map("cth.fits", arr[:,2])
#    hp.write_map("meanpc.fits", arr[:,3])
#    hp.write_map("meantc.fits", arr[:,4])
#    hp.write_map("meantau.fits", arr[:,5])
    mask = (arr[:, 6] == 0.0)
    arr[:, 6][mask] = -1.0
    cfrac = arr[:, 7]/arr[:, 6]
#    hp.write_map("cloudfraction.fits", cfrac)
    ac = 0.0
    al = 1.0
#    hp.write_map("mockalbedo.fits", cfrac*ac+(1-cfrac)*arr[:,0]*al)

    return cfrac*ac+(1-cfrac)*arr[:, 0]*al


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generate LC')
#    parser.add_argument('-i', nargs=1, help='month', type=str)
    args = parser.parse_args()

    # USE D1 data GPCTXT
    gpctxt = "/home/kawahara/sotica/data/ISCCP/d1/ISCCP.D1.1.GLOBAL.2008.06.30.2100.GPC.txt"
    phi, theta, landf, ntot, ncloud, daynight, ctp, cth, meanpc, meantc, meantau, ndata = read_gpctxt(
        gpctxt)

    # USE D1 data ANC FILE
#    gpc="data/ISCCP/ISCCP.D1GRID.0.GLOBAL.1983.99.99.9999.GPC"
#    phi, theta, landf, ndata=read_gpc(gpc)
    alb = conv_healpix_form_test(
        phi, theta, landf, ntot, ncloud, daynight, ctp, cth, meanpc, meantc, meantau, ndata)

    hp.write_map("mockalbedo.fits", alb)
    mmap = hp.read_map("mockalbedo.fits")

    sys.exit("--")
    nside = 16  # CHECK landf.fits if use value larger than 16
    npix = hp.nside2npix(nside)
    arr = np.zeros((npix, 8))
    numarr = np.zeros(npix)
    for idata in range(0, ndata):
        ipix = hp.ang2pix(nside, theta[idata], phi[idata])
        numarr[ipix] = numarr[ipix]+1
    mask = (numarr == 0)
    numarr[mask] = -1
    hp.write_map("num.fits", numarr[:])

    for idata in range(0, ndata):
        ipix = hp.ang2pix(nside, theta[idata], phi[idata])
#        arr[ipix,0]=landf[idata]+2.0*daynight[idata]+arr[ipix,0] #land, ocean1
        arr[ipix, 0] = landf[idata]+arr[ipix, 0]  # land, ocean1
        arr[ipix, 1] = ctp[idata]+arr[ipix, 1]
        arr[ipix, 2] = cth[idata]+arr[ipix, 2]
        arr[ipix, 3] = meanpc[idata]+arr[ipix, 3]
        arr[ipix, 4] = meantc[idata]+arr[ipix, 4]
        arr[ipix, 5] = meantau[idata]+arr[ipix, 5]
        arr[ipix, 6] = ntot[idata]+arr[ipix, 6]
        arr[ipix, 7] = ncloud[idata]+arr[ipix, 7]

    arr = arr/numarr[:, np.newaxis]
    hp.write_map("land.fits", arr[:, 0])
    hp.write_map("ctp.fits", arr[:, 1])
    hp.write_map("cth.fits", arr[:, 2])
    hp.write_map("meanpc.fits", arr[:, 3])
    hp.write_map("meantc.fits", arr[:, 4])
    hp.write_map("meantau.fits", arr[:, 5])
    mask = (arr[:, 6] == 0.0)
    arr[:, 6][mask] = -1.0
    cfrac = arr[:, 7]/arr[:, 6]
    hp.write_map("cloudfraction.fits", cfrac)
    ac = 0.5
    al = 0.3
    hp.write_map("mockalbedo.fits", cfrac*ac+(1-cfrac)*arr[:, 0]*al)

    print("-----------------------------------------------")
    print("COMPLETED DESPITE OF PLENTY OF WARNINGS (^_^)/.")
    print("-----------------------------------------------")
