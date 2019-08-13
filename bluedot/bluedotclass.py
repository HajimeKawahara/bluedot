import healpy as hp
import numpy as np
from astropy.time import Time

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

class PlanetData:
    
    def __init__(self):
        self.mcdpath = "/home/kawahara/bluedot/earth/MODIS/MCD43C1/MCD43C1*.hdf"
        self.wrappath = "/home/kawahara/bluedot/bluedot/wrapgpc.so"
        self.d1path = "/home/kawahara/bluedot/earth/ISCCP/d1"
        self.default_input = "/home/kawahara/bluedot/bluedot/input/template.INP"

    def modismeanpath(self,pcol):
        return "/home/kawahara/bluedot/earth/mean2008/mean2008_"+str(pcol.ispec)+".npz"

class PlanetGeometry:
    
    def __init__(self):        

        self._sd=0.99726958 #siderial day
        self._sy=365.25636302 #siderial year        

        timeveq="2008-3-20 05:48"
        ttime = Time(timeveq, format='iso', scale='utc')

        self._jd0 = ttime.jd  # vernal equinox in 2008 phi=0
        self._jd = self._jd0
        self._inc=60/180.0*np.pi
        self._Thetaeq=0.0/180.0*np.pi
        self._zeta=23.4/180.0*np.pi
        self._nside=16
        self._npix=hp.nside2npix(self._nside)
        self._ipix=0
        #self.phioffset=1.65588 # for JAPAN
        #self.phioffset=0.0 #
        self.update()

    #UPDATE
    def update(self):
        self.clockupdate()
        self.geoupdate()
        self.pixupdate()
        
    def clockupdate(self):
        self._Thetav = np.mod((self._jd-self._jd0), self._sy)/self._sy*2*np.pi
        self._Phiv = np.mod((self._jd-self._jd0), self._sd)*2*np.pi

    def geoupdate(self):
        self._eO=uniteO(self._inc,self._Thetaeq)
        self._eS=uniteS(self._Thetaeq,self._Thetav)

    def npixupdate(self):
        self._npix=hp.nside2npix(self._nside)
        
    def pixupdate(self):
        self._thetax, self._phix = hp.pix2ang(self._nside, self._ipix)
        self._eR=uniteR(self._zeta, self._Phiv, self._thetax, self._phix)

        uRS = np.dot(self._eR, self._eS)[0]
        uRO = np.dot(self._eR, self._eO)[0]
        uOS = np.dot(self._eO, self._eS)
        if uRS > 0.0 and uRO > 0.0:
            self.VI = True
        else:
            self.VI = False
        self.sza = np.arccos(uRS)
        self.vza = np.arccos(uRO)
        self.aza = np.arccos(uOS-uRS*uRO)

        
    @property
    def jd(self):
        return self._jd

    @jd.setter
    def jd(self, jd):
        self._jd = jd
        self.update()

    @property
    def jd0(self):
        return self._jd0

    @jd0.setter
    def jd0(self, jd0):
        self._jd0 = jd0
        self.update()

    @property
    def sd(self):
        return self._sd

    @sd.setter
    def sd(self, sd):
        self._sd = sd
        self.update()

    @property
    def sy(self):
        return self._sy

    @sy.setter
    def sy(self, sy):
        self._sy = sy
        self.update()

    ##### PIXEL ######
    @property
    def nside(self):
        return self._nside

    @nside.setter
    def nside(self, nside):
        self._nside = nside
        self.npixupdate()  
        self.pixupdate()
        
    @property
    def npix(self):
        return self._npix

    @npix.setter
    def npix(self, npix):
        raise ValueError() #cannot directly change Thetav

    @property
    def ipix(self):
        return self._ipix

    @ipix.setter
    def ipix(self, ipix):
        if ipix >=0 and ipix < self._npix:
            self._ipix = ipix
            self.pixupdate()
        else:
            print("ipix: out of range.")
            raise ValueError()

        
    @property
    def thetax(self):
        return self._thetax

    @thetax.setter
    def thetax(self, thetax):
        raise ValueError() #cannot directly change Thetav

    @property
    def phix(self):
        return self._phix

    @phix.setter
    def phix(self, phix):
        raise ValueError() #cannot directly change Thetav
        
    ##### GEOMETRY ######
    @property
    def inc(self):
        return self._inc

    @inc.setter
    def inc(self, inc):
        self._inc = inc
        self.geoupdate()
        self.pixupdate()

    @property
    def Thetaeq(self):
        return self._Thetaeq

    @Thetaeq.setter
    def Thetaeq(self, Thetaeq):
        self._Thetaeq = Thetaeq
        self.geoupdate()
        self.pixupdate()

    @property
    def zeta(self):
        return self._zeta

    @zeta.setter
    def zeta(self, zeta):
        self._zeta = zeta
        self.pixupdate()

    @property
    def eO(self):
        return self._eO

    @eO.setter
    def eO(self, eO):
        raise ValueError() #cannot directly change Thetav
    
    @property
    def eS(self):
        return self._eS

    @eS.setter
    def eS(self, eS):
        raise ValueError() #cannot directly change Thetav

    @property
    def eR(self):
        return self._eR

    @eR.setter
    def eR(self, eR):
        raise ValueError() #cannot directly change Thetav

    @property
    def Phiv(self):
        return self._Phiv

    @Phiv.setter
    def Phiv(self, Phiv):
        raise ValueError() #cannot directly change Phiv

    @property
    def Thetav(self):
        return self._Thetav

    @Thetav.setter
    def Thetav(self, Thetav):
        raise ValueError() #cannot directly change Thetav


class PlanetColor:
    def __init__(self,ispec):        
        # MODIS spectral band
        self._ispec=ispec
        self.modiswav=[[620.,670.],[841.,876.],[459.,479.],[545.,565.],[1230.,1250.],[1628.,1652.],[2105.,2155.]]
        self.wavwidth=5.0 #[nm]
        self.wavupdate()
        
    def makegrid(self):
        self.wavegrid=np.arange(self.lower,self.upper,self.wavwidth) #libradtran wavelength_grid

    def wavupdate(self):
        self.lower=self.modiswav[self.ispec-1][0]
        self.upper=self.modiswav[self.ispec-1][1]
        self.makegrid()
        print("ispec=",self.ispec)
        print("wavelength=",self.lower,"-",self.upper,"[nm]")
        print("width for wavegrid=",self.wavwidth,"[nm]")
        print("Using MODIS band range (you can update them manually). ")
        
    @property
    def ispec(self):
        return self._ispec

    @ispec.setter
    def ispec(self, ispec):
        self._ispec = ispec
        self.wavupdate()

        
if __name__ == "__main__":
    pgeo=PlanetGeometry()
    print(pgeo.jd0)
