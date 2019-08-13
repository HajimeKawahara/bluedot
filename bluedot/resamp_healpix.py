#!/usr/bin/python
import sys
import argparse
import numpy as np
import healpy as hp
import time


def step_by_healpix(arrin, theta, phi, nside=8, ext=True, RUNDEF=-1000.0, FillVal=-1.0):
    ndata = len(arrin)
    if len(theta) != ndata or len(phi) != ndata:
        print("Fatal Error: Inconsisitent data length.")
        return arr

    npix = hp.nside2npix(nside)
    arr = np.zeros(npix)
    numarr = np.zeros(npix)
    ipixarr = hp.ang2pix(nside, theta, phi)

    for idata in range(0, ndata):
        if arrin[idata] == arrin[idata] and arrin[idata] != RUNDEF:
            #        ipix=hp.ang2pix(nside,theta[idata],phi[idata])
            ipix = ipixarr[idata]
            numarr[ipix] = numarr[ipix]+1
            arr[ipix] = arrin[idata]+arr[ipix]  # land, ocean1

    mask = (numarr == 0)
    arr[mask] = FillVal
    numarr[mask] = 1
    arr = arr/numarr

    # extrapolation
    if ext:
        pixorder = np.array(range(0, npix))
        nullpix = pixorder[mask]
        nnull = len(nullpix)
        nullang = hp.pix2ang(nside, nullpix)
        px4 = (hp.get_all_neighbours(nside, nullang[0], nullang[1])).T
        for jpix in range(0, nnull):
            val = np.nanmedian(arr[px4[jpix]])
            ipix = nullpix[jpix]
            arr[ipix] = val


            
    return arr


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generate LC')
#    parser.add_argument('-i', nargs=1, help='month', type=str)
    args = parser.parse_args()
    step_by_healpix([1.0])
