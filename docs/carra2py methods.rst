
================
carra2py Modules and Methods
================

Description of the carra2py modules and its methods.

class carra2py.AVHRR(date):
================

Parameter: date: str
----------------

the processed date, only in 'yyyymmdd' format

Methods:
----------------

AVHRR.get_data(polar=None)
~~~~~~~~~~~~~~~~

Import the raw AVHRR data of the northern hempishere in native resolution of 5000 meters.

**Parameter: polar: bool, optional:**
             
             if None or False the output will be in a EPSG:4326 projection, if True the output will be in a EPSG:3413 projection.
             
             
**Returns:   raw_lon or raw_x: (m,n) array of floats:**
             
             Longitude coordinates (EPSG:4326) of raw data if polar == None or False, x cooordinates (EPSG:3413) of raw data if polar == True.
             
           **raw_lat or raw_y: (m,n) array of floats:**
             Latitiude coordinates (EPSG:4326) of raw data if polar == None or False, y cooordinate (EPSG:3413) of raw data if polar == True.
             
           **raw_alb: (m,n) array of floats:**
             Raw albedo data in native 5000 meter resolution
             
AVHRR.proc(raw_data=None, area=None, res=2500)
~~~~~~~~~~~~~~~~

Reproject and Intepolate raw AVHRR data to ESPG:3413 and a better resolution. The data is also masked to 9 possible search areas in the arctic region

**Parameter: raw_data: tuple**

             if None, the data for the processing wil come from get_data(), else, the user has tp input the data wants processed. the tuple needs to include                        (x,y,albedo) in that order, x and y is the data coordinates in EPSG:3413 with shape (m,n). Albedo is the raw albedo data from AVHRR in shape (m,n)

AVHRR.export_to_tif(polar=None)
~~~~~~~~~~~~~~~~

AVHRR.export_to_csv(polar=None)
~~~~~~~~~~~~~~~~

AVHRR.export_to_nc(polar=None)
~~~~~~~~~~~~~~~~
