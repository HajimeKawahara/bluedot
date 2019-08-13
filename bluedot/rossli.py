#!/usr/bin/python
import numpy as np


def compbrdf(fiso, fgeo, fvol, eS, eR, eO):

    Kvol, Kgeo, weight, mask = getKvolKgeo(eS, eR, eO)
    brdf = fiso + fvol*Kvol + fgeo*Kgeo
#    brdf = fvol*Kvol
    brdf[~mask] = None
    return brdf, Kvol, Kgeo, weight


def getKvol(eS, eR, eO):
    # eS, eO: 3d vector
    # eR: npix x 3d vector
    cosxi = np.inner(eS, eO)
    sinxi = np.sqrt(1.0-cosxi*cosxi)
    xi = np.arccos(cosxi)

    fac1 = (np.pi/2 - xi)*cosxi + sinxi

    cossza = np.dot(eR, eS)
    cosvza = np.dot(eR, eO)

    fac2 = cossza + cosvza
    coeff = fac1/fac2 - np.pi/4.0
 #   mask=(cossza>0.0)*(cosvza>0.0)
 #   coeff[~mask]=0.0

    return coeff


def getKvolKgeo(eS, eR, eO):
    #Kvol & Kgeo
    # eS, eO: 3d vector
    # eR: npix x 3d vector
    # sza: solar zenith angle, vza: view zenith angle, aza: azimath angle
    cosxi = np.inner(eS, eO)
    sinxi = np.sqrt(1.0-cosxi*cosxi)
    xi = np.arccos(cosxi)
    fac1 = (np.pi/2 - xi)*cosxi + sinxi

    cossza = np.dot(eR, eS)
    cosvza = np.dot(eR, eO)

    fac2 = cossza + cosvza

    #Kvol=4.0/(3.0*np.pi)*fac1/fac2 - 1.0/3.0
    Kvol = fac1/fac2 - np.pi/4.0

    # Kgeo assuming b/r=1
    secsza = 1.0/cossza
    secvza = 1.0/cosvza

    tansza2 = secsza*secsza - 1.0
    tanvza2 = secvza*secvza - 1.0

    cosaza = cosxi-cossza*cosvza
    sinaza2 = 1.0 - cosaza*cosaza  # > 0
    d2 = tansza2+tanvza2 - 2.0*np.sqrt(tansza2*tanvza2)*cosaza  # D^2 (42)
    hob = 2  # h/b
    cost = hob*np.sqrt(d2+tansza2*tanvza2*sinaza2)/(secsza+secvza)
    costmask = (cost <= 1.0)*(cost >= -1.0)
    sint = np.sqrt(1.0-cost*cost)
    t = np.arccos(cost)
    Ofunc = (t - sint*cost)*(secsza+secvza)/np.pi  # overlap function
    Ofunc[~costmask] = 0.0
    Kgeo = Ofunc-secsza-secvza+0.5*(1.0+cosxi)*secsza*secvza
    mask = (cossza > 0.0)*(cosvza > 0.0)
    Kvol[~mask] = None
    Kgeo[~mask] = None

    weight = cossza*cosvza  # weight function
    weight[~mask] = None

    return Kvol, Kgeo, weight, mask


if __name__ == "__main__":
    print("test")
