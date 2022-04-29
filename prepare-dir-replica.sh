module load gromacs/2021.4 


currdir=$(pwd)

for i in {0..15}; do
    cd $currdir 
	mkdir replica_${i} 
	cp -r mdp replica_${i}
	rm replica_${i}/*.gro
    rm replica_${i}/*.pdb 
    rm replica_${i}/*.top 
    cp replica_${i}.pdb replica_${i}/ 
    gmx solvate -cp replica_${i}.pdb -cs spc216.gro -o replica_${i}.gro   
    mv replica_${i}.gro replica_${i}/ 
    cp replica_x.top replica_${i}/replica_${i}.top 
    cd $currdir/replica_${i}/mdp 
 	for j in `ls *.mdp`; do 
		sed -i -e "s/lllll/${i}/" $j 
	done 
done 

### redirect output to a txt file for grepping SOL later.