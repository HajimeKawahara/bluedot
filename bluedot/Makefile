FC=/usr/bin/gfortran

FFLAGS=-O3 
ISCCP=D1module.o wrap_isccpd1.o extractgpc.o 

all: extractgpc wrapgpc

extractgpc: $(ISCCP) 
	$(FC) $(FFLAGS) -o extractgpc $(ISCCP) 

wrapgpc:
	$(FC) $(FFLAGS) -shared -fPIC -o wrapgpc.so D1module.F wrap_isccpd1.f90

.f90.so: 
	$(FC) $(FFLAGS) -c $*.F -o $*.o #-I$(LAPACKI)  -I$(HEALPIXINC)#


clean: 
	\rm -rf *.o *.mod *.so
init: 
	\rm -rf *.fits *.gif *.ps *.xbx *.svx

.SUFFIXES:.F .f90 .mod

#.F.o: 
#	$(FC) $(FFLAGS) -c $*.F 

#.f90.o:
#	$(FC) $(FFLAGS) -c $*.f90 

#.mod.o: 
#	$(FC) $(FFLAGS) -c $*.f90 

.F.o: 
	$(FC) $(FFLAGS) -c $*.F -o $*.o #-I$(LAPACKI)  -I$(HEALPIXINC)#

.f90.o:
	$(FC) $(FFLAGS) -c $*.f90 -o $*.o #-I$(LAPACKI)  -I$(HEALPIXINC)

.mod.o: 
	$(FC) $(FFLAGS) -c $*.f90 -o $*.o #-I$(LAPACKI)  -I$(HEALPIXINC)

extractgpc.o : extractgpc.f90 
test.o : test.f90 
wrap_isccpd1.o : wrap_isccpd1.f90 
