program extract_gpc
  !
  ! This program dumps some variables of GPC files into an ascii file
  !
  implicit none
  character argv*100
  INTEGER*4 i, iargc, n
  INTEGER :: LUNANC, IRC
  INTEGER, PARAMETER :: MAXBOX = 6596
  real, dimension(0:MAXBOX-1) :: clong,clati, cth, meantc, meantau,meanpc,ctp
  integer, dimension(0:MAXBOX-1) :: ntot, ncloud, surfaceclass

  n = iargc()
  !------------------------
  !read ANC data
  LUNANC = 9                                                        
  CALL RDANC(LUNANC,IRC,"/Users/kawahara/sotica/bluedot/ANC.GPC")
  !-------------------------

  do i = 1, n
     call getarg( i, argv )
     print *, i, argv, trim(argv)//".txt"
     call wrap_isccpd1_outtxt(trim(argv),trim(argv)//".txt")
  end do

end program extract_gpc
