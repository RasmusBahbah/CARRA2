
================
Examples
================

Several examples of how to use the carra2py modules and methods, and the utility scripts.
All the examples assume that the user has installed the package correctly, has activated the python environemt and is in the correct folder (/user/carra2py).


carra2py.AVHRR()
================

These examples are executed in a python console, the chosen date is 6th of May, 1994

**First import the carra2py package**
   ``import carra2py``
   
**and then input the date in the carra2py.AVHRR() module**
    ``avhrr = carra2py.AVHRR("19940506")``
    
How to get the raw data
------------------------

**get the data in EPSG:4326 using the get_data() method**
    ``rawdata = avhrr.get_data()``
    
**or get the data in EPSG:3413 using the get_data() method**   
    ``rawdata = avhrr.get_data(polar=True)``
    
How to process data 
--------------------
the default settings is set to process for all regions with a resolution of 2500 meters.
Note that the region names have the same spelling as in the table in the introduction section.

**Process with default settings**
    ``output = avhrr.proc()``
    
**Process for Greenland, Iceland and  AlaskaYukon, with a 1000 m resolution**
    ``output = avhrr.proc(area = ["Greenland","Iceland","AlaskaYukon"],res=1000)``
    
**Process with rawdata from user, see "carra2py Modules and Methods" for input specifications**
    ``output = avhrr.proc(raw_data=rawdata)``
    
How to export data
--------------------
the default export settings is set to process for all regions with a resolution of 2500 meters.

**Export as tif with default settings**
     ``avhrr.export_to_tif()``
     
**Export as csv with default settings**
     ``avhrr.export_to_csv()``
     
**Export as netcdf with default settings**
     ``avhrr.export_to_nc()``
     
**Export user defined processed data as tif**
     ``avhrr.export_to_tif(output=output)``   
     
**Export user defined processed data as netcdf in specfic folder**
     ``avhrr.export_to_nc(output=output,path="home/carra2py/john/statoil")``  

multiexec.py
================

These examples are executed as command lines in a terminal, in your carra2py environment.
The default settings is set to process for all regions with a resolution of 2500 meters using 4 CPU cores and then export as tif files.
Please note, the user must input a start and end date for the processing.
These examples are all exectued with the time period 1st of January, 1982 - 31st of December, 2022.

How to process several dates
-----------------------------
**Process with default settings**
     ``python multiexec.py -st 19820101 -en 20221231``  
     
**Process with 1000 meter resolution**
     ``python multiexec.py -st 19820101 -en 20221231 -re 1000``

How to process specific areas
------------------------------
**Process for Svalbard, NorthernArcticCanada and SevernayaZemlya**
     ``python multiexec.py -st 19820101 -en 20221231 -ar [Svalbard,NorthernArcticCanada,SevernayaZemlya]``  
     
**Process for Greenland and Iceland with 1000 meter resolution**
     ``python multiexec.py -st 19820101 -en 20221231 -ar [Greenland,Iceland] -re 1000``  

How to change output format
-----------------------------

**Process with default settings and then export as netcdf files**
     ``python multiexec.py -st 19820101 -en 20221231 -o nc`` 
     
**Process with default settings and then export as csv files**
     ``python multiexec.py -st 19820101 -en 20221231 -o csv`` 
     
How to change the number of cores used
--------------------------------------

**Process using 8 cores**
     ``python multiexec.py -st 19820101 -en 20221231 -c 8`` 
     
**Process using 1 core**
     ``python multiexec.py -st 19820101 -en 20221231 -c 1`` 
     
    
Example with all arguments
--------------------------------------

**Process using 6 cores, for Norway and NovayaZemlya, with a 5000 meter resolution, and then export as netcdf**
     ``python multiexec.py -st 19820101 -en 20221231 -ar [Norway,NovayaZemlya] -c 6 -re 5000 -o nc`` 

     

monthlymaps.py
================

Attention: this function can only be used if the user already have processed the albedo data using either carra2py.py or multiexec.py.
For now, the input and output are in the tif file format, i.e. the carra2py.py or multiexec.pt processing has to be done in the tif format.
These examples are executed as command lines in a terminal, in your carra2py environment.
The default settings is set to make monthly maps for all the regions of all the 2500m output data in the user folders in a given month of the year, and using 4 CPU cores.
Please note the user has to input a specific month in the format "mm", e.g. May is "05" and October is "10". 

How to process specific months
-----------------------------
**Process with default settings for June**
     ``python monthlymaps.py -mo 06``  

**Process with default settings for August**
     ``python monthlymaps.py -mo 08``  

How to process a month, where the input resolution is different than 2500m
-----------------------------
**Process for July with input data at 5000m res.**
     ``python monthlymaps.py -mo 07 -re 5000``  
     
**Process for August with input data at 1000m res.**
     ``python monthlymaps.py -mo 08 -re 1000``  

How to process one Region
-----------------------------
**Process for July in Greenland**
     ``python monthlymaps.py -mo 07 -ar Greenland``  

How to process one Region
-----------------------------
**Process for July in Greenland**
     ``python monthlymaps.py -mo 07 -ar Greenland``  

How to process with more or less than 4 CPU cores
-----------------------------
**Process for July with 12 CPU Cores**
     ``python monthlymaps.py -mo 07 -c 12``  

**Process for July with 1 CPU Core**
     ``python monthlymaps.py -mo 07 -c 1``  
     
     
Example with all arguments
--------------------------------------

**Process using 6 cores, for Svalbard, with a 51000 meter resolution in September**
     ``python multiexec.py -mo 09 -ar Svalbard -re 1000 -c 6`` 

