
================
Processing Scripts
================

Description of utility scripts for carra2py. 


multiexec.py:
================

An executable script used for processing and exporting albedo data over multiple dates in a defined time period. It is also possible to use multiple CPU cores to speed the process.

Arguments:
----------------

**-st: the start date of the process period in the format "yyyymmdd"**

**-en: the end date of the process period in the format "yyyymmdd"**

**-re: the wanted ouput resolution in meters, there are three choices [1000,2500,5000], default is set to 2500**

**-ar: the wanted areas to process, default is set to process for all areas**

**-o: the wanted output format, there are three choices ["tif","csv","nc"], the default is set to "tif"**

**-c: number of CPU cores the user want to use. The default is set to 4** 


monthtlymaps.py:
================

An executable script used for creating monthly means of the processed albedo data. It is also possible to use multiple CPU cores to speed the process.
The outputs are in tif formats.

Arguments:
----------------

**-mo: the month the user wants to process in the format "mm"**

**-re: the input resoultion in meters, there are three choices [1000,2500,5000], default is set to 2500**

**-ar: the wanted areas to process, default is set to process for all areas**

**-c: number of CPU cores the user want to use. The default is set to 4** 
