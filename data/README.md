## Dataset for Code Smell DL Experiments

This folder contains two major set of files:
- CSV files that represented the dataset of each code smell. For instance `CC.csv` is that dataset for `ComplexConditional` code smell.
- JSON files that are the graphs of each method/class depending on the code smell.

First, extract the methods files. Go to the `methods` folder and run the command (assuming you are on a unix-based system): 

`cat methods.* > methods.zip`

Then unzip the file: 

`unzip methods.zip`

Doing so will create another folder called `methods` that has three subfolders `R1`, `R2`, and `R3`. Each subfolder contains the snippet of codes under different representations.  

**NOTE**: Current the JSON files are located in the following path: `~/data/methods/methods/R<1-2-3>/<PROJECT-NAME>/<METHOD-NAME>.json`. Move `R1`, `R2`, and `R3` up one level, so that the path to each JSON file becomes `~/data/methods/R<1-2-3>/<PROJECT-NAME>/<METHOD-NAME>.json`.

### Generating JSON Files for Classes

After the methods' JSON files are extracted, we need to generate JSON files for classes. CONCORD by default output representations at method level. We did so to offer the lowest granularity possible since classes is concept mainly related to OOP.  

To generate classes files run the following command:  

`python3 classes_generator.py`  

By the end of this step, the JSON files will be located in `classes/<REPRESENTATION>/<PROJECT>/<FILE>.json`.  

The classes generation can take a while (up to 3hrs). We have uploaded them on Google Drive too for faster access: https://drive.google.com/file/d/1HtzDoCwBNN7dnFvXkW3WHb0CY9o5eFno/view?usp=sharing

## Dataset for Devign (Vulnerability Detection) dataset

The dataset can be directly downloaded from Google Drive: https://drive.google.com/file/d/1JPJTf2lvOCry88zV3vTBq05f2BZ9Tqhz/view?usp=sharing
