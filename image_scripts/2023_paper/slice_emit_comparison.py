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
dcns_sxr      = top_dir +'/elegant_files/joehold/100MeV/rerun_tmpa205lw9v/dcns_sxr.h5'
#dcns_sxr      = top_dir +'/elegant_files/joehold/tmpa205lw9v/tmpa205lw9v.h5'

cm01 = False

if cm01:
    #For Gauss at end of CM01 - WORKS *with openPMD edits (no ID, no unit check on p)
    gauss_h5 = h5py.File(gauss_cm01, 'r')
    #For DCNS at end of CM01 - WORKS
    dcns_h5 = h5py.File(dcns_cm01, 'r')
    savefile = 'compare_slice_emit_gauss_dcns_cm01_exit.pdf'

else: 
    #For Gauss at end of linac - WORKS
    gauss_h5 = h5py.File(gauss_arb_sxr, 'r')
    #For DCNS at end of linac - WORKS
    dcns_h5  = h5py.File(dcns_sxr, 'r')
    savefile = 'compare_slice_emit_gauss_dcns_sxr_start.pdf'

gauss_data   = elegant_h5_to_data(gauss_h5)
gauss_h5data = ParticleGroup(data=gauss_data)
dcns_h5data  = ParticleGroup(h5=dcns_h5)

gauss_emit_slices_x = slice_statistics(gauss_h5data,  keys=['norm_emit_x'], n_slice=1000, slice_key='t')
dcns_emit_slices_x  = slice_statistics(dcns_h5data,  keys=['norm_emit_x'], n_slice=1000, slice_key='t')
gauss_emit_slices_y = slice_statistics(gauss_h5data,  keys=['norm_emit_y'], n_slice=1000, slice_key='t')
dcns_emit_slices_y  = slice_statistics(dcns_h5data,  keys=['norm_emit_y'], n_slice=1000, slice_key='t')

#PLOTTING lines 
#delta_time = 10**12*(np.max(gauss_h5data.t) - np.min(gauss_h5data.t)) 
#time       = np.arange(-delta_time/2, delta_time/2, delta_time/np.size(gauss_emit_slices_x['norm_emit_x']))
#
#colors = {
#    'blue':    '#377eb8',
#    'orange':  '#ff7f00',
#    'green':   '#4daf4a',
#    'pink':    '#f781bf',
#    'brown':   '#a65628',
#    'purple':  '#984ea3',
#    'gray':    '#999999',
#    'red':     '#e41a1c',
#    'yellow':  '#dede00'
#}

#plt.plot(time, gauss_emit_slices_x['norm_emit_x']*10**6, label=r"Gaussian $\epsilon_{n,x}$", color='purple', linestyle='dotted')
#plt.plot(time, gauss_emit_slices_y['norm_emit_y']*10**6, label=r"Gaussian $\epsilon_{n,y}$", alpha=0.5, color='blue', linestyle='--')
#plt.plot(time, dcns_emit_slices_x['norm_emit_x']*10**6, label=r"DCNS $\epsilon_{n,x}$", color='brown', linestyle='-.')
#plt.plot(time, dcns_emit_slices_y['norm_emit_y']*10**6, label=r"DCNS $\epsilon_{n,y}$", alpha=0.5, color='gray', linestyle='-')
#
##plt.title('Slice emittance at the end of CM01')
#plt.xlabel('Time (ps)')
#plt.ylabel('Emittance (mm-mrad)')
#plt.legend()
##plt.show()
##plt.gca().invert_xaxis()
#plt.savefig(savefile,dpi=250)


xdata = [gauss_emit_slices_x, dcns_emit_slices_x]
ydata = [gauss_emit_slices_y, dcns_emit_slices_y]

for data in xdata:
    print('X sum')
    emit = data['norm_emit_x']*10**6
    test = np.where(emit<0.5)
    print(len(test[0]))


for data in ydata:
    print('Y sum')
    emit = data['norm_emit_y']*10**6
    test = np.where(emit<0.5)
    print(len(test[0]))


