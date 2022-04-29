#!/bin/bash 
#SBATCH --nodes 1
#SBATCH --partition gpgpu 
#SBATCH --qos=gpgpudeakin 
#SBATCH -A pDeak0004
#SBATCH --gres=gpu:4  
#SBATCH --ntasks=16     
#SBATCH --cpus-per-task=1  
#SBATCH --mem=40000M  
#SBATCH --gres-flags=enforce-binding
#SBATCH --time=07-00:00:00 


source /usr/local/module/spartan_new.sh
module load fosscuda/2020b
module load gromacs/2021
export OMP_NUM_THREADS=1 

nt=${OMP_NUM_THREADS} 

currdir=$(pwd)  

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
    mpirun -np 16 --oversubscribe gmx_mpi mdrun -ntomp $nt -deffnm min_${conf} 

    gmx grompp -f mdp/500ps.mdp -p $conf.top -o ${conf}-500ps -c min_${conf} -t min_${conf} -po ${conf}-500ps -n $conf.ndx #-maxwarn 1 
    mpirun -np 16 --oversubscribe gmx_mpi mdrun -ntomp $nt -deffnm ${conf}-500ps  
  
    gmx grompp -f mdp/anneal.mdp -p $conf.top -c ${conf}-500ps -o ${conf}-ann -po ${conf}-ann -n $conf.ndx #-maxwarn 1 
    mpirun -np 16 --oversubscribe gmx_mpi mdrun -ntomp $nt -deffnm ${conf}-ann          

    gmx grompp -f mdp/nvt.mdp -p $conf.top -o $binaryfile -c ${conf}-ann -t ${conf}-ann -po ${conf}-rest -n $conf.ndx #-maxwarn 1 
done

cd $currdir

mpirun -np 16 --oversubscribe gmx_mpi mdrun -ntomp ${nt} -multidir replica_0 replica_1 replica_2 replica_3 replica_4 replica_5 replica_6 replica_7 replica_8 replica_9 replica_10 replica_11 replica_12 replica_13 replica_14 replica_15 -s $binaryfile -replex 1000 -dhdl dhdl.xvg #-cpi state.cpt 

	





#gmx mdrun -ntmpi 1 -ntomp $nt -nb gpu -deffnm ${conf}-rest -cpi ${conf}-rest -append 

   #mpirun -np 16 --oversubscribe gmx_mpi mdrun -ntomp ${nt} -nb gpu -pme gpu -bonded gpu -pmefft gpu -multidir  replica_0 replica_1 replica_2 replica_3 replica_4 replica_5 replica_6 replica_7 replica_8 replica_9 replica_10 replica_11 replica_12 replica_13 replica_14 replica_15 -s $binaryfile -replex 1000 -cpi state.cpt        
   
   


