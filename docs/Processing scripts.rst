
================
Processing Scripts
================

Description of utility scripts for carra2py. 


multiexec.py:
================

An executable script used for processing and exporting albedo data over multiple dates in a defined time period. It is also possible to use multiple cores to speed the process.

Arguments:
----------------

**-st (str): the start date of the process period in the format "yyyymmdd"**

**-en (str): the end date of the process period in the format "yyyymmdd"**

**-re (int): the wanted ouput resolution in meters, there are three choices [1000,2500,5000], default is set to 2500**

**-ar (list of str):  the wanted areas to process, default is set to process for all areas**

**-o (str): the wanted output format, there are three choices ["tif","csv","nc"], the default is set to "tif"**

**-c (int): number of cores the user want to use. The default is set to 4** 
