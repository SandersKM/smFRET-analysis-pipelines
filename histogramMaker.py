from sharedFunctions import *
import pandas as pd
import numpy as np
import os

# start and stop for the binning, as well as bin width
HIST_X_START = -0.05
HIST_X_END = 0.5
BINWIDTH = 0.005
# Width and Height of saved picture in inches
FIG_WIDTH = 15 
FIG_HEIGHT = 10
# Change these if file / label names need to be different
X_LABEL = "FRET Efficiency"
Y_LABEL = "Number Counts"
FRETresult_FILE_NAME = "FRETresult.dat"
HIST_FILE_NAME = "histogram.png"

'''
Makes a single histogram from a FRET result file
    path    - path to a folder containing a FRET result file
'''
def make_histogram(path):
    annotation = get_annotation(path)
    data = get_data(path)
    top = get_max_y(data) + 10
    plt.close()
    fig, ax = plt.subplots()
    plt.hist(data, bins=np.arange(HIST_X_START, HIST_X_END + BINWIDTH, BINWIDTH))
    plt.xlabel(X_LABEL, font(40))
    plt.ylabel(Y_LABEL, font(40))
    plt.ylim(0, top)
    ax.tick_params(axis='both', which='major', labelsize=30)
    ax.tick_params(axis='both', which='minor', labelsize=25)
    plt.text(.5, top - (top*.1), annotation, horizontalalignment='right', fontdict = font(20))
    save_path = path + "\\" + HIST_FILE_NAME
    fig.set_size_inches(FIG_WIDTH, FIG_HEIGHT)
    fig.savefig(save_path, dpi=100)

'''
Makes a stack of histograms using the FRET result data of all subfolders within a folder
    dirpath     - path to the directory that holds all of the desired subdirectories
    subdirs     - list of folder names containing FRET result files
'''
def make_histograms_stacked(dirpath, subdirs):
    data = []
    annotations = []
    y_maxes = []
    fig, axs = plt.subplots(len(subdirs), 1, sharex=True,
                sharey=True, tight_layout=True, gridspec_kw = {'wspace':0, 'hspace':0})
    for subdir in subdirs:
        path = dirpath + "\\" + subdir 
        annotations.append(get_annotation(path))
        data.append(get_data(path))
        y_maxes.append(get_max_y(data[-1]))
    for index in range(len(subdirs)):
        top = max(y_maxes) + 10
        axs[index].hist(data[index], bins=np.arange(HIST_X_START, HIST_X_END + BINWIDTH, BINWIDTH))
        axs[index].text(.5, top - (top * .1 * len(subdirs)), \
            annotations[index], horizontalalignment='right', fontdict=font(12))
        axs[index].set_ylim([0, top])
        axs[index].tick_params(axis='both', which='major', labelsize=10)
    suplabel("y", Y_LABEL, label_prop=font(18))
    suplabel("x", X_LABEL, label_prop=font(18), labelpad=8)
    save_path = dirpath + "\\" + HIST_FILE_NAME
    fig.savefig(save_path, dpi=100)

'''
opens FRETresult file, makes contents into a pandas data frame, and returns the scaled data
    path    - path at which a FRET result file is located
'''
def get_data(path):
    FRETresult = open(path + "//" + FRETresult_FILE_NAME, "r") 
    data = pd.read_fwf(FRETresult, header=None)[0]
    return scale_data(data)

'''
Returns the largest histogram bin size
    data    - pandas dataframe with one column
'''
def get_max_y(data):
    hist = np.histogram(data, bins=np.arange(HIST_X_START, HIST_X_END + BINWIDTH, BINWIDTH))
    sizes = hist[0]
    return max(sizes)

'''
scales the data so that the first peak occurs at x = 0
    data    - panda dataframe with one column
'''
def scale_data(data):
    hist = np.histogram(data, bins=np.arange(HIST_X_START, HIST_X_END + BINWIDTH, BINWIDTH))
    peaks = get_peaks(hist)
    # only scales data if there is more than one peak.
    # adjust the BINWIDTH if you should have more than one peak and that's not happening
    if len(peaks) > 1:
        # centers the first peak at x = 0
        return data - peaks[0]
    return data

'''
returns bins where a peak in the histogram occurs (if peak has > 10 counts)
    hist    - numpy histogram object
'''
def get_peaks(hist):
    sizes = hist[0] # bin size
    spots = hist[1] # bin locations
    peaks = [] # list to keep track of where peaks occur
    index = 0  # index of current bin
    last = 0   # size of the last bin
    increasing = True
    # loops through each bin
    while index < len(sizes): 
        # if there is an increase in the bin size
        if sizes[index] > last: 
            increasing = True
        # if there is a decrease in the bin size
        elif sizes[index] < last:
            # a switch from increasing to decreasing could indicate a peak
            if increasing:
                increasing = False
                # the peak cuttoff here is pretty arbitrary
                if last > 10: 
                    peaks.append(spots[index - 1])
        last = sizes[index]
        index += 1
    return peaks

'''
Makes all individual and stacked histograms
'''
def make_histograms():
    FRET_data = find_files(FRETresult_FILE_NAME)
    for key in FRET_data:
        values = FRET_data[key]
        if len(values) > 1:
            make_histograms_stacked(key, values)
        for v in values:
            make_histogram(key + "//" + v)
 