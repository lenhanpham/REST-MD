#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --partition=gpuq
#SBATCH --constraint=v100
#SBATCH --ntasks-per-node=16    
#SBATCH --ntasks=16 
#SBATCH --gres=gpu:2    
#SBATCH --mem=80gb 
#SBATCH --time=24:00:00
#SBATCH --account=xxxx   
#SBATCH --export=NONE

module load gromacs-gpu/2021.2 
 
currdir=$(pwd) 
    
nt=1 

makeindex() 
{ 
echo "q" | gmx make_ndx -f $conf.gro -o $conf.ndx  
}

for i in {0..15}; do 
    cd $currdir/replica_${i} 
	conf=replica_${i} 
	binaryfile=topol 
    makeindex  

    gmx grompp -f mdp/min.mdp -p $conf.top -o min_${conf} -c ${conf} -po min_${conf} -pp min_${conf} -n $conf.ndx #-maxwarn  
    srun --export=all -n $SLURM_NTASKS mdrun_mpi -ntomp $nt -deffnm min_${conf} 

    gmx grompp -f mdp/500ps.mdp -p $conf.top -o ${conf}-500ps -c min_${conf} -t min_${conf} -po ${conf}-500ps -n $conf.ndx #-maxwarn 1 
    srun --export=all -n $SLURM_NTASKS mdrun_mpi -ntomp $nt -deffnm ${conf}-500ps  
  
    gmx grompp -f mdp/anneal.mdp -p $conf.top -c ${conf}-500ps -o ${conf}-ann -po ${conf}-ann -n $conf.ndx #-maxwarn 1 
    srun --export=all -n $SLURM_NTASKS mdrun_mpi -ntomp $nt -deffnm ${conf}-ann          

    gmx grompp -f mdp/nvt.mdp -p $conf.top -o $binaryfile -c ${conf}-ann -t ${conf}-ann -po ${conf}-rest -n $conf.ndx #-maxwarn 1 
done

cd $currdir

   srun --export=all -n $SLURM_NTASKS mdrun_mpi -ntomp $nt -multidir replica_0 replica_1 replica_2 replica_3 replica_4 replica_5 replica_6 replica_7 replica_8 replica_9 replica_10 replica_11 replica_12 replica_13 replica_14 replica_15 -s $binaryfile -replex 1000 -cpi state.cpt       


	
	#gmx mdrun -ntmpi 1 -ntomp $nt -nb gpu -deffnm ${conf}-rest -cpi ${conf}-rest -append 
   


