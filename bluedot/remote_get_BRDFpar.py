import time
import rossli
import geometry
import read_hdf_MCD
import numpy as np
from pyhdf.SD import SD, SDC
import blue_calendar
import glob
import compref
from astropy.time import Time

ttimestr = "2008-3-22 06:48"
ttime = Time(ttimestr, format='iso', scale='utc')
jd = ttime.jd

ispec = 1

# read mean BRDF par
data = np.load(
    "/Users/kawahara/sotica/data/mean2008/mean2008_"+str(ispec)+".npz")
f_mean = data["arr_0"]
fiso_mean = f_mean[0, :, :]
fvol_mean = f_mean[1, :, :]
fgeo_mean = f_mean[2, :, :]

####
filelist = glob.glob("/Users/kawahara/sotica/data/MODIS/MCD43C1/MCD43C1*.hdf")
jdlist, jdmlist, ut, filelist = blue_calendar.make_jdlist(filelist)
mask = read_hdf_MCD.generate_land_mask(filelist)
fiso, fvol, fgeo = compref.get_BRDF_parameter(
    jd, ispec, filelist, jdmlist, mask, fiso_mean, fvol_mean, fgeo_mean)
