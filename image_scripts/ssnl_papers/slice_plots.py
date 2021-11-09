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
plt.rc('xtick',labelsize=16)
plt.rc('ytick',labelsize=16)
plt.rc('font', size=20)
plt.rc('font', family='STIXGeneral')
plt.rc('mathtext', fontset='stix')

filepath = '/Users/nneveu/github/beam-shaping/sfg/sc_inj_reruns/bw0.5/10mill/92MeV/'


name = filepath.split('/')[-2] #'bw0.5_filter_0_50k'
print(name)
h = File(filepath + 'sc_inj_C1.h5', 'r')
#fig, axs = plt.subplots(nrows = 3, ncols = 2, figsize = (10,9))
#plt.subplots_adjust(left=0.25, bottom=0.1, right=0.75 , top=0.9, wspace=0.6, hspace=0.45)
#print(h.keys())
nslice  = len(h.keys())-1
keyname = 'Step#'+str(nslice)
print(nslice)
step = h[keyname]
s    = opal.opal_to_data(step)   
PG   = ParticleGroup(data = s)
PG.z = PG.z - PG['mean_z']

#plt.figure(figsize=(4, 4))
#plt.hist2d(PG['z']*10**3, PG['energy']*10**-6, bins=120, cmin=1) #, density=True)
#plt.ylabel(r'Energy (MeV)')
#plt.xlabel(r'z (mm)')
#plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight', backend='pgf')
#plt.show()


#plt.hist(
#plt.figure(figsize=(4, 4))
slice_plot(PG,  stat_key = 'norm_emit_x', slice_key='z', n_slice=500)
plt.xlabel(r'z(mm)', size=20)
plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight')
plt.show()


#write_elegant(PG, name+'_elegant_test.txt', verbose=True)
#col = ['t', 'x', 'xp', 'y', 'yp', 'p']
#dat = load_sdds(name+'_elegant_test.txt', col, verbose=True)
#PE = ParticleGroup(data = dat)
