from histogramMaker import make_histograms 
from EfretChartMaker import make_eFRET_charts
from annotationMaker import make_annotations

should_make_annotations = input("Would you like to make annotation files? (Y or N)")
if "Y" in should_make_annotations.upper():
    make_annotations()
should_make_histograms = input("Would you like to make the FRET histograms? (Y or N)")
if "Y" in should_make_histograms.upper():
    make_histograms()
should_make_charts = input("Would you like to make the FRET efficiency charts? (Y or N)")
if "Y" in should_make_charts.upper():
    make_eFRET_charts()
