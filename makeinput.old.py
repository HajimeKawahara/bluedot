def set_line(uvinput,com,val=None):
    if val == None:
        uvinput=uvinput+com+"\n"
    else:
        uvinput=uvinput+com+str(val)+"\n"
    return uvinput

def setip_default(default_uvinput):
    uvinput="# default uvinput file = "+default_uvinput+"\n"
    f = open(default_uvinput)
    uvinput = f.read()
    f.close()
    uvinput=uvinput+"\n"
    return uvinput

def setip_angles(uvinput,sza,vza,aza):
# uvinput angle: sza,vza,aza in radian
#------------------------------------
# sza: # Solar zenith angle in degree, from file
# phi: #Azimuth output angles (in degrees) in increasing order.
# umu: #Cosine of output polar angles in increasing order, starting with negative (down- welling radiance, looking upward) values (if any) and on through positive (upwelling radiance, looking downward) values. Must not be zero.
#------------------------------------
    uvinput=set_line(uvinput,"# angles")
    uvinput=set_line(uvinput,"sza   ",sza*180.0/np.pi)
    uvinput=set_line(uvinput,"phi   ",aza*180.0/np.pi)
    uvinput=set_line(uvinput,"umu   ",np.cos(vza))
    return uvinput

def setip_rossli(uvinput,fiso,fvol,fgeo):
# BRDF data for DISORT 3 test
    uvinput=set_line(uvinput,"# Ross-Li model BRDF parameters")
    uvinput=set_line(uvinput,"brdf_ambrals iso   ",fiso)
    uvinput=set_line(uvinput,"brdf_ambrals vol   ",fvol)
    uvinput=set_line(uvinput,"brdf_ambrals geo   ",fgeo)
    uvinput=set_line(uvinput,"brdf_ambrals_hotspot")
    return uvinput

def setip_ocean(uvinput,uvel=10.0):
    uvinput=set_line(uvinput,"brdf_cam u10 "+str(uvel))
    return uvinput

def setip_const_albedo(uvinput, albedoin=0.0):
    if albedoin > 1.0:
        albedoin=1.0        
    elif albedoin < 0.0:
        albedoin=0.0
    uvinput=set_line(uvinput,"albedo "+str(albedoin))
    return uvinput

