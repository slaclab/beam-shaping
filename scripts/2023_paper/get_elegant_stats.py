import numpy as np
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.interfaces.elegant import elegant_h5_to_data


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
dcns_file       = top_dir +'/joehold/100MeV/elegant_ssnl_100MeV_10mill_de_adjusted_64by512_300emission_steps.txt.out'
gauss_arb_file  = top_dir + '/jingyi/end_linac_arb_lht/SXRSTART_arb_laser.h5' #SXRSTART.out' # CORRECT!? picture matches paper
#gauss_flat_file = '/jingyi/end_linac_flat_lht/SXRSTART.out' #SXRSTART_flat_laser.h5 # picture doesn't match?

#data_dcns = np.loadtxt(dcns_file, skiprows=16)
gauss_data = elegant_h5_to_data(gauss_arb_file)
h5data     = ParticleGroup(data=gauss_data)
#h5data.plot('delta_t', 'delta_pz')
#plt.show()
h5data.slice_plot('norm_emit_x', n_slice=1000) #, slice_key='t')
plt.savefig('gauss_norm_emit.pdf',dpi=250)

print('sigma_x', h5data['sigma_x'])
print('energy', h5data['mean_energy'])
print('gamma',h5data.avg('gamma'))
print('norm_emit',h5data['norm_emit_x'])
