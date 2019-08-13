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
import ctypes
from pathlib import Path
from astropy.time import Time

from datetime import datetime

class GPC:

    def  __init__(self):
        self.dirpath=Path("")
        
    def set_path(self,path):
        self.dirpath=Path(path)

    def load_gpclist(self,filename="filelist.txt"):
        pathf = self.dirpath / Path(filename)
        f=open(pathf)
        data=f.read()
        f.close()
        ds=data.split("\n")
        self.gpcfile=[]
        self.gpcjd=[] #jd
        self.gpctime=[] #datetime object

        for l in ds:
            if len(l) > 2:
                self.gpcfile.append(str(self.dirpath/Path(l)))
                ll=l.split(".")
                utcstr=datetime(int(ll[-5]),int(ll[-4]),int(ll[-3]),int(ll[-2][0:2]), int(ll[-2][3:]), 0)
                ttime=Time(Time(utcstr), format='iso', scale='utc')
                self.gpctime.append(ttime)
                jd=ttime.jd
                self.gpcjd.append(jd)
        self.gpcjd=np.array(self.gpcjd)
        
    def load_anc(self):
        self.ancpath=self.dirpath / Path("ANC.GPC")
        set_anc(str(self.ancpath))


def set_anc(ancfile, flibrary="wrapgpc.so"):
    if Path(flibrary).exists():
        ctypes.add_np = np.ctypeslib.load_library(flibrary, ".")
        ctypes.add_np.set_isccpanc_.argtypes = [ctypes.c_char_p, ctypes.c_long]
        ctypes.add_np.set_isccpanc_.restype = ctypes.c_void_p
        ctypes.add_np.set_isccpanc_((ancfile).encode('utf-8'), len(ancfile))
    else:
        sys.exit("Put wrapgpc.so in the working directory.")
    return

def read_gpc(gpcfile, wrappath, phioffset=1.65588):
    # GPCFILE,clong,clati,galt (ground altitude m),cth, meantc, meantau,meanpc,ctp,ntot, ncloud, surfaceclass, datearr
    MAXBOX = 6596
    ctypes.add_np = np.ctypeslib.load_library(wrappath, ".")
    ctypes.add_np.read_isccpd1_.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        ctypes.c_char_p, ctypes.c_long]
    ctypes.add_np.read_isccpd1_.restype = ctypes.c_void_p

    clong = np.zeros(MAXBOX, dtype=np.float32)
    clati = np.zeros(MAXBOX, dtype=np.float32)
    galt = np.zeros(MAXBOX, dtype=np.float32)
    cth = np.zeros(MAXBOX, dtype=np.float32)
    meantc = np.zeros(MAXBOX, dtype=np.float32)
    meantau = np.zeros(MAXBOX, dtype=np.float32)
    meanwp = np.zeros(MAXBOX, dtype=np.float32)
    meanpc = np.zeros(MAXBOX, dtype=np.float32)
    ctp = np.zeros(MAXBOX, dtype=np.float32)
    ntot = np.zeros(MAXBOX, dtype=np.int32)
    ncloud = np.zeros(MAXBOX, dtype=np.int32)
    surfaceclass = np.zeros(MAXBOX, dtype=np.int32)
    datearr = np.zeros(4, dtype=np.int32)

    ctypes.add_np.read_isccpd1_(clong, clati, galt, cth, meantc, meantau, meanwp, meanpc,
                                ctp, ntot, ncloud, surfaceclass, datearr, gpcfile.encode('utf-8'), len(gpcfile))
    phi = np.mod(clong/180.0*np.pi - phioffset, 2*np.pi)
    theta = (90.0-clati)/180.0*np.pi

    return phi, theta, galt, cth, meantc, meantau, meanwp, meanpc, ctp, ntot, ncloud, surfaceclass, datearr


def testwrap(s, p, flibrary="wrapgpc.so"):
    ctypes.add_np = np.ctypeslib.load_library(flibrary, ".")

    print("+ wrap float32")
    ctypes.add_np.test_.argtypes = [ctypes.POINTER(
        ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
    ctypes.add_np.test_.restype = ctypes.c_void_p

    a, b = 10, 1
    a = ctypes.c_int32(a)
    b = ctypes.c_int32(b)
    ctypes.add_np.test_(ctypes.byref(a), ctypes.byref(b))
    print((a.value, b.value))

    print("+ wrap numpy and str")
    n = 10
    c = np.zeros(n, dtype=np.float32)
    d = np.zeros(n, dtype=np.int32)

    ctypes.add_np.testchar_.argtypes = [np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(
        dtype=np.int32), ctypes.c_char_p, ctypes.c_long]  # for string, you need pointer and long int for length
    ctypes.add_np.testchar_.restype = ctypes.c_void_p
    c[2] = 2.0
    d[1] = 5
    ctypes.add_np.testchar_(c, d, s.encode('utf-8'), len(s))
    print(d)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Reading the isccp GPC files.')
#    parser.add_argument('-i', nargs=1, help='month', type=str)
    args = parser.parse_args()

    gpc=GPC()
    gpc.set_path("/home/kawahara/sotica/data/ISCCP/d1/")
    gpc.load_anc()
    gpc.load_gpclist()
    phi, theta, galt, cth, meantc, meantau, meanwp, meanpc, ctp, ntot, ncloud, surfaceclass, datearr = read_gpc(gpc.gpcfile[0],"/home/kawahara/sotica/bluedot/wrapgpc.so")

#    print(("UT=", datearr))
