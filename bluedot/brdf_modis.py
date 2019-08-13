#!/usr/bin/python
import rossli
import geometry
import read_hdf_MCD
import numpy as np
import blue_calendar


def get_BRDF_parameters(jd,ispec,mcd):
    # this function provides the BRDF parameters for a given ut.
    parameter1 = "BRDF_Albedo_Parameter1_Band"+str(ispec)
    parameter2 = "BRDF_Albedo_Parameter2_Band"+str(ispec)
    parameter3 = "BRDF_Albedo_Parameter3_Band"+str(ispec)

    i, j, alpha = blue_calendar.get_intp_coefficient(jd, mcd.jdmlist)
    print((mcd.filelist[i], "-", mcd.filelist[j]))
    print("alpha=,",alpha)
    print("1-alpha=,",1-alpha)

    fiso0 = read_hdf_MCD.read_MCD(mcd.filelist[i], parameter1)
    fvol0 = read_hdf_MCD.read_MCD(mcd.filelist[i], parameter2)
    fgeo0 = read_hdf_MCD.read_MCD(mcd.filelist[i], parameter3)

    print("sum (fiso0)=,",np.nansum(fiso0))

    fiso1 = read_hdf_MCD.read_MCD(mcd.filelist[j], parameter1)
    fvol1 = read_hdf_MCD.read_MCD(mcd.filelist[j], parameter2)
    fgeo1 = read_hdf_MCD.read_MCD(mcd.filelist[j], parameter3)

    print("sum (fiso1)=, ",np.nansum(fiso1))

    fiso = (1-alpha)*fiso0+alpha*fiso1
    fvol = (1-alpha)*fvol0+alpha*fvol1
    fgeo = (1-alpha)*fgeo0+alpha*fgeo1

    print("sum (fiso)B=, ",np.nansum(fiso))

    # fill by closest value
    defic0 = (fiso0 != fiso0)*(fiso1 == fiso1)
    fiso[defic0] = fiso1[defic0]
    fvol[defic0] = fvol1[defic0]
    fgeo[defic0] = fgeo1[defic0]

    print("sum (fiso)C=, ",np.nansum(fiso))

    defic1 = (fiso0 == fiso0)*(fiso1 != fiso1)
    fiso[defic1] = fiso0[defic1]
    fvol[defic1] = fvol0[defic1]
    fgeo[defic1] = fgeo0[defic1]

    print("sum (fiso)D=, ",np.nansum(fiso))

    # If both are bad pixels, use mean value
    deficit = (mcd.ldmask == True)*(fiso != fiso)
    fiso[deficit] = mcd.fiso_mean[deficit]
    fvol[deficit] = mcd.fvol_mean[deficit]
    fgeo[deficit] = mcd.fgeo_mean[deficit]

    print("sum (fiso)E=, ",np.nansum(fiso))

    return fiso, fvol, fgeo


def get_BRDF(filelist, jdmlist, mask, fiso_mean, fvol_mean, fgeo_mean, jdin, ispec, inc, zeta=0.4084, Thetaeq=0.0, nlat=3600, nlon=7200):

    parameter1 = "BRDF_Albedo_Parameter1_Band"+str(ispec)
    parameter2 = "BRDF_Albedo_Parameter2_Band"+str(ispec)
    parameter3 = "BRDF_Albedo_Parameter3_Band"+str(ispec)

    # set spherical coordinate on a planet
    theta, phi = geometry.setsphere(nlat, nlon)
    theta = theta.flatten()
    phi = phi.flatten()

    eO = geometry.uniteO(inc, Thetaeq)

    iprev = len(jdmlist)
    for jd in jdin:

        Thetav, Phiv = blue_calendar.get_orbital_phase(jd)
        eS = geometry.uniteS(Thetaeq, Thetav)
        eR = geometry.uniteR(zeta, Phiv, theta, phi)

        i, j, alpha = blue_calendar.get_intp_coefficient(jd, jdmlist)

        if i != iprev:
            print(("READ NEW HDF FILES: ", i, "-", j))
            fiso0 = read_hdf_MCD.read_MCD(filelist[i], parameter1)
            fvol0 = read_hdf_MCD.read_MCD(filelist[i], parameter2)
            fgeo0 = read_hdf_MCD.read_MCD(filelist[i], parameter3)

            fiso1 = read_hdf_MCD.read_MCD(filelist[j], parameter1)
            fvol1 = read_hdf_MCD.read_MCD(filelist[j], parameter2)
            fgeo1 = read_hdf_MCD.read_MCD(filelist[j], parameter3)

        iprev = i

        fiso = (1-alpha)*fiso0+alpha*fiso1
        fvol = (1-alpha)*fvol0+alpha*fvol1
        fgeo = (1-alpha)*fgeo0+alpha*fgeo1

        # fill by closest value
        defic0 = (fiso0 != fiso0)*(fiso1 == fiso1)
        fiso[defic0] = fiso1[defic0]
        fvol[defic0] = fvol1[defic0]
        fgeo[defic0] = fgeo1[defic0]

        defic1 = (fiso0 == fiso0)*(fiso1 != fiso1)
        fiso[defic1] = fiso0[defic1]
        fvol[defic1] = fvol0[defic1]
        fgeo[defic1] = fgeo0[defic1]

        # If both are bad pixels, use mean value
        deficit = (mask == True)*(fiso != fiso)
        fiso[deficit] = fiso_mean[deficit]
        fvol[deficit] = fvol_mean[deficit]
        fgeo[deficit] = fgeo_mean[deficit]

        # flatten
        fiso = fiso.flatten()
        fgeo = fgeo.flatten()
        fvol = fvol.flatten()

#        ref=rossli.refRL(fiso,fgeo,fvol,eS,eR,eO)
if __name__ == "__main__":
    print("test")
