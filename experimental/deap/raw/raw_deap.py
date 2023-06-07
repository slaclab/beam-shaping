# NSGA2 example from DEAP documentation:
# https://gist.github.com/darden1/fa8f96185a46796ed9516993bfe24862
# 
# Execute via the following command:
#    mpiexec -np 3 python3 {FILENAME}.py
# The number of concurrent evaluations of the objective function will be 2-1=1.
# """
#import mpi4py
#mpi4py.rc.recv_mprobe = False
#from mpi4py import MPI

import os, sys, glob
import numpy as np

from libensemble.message_numbers import WORKER_DONE, WORKER_KILL, TASK_FAILED, WORKER_KILL_ON_TIMEOUT
from libensemble.libE import libE

from libensemble.alloc_funcs.start_only_persistent import only_persistent_gens as alloc_f
from persistent_deap_nsga2 import deap_nsga2 as gen_f

from libensemble.tools import parse_args, save_libE_output, add_unique_random_streams 
from libensemble.executors.mpi_executor import MPIExecutor

from libensemble import logger
logger.set_level('DEBUG')
nworkers, is_master, libE_specs, _ = parse_args()
assert nworkers >= 2, "Cannot run with a persistent gen_f if only one worker."

from libeopal import opal_deap

# Create executor and register sim to it
exctr = MPIExecutor()  # Use auto_resources=False to oversubscribe

#Setting up the simulation enviornment
TOP_DIR = '/gpfs/slac/staas/fs1/g/accelerator_modeling/nneveu/beam-shaping/experimental/' 
files   = 'templates/'

# Register simulation executable with executor 
sim_app = '/gpfs/slac/staas/fs1/g/accelerator_modeling/nneveu/software/OPAL/opal_mpich/bin/opal'
exctr.register_app(full_path=sim_app, calc_type='sim')

libE_specs['sim_dir_symlink_files'] = [ f for f in glob.glob(TOP_DIR+'fieldmaps/*.txt')]

STAT_NAMES = ['t', 's','numParticles','charge','energy','rms_x', 'rms_y', 'rms_s', \
              'rms_px', 'rms_py', 'rms_ps', 'emit_x', 'emit_y', 'emit_s']#, 'mean_x', \

simpart = 5e4
penalty = 1e2

objscale =  np.array([
        ('emit_x',0.3e-6,6e-6),
        ('rms_s',0.5e-3,4e-3),
        ],dtype=[('name', 'U10'), ('lb', 'f4'), ('ub', 'f4')])

xscale   = np.array([('RADIUS',1e-2), #('GDD', 1.0), ('SF', 0.1), \
                    ('PHGUNB', 1.0), ('PHBUN', 1.0), ('GBUN',0.1), \
                    ('SF1', 1e-3), ('SF2', 1e-3), \
                    ('PHCM1', 1.0), ('GCM1', 1.0),\
                    ('PHCM2', 1.0), ('GCM2', 1.0),\
                    ('PHCM3', 1.0), ('GCM3', 1.0),\
                    ('PHCM4', 1.0), ('GCM4', 1.0),\
                   ],dtype=[('name', 'U10'), ('scale', 'f4')])

xbounds  = np.array([('RADIUS', 15.0, 75.0), #('GDD', 1.0, 30.0), ('SF',0.0, 12.5),
                    ('PHGUNB', -20.0, 10.0), ('PHBUN', -100.0, -10.0), ('GBUN', 10.0, 35.0), \
                    ('SF1', 20.0, 70.0), ('SF2', 20.0, 70.0), \
                    ('PHCM1', -40.0, 40.0), ('GCM1', 0.0, 32.0), \
                    ('PHCM2', -40.0, 40.0), ('GCM2', 0.0, 32.0), \
                    ('PHCM3', -40.0, 40.0), ('GCM3', 0.0, 32.0), \
                    ('PHCM4', -40.0, 40.0), ('GCM4', 0.0, 32.0), \
                   ],dtype=[('name', 'U10'), ('lb', 'f4'), ('ub', 'f4')])

# Keys related to data in OPAL sim and objectives
key_dict = {'data_keys': STAT_NAMES,
            'dvar_keys': list(xbounds['name'][:]),
            'objective_keys':objscale['name']}

num_objs = len(objscale['name'])
#Number of generations, indiviuals, pop size, and objs
ngen     = 50
pop_size = 100 
ind_size = len(xbounds['name']) 
num_objs = len(objscale['name'])
w  = (-1.0, -1.0)


#State the objective function, its arguments, output, and necessary parameters (and their sizes)
sim_specs = {'sim_f': opal_deap, #fitness_opal, # This is the function whose output is being minimized
              'in': ['individual'],# These keys will be given to the above function
              'out': [('fitness_values', float, num_objs)]+ [(key,float) for key in key_dict['data_keys']] + [(key+'_long',float, 2500) for key in key_dict['data_keys']],
              'user': {'key_dict': key_dict, 
                       'basefile_name': 'sc_inj_C1',
                       'input_files_path':TOP_DIR+files,
                       'distgen_file':TOP_DIR+files+'tdist_exp_raw.yaml',
                       'zstop': 14.95, 
                       'penalty': penalty,
                       'xscales':xscale,
                       'objective_scales':objscale,
		       'cores': 2,
                       'sim_particles':simpart,
                       'sim_kill_minutes': 10.0,
                       'laser_filter': 'exp',
                       } # end user specs
            }# end sim specs


# State the generating function, its arguments, output, and necessary parameters.
gen_specs = {'gen_f': gen_f,
             'in':['sim_id'],
             'out': [('individual', float, ind_size), ('generation', int)],
             'user': {'lb': list(xbounds['lb']),
                      'ub': list(xbounds['ub']),
                      'weights': w,
                      'pop_size': pop_size,
                      'indiv_size': ind_size,
                      'cxpb': 0.8,  # probability two individuals are crossed
                      'eta': 20.0,  # large eta = low variation in children
                      'indpb': 0.8/ind_size  # end user                   
                    } # end user specs
            } # end gen specs

alloc_specs = {'out': [('given_back', bool)], 'alloc_f': alloc_f}

libE_specs['save_every_k_sims'] = 1
libE_specs['save_every_k_gens'] = 1
libE_specs['ensemble_dir_path'] = 'ensemble'
# For deap, this should be pop_size*number of generations+1?
exit_criteria = {'sim_max': 7000} #pop_size*(ngen+1)}

H0 = None

persis_info = add_unique_random_streams({}, nworkers + 1)
persis_info['next_to_give'] = 0 #len(H0)
persis_info['total_gen_calls'] = 0

## Perform the run
H, persis_info, flag = libE(sim_specs, gen_specs, exit_criteria, persis_info=persis_info, alloc_specs=alloc_specs, libE_specs=libE_specs, H0=H0)

# Saving data to file
if is_master: 
    save_libE_output(H, persis_info, 'deap_dcns_raw.npy', nworkers) 






