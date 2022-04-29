# This code was written by Le Nhan Pham (March 2022), postdoctoral research fellow at IFM Deakin University https://lenhanpham.github.io/
import math
from datetime import datetime


##### Pay attention before using this code to generate rest md itp files from grommacs dump files
##### Errors will happen if  cpA terms in the dump files are not separated by a space for example  cpA=-8.36799979e-01 in the PDIHS section
##### Use vscode to make space between cpA and minus values 
##### This error may happen to other terms like cpB 
##### The original itp file of the peptide is needed and therefore it should be in the same directory of this code together with the dump files
##### The first few lines below will repalce all "=-" with "= -": one space between = and - signs will be added.
##### Two files are needed for this code to to run: the original itp file and the dump file generated from gmx dump -s $i.tpr -param yes > $i.dump; These two files should be in the same dir of this code  


# open the dump file; find and replace "=-" with "= -""
input = r"MoS2-P28"
with open(input + ".dump", "r") as dumpfile:
    dumpdata = dumpfile.read()

dumpdata = dumpdata.replace('=-', '= -')

with open(input + ".dump", "w") as dumpfile:
    dumpfile.write(dumpdata)

# open the new dumpfile 
itprestmd = open(input + "-restmd.itp", "w")
itpfile = open(input + ".itp", "r")
dumpfile = open(input + ".dump", "r")



inputlines = itpfile.readlines()
outputlines = []

dihedrals = []

linenumber = 0
headnumber = 0

gamma = 0.693

itprestmd.write(
    "{} {} {}{} {} \n".format(
        "; This is the topol file generated for REST-MD simulations",
        "with Gamma =",
        gamma,
        ",",
        str(datetime.now())
    )
)
itprestmd.write(
    "; The code used to generate this file is written by LE NHAN PHAM, https://lenhanpham.github.io \n"
)

#### itprestmd.write the head part of itp files
for inputline in inputlines:
    inputlinesplit = inputline.strip().split()
    itprestmd.write(inputline)
    if "residue" in str(inputline):
        break
    headnumber += 1


### determine line number in itp file
def linenumber(linetype):
    line = 0
    for inputline in inputlines:
        line += 1
        if str(linetype) in inputline:
            break
    return line


def lineimproper(linetype):
    line = 0
    n = 0
    for inputline in inputlines:
        line += 1
        if str(linetype) in inputline:
            n += 1
        elif n == 2:
            break
    return line


### itprestmd.write the atom part
def atoms(headnumber):
    atoms.headnumber = headnumber
    while "residue" in str(inputlines[atoms.headnumber + 1 :]):
        for inputline in inputlines[atoms.headnumber + 1 :]:
            inputlinesplit = inputline.strip().split()
            atoms.headnumber += 1
            if "residue" in inputline:
                itprestmd.write(inputline)
            elif len(inputlinesplit) == 0:
                break
            else:
                itprestmd.write(
                    "{0:8s} {1:8s} {2:8s} {3:8s} {4:8s}  {5:8s} {6:8.4f} {7:10.4f}     {8:7.7s} {9:12.9f} {10:10.4f} \n".format(
                        inputlinesplit[0],
                        inputlinesplit[1],
                        inputlinesplit[2],
                        inputlinesplit[3],
                        inputlinesplit[4],
                        inputlinesplit[5],
                        float(inputlinesplit[6]),
                        float(inputlinesplit[7]),
                        inputlinesplit[1] + "b",
                        float(inputlinesplit[6]) * math.sqrt(gamma),
                        float(inputlinesplit[7]),
                    )
                )


### function to read parameter types
def parameterdump(parametertype):
    parameterllist = []
    for dihedralline in dumplines:
        if str(parametertype) in dihedralline:
            parameterllist.append(dihedralline)
    return parameterllist


def bondparameters(bondlines, headnumber):
    bondparameters.headnumber = headnumber
    for bondnumber in range(len(bondlines)):
        bondlinesplit = str(bondlines[bondnumber]).strip().split()
        inputline = inputlines[bondparameters.headnumber]
        inputlinesplit = inputline.strip().split()
        bondparameters.headnumber += 1
        itprestmd.write(
            "{0:8.8s} {1:8.8s} {2:8.8s}    {3:10.6e}    {4:10.6e}    {5:10.6e}    {6:10.6e} \n".format(
                inputlinesplit[0],
                inputlinesplit[1],
                inputlinesplit[2],
                float(bondlinesplit[6].rstrip(",")),
                float(bondlinesplit[8].rstrip(",")),
                float(bondlinesplit[10].rstrip(",")),
                float(bondlinesplit[12].rstrip(",")) * gamma,
            )
        )


def angles(headnumber):
    anglenumber = 0
    angles.headnumber = headnumber
    for anglenumber in range(len(anglelines)):
        anglelinesplit = str(anglelines[anglenumber]).strip().split()
        inputline = inputlines[angles.headnumber]
        inputlinesplit = inputline.strip().split()
        angles.headnumber += 1
        itprestmd.write(
            "{0:6.6s} {1:6.6s} {2:6.6s} {3:3.2s} {4:15.8e}  {5:15.8e}  {6:15.8e}  {7:15.8e}   {8:15.8e}  {9:15.8e}   {10:15.8e}   {11:15.8e} \n".format(
                inputlinesplit[0],
                inputlinesplit[1],
                inputlinesplit[2],
                inputlinesplit[3],
                float(anglelinesplit[7].rstrip(",")),
                float(anglelinesplit[9].rstrip(",")),
                float(anglelinesplit[11].rstrip(",")),
                float(anglelinesplit[13].rstrip(",")),
                float(anglelinesplit[7].rstrip(",")),
                float(anglelinesplit[9].rstrip(",")),
                float(anglelinesplit[11].rstrip(",")),
                float(anglelinesplit[13].rstrip(",")) 
            )
        )


def dihedrals(dihedrallines, headnumber):

    dihedralnumber = 0

    totalfounddihedrals = 0

    dihedrals.linecounter = 0

    for inputline in inputlines[headnumber:]:
        dihedrals.linecounter += 1
        if len(inputline.strip().split()) == 0:
            break
        else:
            dihedralnumber = 0
            loopcounter = 0
            inputlinesplit = inputline.strip().split()
            while dihedralnumber < len(dihedrallines):
                ### check if the index of dihedrals found in the dump file out range of index of dihedral list.
                ### If true, set all the last index to max value of index by substraction of 1, and set all values
                ### of atoms in dihedrals to 0 to ensure that the second condition is performed
                if totalfounddihedrals < len(dihedrallines):
                    dihedrallinesplit = (
                        str(dihedrallines[totalfounddihedrals]).strip().split()
                    )
                else:
                    totalfounddihedrals = len(dihedrallines) - 1
                    dihedrallinesplit = (
                        str(dihedrallines[totalfounddihedrals]).strip().split()
                    )
                    dihedrallinesplit[3] = "0"
                    dihedrallinesplit[4] = "0"
                    dihedrallinesplit[5] = "0"
                    dihedrallinesplit[6] = "0"
                if (
                    int(inputlinesplit[0]) == int(dihedrallinesplit[3]) + 1
                    and int(inputlinesplit[1]) == int(dihedrallinesplit[4]) + 1
                    and int(inputlinesplit[2]) == int(dihedrallinesplit[5]) + 1
                    and int(inputlinesplit[3]) == int(dihedrallinesplit[6]) + 1
                ):
                    itprestmd.write(
                        "{0:8.8s} {1:8.8s} {2:8.8s} {3:8.8s} {4:6.6s} {5:6.2f}    {6:15.8e}    {7:2d}    {8:6.2f}    {9:15.8e}    {10:2d} \n".format(
                            inputlinesplit[0],
                            inputlinesplit[1],
                            inputlinesplit[2],
                            inputlinesplit[3],
                            inputlinesplit[4],
                            float(dihedrallinesplit[8].rstrip(",")),
                            float(dihedrallinesplit[10].rstrip(",")),
                            int(dihedrallinesplit[15].lstrip("mult=")),
                            float(dihedrallinesplit[12].rstrip(",")),
                            float(dihedrallinesplit[14].rstrip(",")) * gamma,
                            int(dihedrallinesplit[15].lstrip("multi=")),
                        )
                    )
                    dihedralnumber += 1
                    totalfounddihedrals += 1
                    loopcounter += 1
                ### if no parameters are found in the dump file, only atom indices of these dihedrals are taken and paramters are set to zero
                ### in this case, loopcounter is zero, meaning that no paramters are found in the dump file
                elif loopcounter == 0:
                    itprestmd.write(
                        "{0:8.8s} {1:8.8s} {2:8.8s} {3:8.8s} {4:6.6s} {5:6.2f}    {6:15.8e}    {7:2d}    {8:6.2f}    {9:15.8e}    {10:2d} \n".format(
                            inputlinesplit[0],
                            inputlinesplit[1],
                            inputlinesplit[2],
                            inputlinesplit[3],
                            inputlinesplit[4],
                            0,
                            0,
                            1,
                            0,
                            0,
                            1,
                        )
                    )
                    ### set diheralnumber to len of dihedral matrix to break the while loop when no values of dihedral parameters
                    ### are found in the dump file, and all of them are set to zero as above
                    dihedralnumber = len(dihedrallines)
                    ### if parameters are found in the dump files (loopcounter is not zero), they are taken already above, and the loop should be
                    ### breaken to ensure that atom indices of dihedrals are not considered anymore
                elif loopcounter != 0:
                    dihedralnumber = len(dihedrallines)


def idihedrals(dihedrallines, headnumber):
    dihedralnumber = 0
    totalfounddihedrals = 0
    idihedrals.linecounter = 0
    for inputline in inputlines[headnumber:]:
        idihedrals.linecounter += 1
        if len(inputline.strip().split()) == 0:
            break
        else:
            dihedralnumber = 0
            loopcounter = 0
            inputlinesplit = inputline.strip().split()
            while dihedralnumber < len(dihedrallines):
                ### check if the index of dihedrals found in the dump file out range of index of dihedral list.
                ### If true, set all the last index to max value of index by substraction of 1, and set all values
                ### of atoms in dihedrals to 0 to ensure that the second condition is performed
                if totalfounddihedrals < len(dihedrallines):
                    dihedrallinesplit = (
                        str(dihedrallines[totalfounddihedrals]).strip().split()
                    )
                else:
                    totalfounddihedrals = len(dihedrallines) - 1
                    dihedrallinesplit = (
                        str(dihedrallines[totalfounddihedrals]).strip().split()
                    )
                    dihedrallinesplit[3] = "0"
                    dihedrallinesplit[4] = "0"
                    dihedrallinesplit[5] = "0"
                    dihedrallinesplit[6] = "0"
                if (
                    int(inputlinesplit[0]) == int(dihedrallinesplit[3]) + 1
                    and int(inputlinesplit[1]) == int(dihedrallinesplit[4]) + 1
                    and int(inputlinesplit[2]) == int(dihedrallinesplit[5]) + 1
                    and int(inputlinesplit[3]) == int(dihedrallinesplit[6]) + 1
                ):
                    itprestmd.write(
                        "{0:8.8s} {1:8.8s} {2:8.8s} {3:8.8s} {4:6.6s} {5:6.2f}    {6:15.8e}    {7:6.2f}    {8:15.8e} \n".format(
                            inputlinesplit[0],
                            inputlinesplit[1],
                            inputlinesplit[2],
                            inputlinesplit[3],
                            inputlinesplit[4],
                            float(dihedrallinesplit[8].rstrip(",")),
                            float(dihedrallinesplit[10].rstrip(",")),
                            float(dihedrallinesplit[12].rstrip(",")),
                            float(dihedrallinesplit[14].rstrip(",")) * gamma,
                        )
                    )
                    dihedralnumber += 1
                    totalfounddihedrals += 1
                    loopcounter += 1
                ### if no parameters are found in the dump file, only atom indices of these dihedrals are taken and paramters are set to zero
                ### in this case, loopcounter is zero, meaning that no paramters are found in the dump file
                elif loopcounter == 0:
                    itprestmd.write(
                        "{0:8.8s} {1:8.8s} {2:8.8s} {3:8.8s} {4:6.6s} {5:6.2f}    {6:15.8e}    {7:6.2f}    {8:15.8e} \n".format(
                            inputlinesplit[0],
                            inputlinesplit[1],
                            inputlinesplit[2],
                            inputlinesplit[3],
                            inputlinesplit[4],
                            0,
                            0,
                            1,
                            0,
                        )
                    )
                    ### set diheralnumber to len of dihedral matrix to break the while loop when no values of dihedral parameters
                    ### are found in the dump file, and all of them are set to zero as above
                    dihedralnumber = len(dihedrallines)
                    ### if parameters are found in the dump files (loopcounter is not zero), they are taken already above, and the loop should be
                    ### breaken to ensure that atom indices of dihedrals are not considered anymore
                elif loopcounter != 0:
                    dihedralnumber = len(dihedrallines)


def cmap(headnumber):
    for inputline in inputlines[headnumber:]:
        inputlinesplit = inputline.strip().split()
        if "[ cmap ]" in str(inputline):
            itprestmd.write(inputline)
        elif len(inputlinesplit) != 0 and "[ cmap ]" not in str(inputline):
            itprestmd.write(inputline)
        elif len(inputlinesplit) == 0:
            break
    headnumber += 1


##### Start using functions to itprestmd.write paramters 
### atom parameters
headnumber = linenumber("atoms") 
atoms(headnumber)

### bond paramters
headnumber = linenumber("bonds") - 1
itprestmd.write("\n")
itprestmd.write(inputlines[headnumber])
itprestmd.write(inputlines[headnumber + 1])

#### generate list of bond parameters from dump file
dumplines = dumpfile.readlines()
bondlines = parameterdump("(BONDS)")

bondparameters(bondlines, headnumber + 2)

#### itprestmd.write pair list
headnumber = linenumber("pairs") - 1

itprestmd.write("\n")
while len(inputlines[headnumber].strip().split()) != 0:
    itprestmd.write(inputlines[headnumber])
    headnumber += 1


####### Angle part
headnumber = linenumber("angles") - 1
itprestmd.write("\n")
itprestmd.write(inputlines[headnumber])
itprestmd.write(inputlines[headnumber + 1])
anglelines = parameterdump("(UREY_BRADLEY)")
angles(headnumber + 2)


##### itprestmd.write proper dihedral parameters
headnumber = linenumber("dihedrals") - 1
itprestmd.write("\n")
itprestmd.write(inputlines[headnumber])
itprestmd.write(inputlines[headnumber + 1])
dihedrallines = parameterdump(parametertype="(PDIHS)")
dihedrals(dihedrallines, headnumber + 2)


#### itprestmd.write improper dihedral parameters
headnumber = lineimproper("dihedrals") - 2
itprestmd.write("\n")
itprestmd.write(inputlines[headnumber])
idihedrallines = parameterdump(parametertype="(IDIHS)")
idihedrals(idihedrallines, headnumber + 2)

#### CMAP
headnumber = linenumber("cmap") - 1
itprestmd.write("\n")
cmap(headnumber)


itprestmd.close()
itpfile.close()
dumpfile.close()

#### End of making resd md itp file 
