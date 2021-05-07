import glob, sys
sys.path.append('/Users/nneveu/github/pyOPALTools/')
import numpy as np
import matplotlib
from cycler import cycler
import matplotlib.pyplot as plt
plt.rc('axes', prop_cycle=(cycler('markersize', [2]*5)+ cycler('color', ['c', 'm', 'g', 'y', 'k']) +
                               cycler('linestyle', ['-', '--', ':', '-.', '-'])))
from matplotlib.ticker import FormatStrFormatter
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
import pandas as pd 

#Functions from pyOPALTools
#https://gitlab.psi.ch/OPAL/pyOPALTools
from opal import load_dataset

#simdir    = '../slac/lcls2/vtmop/fidelity/sc_inj_'
#pathnames = ['10k', '100k', '1M','10k_low']
#statnames  = 'sc_inj.stat'

#simdir = '../slac/lcls/test_run/' 
#pathnames = [''] 
#statnames = 'lcls_gun.stat'

#simdir = '../slac/ssnl/sc_inj_C1_bw1_10mill/' 
#pathnames = ['32cubed','64cubed','128cubed']#glob.glob(simdir+'*cubed')
#statnames = 'sc_inj_C1.stat'

#simdir = '../slac/paper_test/10mill/' 
#pathnames = ['64cubed_90MeV']#['32cubed','64cubed','128cubed', '64cubed_90MeV']#glob.glob(simdir+'*cubed')
#statnames = 'sc_inj_C1.stat'

#simdir    = '../slac/ssnl/sc_inj_reruns/'
#pathnames = ['run2', 'run2.1', 'run2.2', 'run2.3']#, 'run3']
#statnames = 'sc_inj_C1.stat'

#simdir    = '/Users/nneveu/github/beam-shaping/sfg/adjust_runs/'
#pathnames = ['run2.5', 'run2.6', 'run2.7', 'run2.8', 'run2.9']
#statnames = 'sc_inj_C1.stat'

simdir    = '/Users/nneveu/github/beam-shaping/sfg/sc_inj_reruns/bw1/'
pathnames = ['run6',  'run3', 'run4', 'run5_100MeV']
statnames = 'sc_inj_C1.stat'


#--------------------------------------------------------------------------
zstop = 15.0


f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)


for path in pathnames:
    print(path) 
    ds = load_dataset(simdir+path, fname=statnames)
    #ds = load_dataset(path, fname=statnames)
    z    = ds.getData(var='s') 
    emit = ds.getData(var='emit_x')*10**6
    #xrms = ds.getData(var='rms_x')*10**3
    zrms = ds.getData(var='rms_s')*10**3
    energy = ds.getData(var='energy')
    print(energy[-1])

    ax1.plot(z, emit,'-' , label= path) #'SFG BW 1.0 nm')
    ax2.plot(z, zrms, '-')#, label='zrms')
    #ax2.plot(z, xrms, '.')#, label='xrms')
    ax3.plot(z, energy, '-', label=path)

for ax in [ax1,ax2,ax3]:
    ax.set_xlim(0,zstop)
    ax.grid()


ax3.set_xlabel('Z [meters]')    
ax2.set_ylabel('Beam sizes [mm]')
ax1.set_ylabel('Emittance [um]')
ax3.set_ylabel('Energy [MeV]')
    
ax1.set_ylim(0,1)
#ax3.set_ylim(90,100)
ax1.legend()
plt.savefig(path+'_opal_stats.pdf', dpi=300, bbox_inches='tight')
#plt.show()


