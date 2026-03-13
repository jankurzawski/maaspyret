# Introduction
This is a basic retinotopy script that:
 - Scans specific folders (masks, carriers) for subfolders that contain png stimuli
 - Allows the user to select which they would like to use on launch
 - Allows on-the-fly stimulus frequency and duration (i.e. TR) selection.
 - Timing is non-slip, and prints expected total duration when reaches Ready for Trigger phase
 - Supports a fixation color change detection task (recording button presses).
 - Is extensible - if new masks or carriers are provided, you can use them right away.
 - Starts with either t or 5 from scanner trigger - records r/g/b/y/1/2/3/4 from subject.

The experiment was first built with Builder and then modified to its current state. 
 
# Running The Experiment
To run, open the run_maaspyret.py in PsychoPy runner and hit play. 
It will wait for a scanner trigger after loading the images.
We assume you are using an extended display - and print out details, like ready for trigger and stimlus duration to terminal. 

When you enter subject/session/run numbers, these are saved to the directory and loaded into the dialogue for the next runs. 
The mask folder is used as a task name, and run numbers are incremented. 
The data file is written out with a "BIDS-like" filename. 
Note that we do not currently pair runs number increments with bar/wedge etc - run numbers will increment by 1 each time, even for different masks. 

# Notes on Carrier Stimuli
Two stimuli are provided currently, but more will be added in the future. 
First, stimuli developed by Dr. Kendrick Kay that consist of noise background with objects, sfaces etc. 
They were taken from [here](https://kendrickkay.net/analyzePRF/) and modified for size and png format. 
For large collections of carriers, they will be selected randomly and displayed. 
The next is a 2 checkerboards. If the code detects two images (i.e. your own favorite checkerboard), it will alternate between these. 

# Notes on Masks
The length of you scan will be determined by the number of mask images in the subfolder you select and how long you specify you want each mask to appear. 
The masks are shown in order - see the folder for an idea of naming and filetype formats.  
N.B. There is no built in blank/null time at the beginning nor end - the masks fully control what is on the screen. 
To have empty time, use empty masks - and duplicate if more time is needed, or gaps or desired during stimulus presentation.

# Notes on Fixation
The Fixation point will change from red to green, on average, every 20 seconds. 
We save button presses, but accuracy calculations/attention quantification is currently left as an exercise for the user. 

# PsychoPy Versions
Tested and working with version:
 - 2024.2.4 on Mac M4
 - 2026.1.1 on Mac M4