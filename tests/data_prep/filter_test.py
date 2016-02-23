from toughp_proc import *
import numpy as np
mesh = ToughMesh.Tough_Mesh("../converting/MESH")
assert( mesh.FindElements(filters.near(np.array([.25,1.75,-0.25])))[0] ==
        'A0300') 
assert( 'A0300' in mesh.FindElements(filters.near(np.array([.25,1.75,-0.25]),2.0)) )

print("Tests on finding elements passed")
