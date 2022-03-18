#!/bin/bash 

#SBATCH --partition=shared
#
#SBATCH --job-name=test
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt

#SBATCH --ntasks=4
######SBATCH --cpus-per-task=5
#####SBATCH --mem-per-cpu=1g

#SBATCH --time=00:20:00
# Export SLURM_EXACT because of the new behavior in 21.08
export SLURM_EXACT=1

module remove openmpi
module load devtoolset/9
module list

source ~/.bashrc
export PATH=/gpfs/slac/staas/fs1/g/accelerator_modeling/nneveu/software/OPAL/opal_mpich/bin/:$PATH

/gpfs/slac/staas/fs1/g/accelerator_modeling/nneveu/software/OPAL/opal_mpich/bin/mpiexec -n 9 python call_aposmm.py

#
# Print the date again -- when finished
echo Finished at: `date`
