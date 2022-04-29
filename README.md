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
10. Check if the surface itp exists in the running dir, and then check the forcefield.itp to comment out the forcefield.itp for safe running (ensure that rest md will use parameters in the peptide-restmd.itp only)
11. Run md 

# Prepare the restmd.itp file of peptides
**REST: FILE PREPARATION & HOW-TO for CHARMM variants in GMX**

**Tiff Walsh, Sept 2012, Updated 2013, 2014, 2015….2022**

 

*Recent important changes: Updated for ion scaling and const. cell volume reminder, Sept 2013.*

 

**In the following example, gamma = 0.6. DO NOT use this value in your own work (it is for example purposes only!!!) - you will need to determine your own gamma!! e.g. for a temperature window of 300-430 K,** 

**gamma = 300/430= 0.693**

 

 

**PHASE 1: PREPARE THE FORCE-FIELD FILES FOR YOUR CHOSEN TEMPERATURE WINDOW**

 

1. Set up a     normal md runof the peptide in vacuum      (make a *.tpr file) and use gmxdump to obtain a printout of all     parameters used in the forcefield.

 

1. **Delete ffbonded.itp in your working \*.ff     directory,** and delete     any reference to it in forcefield.itp. Your forcefield.itp file should be     pretty clean-looking at this stage. Total forcefield.itp file is below:

 

[ defaults ]

; nbfunc  comb-rule  gen-pairs  fudgeLJ  fudgeQQ

1    2   yes  1.0  1.0

 

\#include "ffnonbonded.itp"

\#include "cmap.itp"

\#include "ions.itp"

 

 

1. Start     with editing your topology file. In the [atoms] directive, define your     typeB atoms as different atom types, e.g.

[ atoms ]

;  nr    type resnr residue atom  cgnr     charge mass    type  chargeB     massB

​    1    NP   1  PRO     N    1   -0.0700  14.0070   NPb -0.0612  14.007

​    2    HC   1  PRO H1    1    0.2400      1.0080   HCb   0.2099    1.0080

​    3    HC   1  PRO H2    1    0.2400      1.0080   HCb   0.2099    1.0080

​    4   CP3   1  PRO CD    1    0.1600     12.0110   CP3b   0.1399 12.0110

​    5    HA   1  PRO   HD1    1    0.0900 1.0080   HAb  0.0787    1.0080

 

**Scale the charges** in the chargeB column as per the definition of your effective temperature window; defined as **sqrt(beta_high/beta_low) = sqrt(gamma)**, from Terakawa et al. (2010).

 

 

1. Continue     editing the topology file, now adding the explicit bond stretching     parameters (taken from gmxdump) for each bond, giving both the stateA and     then stateB values on each line -- the first entry (ideal bond length)     does not change between stateA and stateB. **Bond stretch force constants must be scaled by gamma (not     sqrt[gamma]):**

 

[ bonds ]

; ai  aj funct        c0       c1       c2       c3

​    1    2    1    1.04000e-01  3.37230e+05  1.04000e-01  2.02338e+05

​    1    3    1    1.04000e-01  3.37230e+05  1.04000e-01  2.02338e+05

​    1    4    1    1.04000e-01  3.37230e+05  1.04000e-01  2.02338e+05

 

 

1. Next, if     you ARE NOT using the CHARMM family of force-fields, edit the [ angles ]     directive in the topology file in a similar way. IF you are using CHARMM, do     not make any alterations - leave this part unscaled. The reason for     this is because the Urey-Bradley form is used for the angle term. In GMX,     Urey-Bradley contributions cannot be scaled using the free-energy     perturbation code....So - this means forget about it. Just slot them in as     normal, don’t try to scale them, or break these contribs. apart (will mess     up your 1-3 list etc). 

 

1. The next     step is to edit the [ dihedrals ] directive in the topology file (for the     proper dihedrals - in CHARMM they are “type 9”, not to be confused with     the improper dihedrals which are “type 2” in CHARMM). **Here you need to be super careful and use the GMXDUMP output to     make sure that the multiply-defined proper dihedrals are repeated in sequence (one directly     after the other) AND in the correct order (see bold     section below).** This format is guaranteed if you use the     gmxdump output as your guide. As for the bonds and angles, **your force constants must be scaled     by gamma for stateB:**

 

[ dihedrals ]

; ai  aj   ak   al funct    c0   c1   c2    c3 c4     c5

 2 1 5 6 9 0.00000000E+00 0.41839999E+00 3 0.00000000E+00 0.25103999E+00 3

 2 1 5 7 9 0.00000000E+00 0.41839999E+00 3 0.00000000E+00 0.25103999E+00 3

 2 1 5 11 9 0.00000000E+00 0.41839999E+00 3 0.00000000E+00 0.25103999E+00 3

….. ….. etc

 **5 11 13 15 9 0.00000000E+00 0.66943998E+01 1 0.00000000E+00    0.40166399E+01 1**

 **5 11 13 15 9 0.18000000E+03 0.10460000E+02 2 0.18000000E+03    0.62760000E+01 2**

**….. ….. etc**

 

​    

1. Finish up     your changes to the topology file by editing the [ dihedrals ] directive     for the improper dihedrals (“type 2” dihedrals in charmm): again, **scale the force constants by gamma**     for stateB:

 

 

[ dihedrals ]

; ai  aj   ak   al funct        c0       c1       c2        c3

  11  5    13   12   2    0.00000E+00  0.10042E+04  0.00000E+00    0.60250E+03

  13  11   15   14   2   0.00000E+00   0.16736E+03  0.00000E+00    0.10042E+03

  32  15   34   33   2   0.00000E+00   0.10042E+04  0.00000E+00    0.60250E+03

 

 

1. The other     directive entries in the topology file, such as [     cmap ] (only required for Proline and Glycine)     and [     pairs ] should not be edited. Put them at the end of     the file if they are not already there.

 

1. The next     file you need to edit is ffnonbonded.itp. In this file, under the [ atomtypes ] directive,     you need to define sigma & epsilon values for your stateB atom types     (e.g. NPb, HCb, etc - see Item 3, where stateB atomtypes were first     introduced). The new atomtypes and their sigma/epsilon values must be     given one per line, one their own line (not sharing with the stateA     atomtypes and values). **Scale the     epsilon values by gamma, and the charges by sqrt(gamma)** [*although, this shouldn’t matter because     the topology charges should take precedence...but just in case......*]     e.g.:

 

[ atomtypes ]

;name  at.num  mass  charge  ptype  sigma   epsilon

C  6  12.01100  0.51  A  0.356359487256  0.46024

CA  6  12.01100  -0.115  A  0.355005321205  0.29288

CC  6  12.01100  0.62  A  0.356359487256  0.29288

…... ….. etc

;

; now for stateB definitions

;

  Cb 6  12.01100  0.395   A   0.356359487256 0.2761440

 CAb 6  12.01100 -0.089   A   0.355005321205 0.1757280

 CCb 6  12.01100  0.480   A   0.356359487256 0.1757280

…... ….. etc

 

 

1. Then edit     the [     pairtypes ] directive, again adding new pairs for all     stateB atoms, each on their own line; **epsilon     values are scaled by gamma**:

 

[ pairtypes ]

; i  j  func  sigma1-4  epsilon1-4 ; THESE ARE 1-4 INTERACTIONS

CP1  CP1  1  0.338541512893  0.04184

CP1  CP2  1  0.338541512893  0.04184

CP1  CP3  1  0.338541512893  0.04184

CP1  CPT  1  0.338541512893  0.12552

…. etc ….

;

; now for stateB pairtypes

;

 CP1b  CP1b      1    0.338541512893 0.025104000000

 CP1b  CP2b      1    0.338541512893 0.025104000000

 CP1b  CCb       1    0.347450500074 0.066418940913

…. etc ….

 

 

 

1. **NOTE:** if your peptide     carries an overall CHARGE, and you are using counterions to balance this     charge, then this counter-charge (AND ONLY this countercharge) must be     scaled. Consider the peptide PLUS countercharge as the “biomolecule”. To     avoid confusion, you should create a NEW ion atom type - e.g. if you need     CL ions, create an atom type called CLP. 

2. 1. **You need to assign some CL ions in your gro file as      CLP.**
   2. **You must update your topol.top file accordingly to      reflect this change (so there are x number of CLP atoms in the system, in      the right running order).**
   3. **You must edit the ffnonbonded entry - add an entry      for CLP with the same params as CL. Similarly, add a CLPb entry with      scaled params.**
   4. **You MUST edit ions.itp too - this is to ensure the      right CL atoms end up getting scaled in stateB. ) This is necessary for      this counterion to make sure the system described by stateB (and thus      any admixture of stateA & stateB) is charge-neutral.** This may involve tweaking the last decimal place of a few of the      scaled charges on the peptide to get the overall charge close enough to      zero.....**(CHECK THE NOTES AND      WARNINGS AFTER GROMPP!!)**

**Note: Should calculate total charge of StateB of the used peptide in the itp file, and the StateB of CLPb (or cation NA,K,..) should be scaled to cancel the charge of the stateB of peptide in the ions.itp** 

 

 

**The ions.itp entry looks like this:**

[ moleculetype ]

; molname  nrexcl

CLP      1

 

[ atoms ]

; id  at type     res nr residu name at name cg nr charge  

1    CLP       1    CLP      CLP   1    -1  35.45 CLPb -0.775 35.45

 

 

There is a secondary issue if you wish later on to add additional salt ions (say to test ionic strength effects). The extra ions in your system should not be FEP scaled - this is why you should define two sets of ion params for Chloride in this instance (one for solute--charge-balancing and the other, unscaled, for general purpose).

 

1. Once you     have prepared all the files, I suggest you run some example runs (with     same MD seed) to check the     lambda=0.0 (no admixture, all unscaled), lambda=1.0 (no admixture, all     scaled), and lambda=0.5 cases (50:50 admixture of 0.0 and 1.0 cases) - as     in Terakawa et al (2010). See the mdp file addition in the Item below to     get the parameter scaling stuff working.

 

1. Now     prepare a .mdp file - one for each lambda value (i.e. each “effective     temperature” between your highest and lowest “effective temperature”). **Remember that each replica will be run     at the same physical temperature (e.g. 300K)**. Include the free energy     directives as below, altering the value of lambda to scale between 0.0     (your reference replica) and 1.0 (the replica for your highest effective     temperature). Eventually you will have to adjust the spacing (in lambda     space) between the replicas to ensure that the exchange probability     between adjacent replicas is as even as you can get it. Below are the     relevant settings for the XXXth replica: (where XXX is an integer between     0 and n-1, where n is the number of replicas). Note the entries for the     lambdas (0.0 0.057 0.114 0.177 etc...) should be on one continuous line     (without line breaks):

 

; Free energy control stuff
 free_energy       = yes
 ;set init-lambda to the lambda value for the replica
 ;no linger used in 4.6.x use init_lamdba state instead
 ;init_lambda       = 0.0
 ;delta-lambda =0 needed for H-REMD
 delta_lambda       = 0
 ;foreign_lambda       = 0
 sc_alpha         = 0
 sc_power         = 0
 sc_sigma         = 0.3
 init_lambda_state    = XXX
 coul-lambdas       = 0.0 0.057 0.114 0.177 0.240 0.310 0.382 0.458 0.528 0.597 0.692 0.750 0.803 0.855 0.930 1.000 
 vdw-lambdas       = 0.0 0.057 0.114 0.177 0.240 0.310 0.382 0.458 0.528 0.597 0.692 0.750 0.803 0.855 0.930 1.000 
 bonded-lambdas      = 0.0 0.057 0.114 0.177 0.240 0.310 0.382 0.458 0.528 0.597 0.692 0.750 0.803 0.855 0.930 1.000 

 

**PHASE 2: SETTING UP THE REST RUN**

 

1. Setup each     replica in a separate directory, named replica_0, replica_1, replica_2,     ...etc . Set up the mdp file in     each directory such that you run each replica at the same physical     temperature (ie 300 K), but with a different value of “init_lambda_state”     (shown as XXX in Step 13). **In each replica directory, use the     same name for the .tpr file (in this example, we use topol.tpr).**

 

1.  Generate an initial configuration for     each replica - advisable to have different starting configs for each     replica unless you have a specific test you wish to run....Equilibrate     each replica at the same temperature (eg 300 K) but with different lambda     values for at least 0.5 ns. ***If you are running an NVT REST run, the     cell dimensions for each replica must be the same.\***

 

1. In the     top working directory (such that sub-directories 0, 1 2, 3 etc are     immediately underneath), execute the following command (for an example of     12 replicas, with an attempted exchange interval of 1000 steps):

 

GMX5 on avoca, slurm command:

srun --ntasks-per-node=16 mdrun_mpi -multidir replica_? replica_?? -s topol.tpr 
 -cpi state.cpt -ntomp 4 -dd 2 7 2 -npme 4 -maxh 140 -noappend -replex 1000 

 

GMX 4.5.X on barcoo:

mpirun mdrun -s mdrun.tpr -multidir 0 1 2 3 4 5 6 7 8 9 10 11 -replex 1000 

 

The multidir flag ensures the .tpr file is read from the replica_0, replica_1, replica_2 etc directories, and that the output from the simulation is written to each directory appropriately.

 

1. ...That     should be enough info?

 

**PHASE 3: Restarting REST from a crash**

 

Let's say, for arguments sake that your job crashed when the last time frame was 4125, and you had intended that the job run for 8000 steps. You need to make up an extra 3875 steps.

 

cd into each directory, (from list 0,1,2,3...etc up to 15) and do the following. copy your mdp file for each value of lambda in each directory (say it's called grompp.mdp):

 

cp grompp.mdp contin.mdp

 

now edit contin.mdp. You need to change the following things

init_step = 4125

nsteps = 3875

gen_vel = no

(this last one is very important, otherwise gmx will ignore the velocities in the last frame and generate a new set of velocities)

 

then you need to grompp. For this you need the old .trr file (called traj-old.trr in this example) and ideally, the .edr file (called ener-old.edr). Make sure you don't end up overwriting anything when you restart your run (I'd still use the extend script to do mv stuff).

 

In each directory, do the following

 

grompp -f contin.mdp -t traj-old.trr -o mdrun.tpr -c latest-frame.gro -e ener-old.edr

 

(you need to make sure that the latest timestep matches the latest frame - otherwise amend init_step to reflect the last frame for which you have a .gro file - obtain from the .xtc file if necessary using tbpconv) *If you change init_step, then you must also change nsteps accordingly (to keep to your total of 8000 steps).

 

then set up your slurm script with this type of command (below) - it's the same as before (without the -cpi state.cpt and without the noappend) - modify for your number of directories etc.

 

module load gromacs-xl/4.5.5-p1 ; srun --ntasks-per-node=64 mdrun_mpi_bg -s mdrun.tpr -multidir 0 1 2 3 -replex 1000 -c out.gro

 

I've tried this and it runs on avoca.



 

For the purpose of the REST-MD simulations (for which the MoS2 substrate is held fixed, so we don't need to calculate the internal vdW interactions within the slab), we only need to consider one type of Mo and one type of Sulfur for MoS2. We need **one** file, it should be called ffnonbonded-REST.itp, and it needs to contain (1) the regular (state A) and state B [atomtypes] section, and then (2) the regular (state A) and state B [pairtypes] section, followed by (3) the regular (state A) and state B [nonbond params] section. The regular (state A) and state B [nonbond params] section should contain all the MoS2/peptide bespoke cross terms.

 

