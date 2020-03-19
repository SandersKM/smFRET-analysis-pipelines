import os

# Creates a dictionary where the value is a folder which contains a file with the 'keyword'
# and the key is the path leading to where that folder is located. 
# IMPORTANT: Before using this, change the rootDir to match where your files are located.
# The directory structure might be a bit different for Mac / Linux users 
def list_FRETresult_folders(keyword, rootDir="\\Users\\kates\\Desktop\\Triplet Repeat\\Data"):
    dir_dict = {}
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if keyword in fname:
                key, value = os.path.split(dirName)
                if key not in dir_dict:
                    dir_dict[key] = []
                dir_dict[key].append(value)
    return dir_dict
