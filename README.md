# Step to prepare all files for REST MD
1. Prepare replica_x.pdp files by using pymol (add peptide to the surface and export structures to pdb)
2. Use prepare-dir-replica.sh to prepare all replica_x dirs
3. Copy output of solvation process to a txt file (solvent.txt)
4. Use gep-solvent.shell to collect all water numbers added 
5. Copy water number to vscode and then import all to excell to calculate the numbers of water molecules needed to add to individual replica to have the same number of water molecules in all replica 
6. Copy numbers of water molecules to the add-more-water.sh and then use this command to add water 
7. Update the top files by using update-top-file.shell 
8. If ions are needed, add ion to the replica by using add-ion.shell
9. Rescale charge of ion state B to have neutral system for stateB: sum all charge of stateB of peptide and then add this charge to stateB of the ion (CLAb for example) in the ions.itp 
10. Check if the surface itp exists in the running dir, and then check the forcefield.itp to comment out the ffbonded.itp for safe running (ensure that rest md will use parameters in the peptide-restmd.itp only)
11. Run md 
 

###########For the purpose of the REST-MD simulations (for which the MoS2 substrate is held fixed, so we don't need to calculate the internal vdW interactions within the slab), we only need to consider one type of Mo and one type of Sulfur for MoS2. We need **one** file, it should be called ffnonbonded-REST.itp, and it needs to contain (1) the regular (state A) and state B [atomtypes] section, and then (2) the regular (state A) and state B [pairtypes] section, followed by (3) the regular (state A) and state B [nonbond params] section. The regular (state A) and state B [nonbond params] section should contain all the MoS2/peptide bespoke cross terms.

 

