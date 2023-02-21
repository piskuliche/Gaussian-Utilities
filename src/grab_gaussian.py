#!/usr/bin/env python
import numpy as np
import argparse

def grab_excited(state):
    """This grabs the excited state energy from the vert_exc.log file


    This function grabs the excited state energy from the vert_exc.log file,
    which is the output of a single point calculation of the excited state at
    the ground state geometry. This is
    used to calculate the absorption wavelength.

    Args:
        state (int): The excited state to grab the energy for

    Returns:
        energy (float): The excited state energy in Hartrees

    """
    with open("vert_exc/vert_exc.log",'r') as f:
        lines = f.readlines()
        for line in lines:
            if "Excited State" in line:
                vals=line.strip().split()
                if state == int(vals[2][0]) or state == -1:
                    print("Excited_State %s" % vals[2])
                    print("%s"%vals[8])
                    print("***")
                    print("Absorption Wavelength %10.5f nm" % float(vals[6]))
                    energy = float(vals[6])
                    if state != -1:
                        return energy
def grab_exc_solv():
    """This grabs the excited state energy from the exc_solv.log file
    
    
    This function grabs the excited state energy from the exc_solv.log file,
    which is the output of a single point calculation of the excited state at
    the excited state geometry with the nonequilibrium solvation model. This is
    used to calculate the emission wavelength.

    Returns:
        energy (float): The excited state energy in Hartrees

    """
    energy = 0.0
    with open("exc_solv/exc_solv.log",'r') as f:
        lines = f.readlines()
        for line in lines:
            if "Total energy after correction" in line:
                vals = line.strip().split()
                energy = float(vals[5])

    return energy

def grab_gs_sp():
    """This grabs the ground state energy from the gs_sp.log file

    This function grabs the ground state energy from the gs_sp.log file, which
    is the output of a single point calculation of the ground state at the 
    excited state geometry with the nonequilibrium solvation model. This is
    used to calculate the emission wavelength.

    Returns:
        energy (float): The ground state energy in Hartrees
    

    """
    energy = 0.0
    with open("gs_sp/gs_sp.log",'r') as f:
        lines = f.readlines()
        for line in lines:
            if "SCF Done" in line:
                vals = line.strip().split()
                energy = float(vals[4])

    return energy

def conv_en(value):
    return 45.56337117/value

if __name__ == "__main__":
    grab_excited(1)
    en5 = grab_exc_solv()
    en6 = grab_gs_sp()

    em_en = en5-en6
    print("Emission Wavelength: %10.5f nm" % conv_en(em_en))