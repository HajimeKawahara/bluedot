# bluedot

Blue-dot (disk-integrated Earth) simulator. 

## Requirements for Installation

- Python 3
- pyhdf or python-hdf4 (for instance, conda install -c conda-forge pyhdf)
- healpy
- libradtran 2 (also netcdf4)

Add your_install_directory/bluedot to your PYTHONPATH.

### Some tips for install


For installing libradtran 2.0.2, first you need to install netcdf4 (I needed to put -fPIC option in CFLAGS and CPPFLAGS in Makefile). Also

```
sudo mkdir /usr/local/share/libRadtran/data/ic/yang2013
```
and make a soft link of libRadtran2.0.2/data to the directory upper to the working directory.

Remove ".sol" in ic/yang2013/Makefile
```
DATAFILE = $(wildcarf *.sol.cdf)
```
Also, libradtran2 uses python 2.7 but bluedot uses python 3. So, when installing, I switch to py27 using conda,

```
conda create -n py27 python=2.7 anaconda
source activate py27
```
Then, configure, make, make install in libRadt


### Data 

- ISCCP (cloud data)
- MODIS (albedo)

Download bluedot.data.tar.gz from http://secondearths.sakura.ne.jp/bluedot/bluedot.data.tar.gz
Untar the file and put directory as bluedot/earth.

Download bluedot.data.tar.gz from http://secondearths.sakura.ne.jp/bluedot/librad.data.tar
Untar the file and put directory as bluedot/data.

### Making wrapgpc.so

- read_isccp.py is the python binding for IO of ISCCP/GPC files. To use it, compile fortran (90) files as
In bluedot/bluedot directory, execute

````
make
````
Then, you'll find wrapgpc.so.

## Samples

In bluedot/bluedot directory, you can try these ones.

- Generate a pickle file (setting file) for PlanetMovie

````
python makemovie.py -p 
````

- Make a snapshot

````
python makemovie.py -f test.pickle -i 1
````

- Plot a snapshot

````
python plotgeo.py -i 1
````

- Emulate (for debugging)

````
 python ../makeexe.py -f emulate.pickle -i 1 30 -n 1 -e
````

