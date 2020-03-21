# Single-molecule FRET Visualization pipelines

![individual histogram](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/individual/histogram.png "Individual Histogram")

![stacked histogram](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/stacked/histogram.png "Stacked Histogram")

![Individual FRET efficiency chart](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/individual/eFRET_plot.png "Individual FRET efficiency chart")

![Stacked FRET efficiency chart](https://github.com/SandersKM/smFRET-analysis-pipelines/blob/master/Example_images/stacked/eFRET_plot.png "Stacked FRET efficiency chart")

These python files are for creating annotated, stacked FRET histograms and FRET efficiency charts. Read about each file below. 

## `sharedFunctions.py`

**IMPORTANT** - Change the `ROOT_DIR` variable at the top of this file

This file contains a variety of functions that are used in multiple files:
* `find_files` finds all occurances of a certain file starting at a specific file path
* `get_annotation` opens an annotation file from a specific folder (given the folder path)
* `suplabel` makes the combined x an y axes of a stacked plot
* `font` returns a standardized font dictionary of a certain size
