from sharedFunctions import *
import pandas as pd
import numpy as np

# Change these if file / label names need to be different
X_LABEL = "Time (s)"
Y_LABEL = "E FRET"
eFRET_FILE_NAME = "eFRET.dat"
FIG_NAME = "eFRET_plot.png"
# Width and Height of saved picture in inches
FIG_WIDTH = 20
FIG_HEIGHT = 10

'''
Opens eFRET data file with columns: 1) Time, 2) Donor, 3) Acceptor.
Adds a new column 4) eFRET, with the ratio (A / (D + A)).
Returns the new Pandas Data Frame. 
    path    - path the the eFRET data file
'''
def get_eFRET_data(path):
    FRETresult = open(path + "\\" + eFRET_FILE_NAME, "r") 
    data = pd.read_fwf(FRETresult, header=None)
    data.columns = ["time", "donor", "acceptor"]
    data["eFRET"] = (data["acceptor"]) / (data["donor"] + data["acceptor"])
    return adjust_eFRET_data(data)

'''
Adjusts the data so that the photobleaching is centered around zero.
    data    - pandas dataframe containing the "eFRET" column
'''
def adjust_eFRET_data(data):
    # Make a histogram with two bins
    # so one bin in actual fret and the other is photobleaching
    bin_edges = np.histogram(data["eFRET"], bins=2)[1]
    # divide the far edge of the first bin (photobleached) by 2 to get the midpoint
    offset = bin_edges[1] / 2
    # subtract that midpoint of from all of the eFRET data
    data["eFRET"] = data["eFRET"] - offset
    return data

'''
Makes a stack of FRET efficiency charts using the eFRET data of all subfolders within a folder
    dirpath     - path to the directory that holds all of the desired subdirectories
    subdirs     - list of folder names containing FRET result files
'''
def make_eFRET_stacked(dirpath, subdirs):
    index = 0
    annotations = []
    all_data = []
    max_time = 0
    min_data = 0
    max_data = 0
    fig, axs = plt.subplots(len(subdirs), 1, sharex=True,
                sharey=True, tight_layout=True, gridspec_kw = {'wspace':0, 'hspace':0})
    for subdir in subdirs:
        path = dirpath + "\\" + subdir
        annotations.append(get_annotation(path))
        data = get_eFRET_data(path)
        if data["time"].max() > max_time:
            max_time = data["time"].max()
        if data["eFRET"].min() < min_data:
            min_data = data["eFRET"].min()
        if data["eFRET"].max() > max_data:
            max_data = data["eFRET"].max()
        all_data.append(data)
    for index in range(len(subdirs)):
        axs[index].plot(all_data[index]["time"], all_data[index]["eFRET"])
        axs[index].set_ylim([min_data, max_data])
        axs[index].tick_params(axis='both', which='major', labelsize=25)
        axs[index].text(max_time, max_data - (.1 * max_data * len(subdirs)), \
            annotations[index], horizontalalignment='right', fontdict=font(30))
    suplabel("y", Y_LABEL, label_prop=font(40), labelpad=((max_time // 10) + 3))
    suplabel("x", X_LABEL, label_prop=font(40), labelpad=8)
    fig.set_size_inches(FIG_WIDTH, FIG_HEIGHT)
    save_path = dirpath + "\\" + FIG_NAME
    fig.savefig(save_path, dpi=100)

'''
Makes a single chart from an eFRET data file
    path    - path to a folder containing an eFRET data file
'''
def make_eFRET(path):
    data = get_eFRET_data(path)
    plt.close()
    fig, ax = plt.subplots()
    plt.plot(data["time"], data["eFRET"])
    plt.xlabel(X_LABEL, font(40))
    plt.ylabel(Y_LABEL, font(40))
    ax.tick_params(axis='both', which='major', labelsize=30)
    ax.tick_params(axis='both', which='minor', labelsize=25)
    save_path = path + "\\" + FIG_NAME
    fig.set_size_inches(FIG_WIDTH*2.5, FIG_HEIGHT)
    fig.savefig(save_path, dpi=100)

'''
Makes all individual and stacked FRET efficiency charts
'''
def make_eFRET_charts():
    FRET_data = find_files(eFRET_FILE_NAME)
    for key in FRET_data:
        values = FRET_data[key]
        if len(values) > 1:
            make_eFRET_stacked(key, values)
        for v in values:
            make_eFRET(key + "//" + v)