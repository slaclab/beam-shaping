import subprocess
import numpy as np
import glob, os, sys
import matplotlib
import matplotlib.pyplot as plt
font = {'family' : 'DejaVu Sans','size':14}
sys.path.append('/Users/nneveu/github/pyssnl/')
sys.path.append('/Users/nneveu/github/emittance_minimization/code/')
from libeopal import LibeOpal
'''
'''
#'/Users/nneveu/github/emittance_minimization/code/slac/ssnl/' #
TEST_DIR = '/Users/nneveu/github/beam-shaping/template_files/'
FMAP_DIR = '/Users/nneveu/github/beam-shaping/fieldmaps/'

STAT_NAMES = ['t', 's','numParticles','charge','energy','rms_x', 'rms_y', 'rms_s', \
              'rms_px', 'rms_py', 'rms_ps', 'emit_x', 'emit_y', 'emit_s', 'dE'] #'mean_x', \

OBJ_SCALE =  np.array([('emit_x',0.3e-6,6e-6), ('rms_s',0.5e-3,4e-3), 
                ],dtype=[('name', 'U10'), ('lb', 'f4'), ('ub', 'f4')])

XBOUNDS   = np.array([ ('RADIUS', 15.0, 75.0), ('GDD', 1.0, 30.0), ('SF',0.0, 12.5), 
                    ('PHGUNB', -20.0, 10.0), ('PHBUN', -100.0, -10.0), ('GBUN', 10.0, 35.0), \
                    ('SF1', 20.0, 70.0), ('SF2', 20.0, 70.0), \
                    ('PHCM1', -40.0, 40.0), ('GCM1', 0.0, 32.0), \
                    ('PHCM2', -40.0, 40.0), ('GCM2', 0.0, 32.0), \
                    ('PHCM3', -40.0, 40.0), ('GCM3', 0.0, 32.0), \
                    ('PHCM4', -40.0, 40.0), ('GCM4', 0.0, 32.0), \
                   ],dtype=[('name', 'U10'), ('lb', 'f4'), ('ub','f4')])

XSCALE  = np.array([ ('RADIUS',1e-2), ('GDD', 1.0), ('SF', 0.1), \
                    ('PHGUNB', 1.0), ('PHBUN', 1.0), ('GBUN',0.1),\
                    ('SF1', 1e-3), ('SF2', 1e-3), \
                    ('PHCM1', 1.0), ('GCM1', 1.0), \
                    ('PHCM2', 1.0), ('GCM2', 1.0),\
                    ('PHCM3', 1.0), ('GCM3', 1.0), \
                    ('PHCM4', 1.0), ('GCM4', 1.0),\
                   ],dtype=[('name', 'U10'), ('scale', 'f4')])


num_objs  = 2 #len(OBJSCALE['name'])
key_dict  = {'dvar_keys':XSCALE['name'],'data_keys':STAT_NAMES, 'objective_keys':OBJ_SCALE['name']}
SIM_SPECS = {
        'user':
        {
        'basefile_name':'sc_inj_C1',
        'input_files_path':TEST_DIR,
        'fieldmap_path':FMAP_DIR,
        'distgen_file':TEST_DIR+'tlaser_dist.yaml',
        'sim_kill_minutes':8,
        'key_dict':key_dict,
        'sim_particles':5e4,
        'laser_filter':1.0,
        'cores':2,
        'zstop':15.0,
        'xscales':XSCALE,
        'penalty_scale':20,
        'objective_scales':OBJ_SCALE,
                },

        'out': [('f', float, num_objs)] +  [(key,float) for key in key_dict['data_keys']] + [(key+'_long',float, 2500) for key in key_dict['data_keys']],
        }

# picking which sims to do
filename = glob.glob('/Users/nneveu/github/beam-shaping/sfg/datasets/*1*.npy')
data = np.load(filename[0])

#bunch length
rms_s = data['rms_s']
# roughly 1 mm
# six runs for bw0.7
mask = (data['rms_s']>0.00098) & (data['rms_s']<0.00102) & (data['emit_x']<0.4e-6)
#print(data[mask]['emit_x'])
# cut data, last 5 ar unique
cut = data[mask]
#print(cut['individual'])
#print('emittance:', cut['emit_x'])
#print('bunch length:', cut[i]['rms_s'])
#print('x values', np.round(cut['individual'], decimals=2))

#import pdb; pdb.set_trace()
for i in range(0,len(cut)):
    print(i)
    XVALS = np.round(cut[i]['individual'], decimals=2)
    print(XVALS)
    dirname = 'bw1_'+str(i)
    print(dirname)
    #try:
    #    os.mkdir(dirname)
    #except Exception as e:
    #    print(e)
    os.chdir(dirname)
    osim      = LibeOpal(SIM_SPECS)
    dist      = osim.make_ssnl_dist(XVALS)
    opal_file = osim.make_sim_file(XVALS)
    tkill   = SIM_SPECS['user']['sim_kill_minutes']*60 # seconds
    mpi     = ['mpirun', '-np', str(SIM_SPECS['user']['cores'])]
    obin    = ['/Users/nneveu/code/OPAL-2.4.0/bin/opal']
    simfile = [osim.opal_input_file]
    cmd     = mpi+obin+simfile
#
    print('the commdand is:', cmd)
    print('the dir is:', os.getcwd())
    with open("stdout.txt","wb") as out, open("stderr.txt","wb") as err:
        subprocess.run(cmd,stdout=out,stderr=err, timeout=tkill)
        #print('yes')  
#
    os.chdir('/Users/nneveu/github/beam-shaping/sfg/joe_runs')
