Hydr = """\
HYDRATE--1----*----2----*----3----*----4----*----5----*----6----*----7----*----8
     1                       ! HCom%NCom
'CH4'  6.0d0 1.00d00         ! Name, hydration number, mole fraction in composite hydrate
     1                       ! Number of coefficients in thermal conductivity polynomial
  4.5e-1                     ! Coefficients in the thermal conductivity polynomial
     1                       ! Number of coefficients in the specific heat polynomial
  2.1e03                     ! Coefficients in the specific heat polynomial
     1                       ! Number of coefficients in density polynomial
  9.2e02                     ! Coefficients in the density polynomial
.FALSE. 5.0d0  1.0d-2 58.448e0 2.6e3  6.6479d4 1.3d-9 ! T_MaxOff,C_MaxOff,MW_Inhib,D_Inhib,H_InhSol,DifCo_Inh  
0                            ! F_EqOption
'EQUILIBRIUM'                ! Type of dissociation
"""
