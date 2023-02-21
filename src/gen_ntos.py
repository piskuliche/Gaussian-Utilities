#!/usr/bin/env python
import numpy as np
import os, sys

def gen_header(nproc, oldchk, chk, mem):
    """Generate gaussian input file header"""
    line1="%%NProcShared=%d" % nproc
    if oldchk is not None:
        line2="%%oldchk=%s" % oldchk
    line3="%%chk=%s" % chk
    line4="%%mem=%dGB" % mem
    header = []
    if oldchk is not None:
        header = [line1, line2, line3, line4]
    else:
        header = [line1, line3, line4]

    return header

def grab_trans(state=1):
    flag = 0
    trans = []
    with open('vert_exc/vert_exc.log','r') as f:
        lines = f.readlines()
        for line in lines:
            if "Excited State" in line:
                vals = line.strip().split()
                if state == int(vals[2][0]):
                    flag=1
                else:
                    flag=0
            if flag == 1 and "->" in line:
                trans.append(line)
    return trans
            
            



def gen_all_ntos(functional="B3LYP", basis="6-31(d,p)", dispersion=1,
                    solvent="Methanol", charge=0, multiplicity=1, nproc=28, mem=100):
    """This generates a set of ntos calculations for each transition"""

    num_trans = 0
    trans = grab_trans(state=1)
    for i in range(len(trans)):    
        header = gen_header(nproc, "../../vert_exc/vert_exc.chk", "state_%d.chk"%(i+1), mem)
        os.makedirs("ntos/%d"%(i+1),exist_ok=True)
        gen_sub_script(solvent=solvent, nproc=nproc, state=i+1)
        with open("ntos/%d/state_%d.gjf"%(i+1,i+1),"w") as f:
            for line in header:
                f.write(line+"\n")
            if dispersion == 1:
                f.write("#n %s/%s empiricaldispersion=gd3 Geom=AllCheck Guess=(Read,Only) Density=(Check,Transition=%d) Pop=(Minimal,NTO,SaveNTO) SCRF=(Solvent=%s)\n" % (functional, basis,i+1, solvent))
            else:
                f.write("#n %s/%s Geom=AllCheck Guess=(Read,Only) Density=(Check,Transition=%d) Pop=(Minimal,NTO,SaveNTO) SCRF=(Solvent=%s)\n" % (functional, basis, i+1, solvent))
            f.write("\n")
            f.write("Calculation of the Natural Transition Orbitals\n")
            f.write("\n")
            f.write("%d %d\n" % (charge, multiplicity))
            f.write("\n")
    gen_automate(len(trans))

def gen_sub_script(solvent,nproc=28,state=1):
    with open("ntos/%d/sub_ntos.sh"%state,"w") as f:
        f.write("#!/bin/bash\n")
        f.write("#\n")
        f.write("#$ -N %s-nto%s\n" % (solvent[:4],state))
        f.write("#$ -j y\n")
        f.write("#$ -l h_rt=12:00:00\n")
        f.write("#$ -pe mpi_28_tasks_per_node %d\n" % nproc)
        f.write("#$ -l mem_per_core=4G\n")
        f.write("#$ -V\n")

        f.write("module load gaussian/16.C.01\n")
        f.write("g16 state_%d.gjf\n"%state) 

def gen_automate(ns):
    with open("automate_nto.sh","w") as f:
        f.write("#!/bin/bash\n")
        f.write("for i in {1..%d}; do\n"%ns)
        f.write("    cd ntos/$i\n")
        f.write("    qsub sub_ntos.sh\n")
        f.write("    cd ../..\n")
        f.write("done\n")



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-basis', type=str, default="6-31(d,p)", help='Basis set to use [default: 6-31(d,p)]')
    parser.add_argument('-functional', type=str, default="B3LYP", help='Functional to use [default: B3LYP]')
    parser.add_argument('-dispersion', type=int, default=1, help='Use dispersion? [0] No [1] Yes')
    parser.add_argument('-charge', type=int, default=0, help='Charge of the molecule [default: 0]')
    parser.add_argument('-multiplicity', type=int, default=1, help='Multiplicity of the molecule [default: 1]')
    parser.add_argument('-nproc', type=int, default=28, help='Number of processors to use [default: 28]')
    parser.add_argument('-mem', type=int, default=100, help='Memory to use in GB [default: 100]')
    parser.add_argument('-solvent', type=str, default="Methanol", help='Solvent to use [default: Methanol]')
    args = parser.parse_args()

    gen_all_ntos(functional=args.functional, basis=args.basis, dispersion=args.dispersion,
                    solvent=args.solvent, charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem)
