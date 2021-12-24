import csv
from .NRLMSISE00.nrlmsise_00_header import *
from .NRLMSISE00.nrlmsise_00 import *
import os

def read_csv(filename):
    if filename == None:
        return {}
    dic = {}
    with open(filename, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            dic = line
    return dict([key, float(value)] for key, value in dic.items())

def atmo_model(altitude):
    """
    Args:
        altitude: altitude to get data at (m)
    Returns:
        rho: air density at altitude (kg/m^3)
        temp: temperature (degrees C)
    """
    # Get output data, input data, and flags from NRLMSISE library
    output = nrlmsise_output()
    model_input = nrlmsise_input()
    flags = nrlmsise_flags()

    # Create an array to hold Ap-indexes for past (geomagnetic activity)
    aph = ap_array()

    # Ensure output is in MKS units
    flags.switches[0] = 0

    # Convert altitude to km
    model_input.alt = altitude / 1000

    # Set location to Spaceport America
    model_input.g_lat = 32.990371  # Spaceport America
    model_input.g_long = -106.975116

    # For simplicity, assume the Ap-index has been 100 for the last while
    for i in range(7):
        aph.a[i] = 100

    # Use all default settings
    for i in range(1, 24):
        flags.switches[i] = 1

    # Run the model
    gtd7(model_input, flags, output)

    # Get air density in kg/m^3
    rho = output.d[5] * 1000

    # Get temperature
    temp = output.t[1]
    return rho, temp

def fill_list(lst):
    for i in range(len(lst)):
        if i > 0 and lst[i] == -1:
            lst[i] = lst[i-1]

def join(lst):
    path = ''
    for str in lst:
        path = os.path.join(path, str)
    return path

def insert_newlines(string, every=50):
    ind = 0
    lst_ind = 0
    lst_nl = 0
    while ind != -1:
        ind = string.find(',', lst_ind)
        if ind - lst_nl > every:
            string = string[:lst_ind] + '\n' + ' '*8 + string[lst_ind:] # datcom doesn't like tabs
            lst_nl = ind
        lst_ind = ind + 1 # want new lines after commas
    return string
        