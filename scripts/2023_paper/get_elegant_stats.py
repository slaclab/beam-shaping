import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.interfaces.elegant import elegant_h5_to_data
from pmd_beamphysics.interfaces.opal import opal_to_data

#print(mpl.rcParams.keys())
mpl.rcParams['xtick.labelsize']= 16
mpl.rcParams['ytick.labelsize']= 16
mpl.rcParams['font.size']= 16
mpl.rcParams['figure.autolayout'] =True
#figure.figsize: 6.75,4.57
mpl.rcParams['axes.titlesize']= 16
mpl.rcParams['axes.labelsize']= 16
#legend.fontsize: 13
mpl.rcParams['mathtext.fontset']= 'stix'
mpl.rcParams['font.family']= 'STIXGeneral'



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
dcns_cm01       = top_dir +'/elegant_files/elegant_ssnl_100MeV_10mill_de_adjusted_64by512_300emission_steps.h5'
gauss_cm01      = top_dir +'/elegant_files/jingyi/end_CM01/gauss_linac_input.h5'

# Start of SXR
gauss_arb_sxr = top_dir + '/elegant_files/jingyi/end_linac_arb_lht/SXRSTART_arb_laser.h5' #SXRSTART.out' # CORRECT!? picture matches paper
dcns_sxr      = top_dir +'/elegant_files/elegant_ssnl_100MeV_10mill_de_adjusted_64by512_300emission_steps_2.h5'


#For Gauss at end of CM01 - WORKS *with openPMD edits (no ID, no unit check on p)
#gauss_h5 = h5py.File(gauss_cm01, 'r')
#gauss_data = elegant_h5_to_data(gauss_h5)
#h5data     = ParticleGroup(data=gauss_data)

#For DCNS at end of CM01 - WORKS
dcns_h5 = h5py.File(dcns_cm01, 'r')
h5data  = ParticleGroup(h5=dcns_h5)

fig = h5data.slice_plot('norm_emit_x', n_slice=1000) #, slice_key='t')
#plt.title('Gaussian to CM01')
#plt.title('DCNS to CM01')

#plt.gca().invert_xaxis()
plt.show()
#plt.savefig('gauss_norm_emit.pdf',dpi=250)
#h5data.plot('delta_t', 'delta_pz')

#slice_data = slice_statistics(h5data,  keys=['norm_emit_x'], n_slice=40, slice_key='z')
#import pdb; pdb.set_trace()

print('sigma_x', h5data['sigma_x'])
print('energy', h5data['mean_energy'])
print('gamma',h5data.avg('gamma'))
print('norm_emit',h5data['norm_emit_x'])
