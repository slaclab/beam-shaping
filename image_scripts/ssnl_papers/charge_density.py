from h5py import File
import numpy as np
import matplotlib.pyplot as plt
from pmd_beamphysics.interfaces import opal
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.statistics import slice_statistics
from pmd_beamphysics.units import nice_array
plt.rc('xtick',labelsize=16)
plt.rc('ytick',labelsize=16)
plt.rc('font', size=20)
plt.rc('font', family='STIXGeneral')
plt.rc('mathtext', fontset='stix')

filepath = '/Users/nneveu/github/beam-shaping/sfg/sc_inj_reruns/bw0.5/10mill/92MeV/'
name = filepath.split('/')[-2] #'bw0.5_filter_0_50k'
print(name)
h = File(filepath + 'sc_inj_C1.h5', 'r')
nslice  = len(h.keys())-1
keyname = 'Step#'+str(nslice)
print(nslice)
step = h[keyname]
s    = opal.opal_to_data(step)  
PG   = ParticleGroup(data = s)
PG.z = PG.z - PG['mean_z']


def slice_plot(particle_group, 
               stat_key='sigma_x',
               n_slice=40,
               slice_key='z',
               tex=True,
               **kwargs):
    """
    Complete slice plotting routine. Will plot the density of the slice key on the right axis. 
    """
    
    x_key = 'mean_'+slice_key
    y_key = stat_key
    slice_dat = slice_statistics(particle_group, n_slice=n_slice, slice_key=slice_key,
                            keys=[x_key, y_key, 'ptp_'+slice_key, 'charge'])
    
    
    slice_dat['density'] = slice_dat['charge']/ slice_dat['ptp_'+slice_key]
    y2_key = 'density'
    fig, ax = plt.subplots(**kwargs)
    
    # Get nice arrays
    x, _, prex = nice_array(slice_dat[x_key])
    y, _, prey = nice_array(slice_dat[y_key])
    y2, _, prey2 = nice_array(slice_dat[y2_key])
    
    x_units = f'{prex}{particle_group.units(x_key)}'
    y_units = f'{prey}{particle_group.units(y_key)}'    
    
    # Convert to Amps if possible
    y2_units = f'C/{particle_group.units(x_key)}'
    if y2_units == 'C/s':
        y2_units = 'A'
    y2_units = prey2+y2_units 
    
    # Labels
    

    #labelx = mathlabel(slice_key, units=x_units, tex=tex)
    #labely = mathlabel(y_key, units=y_units, tex=tex)    
    #labely2 = mathlabel(y2_key, units=y2_units, tex=tex)        
    #
    #ax.set_xlabel(labelx)
    #ax.set_ylabel(labely)
   
    ax.set_xlabel(r'z (mm)')
    ax.set_ylabel(r'Emittance ($\mu$m)')
 
    # Main plot
    ax.plot(x, y, color = 'black')
    #ax.set_ylim(0, 1.1*ymax )

    ax2 = ax.twinx()
    #ax2.set_ylabel(labely2)
    ax2.set_ylabel(r'Charge Density (FIX)')
    ax2.fill_between(x, 0, y2, color='black', alpha = 0.2)


    import matplotlib.patches as mpatches

    pop_a = mpatches.Patch(color='k', linestyle='-', label='slice $\epsilon_x$')
    pop_b = mpatches.Patch(color='#89bedc', label='charge')

    ax.legend(handles=[pop_a,pop_b])
    
    return fig

#import pdb; pdb.set_trace()
slice_plot(PG,  stat_key = 'norm_emit_x', slice_key='z', n_slice=500)
plt.savefig(name+'_emit_sliceplot.pdf', dpi=200, bbox_inches='tight')
plt.show()
