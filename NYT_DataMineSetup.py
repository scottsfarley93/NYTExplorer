print "Running Setup Script to Install Packages Needed for NYT_DataMine"
print "This script requires sudo access."
print "Modules Required: \n" \
      "\tnltk -- Natural Language Tool Kit\n" \
      "\tprogressbar -- Graphic Progress Bars\n" \
      "\turllib2 -- HTML I/O\n" \
      "\tjson -- json object parsing\n" \
      "\ttime -- sleep functions\n" \
      "\tBeautiful Soup (bs4)-- HTML Parsing\n" \
      "\trequests -- HTML I/O\n" \
      "\tcollections -- Containers & Counters\n" \
      "\toperator -- For sorting dictionaries\n" \
      "\tos - File i/o\n" \
      "\tmatplotlib - Plotting\n" \
      "\tpandas - Time series and other data analysis functions \n" \
      "\tast - Loading json data from disk\n\n"

print "This script will only install:\n" \
      "\tnltk package and required datasets\n" \
      "\tprogressbar package\n" \
      "\tBeautiful Soup\n" \
      "\tMatplotlib\n" \
      "\tPandas\n" \
      "All other modules are built-in to python 2.7" \
      "Please correctly configure your python if you do not have the other modules."


import sys
import pip

## NLTK Package
pip.main(['install', 'nltk'])

##Progressbar package
pip.main(['install', 'progressbar'])

##Beautiful soup
pip.main(['install', 'beautifulsoup4'])

##Matplotlib
pip.main(['install', 'matplotlib'])

##pandas
pip.main(['install', 'pandas'])

##Make sure setup went correctly
try:
    import nltk
except ImportError:
    print "Failed to import nltk."
    sys.exit()

try:
    import progressbar
except ImportError:
    print "Failed to import progressbar."
    sys.exit()

try:
    import bs4
except:
    print "Failed to import Beautiful Soup."
    sys.exit()

try:
    import matplotlib.pyplot
except:
    print "Failed to import matplotlib.pyplot"
    sys.exit()

try:
    import pandas
except:
    print "Failed to import pandas."
    sys.exit()

##download nltk packages
nltk.download('all')

print "You're all set!"


