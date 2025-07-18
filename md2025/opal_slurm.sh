#! /bin/bash

#SBATCH --account=#! /bin/bash

#SBATCH --partition=milano
#SBATCH --job-name=Opal
#SBATCH --output=job_%j.out
#SBATCH --error=job_%j.err
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4g
#SBATCH --time=0-0:05:00
#--exclude=sdfmilan[023-026.120]

#SBATCH --exclusive
# This script is used to submit opal jobs through the slurm manager on s3df. 
# it takes an input (sc_inj.in) 
# Example usage: sbatch  slurm.sh


echo -e Started at: `date` 
echo -e "Master process running on: $HOSTNAME"  
echo -e "job ID: $SLURM_JOBID"

# Copy files to a scratch directory where the simulation will run.
#-------------
cwd=$PWD
echo -e "Calling directory:" $cwd
echo -e $USER

#-----------
# Make sure correct paths are set by loading the module used to compile Genesis4
#-----------
#source /sdf/group/ad/beamphysics/paris/software/elegant/setup_elegant
#-------------
source /sdf/data/ad/ard/u/paris/spack/share/spack/setup-env.sh

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sdf/data/ad/ard/u/paris/spack/var/spack/environments/milano_opal/.spack-env/view/lib
export LIBRARY_PATH=$LIBRARY_PATH:/sdf/data/ad/ard/u/paris/spack/var/spack/environments/milano_opal/.spack-env/view/lib
export SRC_DIR=/sdf/data/ad/ard/u/paris
export PREFIX=/sdf/data/ad/ard/u/paris/OPAL/install
export OTB_PREFIX=$PREFIX
export LIBRARY_PATH=$LIBRARY_PATH:$PREFIX
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PREFIX

spack env activate milano_opal

#mkdir -p "/sdf/scratch/$USER" #make scratch directory, if needed
#scratch="/sdf/scratch/$USER/Elegant_$SLURM_JOBID"  #LSCRACTCH would be better, but Genesis is not smart enough to cat across nodes yet. Should work on that sometime.
#mkdir $scratch
#cp *.wake $scratch # cp fails if there is no file, so we will use find
#find . -maxdepth 1 -type f -iname "*.ele" -exec cp {} "$scratch/" \; && true
#find . -maxdepth 1 -type f -iname "*.lte" -exec cp {} "$scratch/" \; && true
#cd $scratch
echo -e "Working dir:" $PWD

OPAL=/sdf/data/ad/ard/u/paris/OPAL/install/bin/opal
#OPALMPI=/sdf/group/ad/beamphysics/nneveu/spack/var/spack/environments/opalenv/.spack-env/view/bin/mpirun
OPAL=${OPAL}
#OPALMPI=${OPALMPI}
# #----------
# # print inputfile to log. Assumes only one input file in folder.
# #----------
tmp=(*.in)
inputfile=${tmp[0]}
echo -e "" 
cat $inputfile
echo  "" 


#-------
# Run elegant. Use timeout to kill elegant, if needed, and report status. Important since sometimes it hangs. Perhaps when s3df is mature we won't need this.
# timeout -k 5 xxm  will kill the sim after xx minutes (in the case that it hangs). It will also kill the simulation if hasn't finished, so you should always set the timeout to be longer than the SBATCH --time option.
#-------
#timeout -k 5 35m $OPALMPI $OPAL $inputfile
#mpirun $OPAL $inputfile

mpirun -np 16 $OPAL
#mpirun -np 16 $OPAL $inputfile
exit_status=$? 
if [[ $exit_status -gt 100 ]]; then 
   echo -e "timeout opal aborted" 
fi 

#------
#Clean up files we don't want, and copy the rest of the output to the original working directory. 
#------
sleep 1  
#cp ./* $cwd
#rm -rf $scratch # clean up scratch directory. Can be commented out, since admin's auto-purge scratch.

#finish time 
echo Finished executing slurm script at: `date`
