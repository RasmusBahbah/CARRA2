
================
Introduction
================

carra2py is a simple python package for downloading, reprojecting and processing albedo data for CARRA2 in the arctic region.
For now it includes the Advanced Very High Resolution Radiometer (AVHRR) dataset from 1984-present.


Installation
================

**Clone the repository:**
    ``git clone git@github.com:RasmusBahbah/carra2py.git``

**Or download from https://github.com/RasmusBahbah/carra2py:**
    
**Change into the top-level directory:**
    ``cd carra2py``

**Create python environement:**
    ``conda env create -f carra2py.yml``

**Activate python environement:**
    ``conda activate carra2py``


Dependencies
================

Python 3.5 or up


Processing Regions
================

The latest carra2py version can process 9 different Regions: 

+----------------------+-------------+
| Region               | area [km^2] |
+======================+=============+
| Greenland            | 1,744,666   |
+----------------------+-------------+
| Norway               | 34,018      |
+----------------------+-------------+
| Svalbard             | 32,506      |
+----------------------+-------------+
| Iceland              | 11,489      |
+----------------------+-------------+
| NorthernArcticCanada | 100,691     |
+----------------------+-------------+
| SouthernArcticCanada | 40,970      |
+----------------------+-------------+
| AlaskaYukon          | 96,909      |
+----------------------+-------------+
| NovayaZemlya         | 21,506      |
+----------------------+-------------+
| SevernayaZemlya      | 15,842      |
+----------------------+-------------+

