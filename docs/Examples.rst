
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

How to download raw data
------------------------

**input the date in the carra2py.AVHRR() module**
    ``avhrr = carra2py.AVHRR("19940506")``

**get the data in EPSG:4326 using the get_data() method**
    ``rawdata = avhrr.get_data()``
    
**or get the data in EPSG:3413 using the get_data() method**   
    ``rawdata = avhrr.get_data(polar=True)``
    
How to process data 
--------------------

How to export data
--------------------

multiexec.py
================

These examples are executed as command lines in a terminal, in your carra2py environment.

How to process several dates
-----------------------------

How to process specific areas
------------------------------

How to change output format
-----------------------------

how to change the number of cores used
--------------------------------------
