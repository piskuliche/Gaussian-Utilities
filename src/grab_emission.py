#!/usr/bin/env python

import numpy as np

def grab_spectra(logfile):
    """This grabs the spectra from the band_shape.log file

    This function grabs the spectra from the band_shape.log file, which is the
    output of a band shape calculation.

    Args:
        logfile (str): The name of the log file to grab the spectra from.
    
    Returns:
        freq (np.array): The frequencies of the spectra in cm^-1
        intensity (np.array): The intensities of the spectra in a.u.

    """
    freq = np.array([])
    intensity = np.array([])
    with open(logfile,'r') as f:
        lines = f.readlines()
        spect_flag=0
        read_flag=0
        start_read =0
        for line in lines:
            if len(line.strip().split()) == 2 and spect_flag == 1:
                start_read = 1
                vals = line.strip().split()
                freq = np.append(freq,float(vals[0]))
                intensity = np.append(intensity,float(vals[1].replace("D","E")))
            if "----" in line and start_read == 1:
                spect_flag = 0
                start_read = 0
            if "Final Spectrum" in line:
                spect_flag = 1
            
    return freq, intensity



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, default="band_shape.log", help="The band shape to grab the spectra for.")
    args = parser.parse_args()
    freq, I = grab_spectra(args.f)
    np.savetxt("spectra.dat",np.column_stack((freq,I)),fmt="%10.5f",header="Frequency (cm^-1) Intensity (a.u.)")

    import matplotlib.pyplot as plt
    plt.plot(1E7/freq,I)
    plt.show()