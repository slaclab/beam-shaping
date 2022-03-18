#!/bin/bash 

#SBATCH --partition=shared
#
#SBATCH --job-name=test
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt

#SBATCH --ntasks=4
######SBATCH --cpus-per-task=5
#####SBATCH --mem-per-cpu=1g

#SBATCH --time=00:10:00

# Export SLURM_EXACT because of the new behavior in 21.08
export SLURM_EXACT=1

# Using my own mpi
module remove openmpi
module load devtoolset/9
module list

# Setting some enviornment variables
source ~/.bashrc
export PATH=/gpfs/slac/staas/fs1/g/g.beamphysics/nneveu/software/OPAL/opal_mpich/bin/:$PATH

/gpfs/slac/staas/fs1/g/g.beamphysics/nneveu/software/OPAL/opal_mpich/bin/mpiexec -n 32 opal sc_inj_C1.in

#
# Print the date again -- when finished
echo Finished at: `date`
