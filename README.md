Prerequisites
1) Python 2.7
2) Numpy
3) Scipy
4) Matplotlib
5) E3D binary
6) ffmpeg codec (optional, required for video output)
7) OpenMPI (optional, required for multicore processing)

Installation
PyE3D is an open-source project by Christopher Sherman at the University of California Berkeley designed to serve as a Python-based graphical user interface to the Finite Difference code E3D. Note that the E3D code is developed by Shawn Larsen and Lawrence Livermore National Laboratory, and is not available as part of this package.
To install PyE3D, begin by installing the prerequisites, downloading the source code located at: https://github.com/cssherman/PyE3D, and placing these files in a convenient location. From the command line, run the python file e3d gui.py. If this is the first time the GUI has been opened, there will be a command-line prompt asking for a username, which is used to help organize files on the hard drive. Finally, once the GUI opens, go to the advanced tab and set the appropriate paths for the input/output files and the E3D binary.


Some important notes:
1. If you would like to use email alerts, you should edit the function e3d gmail, which is located in the file e3d functions.py, and change the example gmail login criteria fromaddr and passwd to match your desired values before running the GUI.
2. This code is designed and tested to run for a Unix-style operating system. Some modifications to the code may be necessary to work in a Windows environment.

Basic PyE3D Usage
To begin call the file e3d gui.py from the terminal, which will open the PyE3D GUI in a new window (see Figure A.1). The purpose of this GUI is to create a configuration file (./e3d default.pkl), which is sent to the program, e3 main.py. This is the bulk of the work is done to build models, communicate with E3D, and process the results. At the top of the GUI there are seven tabs that step through the model configuration process. These include:
- Main (basic model setup, boundary conditions, analysis options) 
- Advanced (timesteps, material control, paths)
- Materials (material velocity, density, statistics, geometry)
- Sources (source location, type, frequency)
- Traces (seismograph output locations, types) 
- Movies (movie output locations, types)
- Rendering (decimation, plot saturation, etc.)

At the base of the window, there are six buttons that are used to start the analysis and manage configuration files. These include:
- Run PyE3D: This sends the current configuration file to e3 main.py and starts the analysis
- Run Post: This triggers any post-processing that is requested in the Rendering tab (targets the files specified under the Linking Directory)
- Save: This saves the current configuration of the GUI to the file ./e3d default.pkl
- Export: This exports the current GUI configuration to a user-specified location
- Load: This reads the user-specified configuration file and updates the GUI
- Restore: This loads the default settings for the configuration file, which are found in e3d classes.py.

While running the function e3d main.py, the results will be stored in the location spec- ified by the Output Location, which is defined under the Advanced tab. The directory structure created is as follows: [outputlocation]/[username]/[dateof simulation in M-Y format]/[modelnumber]/. This directory may contain the following files:

- ./E3D in.txt: The main file sent to the E3D code
- ./[property].pv: Files containing the velocity model structure 
- ./wav.sac: The file containing the custom input wavelet
- ./sac/: A folder containing seismograph outputs
- ./mov/: A folder containing movie outputs

To organize longer series of simulations, each of these directories are linked to the location specified under Linking Directory, which is defined in the Advanced tab: [linking directory]/ [model number]/.
