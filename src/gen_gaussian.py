#!/usr/bin/env python
import numpy as np
import argparse
import os

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

def gen_gs_geom_opt(coords, functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28,mem=100):
    """Generate gaussian input file for geometry optimization"""

    header = gen_header(nproc, None, "ground_state_geom_opt.chk", mem)
    os.makedirs("ground_state_geom_opt",exist_ok=True)
    with open("ground_state_geom_opt/geom_opt.gjf","w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 opt freq SCRF=(%s,Solvent=%s)\n" % (functional, basis, solv_model,solvent))
        else:
            f.write("#n %s/%s opt freq SCRF=(%s,Solvent=%s)\n" % (functional, basis, solv_model, solvent))
        f.write("\n")
        f.write("Ground state geometry optimization\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))
        for coord in coords:
            f.write("%s\n" % (coord))
        f.write("\n")

def gen_vert_exc(nstates=6, functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28,mem=100):
    header = gen_header(nproc, "../ground_state_geom_opt/ground_state_geom_opt.chk", "vert_exc.chk", mem)
    os.makedirs("vert_exc",exist_ok=True)
    with open("vert_exc/vert_exc.gjf","w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 TD=(Nstates=%d,Root=1) Geom=Check Guess=Read SCRF=(%s,Solvent=%s,CorrectedLR)\n" % (functional, basis, nstates, solv_model, solvent))
        else:
            f.write("#n %s/%s TD=(Nstates=%d,Root=1) Geom=Check Guess=Read SCRF=(%s,Solvent=%s,CorrectedLR)\n" % (functional, basis, nstates, solv_model, solvent))
        f.write("\n")
        f.write("Excited state corrected LR calculation\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))

def gen_exc_geom(nstates=6, functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28,mem=100):
    header = gen_header(nproc, "../vert_exc/vert_exc.chk", "exc_geom.chk", mem)
    os.makedirs("exc_geom",exist_ok=True)
    with open("exc_geom/exc_geom.gjf","w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 TD=(Nstates=%d,Root=1) Geom=Check Guess=Read SCRF=(%s, Solvent=%s)  opt=CalcFC Freq NoSymm\n" % (functional, basis, nstates, solv_model, solvent))
        else:
            f.write("#n %s/%s TD=(Nstates=%d,Root=1) Geom=Check Guess=Read SCRF=(%s,Solvent=%s) opt=CalcFC Freq NoSymm\n" % (functional, basis, nstates, solv_model, solvent))
        f.write("\n")
        f.write("Excited state geometry optimization calculation\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))

def gen_exc_solv(nstates=6, functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28,mem=100):
    header = gen_header(nproc, "../exc_geom/exc_geom.chk", "exc_solv.chk", mem)
    os.makedirs("exc_solv",exist_ok=True)
    with open("exc_solv/exc_solv.gjf","w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 TD=(Nstates=%d,Root=1) Geom=Check Guess=Read SCRF=(%s,Solvent=%s,CorrectedLR,NonEquilibrium=Save)  NoSymm\n" % (functional, basis, nstates, solv_model, solvent))
        else:
            f.write("#n %s/%s TD=(Nstates=%d,Root=1) Geom=Check Guess=Read SCRF=(%s,Solvent=%s,CorrectedLR,NonEquilibrium=Save) NoSymm\n" % (functional, basis, nstates, solv_model, solvent))
        f.write("\n")
        f.write("Excited state solvent field calculation\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))

def gen_gs_sp(functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28,mem=100):
    header=gen_header(nproc, "../exc_solv/exc_solv.chk", "gs_sp.chk", mem)
    os.makedirs("gs_sp",exist_ok=True)
    with open("gs_sp/gs_sp.gjf","w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 Geom=Check Guess=Read SCRF=(%s,Solvent=%s,NonEquilibrium=Read) NoSymm\n" %(functional, basis, solv_model, solvent))
        else:
            f.write("#n %s/%s Geom=Check Guess=Read SCRF=(%s,Solvent=%s,NonEquilibrium=Read) NoSymm\n"% (functional, basis, solv_model, solvent))
        f.write("\n")
        f.write("Ground state single point calculation\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))

def read_coords(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
        coords = []
        for line in lines:
            if line[0] != "#":
                coords.append(line.strip())
    return coords

def read_xyz(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
        coords = []
        for line in lines[2:]:
            coords.append(line.strip())
    return coords

def gen_sub_script(solvent,nproc=28,functional="B3LYP"):
    with open("sub_script.sh","w") as f:
        f.write("#!/bin/bash\n")
        f.write("#\n")
        f.write("#$ -N %s-%s\n" % (solvent[:4],functional))
        f.write("#$ -j y\n")
        f.write("#$ -l h_rt=12:00:00\n")
        f.write("#$ -pe mpi_28_tasks_per_node %d\n" % nproc)
        f.write("#$ -l mem_per_core=4G\n")
        f.write("#$ -V\n")

        f.write("module load gaussian/16.C.01\n")
        f.write("cd ground_state_geom_opt\n")
        f.write("g16 geom_opt.gjf\n")
        f.write("cd ../vert_exc\n")
        f.write("g16 vert_exc.gjf\n")
        f.write("cd ../exc_geom\n")
        f.write("g16 exc_geom.gjf\n")
        f.write("cd ../exc_solv\n")
        f.write("g16 exc_solv.gjf\n")
        f.write("cd ../gs_sp\n")
        f.write("g16 gs_sp.gjf\n")

def gen_ir(coords, molecule, functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28, mem=100):
    """Generate gaussian input file for IR calculation"""

    header = gen_header(nproc, None, "infrared.chk", mem)
    os.makedirs("%s/infrared"%molecule,exist_ok=True)
    with open("%s/infrared/infrared.gjf"%molecule,"w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 opt freq SCRF=(%s,Solvent=%s)\n" % (functional, basis, solv_model,solvent))
        else:
            f.write("#n %s/%s opt freq SCRF=(%s,Solvent=%s)\n" % (functional, basis, solv_model, solvent))
        f.write("\n")
        f.write("Ground state geometry optimization\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))
        for coord in coords:
            f.write("%s\n" % (coord))
        f.write("\n")

def gen_raman(coords, molecule, functional="B3LYP", basis="6-31(d,p)", dispersion=1, solv_model="PCM", solvent="Methanol", charge=0, multiplicity=1, nproc=28, mem=100):
    """Generate gaussian input file for Raman calculation"""

    header = gen_header(nproc, None, "raman.chk", mem)
    os.makedirs("%s/raman"%molecule,exist_ok=True)
    with open("%s/raman/raman.gjf"%molecule,"w") as f:
        for line in header:
            f.write(line+"\n")
        if dispersion == 1:
            f.write("#n %s/%s empiricaldispersion=gd3 opt freq=Raman SCRF=(%s,Solvent=%s)\n" % (functional, basis, solv_model,solvent))
        else:
            f.write("#n %s/%s opt freq=Raman SCRF=(%s,Solvent=%s)\n" % (functional, basis, solv_model, solvent))
        f.write("\n")
        f.write("Ground state geometry optimization\n")
        f.write("\n")
        f.write("%d %d\n" % (charge, multiplicity))
        for coord in coords:
            f.write("%s\n" % (coord))
        f.write("\n")

def gen_spec_script(solvent, molecule, nproc=28, functional="B3LYP"):
    with open("%s/sub_script.sh"%molecule,"w") as f:
        f.write("#!/bin/bash\n")
        f.write("#\n")
        f.write("#$ -N ir-%s\n" % (molecule))
        f.write("#$ -j y\n")
        f.write("#$ -l h_rt=12:00:00\n")
        f.write("#$ -pe mpi_28_tasks_per_node %d\n" % nproc)
        f.write("#$ -l mem_per_core=4G\n")
        f.write("#$ -V\n")

        f.write("module load gaussian/16.C.01\n")
        f.write("cd infrared\n")
        f.write("g16 infrared.gjf\n")
        f.write("cd ../raman\n")
        f.write("g16 raman.gjf\n")
        f.write("cd ../\n")

def write_submit(append, molecule):
    if append == 1:
        with open("submit.sh","a") as f:
            f.write("cd %s\n" % molecule)
            f.write("qsub sub_script.sh\n")
            f.write("cd ..\n")
    else:
        with open("submit.sh", 'w') as f:
            f.write("cd %s\n" % molecule)
            f.write("qsub sub_script.sh\n")
            f.write("cd ..\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate gaussian input files for absorption/emission calculations')
    parser.add_argument('-cfile', type=str, default=None, help='Coordinates file to use')
    parser.add_argument('-basis', type=str, default="6-31(d,p)", help='Basis set to use [default: 6-31(d,p)]')
    parser.add_argument('-functional', type=str, default="B3LYP", help='Functional to use [default: B3LYP]')
    parser.add_argument('-dispersion', type=int, default=1, help='Use dispersion? [0] No [1] Yes')
    parser.add_argument('-charge', type=int, default=0, help='Charge of the molecule [default: 0]')
    parser.add_argument('-multiplicity', type=int, default=1, help='Multiplicity of the molecule [default: 1]')
    parser.add_argument('-nstates', type=int, default=6, help='Number of states to calculate [default: 6]')
    parser.add_argument('-nproc', type=int, default=28, help='Number of processors to use [default: 28]')
    parser.add_argument('-mem', type=int, default=100, help='Memory to use in GB [default: 100]')
    parser.add_argument('-solvent', type=str, default="Methanol", help='Solvent to use [default: Methanol]')
    parser.add_argument('-solv_model', type=str, default="PCM", help='Solvent model to use [default: PCM]')
    parser.add_argument('-irraman', type=int, default=0, help='Calculate IR/Raman? [0] No [1] Yes')
    parser.add_argument('-append', type=int, default=1, help='Append to existing files? [0] No [1] Yes')
    args = parser.parse_args()

    if args.cfile == None:
        raise ValueError("Please provide a coordinates file")

    
    if args.irraman == 0:
        coords = read_coords(args.cfile)
        gen_gs_geom_opt(coords, functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
        charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem) # step 1
        gen_vert_exc(nstates=6, functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
        charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem) # step 3
        gen_exc_geom(nstates=6, functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
        charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem) # step 4
        gen_exc_solv(nstates=6, functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
        charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem) # step 5
        gen_gs_sp(functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
        charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem) # step 6
        gen_sub_script(args.solvent, nproc=args.nproc, functional=args.functional)
    elif args.irraman == 1:
        print('Working on molecule %s' % args.cfile.strip('xyz'))
        write_submit(args.append, args.cfile.strip('.xyz').replace("coords/",""))
        coords = read_xyz(args.cfile)
        gen_ir(coords, args.cfile.strip('.xyz').replace("coords/",""), functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
               charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem)
        gen_raman(coords, args.cfile.strip('.xyz').replace("coords/",""), functional=args.functional, basis=args.basis, dispersion=args.dispersion, solv_model=args.solv_model, solvent=args.solvent,
                  charge=args.charge, multiplicity=args.multiplicity, nproc=args.nproc, mem=args.mem) 
        gen_spec_script(args.solvent, args.cfile.strip('.xyz').replace("coords/",""), nproc=args.nproc, functional=args.functional)       