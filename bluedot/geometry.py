#!/usr/bin/python
import sys
import numpy as np
import healpy as hp


def set_heal_thetaphi(nside):
    npix = hp.nside2npix(nside)
    thetax, phix = hp.pix2ang(nside, list(range(0, npix)))
    return thetax, phix


def uniteO(inc, Thetaeq):
    # (3)
    eO = np.array([np.sin(inc)*np.cos(Thetaeq), -
                   np.sin(inc)*np.sin(Thetaeq), np.cos(inc)])
    return eO


def uniteS(Thetaeq, Thetav):
    # (3,nsamp)
    eS = np.array([np.cos(Thetav-Thetaeq), np.sin(Thetav-Thetaeq), 0.0])
    return eS


def uniteR(zeta, Phiv, theta, phi):
    # (3,nsamp,npix)
    np.array([Phiv]).T
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    cosphiPhi = np.cos(phi+np.array([Phiv]).T)
    sinphiPhi = np.sin(phi+np.array([Phiv]).T)
#    cosphiPhi=np.cos(omega[:,1]-np.array([Phiv]).T)
#    sinphiPhi=np.sin(omega[:,1]-np.array([Phiv]).T)

    x = cosphiPhi*sintheta
    y = np.cos(zeta)*sinphiPhi*sintheta+np.sin(zeta)*costheta
    z = -np.sin(zeta)*sinphiPhi*sintheta+np.cos(zeta)*costheta
    eR = np.array([x, y, z]).T

    return eR


def setsphere(nlat, nlon, phioffset=0.0):
    print(("# of latitude:", nlat))
    print(("# of latitude:", nlon))
    lat = np.arange(0, np.pi, np.pi/nlat)
    theta = lat.reshape(nlat, 1)+np.zeros(nlon)

    lon = np.arange(-np.pi, np.pi, 2*np.pi/nlon)
    lon = np.mod(lon-phioffset, 2*np.pi)
    phi = lon+np.zeros(nlat).reshape(nlat, 1)

    return theta, phi


if __name__ == "__main__":
    print("geometry")
