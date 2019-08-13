#!/usr/bin/python
import numpy as np
from astropy.time import Time
from pyhdf.SD import SD, SDC


#def init_calendar(sd=0.99726958, sy=365.25636302, timeveq="2008-3-20 05:48"):
#    # sd: Siderial day, sy: Siderial year
    # vernal equinox in 2008
#    ttime = Time(timeveq, format='iso', scale='utc')
#    j0 = ttime.jd  # vernal equinox in 2008 phi=0
#
#    return sd, sy, j0

#def get_orbital_phase(jd):
#    sd, sy, j0 = init_calendar()#
#
#    Thetav = np.mod((jd-j0), sy)*2*np.pi
#    Phiv = np.mod((jd-j0), sd)*2*np.pi
#    return Thetav, Phiv

##################################################################

def get_jdhdf(f, exttime="RANGEBEGINNINGDATE"):
    # extract JD from hdf files (tested only for MCD43C1)
    v = f.attributes()
    try:
        i = v["CoreMetadata.0.1"].find(exttime)
        ttimestr = v["CoreMetadata.0.1"][i:i+120].split('"')[1]
    except:
        i = v["CoreMetadata.0"].find(exttime)
        ttimestr = v["CoreMetadata.0"][i:i+120].split('"')[1]

    ttime = Time(ttimestr, format='iso', scale='utc')
    jdtime = ttime.jd

    return jdtime, ttimestr




def make_jdlist(filelist):
    # make a JD list from hdf files (tested only for MCD43C1)
    jdlist = []
    jdmlist = []
    ut = []
    for filename in filelist:
        f = SD(filename, SDC.READ)
        jdstart, ttimestrstart = get_jdhdf(f, "RANGEBEGINNINGDATE")
        jdend, ttimestrend = get_jdhdf(f, "RANGEENDINGDATE")
        jdmed = (jdstart+9)
        jdmlist.append(jdmed)
        jdlist.append([jdstart, jdend])
        ut.append([ttimestrstart, ttimestrend])

    # sorting
    ind = np.argsort(jdmlist)
    filelist = np.array(filelist)[ind]
    print("filelist was sorted by order of date.")
    jdlist = np.array(jdlist)[ind]
    jdmlist = np.array(jdmlist)[ind]
    ut = np.array(ut)[ind]

    return jdlist, jdmlist, ut, filelist


def get_intp_coefficient(jd, jdmlist):
    # compute the linear interpolation coefficient, alpha
    j = np.digitize([jd], jdmlist)[0]
    i = j-1
    if i < 0 or j >= len(jdmlist):
        print("out of range")
        alpha = 0.0
        sys.exit("EXIT.")
    else:
        alpha = (jd - jdmlist[i])/(jdmlist[j]-jdmlist[i])

    # i: left index of a hdf file
    # j: right index of a hdf file
    return i, j, alpha
