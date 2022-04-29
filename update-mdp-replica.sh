


currdir=$(pwd)

for i in {0..15}; do
    cp -r $currdir/mdp $currdir/replica_${i}
    cd $currdir/replica_${i}/mdp 
 	for j in `ls *.mdp`; do 
		sed -i -e "s/lllll/${i}/" $j 
	done 
done 

