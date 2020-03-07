import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# start and stop for the binning, as well as bin width
HIST_X_START = -0.05
HIST_X_END = 0.5
BINWIDTH = 0.01

# Width and Height of saved picture in inches
FIG_WIDTH = 15 
FIG_HEIGHT = 10

# Font for axes
FONT = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 20,
        }

# Lista all paths leading to 'FRETresult.dat' in the dir
def list_FRETresult_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if "result.dat" in name:
                r.append(os.path.join(root, name))
    return r

# finds where the peaks occur (if peak has > 100 counts)
def get_hump_peaks(hist):
    sizes = hist[0]
    spots = hist[1]
    peaks = []
    index = 0
    last = 0
    increasing = True
    while index < len(sizes):
        if sizes[index] > last:
            if not increasing:
                increasing = True
        elif sizes[index] < last:
            if increasing:
                increasing = False
                if last > 100:
                    peaks.append(spots[index - 1])
        last = sizes[index]
        index += 1
    return peaks

# if there is more than one peak, the first peak is centered at x = 0
def get_scaled_data(data):
    hist = plt.hist(data, bins=np.arange(HIST_X_START, HIST_X_END + BINWIDTH, BINWIDTH))
    peaks = get_hump_peaks(hist)
    if len(peaks) > 1:
        return data - peaks[0]
    return data

# Creates and saves a histogram given a path to a 'FRETresult.dat' file
def make_histogram(path):
    split_path = path.split("\\")
    f = open(path, "r")
    data = pd.read_fwf(f, header=None)[0]
    scaled_data = get_scaled_data(data)
    plt.close()
    fig, ax = plt.subplots()
    plt.hist(scaled_data, bins=np.arange(HIST_X_START, HIST_X_END + BINWIDTH, BINWIDTH))
    plt.xlabel("FRET Efficiency", FONT)
    plt.ylabel("Number Counts", FONT)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.tick_params(axis='both', which='minor', labelsize=15)
    save_path = "\\".join(split_path[:-1]) + "\\histogram.png"
    print(save_path) # delete later, but prints out where the histogram is saved
    fig.set_size_inches(FIG_WIDTH, FIG_HEIGHT)
    fig.savefig(save_path, dpi=100)


rootdir = "\\Users\\kates\\Desktop\\Triplet Repeat\\Data"
FRET_data = list_FRETresult_files(rootdir)
make_histogram(FRET_data[0])