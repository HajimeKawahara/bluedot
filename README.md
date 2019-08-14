# bluedot

Blue-dot (disk-integrated Earth) simulator. 

## Requirements for Installation

- Python 3
- pyhdf or python-hdf4 (for instance, conda install -c conda-forge pyhdf)
- healpy
- libradtran 2

Add your_install_directory/bluedot to your PYTHONPATH.

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

