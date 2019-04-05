# FROG
This a python based GUI for implementing the Frequency Resolved Optical Gating (FROG) setup. It involves automating two devices: first one is Thorlabs Linear Stage controller (KDC 101) the other one is UV-VIS spectrometer from Research India Ltd.

In order to run this, download all files, and run the file "interface.py". This is itself a fully functional GUI to run the FROG. It imports the respective driver filed for the KDC 101 (APT.dll) controller and the spectrometer (spectrlib64.dll). 
The file PyAPT.py defines functions for the KDC 101 controller, while the "camera.py" defines functions for the spectrometer.

On running the GUI, we need to do the following steps for getting the spectrogram:

Step 1: push connect button, and wait until it turns green
Step 2: push "go to zero" button, so that the stage recalliberates itself, and goes to its absolute 0. (from there you can take it any position you want)
Step 3: set the required "time of exposure" and "number of scans" in their respective boxes.
Step 4: Write the name of the file where you want to store data.
Step 5: Press "start scan", you will see the progressing running, wait until it goes to 100%.
Step 6: Click on "plot" and there you go, you have the spectrogram with you.

You can use this spectrogram to deconvolve and find the E(t) of the ultrafast you trying to measure.
