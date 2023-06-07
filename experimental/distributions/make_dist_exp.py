import numpy as np
import matplotlib.pyplot as plt
import glob, sys, h5py
import seaborn as sns

import distgen
from distgen import *
from distgen import Generator
from distgen.writers import *
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.plot import marginal_plot

#2022
sim_test     = 'tdist_sim.yaml'
exp_nofilter = 'tdist_exp1_nofilter.yaml'
exp_p1000fs  = 'tdist_exp2_p1000fs.yaml'
exp_gauss    = 'tdist_exp_gauss.yaml'

#2023
exp_raw    = 'tdist_exp_raw.yaml'
exp_smooth = 'tdist_exp_smooth.yaml'

for filename in [exp_raw, exp_smooth]: #exp_gauss, sim_test, sim_test, exp_nofilter,exp_p1000fs]:
    ext = filename.split('.')[0]
    dist = Generator(input_file=filename, verbose=True)
    dist.run()
    particles = dist.particles
    particles.write_opal('opal_emitted_'+ext+'.txt', dist_type= 'emitted')
