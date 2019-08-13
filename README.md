# bluedot

Blue-dot (disk-integrated Earth) simulator. 

## Requirements for Installation

- Python 3
- python-hdf4
- healpy
- libradtran 2

###

- read_isccp.py is the python binding for IO of ISCCP/GPC files. To use it, compile fortran (90) files as

````
make
````

-Generating a pickle file


-Generating executables


-Emulating (for debugging)

 python ../makeexe.py -f emulate.pickle -i 1 30 -n 1 -e
   


###

makeexe - makemovie - snapshot - generate_globe - brdf_modis - blue_calendar 



BRDF 

fisox 
<- set_gsurface_brdf (generate_globe) 
<- brdf_modis.get_BRDF_parameters (brdf_modis)
<- get_intp_coefficient (blue_calendar)