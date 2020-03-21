from sharedFunctions import find_files
import os

# The annotation file will end up in the same directory as the Keyword file
KEYWORD = "FRETresult.dat"
ANNOTATION_FILE_NAME = "annotation.txt"

# Main function, which gathers folders with the KEYWORD file
# then calls a function to ask what the annotation file should contain
def make_annotations():
    FRET_data = find_files(KEYWORD)
    for key in FRET_data:
        values = FRET_data[key]
        add_annotations_files(key, values)

# Helper function, prints out the names of the folders in a directory
# and asks what annotation you would like for each of them
def add_annotations_files(root, names):
    print("Folders at location '" + os.path.split(root)[1] + "' :")
    for name in names:
        print(name)
    for name in names:
        annotation = input("Annotation for folder '" + name + "' : ")
        f = open(root+"\\"+name+"\\"+ANNOTATION_FILE_NAME,"w")
        f.write(annotation)
        f.close()