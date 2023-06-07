import numpy as np
import glob

files = glob.glob('*.csv')

for filename in files:
    name = filename.split('IR')[1]
    data = np.loadtxt(filename, delimiter=',')
    time = data[:,0]
    intensity = data[:,2]
    laser = np.stack((time, intensity), axis=-1)
    np.savetxt('exp_'+name+'.txt', laser, delimiter=' ')
