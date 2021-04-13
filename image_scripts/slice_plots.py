#slice plots
from h5py import File
from pmd_beamphysics.interfaces import opal
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

#base = '/gpfs/slac/staas/fs1/g/accelerator_modeling/nneveu/emittance_minimization/code' 
#filepath = base+'/slac/ssnl/sc_inj_C1_bw1_10mill/64cubed_90MeV/'
#filepath = base+'/slac/paper_test/sc_inj_C14ce31345211d0af9d69c52e265b3abc215c7de5f/128cubed/'
#filepath = '/Users/nneveu/github/emittance_minimization/code/slac/ssnl/sc_inj_C1_bw1_10mill/128cubed/'
#filepath = '/Users/nneveu/github/emittance_minimization/code/slac/ssnl/sc_inj_C1_bw1_10mill/32cubed/'
#filepath = '/Users/nneveu/github/emittance_minimization/code/slac/ssnl/sc_inj_C1_bw1/'
#filepath = '/Users/nneveu/github/emittance_minimization/code/slac/paper_test/sc_inj_C14ce31345211d0af9d69c52e265b3abc215c7de5f/'
#filepath = '/Users/nneveu/github/emittance_minimization/code/slac/ssnl/sc_inj_reruns/run2/'
#filepath = '/Users/nneveu/github/emittance_minimization/code/slac/ssnl/sc_inj_reruns/run2.3/'
filepath = '/Users/nneveu/github/beam-shaping/sfg/sc_inj_reruns/bw1/run10/'


#name = 'ssnl_64cubed_90MeV_10mill'
#name = 'gauss_32cubed_50k'
name = 'run10_50k_sfg_1nm_filter'
h = File(filepath + 'sc_inj_C1.h5', 'r')
#fig, axs = plt.subplots(nrows = 3, ncols = 2, figsize = (10,9))
#plt.subplots_adjust(left=0.25, bottom=0.1, right=0.75 , top=0.9, wspace=0.6, hspace=0.45)
#print(h.keys())
nslice  = len(h.keys())-1
keyname = 'Step#'+str(nslice)
print(nslice)
step = h[keyname]
s = opal.opal_to_data(step)   
PG = ParticleGroup(data = s)

PG.z = PG.z - PG['mean_z']
slice_plot(PG,  stat_key = 'norm_emit_x', slice_key='z')
plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight')
plt.show()

marginal_plot(PG, 'z', 'energy', bins=250)
plt.savefig(name+'_espread_sliceplot.pdf', dpi=200, bbox_inches='tight')
plt.show()

#write_elegant(PG, name+'_elegant_test.txt', verbose=True)
#col = ['t', 'x', 'xp', 'y', 'yp', 'p']
#dat = load_sdds(name+'_elegant_test.txt', col, verbose=True)
#PE = ParticleGroup(data = dat)
