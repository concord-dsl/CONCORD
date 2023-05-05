## Dataset for DL Experiments

This folder contains two major set of files:
- CSV files that represented the dataset of each code smell. For instance `CC.csv` is that dataset for `ComplexConditional` code smell.
- JSON files that are the graphs of each method/class depending on the code smell.

First, extract the methods files. Go to the `methods` folder and run the command (assuming you are on a unix-based system): 

`cat methods.* > methods.zip`

Then unzip the file: 

`unzip methods.zip`

Doing so will create another folder called `methods` that has three subfolders `R1`, `R2`, and `R3`. Each subfolder contains the snippet of codes under different representations.  

**NOTE**: Current the JSON files are located in the following path: `~/data/methods/methods/R<1-2-3>/<PROJECT-NAME>/<METHOD-NAME>.json`. Move `R1`, `R2`, and `R3` up one level, so that the path to each JSON file becomes `~/data/methods/R<1-2-3>/<PROJECT-NAME>/<METHOD-NAME>.json`.

