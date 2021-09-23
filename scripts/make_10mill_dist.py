import subprocess
import sys, os, copy
sys.path.append('/Users/nneveu/github/emittance_minimization/code/')
sys.path.append('/Users/nneveu/github/pyssnl')
sys.path.append('/Users/nneveu/github/libensemble')
import pandas as pd
import numpy as np
from argparse import ArgumentParser
from libeopal import LibeOpal, run_opal
import ssnl

OPAL_EXEC_PATH  = '/Users/nneveu/Code/OPAL-2.4.0/bin/opal' 
#'/lcrc/project/MCS-SLAC/software/opal_build/OPAL/version-2.4/bin/opal'
TEST_DIR        = '/Users/nneveu/github/emittance_minimization/code/slac/ssnl/' 
#'/lcrc/project/MCS-SLAC/emittance_minimization/code/vtmop_paper/'
FMAP_DIR       = '' 
#'/lcrc/project/MCS-SLAC/emittance_minimization/code/slac/fieldmaps'

STAT_NAMES = ['t', 's','numParticles','charge','energy','rms_x', 'rms_y', 'rms_s', \
              'rms_px', 'rms_py', 'rms_ps', 'emit_x', 'emit_y', 'emit_s', 'dE'] #'mean_x', \

xvals = np.array([60.0, 26.5, 9.6, 2.0, -64.5, 25.0, 57.0, 36.0, -30.0, 18.0, -10.0, 6.5, -35.0, 18.0, 23.0, 18.0])


xscale   = np.array([('RADIUS',1e-2), ('GDD', 1.0), ('SF', 0.1), \
                    ('PHGUNB', 1.0), ('PHBUN', 1.0), ('GBUN',0.1), \
                    ('SF1', 1e-3), ('SF2', 1e-3), \
                    ('PHCM1', 1.0), ('GCM1', 1.0),\
                    ('PHCM2', 1.0), ('GCM2', 1.0),\
                    ('PHCM3', 1.0), ('GCM3', 1.0),\
                    ('PHCM4', 1.0), ('GCM4', 1.0),\
                   ],dtype=[('name', 'U10'), ('scale', 'f4')])


num_objs  = 3 # len(objscale['name'])
key_dict  = {'dvar_keys':xscale['name'],'data_keys':STAT_NAMES} #, 'objective_keys':objscale['name']}
sim_specs = {
		'user':
		{
		'basefile_name':'sc_inj_C1',
                'input_files_path':TEST_DIR,
		'distgen_file':'tlaser_dist.yaml',
                'fieldmap_path':FMAP_DIR,
		'sim_kill_minutes':6,
		'key_dict':key_dict,
		'sim_particles':1e6,
		'cores':2,
                'zstop':15.0,
                'xscales':xscale,
                'penalty_scale':1e2
                },
	      
        'out': [('f', float, num_objs)] +  [(key,float) for key in key_dict['data_keys']] + [(key+'_long',float, 2500) for key in key_dict['data_keys']],
        }

print('x in run_opal:', xvals)
osim      = LibeOpal(sim_specs)

if 'FWHM' in osim.xscale['name']:
    dist = osim.make_gaussian_dist(xvals)
elif 'GDD' in osim.xscale['name']:
    dist = osim.make_ssnl_dist(xvals)


