import pylab
import matplotlib.pyplot as plt
import healpy as hp
import numpy as np
import sys
import argparse
from bluedotclass import PlanetData
from pathlib import Path

def plotall(fisox, fvolx, fgeox, landfx, fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask, cmap=plt.cm.jet):

    p=Path("png")
    p.mkdir(parents=False, exist_ok=True)

    hp.mollview(fisox, title="fisox", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/fisox.png")

    hp.mollview(fvolx, title="fvolx", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/fvolx.png")

    hp.mollview(fgeox, title="fgeox", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/fgeox.png")
    
    hp.mollview(landfx, title="landfx", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/landfx.png")

    hp.mollview(fcl, title="fcl", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/fcl.png")
    
    hp.mollview(meantauxd, title="meantauxd", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/meantauxd.png")

    #(fisox, fvolx, fgeox, landfx, fcl, meantauxd, cthx, meanwpxd,iselmapt,iselmapw, vimask

    hp.mollview(cthx, title="cthx (cloud top height)", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/cthx.png")

    mask=(meanwpxd<=0.0)
    meanwpxd[mask]=None
    hp.mollview(meanwpxd, title="meanwpxd (water path)", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/meanwpxd.png")

    hp.mollview(np.log10(meanwpxd/1.e3), title="meanwcxd (water content in 1km)", flip="geo", cmap=cmap,min=-3,max=1)
    hp.graticule(color="orange")
    plt.savefig("png/meanwcxd.png")


    hp.mollview(iselmapt, title="iselmapt", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/iselmapt.png")

    hp.mollview(iselmapw, title="iselmapw", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/iselmapw.png")


    hp.mollview(np.array(vimask,dtype=np.float), title="vimask", flip="geo", cmap=cmap)
    hp.graticule(color="orange")
    plt.savefig("png/vimask.png")


def plotsnapshot(radfile):
    newd = np.load(radfile)
    npix=hp.nside2npix(16)
    tradcs=np.zeros(npix)
    tradcl=np.zeros(npix)
    fcl=np.zeros(npix)

    arripix=np.array(newd["arr_0"])
    ereo=np.array(newd["arr_1"])
    arr5=np.array(newd["arr_4"])
    arr6=np.array(newd["arr_5"])
    arr7=np.array(newd["arr_6"])
    print(np.shape(fcl))

    for i in range(0,len(arripix)):
        ipix=arripix[i]
        tradcl[ipix]=np.sum(arr5[i])*ereo[i]
        tradcs[ipix]=np.sum(arr6[i])*ereo[i]
        fcl[ipix]=np.sum(arr7[i])
    

    hp.mollview(tradcl*fcl+tradcs*(1.0-fcl), title="simple sum rad (post)", flip="geo", cmap=plt.cm.pink, min=0.0,max=30000)
#    hp.orthview(trad, title="simple sum rad", flip="geo", cmap=plt.cm.jet, min=0.0)
    hp.graticule(color="orange")

    hp.mollview(tradcs*(1.0-fcl), title="simple sum rad (clear sky)", flip="geo", cmap=plt.cm.pink, min=0.0,max=30000)
#    hp.orthview(trad, title="simple sum rad", flip="geo", cmap=plt.cm.jet, min=0.0)
    hp.graticule(color="orange")

    hp.mollview(tradcs, title="simple sum rad (clear sky 100%)", flip="geo", cmap=plt.cm.pink, min=0.0,max=30000)
#    hp.orthview(trad, title="simple sum rad", flip="geo", cmap=plt.cm.jet, min=0.0)
    hp.graticule(color="orange")

    hp.mollview(tradcl*fcl, title="simple sum rad (cloud)", flip="geo", cmap=plt.cm.pink, min=0.0)
#    hp.orthview(trad, title="simple sum rad", flip="geo", cmap=plt.cm.jet, min=0.0)
    hp.graticule(color="orange")


#    hp.mollview(tradcl, title="simple sum rad (cloud sky)", flip="geo", cmap=plt.cm.pink, min=0.0)
#    hp.graticule(color="orange")
#    hp.mollview(tradcs, title="simple sum rad (clear sky)", flip="geo", cmap=plt.cm.pink, min=0.0)
#    hp.graticule(color="orange")

    hp.mollview(fcl, title="cloud fraction", flip="geo", cmap=plt.cm.pink, min=0.0)
    hp.graticule(color="orange")


    plt.show()

if __name__ == "__main__":
    from makemovie import PlanetMovie
    import makemovie as mm

    parser = argparse.ArgumentParser(description='generating a snapshot.')
    parser.add_argument('-f',default=["test.pickle"],nargs=1, help='pickle file', type=str)
    parser.add_argument('-i',default=[1],nargs=1, help='PM ID.', type=int)
    args = parser.parse_args()
    pfile=args.f[0]

    pmov=mm.loadpmov(pfile)
    pmov.setPMid(args.i[0])
    plotsnapshot(pmov.inpdir+"/rads.npz")

