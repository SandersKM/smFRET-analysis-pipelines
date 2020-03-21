# Single-molecule FRET Visualization pipelines

These python files are for creating annotated, stacked FRET histograms and FRET efficiency charts. Read about each file below. 

**IMPORTANT** - These files assume a specific folder structure, listed bottom to top below:
* (A) Folder containing `FRETresult.dat` and `eFRET.dat` files for a single experiment
* (B) Folder containing several (A) experiment folders that you want to appear in a single stacked plot
* (C) Any number of wrapper folders leading back to the `ROOT_DIR` location

## sharedFunctions.py

**IMPORTANT** - Change the `ROOT_DIR` variable at the top of this file. This path variable should lead to the folder that contains all sets of folders that you want stacked and individual plots for. 

This file contains a variety of functions that are used in multiple files:
* `find_files` finds all occurances of a certain file starting at a specific file path
* `get_annotation` opens an annotation file from a specific folder (given the folder path)
* `suplabel` makes the combined x an y axes of a stacked plot
* `font` returns a standardized font dictionary of a certain size

## annotationMaker.py

**IMPORTANT** - The other plotting files will crash if you don't have annotation files within each folder you want to plot data from. I might fix this later, but I'm assuming most stacked histograms could do with annotations.

**IMPORTANT** - The `KEYWORD` is a file that is in the same folder you want an annotation file in. You may need to change this if you want annotation files in folders that don't also contain a `FRETresult.dat` file. 

The main function in this file is `make_annotations`. For each folder of type (B), all subfolders (A) are printed out. You will then be asked what annotation you want for each of these experiments. Your response will create an `annotation.txt` file within that (A) folder. If you don't want an annotation for a specific experiment, just press enter without entering any text.

## histogramMaker.py

The main function, `make_histograms`, makes all individual and stacked FRET histograms from `FRETresult.dat` files (where the data to be plotted is the first column of the data file). The program automatically scales the data so that the first histogram peak occurs at x = 0. The file itself has lots of comments, so you should be able to customize the aestetics of the histograms fairly easily. Examples of an individual and stacked histogram are below. 

![individual histogram](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/individual/histogram.png "Individual Histogram")

![stacked histogram](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/stacked/histogram.png "Stacked Histogram")

## EfretChartMaker.py

The main function, `make_eFRET_charts`, makes all individual and stacked FRET Efficiency charts from `eFRET.dat` files. The program automatically scales the data so that the photobleached section of the data is around y = 0. The file itself has lots of comments, so you should be able to customize the aestetics of the charts fairly easily. Examples of an individual and stacked chart are below. 

![Individual FRET efficiency chart](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/individual/eFRET_plot.png "Individual FRET efficiency chart")

![Stacked FRET efficiency chart](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/stacked/eFRET_plot.png "Stacked FRET efficiency chart")

## FRET_analysis.py

This is the main file. When run, it will ask you whether you want to make annotation files, FRET histograms, and/or E FRET charts. Your responses (Y or N) will determine which of the above files to run. 

