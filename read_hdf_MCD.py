#!/usr/bin/python
import numpy as np
from pyhdf.SD import SD, SDC
import sys
import glob
import blue_calendar
import geometry
nlat_MCD43C1 = 3600
nlon_MCD43C1 = 7200
    
class ModisMCD:
    def __init__(self):
        self.nlat_MCD43C1 = 3600
        self.nlon_MCD43C1 = 7200

    def load_fmean(self,modismeanpath):
        data = np.load(modismeanpath)
        f_mean = data["arr_0"]
        self.fiso_mean = f_mean[0, :, :]
        self.fvol_mean = f_mean[1, :, :]
        self.fgeo_mean = f_mean[2, :, :]

    def load_mcdpathlist(self,mcdpath):
        mcdfilelist = glob.glob(mcdpath)
        self.jdlist, self.jdmlist, self.ut, self.filelist = blue_calendar.make_jdlist(mcdfilelist)

    def load_ldmask(self):
        self.ldmask = generate_land_mask(self.filelist)

    def set_grid(self):
        print("* Set the MODIS grid")
        phioffset=0.0
        self.thetam, self.phim = geometry.setsphere(self.nlat_MCD43C1, self.nlon_MCD43C1, phioffset)


        
def read_MCD(filename, parameter):
    # filename="/Users/kawahara/sotica/data/MODIS/MCD43C1/MCD43C1.A2008129.005.2008152165510.hdf"
    # parameter="BRDF_Albedo_Parameter1_Band1"
    f = SD(filename, SDC.READ)
    v = f.select(parameter)
    a = np.array(v[0:nlat_MCD43C1, 0:nlon_MCD43C1], dtype=float)
#    a=np.array(v[0:nlat_MCD43C1:2,0:nlon_MCD43C1:2],dtype=float)

    if parameter[0:11] == "BRDF_Albedo":
        vr = v.attributes()["valid_range"]
        fv = v.attributes()["_FillValue"]
        ao = v.attributes()["add_offset"]
        sf = v.attributes()["scale_factor"]
        a[a == fv] = None
        a = (a-ao)*sf

    return a


def generate_land_mask(filelist):
    # generate land/water mask from hdf files
    parameter = "BRDF_Albedo_Parameter1_Band1"
    mask = np.zeros((nlat_MCD43C1, nlon_MCD43C1), dtype=bool)

    for filename in filelist:
        f = SD(filename, SDC.READ)
        v = f.select(parameter)
        fv = v.attributes()["_FillValue"]
        a = np.array(v[0:nlat_MCD43C1, 0:nlon_MCD43C1], dtype=float)
        mask[a != fv] = True

    return mask


def generate_mean(filelist, speci):
    parameter = ["BRDF_Albedo_Parameter1_Band"+str(speci), "BRDF_Albedo_Parameter2_Band"+str(
        speci), "BRDF_Albedo_Parameter3_Band"+str(speci)]
    f_mean = np.zeros((nlat_MCD43C1, nlon_MCD43C1, 3))
    n_mean = np.zeros((nlat_MCD43C1, nlon_MCD43C1))

    for filename in filelist:
        print(filename)
        f = SD(filename, SDC.READ)

        for i in range(0, 3):
            v = f.select(parameter[i])
            a = np.array(v[0:nlat_MCD43C1, 0:nlon_MCD43C1], dtype=float)

            vr = v.attributes()["valid_range"]
            fv = v.attributes()["_FillValue"]
            ao = v.attributes()["add_offset"]
            sf = v.attributes()["scale_factor"]
            mask = (a == fv)
            a[mask] = 0.0
            a = (a-ao)*sf
            f_mean[:, :, i] = f_mean[:, :, i]+a
            if i == 0:
                n_mean[~mask] = n_mean[~mask]+1

    fiso_mean = f_mean[:, :, 0]/n_mean
    fvol_mean = f_mean[:, :, 1]/n_mean
    fgeo_mean = f_mean[:, :, 2]/n_mean

    return fiso_mean, fvol_mean, fgeo_mean


if __name__ == "__main__":
    print("test")
