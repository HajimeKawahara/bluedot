#!/usr/bin/python
import numpy as np
import argparse
import sys

def derive_R_eff(WP,tau):
    #WP: (Cloud or Liquid) Water Path [g/m2]
    #R_eff um
    R_eff = WP/(0.692*tau) #see Rossow and Schiffer (1999)
    return R_eff

def derive_LWC(WP,widthkm):
    #LWC: Liquid Water Contents  [g/m3]
    return WP/(widthkm*1.e3)

def thin_profile(WP,tau,cth,widthkm=1.0,fidreff=10.0):
    #cth cloud top height [m]
    #fidreff=10.0 micron (effective radius)
    cthkm=cth*1.e-3
    if cthkm < widthkm:
        z=[widthkm,0.0]
    else:
        z=[cthkm,cthkm-widthkm]

    LWC=[0.0,WP/(widthkm*1.e3)] #g/m3
    print("z=",z,"LWC=",LWC)
    R_eff=[0.0,fidreff]

    return z, LWC, R_eff
