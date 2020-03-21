from matplotlib import pyplot as plt
import os

'''
IMPORTANT: Before using this, change the rootDir to match where your files are located.
The directory structure might be a bit different for Mac / Linux users 
'''
ROOT_DIR = "\\Path\\To\\Data"
ANNOTATION_FILE_NAME = "annotation.txt"

'''
makes standard font with a given size
    size    - the size you want the font to be
'''
def font(size):
    return {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': size }

'''
Creates a dictionary where the value is a folder which contains a file with the 'keyword'
and the key is the path leading to where that folder is located. 
    keyword     - file name (or portion of file name) to locate within subfolders
    rootDir     - path to directory within which this search occurs
'''
def find_files(keyword, rootDir=ROOT_DIR):
    dir_dict = {}
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if keyword in fname:
                key, value = os.path.split(dirName)
                if key not in dir_dict:
                    dir_dict[key] = []
                dir_dict[key].append(value)
    return dir_dict

'''
Returns the contents of the annotation file within a folder
    path        - path to directory where an annotation file should be located
'''
def get_annotation(path):
    try:
        return open(path + "\\" + ANNOTATION_FILE_NAME, "r").readline().strip()
    except:
        print("ERROR: file not found")

''' 
Add super ylabel or xlabel to the figure
Similar to matplotlib.suptitle
    axis       - string: "x" or "y"
    label      - string
    label_prop - keyword dictionary for Text
    labelpad   - padding from the axis (default: 5)
    ha         - horizontal alignment (default: "center")
    va         - vertical alignment (default: "center")
Source:
https://stackoverflow.com/questions/6963035/pyplot-axes-labels-for-subplots
'''
def suplabel(axis,label,label_prop=None,
             labelpad=10,
             ha='center',va='center'):
    fig = plt.gcf()
    xmin = []
    ymin = []
    for ax in fig.axes:
        xmin.append(ax.get_position().xmin)
        ymin.append(ax.get_position().ymin)
    xmin,ymin = min(xmin),min(ymin)
    dpi = fig.dpi
    if axis.lower() == "y":
        rotation=90.
        x = xmin-float(labelpad)/dpi
        y = 0.5
    elif axis.lower() == 'x':
        rotation = 0.
        x = 0.5
        y = ymin - float(labelpad)/dpi
    else:
        raise Exception("Unexpected axis: x or y")
    if label_prop is None: 
        label_prop = dict()
    plt.text(x,y,label,rotation=rotation,
               transform=fig.transFigure,
               ha=ha,va=va,
               **label_prop)
