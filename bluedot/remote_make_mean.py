import time
import rossli
import geometry
import read_hdf_MCD
import numpy as np
from pyhdf.SD import SD, SDC
import blue_calendar
import glob

print("compute 2008 mean")
filelist = glob.glob(
    "/Users/kawahara/sotica/data/MODIS/MCD43C1/MCD43C1.A2008*.hdf")
for i in range(1, 8):
    print(("Computing spec=", i))
    jdlist, jdmlist, ut, filelist = blue_calendar.make_jdlist(filelist)
    fiso_mean, fvol_mean, fgeo_mean = read_hdf_MCD.generate_mean(filelist, i)
    np.savez("mean2008_"+str(i)+".npz",
             np.array([fiso_mean, fvol_mean, fgeo_mean]))
