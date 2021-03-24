#slice plots
import sys
software = '/Users/nneveu/github/'
sys.path.append(software+'openPMD-beamphysics')
from h5py import File
from pmd_beamphysics.interfaces import opal, elegant
from pmd_beamphysics.plot import slice_plot
from pmd_beamphysics.plot import marginal_plot, density_plot
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.plot import marginal_plot
from pmd_beamphysics.interfaces.elegant import write_elegant, load_sdds

import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
plt.rc('font', size=16)
plt.rc('font', family='STIXGeneral')
plt.rc('mathtext', fontset='stix')


filepath = 'elegant_ssnl_64by512_100MeV_10mill_300emission_steps.txt'
name = filepath.split('.')[0]

col = ['t', 'x', 'xp', 'y', 'yp', 'p']
dat = load_sdds(filepath, col, verbose=True)
PE = ParticleGroup(data = dat)

#fig, axs = plt.subplots(nrows = 3, ncols = 2, figsize = (10,9))
#plt.subplots_adjust(left=0.25, bottom=0.1, right=0.75 , top=0.9, wspace=0.6, hspace=0.45)
#
#PG.z = PG.z - PG['mean_z']
#slice_plot(PG,  stat_key = 'norm_emit_x', slice_key='z')
#plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight')
#plt.show()

marginal_plot(PE, 'z', 'energy', bins=250)
plt.savefig(name+'_espread_sliceplot.pdf', dpi=200, bbox_inches='tight')
plt.show()

#write_elegant(PG, name+'_elegant_test.txt', verbose=True)

