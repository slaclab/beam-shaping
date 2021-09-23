#slice plots
import sys
software = '/Users/nneveu/github/'
sys.path.append(software+'openPMD-beamphysics')
import numpy as np
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

filepath = '/Users/nneveu/github/beam-shaping/ssnl/sc_inj_reruns/run2.3/'

name = 'run2.3_50k_sfg_0.5nm_filter'
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
#slice_plot(PG,  stat_key = 'norm_emit_x', slice_key='z')
#plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight')
#plt.show()
#
#marginal_plot(PG, 'z', 'energy', bins=250)
#plt.savefig(name+'_espread_sliceplot.pdf', dpi=200, bbox_inches='tight')
#plt.show()


write_elegant(PG, name+'_elegant_dist.txt', verbose=True)

#outfile = 'elegant_files/run2.3_50k_sfg_0.5nm_filter_elegant_test.txt'
#test = np.loadtxt(outfile, skiprows=17)
#
#t = 10**12*(test[:,0]-np.mean(test[:,0]))
#x = test[:,1]
#xp = test[:,2]
#y = test[:,3]
#yp = test[:,4]
#p = test[:,5]
#
#pz = p/ np.sqrt(1+xp**2+yp**2)
#
#plt.hist2d(t, p, bins=100)
#plt.show()
#
#plt.hist2d(x,y, bins=100)
#plt.show()
