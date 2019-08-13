!program wrap

subroutine set_isccpanc(ANCFILE)
  CHARACTER(len=*) :: ANCFILE
  INTEGER :: LUNANC, IRC
  LUNANC = 9           
  write(*,*) ANCFILE, " (wrap_isccp.f90)"

  !CALL RDANC(LUNANC,IRC,"/home/kawahara/sotica/bluedot/ANC.GPC")                                        
  write(*,*) trim(adjustl(ANCFILE))
  CALL RDANC(LUNANC,IRC,trim(adjustl(ANCFILE)))
  IF ( IRC .NE. 0 )THEN
     WRITE(*,*) "FATAL: NO ANCILLARY DATA: PREPARE ANC.GPC."
  ENDIF
end subroutine set_isccpanc

subroutine read_isccpd1(clong,clati, galt, cth, meantc, meantau, meanwp, meanpc,ctp,ntot, ncloud, surfaceclass,datearr,GPCFILE)
  !implicit none
  INTEGER, PARAMETER :: MAXVAR = 202  
  INTEGER, PARAMETER :: MAXLON = 144 
  INTEGER, PARAMETER :: MAXLAT = 72
  INTEGER, PARAMETER :: MAXBOX = 6596
  INTEGER, PARAMETER :: IUNDEF = 255
  REAL, PARAMETER :: RUNDEF = -1000.0 
  COMMON /D1HEAD/ LUND1,IREC,IFILE,IYEAR,MONTH,IDAY,IUTC,LATBEG,LATEND,LONBEG,LONEND,IBXBEG,IBXEND                   
  COMMON /D1DATA/ LAT,NLON,IVAR(MAXVAR,MAXLON),RVAR(MAXVAR,MAXLON)  
  COMMON /D1GRID/ NCELLS(MAXLAT),ICELLS(MAXLAT)                     
  INTEGER, PARAMETER :: MAXCNT = 255 
  COMMON/CNTTAB/TMPTAB(0:MAXCNT),TMPVAR(0:MAXCNT),PRETAB(0:MAXCNT), &
       &RFLTAB(0:MAXCNT),TAUTAB(0:MAXCNT),PRWTAB(0:MAXCNT), OZNTAB(0:MAXCNT) 
  REAL :: EQMAP(MAXBOX)                                              
  REAL :: SQMAP(MAXLON,MAXLAT)                                       
  CHARACTER*7 :: STARS='-(*_*)-'
  integer :: CHECK, outtxti

  !------------
  character(len=*), intent(in) :: GPCFILE
  !  integer :: ntot, ncloud, surfaceclass
  !  real :: clong, clati, cth, meantc, meantau, meanpc,ctp
  real, dimension(0:MAXBOX-1), intent(inout) :: clong,clati, cth, meantc, meantau,meanpc,ctp, galt, meanwp
  integer, dimension(0:MAXBOX-1), intent(inout) :: ntot, ncloud, surfaceclass
  integer, dimension(4), intent(inout) :: datearr

  real :: clongt,clatit, ctht, meantct, meantaut,meanpct,ctpt, galtt, meanwpt
  integer :: ntott, ncloudt, surfaceclasst

  !  GPCFILE = "TEST_D1.GPC"


  !  LUNANC = 9                                                        
  !  CALL RDANC(LUNANC,IRC)                                            
  !  IF ( IRC .NE. 0 )THEN
  !     WRITE(*,*) "FATAL: NO ANCILLARY DATA: PREPARE ANC.GPC."
  !     GOTO 900                                        
  !  ENDIF

  DO I=1,MAXBOX
     EQMAP(I) = -1000.0
  ENDDO
  LUND1 = 10                                                        
  !-----------------------------
  write(*,*) "READ GPC:="//trim(adjustl(GPCFILE))
  !  write(*,*) "lon lat surface_class ntot ncloud cloud_top_pressure[mb] cloud_top_height[m] meanpc meantc meantau"
  !  write(*,*) "0 0 6 11 12 0 0 78 85 92"
  CALL D1OPEN(IRC, GPCFILE)                                                  

  IF ( IRC .NE. 0 ) GOTO 910                                        
  IBOX = 0                                                          
  IIBOX=0
  IFULL = 0  

  DO LAT=1,MAXLAT
     CALL D1READ(IRC)                                               
     IF ( IRC .NE. 0 ) THEN                                         
        GOTO 800                                                    
     END IF
     CALL D1PHYS                                                    
     DO LON=1,NLON
        IBOX = IBOX + 1
        IIBOX=IBOX-1
        IF ( IVAR(6,LON) .EQ. 255 ) GOTO 400                           
        IFULL = IFULL + 1
        CALL CLDHGT(LON, ctpt, ctht, galtt)           
        ctp(IIBOX)=ctpt 
        cth(IIBOX)=ctht
        galt(IIBOX)=galtt
        CALL CENTER(LON, clong(IIBOX), clati(IIBOX))     
        meanpc(IIBOX) = RVAR(78,LON)
        meantc(IIBOX) = RVAR(85,LON)
        meantau(IIBOX) = RVAR(92,LON)
        meanwp(IIBOX) = RVAR(99,LON)

        surfaceclass(IIBOX)=IVAR(6,LON)
        ntot(IIBOX)=IVAR(11,LON)
        ncloud(IIBOX)=IVAR(12,LON)
        !        CALL EXTRACTRVAR(LON, meanpc, meantc, meantau)
        !integer surfaceclass,meanpc,ctp
        !        write(*,*) clong,clati,surfaceclass,ntot,ncloud,int(ctp),cth,int(meanpc), meantc, meantau
        EQMAP(IBOX) = RVAR(12,LON)                                     
400  ENDDO
500 ENDDO
  !date
  datearr(1)=2000+IYEAR
  datearr(2)=MONTH
  datearr(3)=IDAY
  datearr(4)=IUTC

800 CONTINUE                                                          
900 CONTINUE                                                          
  !  PRINT *,'ERROR:  RDANC  RC=',IRC                                  
  !  STOP 999                                                          
910 CONTINUE                                                          
  !  PRINT *,'ERROR:  D1OPEN RC=',IRC                                  
  !  STOP 999                                                          
920 CONTINUE                                                          
  !  PRINT *,'ERROR:  D1READ RC=',IRC                                  
  !  STOP 999                                                          


END SUBROUTINE read_isccpd1

subroutine wrap_isccpd1_outtxt(GPCFILE,OUTFILE)
  !implicit none
  INTEGER, PARAMETER :: MAXVAR = 202  
  INTEGER, PARAMETER :: MAXLON = 144 
  INTEGER, PARAMETER :: MAXLAT = 72
  INTEGER, PARAMETER :: MAXBOX = 6596
  INTEGER, PARAMETER :: IUNDEF = 255
  REAL, PARAMETER :: RUNDEF = -1000.0 
  COMMON /D1HEAD/ LUND1,IREC,IFILE,IYEAR,MONTH,IDAY,IUTC,LATBEG,LATEND,LONBEG,LONEND,IBXBEG,IBXEND                   
  COMMON /D1DATA/ LAT,NLON,IVAR(MAXVAR,MAXLON),RVAR(MAXVAR,MAXLON)  
  COMMON /D1GRID/ NCELLS(MAXLAT),ICELLS(MAXLAT)                     
  INTEGER, PARAMETER :: MAXCNT = 255 
  COMMON/CNTTAB/TMPTAB(0:MAXCNT),TMPVAR(0:MAXCNT),PRETAB(0:MAXCNT), &
       &RFLTAB(0:MAXCNT),TAUTAB(0:MAXCNT),PRWTAB(0:MAXCNT), OZNTAB(0:MAXCNT) 
  REAL :: EQMAP(MAXBOX)                                              
  REAL :: SQMAP(MAXLON,MAXLAT)                                       
  CHARACTER*7 :: STARS='-(*_*)-'
  integer :: CHECK, outtxti
  character(len=*), intent(in) :: GPCFILE, OUTFILE
  real :: clong, clati
  real :: cth, meantc, meantau
  real :: meanpc,ctp, galt
  integer :: ntot, ncloud, surfaceclass
  !GPCFILE = "test.GPC"

  LUNANC = 9                                                        
!  CALL RDANC(LUNANC,IRC,"ANC.GPC")                                            
!  IF ( IRC .NE. 0 ) GOTO 900                                        
!  write(*,*) '---'

  DO I=1,MAXBOX
     EQMAP(I) = -1000.0
  ENDDO
 
  LUND1 = 10                                                        
  !-----------------------------
  outtxti=345
  open(outtxti, file=OUTFILE, form="formatted",status="replace")  
  write(outtxti,*) "#Created by wrap_isccpd1.f90" 
  write(outtxti,*) "#original GPC="//trim(adjustl(GPCFILE))
  write(outtxti,*) "#lon lat surface_class ntot ncloud cloud_top_pressure[mb] cloud_top_height[m] meanpc meantc meantau"
  write(outtxti,*) "#0 0 6 11 12 0 0 78 85 92"
  CALL D1OPEN(IRC, GPCFILE)                                                  
  IF ( IRC .NE. 0 ) GOTO 910                                        
  IBOX = 0                                                          
  IFULL = 0                                                         
  DO LAT=1,MAXLAT
     CALL D1READ(IRC)                                               
     IF ( IRC .NE. 0 ) THEN                                         
        GOTO 800                                                    
     END IF
     CALL D1PHYS                                                    
     DO LON=1,NLON
        IBOX = IBOX + 1
        IF ( IVAR(6,LON) .EQ. 255 ) GOTO 400                           
        IFULL = IFULL + 1                                              
        CALL CLDHGT(LON, ctp, cth, galt)           
        CALL CENTER(LON, clong, clati)     
        meanpc = RVAR(78,LON)
        meantc = RVAR(85,LON)
        meantau = RVAR(92,LON)
        surfaceclass=IVAR(6,LON)
        ntot=IVAR(11,LON)
        ncloud=IVAR(12,LON)
        !        CALL EXTRACTRVAR(LON, meanpc, meantc, meantau)
        !integer surfaceclass,meanpc,ctp
        write(outtxti,*) clong,clati,surfaceclass,ntot,ncloud,int(ctp),cth,int(meanpc), meantc, meantau
        CHECK=0
        IF (CHECK==1) THEN
           PRINT *,"------"
           PRINT *, "lon/lat indices (1,2)=",LON,LAT                                     
           PRINT *, "longitude/latitude in the center of the pixel",clong, clati
           PRINT *, "Day/night/land/water/coast code (6)",IVAR(6,LON)
           PRINT *, "TOTAL NUMBER OF PIXELS (11)",IVAR(11,LON)
           PRINT *, "Number of cloudy pixels (12)",IVAR(12,LON)
           PRINT *, "Cloud top pressure (mb)",ctp
           PRINT *, "CLOUD TOP HEIGHT (m)",cth
        ENDIF
        EQMAP(IBOX) = RVAR(12,LON)                                     
400  ENDDO
500 ENDDO
  close(outtxti)
800 CONTINUE                                                          
900 CONTINUE                                                          
  !  PRINT *,'ERROR:  RDANC  RC=',IRC                                  
  !  STOP 999                                                          
910 CONTINUE                                                          
  !  PRINT *,'ERROR:  D1OPEN RC=',IRC                                  
  !  STOP 999                                                          
920 CONTINUE                                                          
  !  PRINT *,'ERROR:  D1READ RC=',IRC                                  
  !  STOP 999                                                          

END SUBROUTINE wrap_isccpd1_outtxt


subroutine test(a,b)
  implicit none
  integer :: a, b
  b=a*a
end subroutine test

subroutine testchar(a,b,s)
  implicit none
  character(len=*), intent(in) :: s ! s should be placed at the end
  real, dimension(10), intent(inout) :: a 
  integer, dimension(10), intent(inout) :: b

  write(*,*) s, "from testchar in wrap_isccd1.f90"
  a(1)=a(1)+1.0
  b(4)=b(4)+16
  write(*,*) b

end subroutine testchar

