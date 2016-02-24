MEMORY = """\
MEMORY
'HYDRATE-EQUILIBRIUM'
   2     3    4    .FALSE.            ! NK,NEQ,NPH,binary_diffusion
'Cartesian'   38000   100000     5  .FALSE. ! MNEL,MNCON,No_CEN,active_conx_only
   2                                  ! MaxNum_SS
   3                                  ! MaxNum_Media
.FALSE.  .FALSE.  .FALSE.             ! element_by_element_properties, porosity_perm_dependence, scaled_capillary_pressure
.FALSE.  'Continuous'                 ! coupled_geochemistry, property_update = 'Continuous', 'Iteration', 'Timestep'
.TRUE.  'Time Step'  0                ! coupled_geomechanics, property_update, num_geomech_param"""

START = """\
START----1----*----2----*----3----*----4----*----5----*----6----*----7----*----8
----*----1 MOP: 123456789*123456789*1234 ---*----5----*----6----*----7----*----8
"""

PARAM = """\
TODO: I don't get this format
"""
