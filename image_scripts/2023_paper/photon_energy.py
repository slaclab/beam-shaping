import numpy as np
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.statistics import slice_statistics
from pmd_beamphysics.interfaces.elegant import elegant_h5_to_data
from pmd_beamphysics.interfaces.opal import opal_to_data

#print(mpl.rcParams.keys())
mpl.rcParams['xtick.labelsize']= 16
mpl.rcParams['ytick.labelsize']= 16
mpl.rcParams['font.size']= 16 
mpl.rcParams['figure.autolayout'] =True
#figure.figsize: 6.75,4.57
mpl.rcParams['axes.titlesize']= 16
mpl.rcParams['axes.labelsize']= 20
#legend.fontsize: 13
mpl.rcParams['mathtext.fontset']= 'stix'
mpl.rcParams['font.family']= 'STIXGeneral'


photon_energy = np.arange(0.3,1.1,0.1)
dcns  = np.array([2.422, 2.55, 2.614, 2.639, 2.637, 2.618, 2.585, 2.544])
gauss = np.array([1.758,1.859,1.913,1.938,1.944,1.935,1.916,1.889])	

percent = 100*((dcns - gauss)/gauss)
print(percent)

plt.plot(photon_energy, gauss, color='purple', linestyle='-.', linewidth=4, label='Gaussian')
plt.plot(photon_energy, dcns, color='grey', linestyle='-', linewidth=4, label = 'DCNS')
plt.xlabel('Photon energy (keV)')
plt.ylabel('X-ray pulse energy (mJ)')
plt.legend()
#plt.show()
plt.savefig('xray_energy.pdf', dpi=250, bbox_inches='tight')
