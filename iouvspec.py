#!/usr/bin/python
import sys
import argparse
import subprocess
from subprocess import Popen, PIPE
import time
import numpy as np


def uvspec_form1(inputfile):
    # output: lamb (wavelength), rad (uu(umu(0),phi(0)) in libradtran (see p26)
    # mW/(m 2 nm sr) for solar_flux
    p = Popen(["uvspec", "-i", inputfile], stdout=PIPE)
    output = p.communicate()[0]
    p.stdout.close()
    output = str(output).replace("b'", "").split("\\n")
    if output[0] == "":
        print("uvspec error.")
        print(("Check by [uvspec < "+inputfile+"]"))

    a = np.core.defchararray.split(output[0::3][0:-1])
    b = np.core.defchararray.split(output[2::3][0:])
    
    lamb = []
    for line in a:
        lamb.append(float(line[0]))
    rad = []
    ex = 0
    for line in b:
        try:
            rad.append(float(line[-1]))
        except:
            ex = ex+1

    lamb = np.array(lamb)
    rad = np.array(rad)

    return lamb, rad


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='iouvspec')
    parser.add_argument('-i', nargs=1, default=["test_brdf.INP"], type=str)
    args = parser.parse_args()

    start = time.time()
    inputfile = args.i[0]
    lamb, rad = uvspec_form1(inputfile)

#    np.savez("clear_sky.npz", [lamb, rad])

    # ------------------------------------
    import pylab
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(lamb, rad,".")
    ax.plot(lamb, rad)
    plt.xlabel("wavelength [nm]")
    plt.ylabel("Radiance")
    plt.show()

    elapsed_time = time.time() - start
    print((("CPU elapsed_time:{0}".format(elapsed_time)) + "[sec]"))
