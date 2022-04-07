import numpy as np
import pytest
from climlab_emanuel_convection import emanuel_convection


ND = 20 # number of layers
NL = ND-1 # max number of levels to which convection can penetrate
NCOL = 1 # number of independent columns
# Set up the pressure domain
ps = 1000. #  Surface pressure in hPa
deltap = ps / ND  # pressure interval
PH = np.linspace(ps, 0., ND+1)  # pressure bounds
P = np.linspace(ps-deltap/2., deltap/2., ND)


#  These test data are based on direct single-column tests of the CONVECT43c.f
#  fortran source code. We are just checking to see if we get the right tendencies
T = np.array([[278.0, 273.9, 269.8, 265.7, 261.6, 257.5, 253.4, 249.3, 245.2,
    241.1, 236.9, 232.8, 228.7, 224.6, 220.5, 216.4, 212.3, 214.0, 240., 270.]])
Q = np.array([[3.768E-03, 2.812E-03, 2.078E-03, 1.519E-03, 1.099E-03,
            7.851E-04, 5.542E-04, 3.860E-04, 2.652E-04, 1.794E-04,
            1.183E-04, 7.739E-05, 4.970E-05, 3.127E-05, 1.923E-05,
            1.152E-05, 6.675E-06, 5.000E-06, 5.000E-06, 5.000E-06]])
# Saturation specific humidity for the above T and P, pre-computed using climlab routines
QS = np.array([[5.52343649e-03, 4.34973488e-03, 3.40199572e-03, 2.64202692e-03,
        2.03705026e-03, 1.55910490e-03, 1.18449723e-03, 8.93293406e-04,
        6.68851878e-04, 4.97394383e-04, 3.63951218e-04, 2.67519554e-04,
        1.95988773e-04, 1.43526774e-04, 1.05574353e-04, 7.86583508e-05,
        6.02944587e-05, 1.04896114e-04, 3.13532026e-03, 1.30153225e-01]])
U = np.array([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]])
V = 5. * np.ones_like(U)

#  Set thermodynamic constants to their defaults from Emanuel's code
CPD=1005.7
CPV=1870.0
RV=461.5
RD=287.04
LV0=2.501E6
G=9.8
ROWL=1000.0
# specific heat of liquid water -- artifically small!
#   Kerry Emanuel's notes say this is intentional, do not change this.
CL=2500.0

NTRA = 1
TRA = np.zeros((NCOL,ND,NTRA), order='F')  # tracers ignored
DELT = 60.0*10.
CBMF = 0.
# Input arguments and default values (taken from convect43.f fortran source):
MINORIG = 0 # index of lowest level from which convection may originate (zero means lowest)
ELCRIT = 0.0011 # autoconversion threshold water content (g/g)
TLCRIT = -55.0 # critical temperature below which the auto-conversion threshold is assumed to be zero (the autoconversion threshold varies linearly between 0 C and TLCRIT)
ENTP = 1.5 # coefficient of mixing in the entrainment formulation
SIGD = 0.05 # fractional area covered by unsaturated downdraft
SIGS = 0.12 # fraction of precipitation falling outside of cloud
OMTRAIN = 50.0 # assumed fall speed (Pa/s) of rain
OMTSNOW = 5.5 # assumed fall speed (Pa/s) of snow
COEFFR = 1.0 # coefficient governing the rate of evaporation of rain
COEFFS = 0.8 # coefficient governing the rate of evaporation of snow
CU = 0.7 # coefficient governing convective momentum transport
BETA = 10.0 # coefficient used in downdraft velocity scale calculation
DTMAX = 0.9 # maximum negative temperature perturbation a lifted parcel is allowed to have below its LFC
ALPHA = 0.2 # first parameter that controls the rate of approach to quasi-equilibrium
DAMP = 0.1 # second parameter that controls the rate of approach to quasi-equilibrium (DAMP must be less than 1)
IPBL = 0 # switch to bypass the dry convective adjustment (bypass if IPBL==0)

#  TENDENCIES FROM FORTRAN CODE
FTtarget = np.array([[-1.79012722e-05, -5.30474102e-06, -1.31791678e-05,
        -1.52691407e-06,  2.39796248e-05,  5.00321776e-05,
         5.81085251e-05,  3.53241836e-05,  2.92659212e-05,
         1.72941819e-05, -1.29258611e-05, -1.95583598e-05,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00]])
FQtarget = np.array([[-1.25265799e-07, -1.77207007e-08,  2.25623932e-08,
         1.20605250e-08, -2.24795916e-09, -8.65551558e-09,
         1.32081499e-08,  3.48952331e-08,  4.61431533e-09,
         3.59264661e-09,  3.54263054e-09,  1.12591034e-09,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00]])
FUtarget = np.array([[ 6.96135486e-05,  2.54272652e-05, -4.23745237e-06,
        -2.25829445e-06,  5.97676516e-06,  1.29817497e-05,
        -7.07183988e-06, -5.06040666e-05, -8.67351863e-06,
        -1.08615293e-05, -1.97420065e-05, -1.05506113e-05,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00]])
FVtarget = np.zeros_like(FUtarget)


def test_convect_tendencies():
    (IFLAG, FT, FQ, FU, FV, FTRA, PRECIP, WD, TPRIME, QPRIME, CBMFnew,
        Tout, Qout, QSout, Uout, Vout, TRAout) = \
            emanuel_convection(T, Q, QS, U, V, TRA, P, PH, NCOL, ND, NL, NTRA,
                    DELT, IPBL, CBMF,
                    CPD, CPV, CL, RV, RD, LV0, G, ROWL, MINORIG,
                    ELCRIT, TLCRIT, ENTP, SIGD, SIGS,
                    OMTRAIN, OMTSNOW, COEFFR, COEFFS,
                    CU, BETA, DTMAX, ALPHA, DAMP
                    )
    assert IFLAG == 1
    #  relative tolerance for these tests ...
    tol = 1E-5
    assert CBMFnew == pytest.approx(0.0310373, rel=tol)
    assert FTtarget == pytest.approx(FT, rel=tol)
    assert FQtarget == pytest.approx(FQ, rel=tol)
    assert FUtarget == pytest.approx(FU, rel=tol)
    assert FVtarget == pytest.approx(FV, rel=tol)
