import numpy as np
import h5py
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.interfaces.elegant import elegant_h5_to_data
from pmd_beamphysics.interfaces.opal import opal_to_data

'''
SDDS1
!
! Created using the openPMD-beamphysics Python package
! https://github.com/ChristopherMayes/openPMD-beamphysics
! species: electron
!
&parameter name=Charge, type=double, units=C, description="total charge in Coulombs" &end
&column name=t,  type=double, units=s, description="time in seconds" &end
&column name=x,  type=double, units=m, description="x in meters" &end
&column name=xp, type=double, description="px/pz" &end
&column name=y,  type=double, units=m, description="y in meters" &end
&column name=yp, type=double, description="py/pz" &end
&column name=p,  type=double, description="relativistic gamma*beta" &end
&data mode=ascii &end
1.0000000000017146e-10
10000000
'''

# Load and get parameters from elegant files:
top_dir         = '/Users/nneveu/github/beam-shaping/sfg'
# End of CM01
dcns_file       = top_dir +'/elegant_files/elegant_ssnl_100MeV_10mill_de_adjusted_64by512_300emission_steps.h5' #_2.h5'
gauss_cm01      = top_dir +'/elegant_files/jingyi/end_CM01/gauss_linac_input.h5'

# Start of SXR
gauss_arb_file  = top_dir + '/elegant_files/jingyi/end_linac_arb_lht/SXRSTART_arb_laser.h5' #SXRSTART.out' # CORRECT!? picture matches paper

#gauss_data = elegant_h5_to_data(gauss_arb_file)
#h5data     = ParticleGroup(data=gauss_data)

dcns_data = h5py.File(dcns_file, 'r')
h5data    = ParticleGroup(h5=dcns_data)

h5data.slice_plot('norm_emit_x', n_slice=1000) #, slice_key='t')
plt.show()
#plt.savefig('gauss_norm_emit.pdf',dpi=250)
#h5data.plot('delta_t', 'delta_pz')

print('sigma_x', h5data['sigma_x'])
print('energy', h5data['mean_energy'])
print('gamma',h5data.avg('gamma'))
print('norm_emit',h5data['norm_emit_x'])
