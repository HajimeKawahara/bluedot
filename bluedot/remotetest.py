import read_hdf_MCD
import numpy as np
import time
import rossli
import geometry
import sys
start = time.time()

filename = "/Users/kawahara/sotica/data/MODIS/MCD43C1/MCD43C1.A2008129.005.2008152165510.hdf"
parameter1 = "BRDF_Albedo_Parameter1_Band1"
parameter2 = "BRDF_Albedo_Parameter2_Band1"
parameter3 = "BRDF_Albedo_Parameter3_Band1"

fiso = read_hdf_MCD.read_MCD(filename, parameter1)
fgeo = read_hdf_MCD.read_MCD(filename, parameter2)
fvol = read_hdf_MCD.read_MCD(filename, parameter3)
theta, phi = geometry.setsphere(np.shape(fiso)[0], np.shape(fiso)[1])

# flatten------------
fiso = fiso.flatten()
fgeo = fgeo.flatten()
fvol = fvol.flatten()
theta = theta.flatten()
phi = phi.flatten()
# -------------------

eR = np.random.rand(np.shape(fiso)[0], 3)-0.5  # npix x 3
eS = np.array([0.0, 1.0, 0.0])  # 1 x 3
eO = np.array([0.2, 0.3, 0.1])  # 1 x 3

ref = rossli.refRL(fiso, fgeo, fvol, eS, eR, eO)

elapsed_time = time.time() - start
print((("CPU elapsed_time:{0}".format(elapsed_time)) + "[sec]"))
