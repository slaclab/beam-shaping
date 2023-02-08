import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

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

#deap data
#n = 4000
datadir = '/Users/nneveu/github/beam-shaping/sfg/datasets/1030nm_results/'

filenames = ['deap_run3_gauss_nosample_history_length=5300_evals=5274.npy',				
'deap_ssnl_bw0.5_32MV_history_length=7000_evals=6570_workers=36.npy',
'deap_ssnl_bw0.7_32MV_history_length=7000_evals=7000_workers=36.npy',			
'deap_ssnl_bw1_32MV_history_length=7000_evals=7000_workers=36.npy']

titles = ['Gaussian', 'DCNS + 0.5 (nm) bw filter', 
          'DCNS + 0.7 (nm) bw filter', 'DCNS + 1.0 (nm) bw filter']

#pareto_points_paper_deap_run3_gauss_nosample_history_length=5300_evals=5274.npy
#pareto_points_paper_deap_ssnl_bw0.7_32MV_history_length=7000_evals=7000_workers=36.npy
#pareto_points_paper_deap_ssnl_bw0.5_32MV_history_length=7000_evals=6570_workers=36.npy
#pareto_points_paper_deap_ssnl_bw1_32MV_history_length=7000_evals=7000_workers=36.npy


for index, filename in enumerate(filenames):
    print(datadir+filename)
    data    = np.load(datadir+filename)
    dindex  = np.where(data['numParticles']==50000)
    demit   = data['emit_x'][dindex]*10**6
    drms    = data['rms_s'][dindex]*10**3
    denergy = data['energy'][dindex]

    fig, ax = plt.subplots()
    df = pd.DataFrame({'demit': demit, 'drms': drms, 'denergy': denergy})
    sc = ax.scatter(df.drms, df.demit, c=df.denergy,  alpha=0.5, cmap="viridis")
    cb = fig.colorbar(sc, ax=ax)
    cb.ax.set_ylabel('Energy (MeV)', rotation=270, labelpad=20)
 
    ax.grid()
    ax.set_xlim(0,2)
    ax.set_ylim(0,2)
    ax.set_axisbelow(True)
    ax.set_title(titles[index])
    ax.set_ylabel(r'Emittance (mm-mrad)')
    ax.set_xlabel('Bunch length (mm)')
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start,end,0.25))
    savename = filename.split('.npy')[0]
    plt.savefig('/Users/nneveu/github/beam-shaping/image_scripts/2023_paper/'+savename+'.pdf', dpi=250, bbox_inches='tight')
    plt.show()

#if flag:
#    df = pd.DataFrame({'uemit': uemit, 'urms': urms, 'ude': ude})
#    scu = ax.scatter(df.urms, df.uemit, c=df.ude,  alpha=0.5, cmap="viridis")
#    cb2 = fig.colorbar(scu, ax=ax)
#    #cb2.ax.set_title('Uniform \n start')
#    cb2.ax.set_ylabel('Energy spread [MeV]', rotation=270, labelpad=20)
#    print(len(df.urms))
#    ax.set_title('NSGA-II results uniform start')
#
#plt.savefig('/Users/nneveu/github/emittance_minimization/tex/cpc20/resubmission/fig6_dlhs_scatter.pdf', dpi=250, bbox_inches='tight')
#plt.show()

