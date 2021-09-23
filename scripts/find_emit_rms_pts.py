import glob, sys, os
import numpy as np
import matplotlib.pyplot as plt
plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
plt.rc('font', family='STIXGeneral')
plt.rc('mathtext', fontset='stix')

#np.set_printoptions(threshold=sys.maxsize)

sys.path.append('/Users/nneveu/github/pyssnl')
import ssnl
labels   = ['Gaussian', 'DCNS + \n 0.5 (nm) bw filter', 'DCNS + \n 1.0 (nm) bw filter']
data_dir = 'data/'

# All opt files 
#opt_files = glob.glob(data_dir+'paper_test/good_results/sol1_40-70/*.npy')+glob.glob(data_dir+'ssnl/ssnl_results/*0.5*.npy')+ glob.glob(data_dir+'ssnl/ssnl_results/*1*.npy')
#opt_files = glob.glob(data_dir+'paper_test/good_results/sol1_20-70/*.npy')+glob.glob(data_dir+'ssnl/ssnl_results/*.npy')
opt_files = glob.glob(data_dir+'*bw1*.npy')

print(len(opt_files))
#print(opt_files)
#f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10,8), sharey=True)
#axs = [ax1,ax2,ax3]

for i,filename in enumerate(opt_files):
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    print(filename)
    
    H0_2obj = np.load(filename)[:]
    H0_2obj = H0_2obj[H0_2obj['emit_x']>0]
    H0_2obj = H0_2obj[H0_2obj['s']>14.85]
    print(len(H0_2obj))
    H2      = H0_2obj[H0_2obj['numParticles'] == 5e4]
    H2_lost = H0_2obj[(H0_2obj['numParticles']) < 5e4]
    print(len(H2))

    emit = np.trim_zeros(H2['emit_x'][:]*1e6, 'b')
    zrms = np.trim_zeros(H2['rms_s'][:]*1e3, 'b')
    xrms = np.trim_zeros(H2['rms_x'][:]*1e3, 'b')
    
    emit_lost = np.trim_zeros(H2_lost['emit_x'][:]*1e6, 'b')
    zrms_lost  = np.trim_zeros(H2_lost['rms_s'][:]*1e3, 'b')
    xrms_lost  = np.trim_zeros(H2_lost['rms_x'][:]*1e3, 'b')
        
    index  = np.where(emit < 0.5)   
    iemit  = emit[index] 
    izrms  = zrms[index]
    #import pdb; pdb.set_trace()
    ix   = H2['individual'][index] #np.trim_zeros(H2['individual'][:]*1e6, 'b')[index]

    # Min emittance
#    minindex = np.argsort(iemit)[:3]
#    print(np.c_[iemit[minindex], izrms[minindex]]) 
#    print(ix[minindex])
    
    # Certain bunch lengths
    #print(iemit[sindex], izrms[sindex])
    mask = (izrms >= 0.999) & (izrms <= 1.0015)
    #mask = (izrms >= 0.499) & (izrms <= 0.501)
    #mask = (izrms >= 0.245) & (izrms <= 0.255)
    print(np.c_[iemit[mask], izrms[mask]]) 
    print(ix[mask])    
    #
    #best_sort2 = np.argsort(emit[index])#+ 30*(zrms[index]-1e-3)**2)
    #best_sort2 = best_sort2[:5]
    #print('emit  zrms')
    #print(emit[best_sort2], zrms[best_sort2])
    #print(np.c_[emit[best_sort2], zrms[best_sort2]]) 
    #print(labels[i])
#    c = axs[i].hist2d(zrms[index], emit[index], bins=40, cmin=1)#, label=labels[i])
    #axs[i].legend(loc='lower left')
    #print('mean:', np.mean(emit[index]))
    #print('std:', np.std(emit[index]))
    #print('\n\n') 
    #axs[i].annotate(labels[i], xy=(0.05, 0.05), xycoords='axes fraction', size=14)
#for ax in axs:#[ax1,ax2,ax3]: #,ax2]:
#    #ax.set_xlabel(r'Bunch length (mm)', size=14)
#    ax.set_xlim(0,1.5)
#    ax.set_ylim(0,1)
#    ax.set_axisbelow(True)
#    ax.grid()
#ax1.legend(labels[0], loc='lower left')
#ax2.legend(labels[1], loc='lower left')
##ax3.legend(labels[2], loc='lower left')
#ax1.set_ylabel(r'Emittance (um)', size=16)
#f.colorbar(c[3], ax=axs, orientation='vertical', fraction=.1)
#f.savefig('hist_bw1_bw0.5_gauss_16x9.pdf', dpi=500, bbox_inches='tight')
#
#plt.show()    
