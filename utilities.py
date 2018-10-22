"""
Some utility functions for Oslo spectra.
Written by J{\o}rgen E. Midtb{\o}, UiO, 2016-2018
"""

import numpy as np 

def read_mama_2D(filename):
    # Reads a MAMA matrix file and returns the matrix as a numpy array, 
    # as well as a list containing the four calibration coefficients
    # (ordered as [bx, ax, by, ay] where Ei = ai*channel_i + bi)
    # and 1-D arrays of calibrated x and y values for plotting and similar.
    matrix = np.genfromtxt(filename, skip_header=10, skip_footer=1)
    cal = {}
    with open(filename, 'r') as datafile:
        calibration_line = datafile.readlines()[6].split(",")
        # a = [float(calibration_line[2][:-1]), float(calibration_line[3][:-1]), float(calibration_line[5][:-1]), float(calibration_line[6][:-1])]
        # JEM update 20180723: Changing to dict, including second-order term for generality:
        # print("calibration_line =", calibration_line, flush=True)
        cal = {"a0x":float(calibration_line[1]), "a1x":float(calibration_line[2]), "a2x":float(calibration_line[3]), 
             "a0y":float(calibration_line[4]), "a1y":float(calibration_line[5]), "a2y":float(calibration_line[6])}
    Ny, Nx = matrix.shape
    y_array = np.linspace(0, Ny-1, Ny)
    y_array = cal["a0y"] + cal["a1y"]*y_array + cal["a2y"]*y_array**2
    x_array = np.linspace(0, Nx-1, Nx)
    x_array = cal["a0x"] + cal["a1x"]*x_array + cal["a2x"]*x_array**2
    return matrix, cal, y_array, x_array # Returning y (Ex) first as this is axis 0 in matrix language


def read_response(fname_resp_mat, fname_resp_dat):
    # Import response matrix
    R, cal_R, Eg_array_R, tmp = read_mama_2D(fname_resp_mat)
    # We also need info from the resp.dat file:
    resp = []
    with open(fname_resp_dat) as file:
        # Read line by line as there is crazyness in the file format
        lines = file.readlines()
        for i in range(4,len(lines)):
            try:
                row = np.array(lines[i].split(), dtype="double")
                resp.append(row)
            except:
                break
    
    
    resp = np.array(resp)
    # Name the columns for ease of reading
    FWHM = resp[:,1]#*6.8 # Correct with fwhm @ 1.33 MeV?
    eff = resp[:,2]
    pf = resp[:,3]
    pc = resp[:,4]
    ps = resp[:,5]
    pd = resp[:,6]
    pa = resp[:,7]
    
    return R, FWHM, eff, pc, pf, ps, pd, pa, Eg_array_R