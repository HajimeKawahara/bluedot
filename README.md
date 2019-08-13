# bluedot

Blue-dot (disk-integrated Earth) simulator. 

## Requirements for Installation

- Python 3
- python-hdf4
- healpy
- libradtran 2

### Data source

- ISCCP (cloud data)
- MODIS (albedo)

Download bluedot.data.tar.gz from http://secondearths.sakura.ne.jp/bluedot/bluedot.data.tar.gz
Untar the file and put directory as bluedot/earth.

Download bluedot.data.tar.gz from http://secondearths.sakura.ne.jp/bluedot/librad.data.tar
Untar the file and put directory as bluedot/data.



###

- read_isccp.py is the python binding for IO of ISCCP/GPC files. To use it, compile fortran (90) files as
In bluedot directory, execute

````
make
````
Then, you'll find wrapgpc.so.


- Generate a pickle file (setting file) for PlanetMovie

````
python makemovie.py -p 
````

- Make a snapshot

````
python makemovie.py -f test.pickle -i 1
````

- Emulating (for debugging)

````
 python ../makeexe.py -f emulate.pickle -i 1 30 -n 1 -e
````

