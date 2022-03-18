#slice plots
import sys
import numpy as np
from h5py import File
from pmd_beamphysics.interfaces import opal
from pmd_beamphysics.plot import slice_plot
from pmd_beamphysics.plot import marginal_plot, density_plot
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.plot import marginal_plot
from pmd_beamphysics.interfaces.elegant import write_elegant, load_sdds, elegant_to_data
from pmd_beamphysics.interfaces.opal import write_opal
#import matplotlib
#import matplotlib.pyplot as plt
#plt.rc('xtick',labelsize=14)
#plt.rc('ytick',labelsize=14)
#plt.rc('font', size=16)
#plt.rc('font', family='STIXGeneral')
#plt.rc('mathtext', fontset='stix')

filepath = '/gpfs/slac/staas/fs1/g/g.beamphysics/neveu/beam-shaping/backtracking/name'
name     = 'LH_3kA.in'

sddsfile  = filepath+name
particles = elegant_to_data(sddsfile, sdds2plaindata_bin='sdds2plaindata', species='electron', verbose=True) 
opart     = write_opal(particles, 'opal_backtrack.dist')

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

#h = File(filepath + name, 'r')
#nslice  = len(h.keys())-1
#keyname = 'Step#'+str(nslice)
#print(nslice)
#step = h[keyname]
#s    = opal.opal_to_data(step)   
#PG   = ParticleGroup(data = s)
#PG.z = PG.z - PG['mean_z']
#slice_plot(PG,  stat_key = 'norm_emit_x', slice_key='z')
#plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight')
#plt.show()
#
#marginal_plot(PG, 'z', 'energy', bins=250)
#plt.savefig(name+'_espread_sliceplot.pdf', dpi=200, bbox_inches='tight')
#plt.show()

#write_elegant(PG, name+'_elegant_dist.txt', verbose=True)


