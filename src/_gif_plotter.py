# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:35:58 2023

@author: rabni
"""

import glob
import xarray as xr
import os 
import numpy as np
import rioxarray as rio
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import merge_tiffs
from osgeo import gdal
import subprocess

data_folder = r'C:\Users\rabni\Desktop\CARRA2_Albedo_AVHRR_v2\CARRA2_Albedo_AVHRR_v2'
merged_f = r'C:\Users\rabni\Desktop\CARRA2\src\merged'

data_files = glob.glob(data_folder +  os.sep + "**" + os.sep + "*5000m_AVHRR.tif", recursive = True)
data_files = [df for df in data_files if "1982" in df]


dates = [d.split(os.sep)[-2] for d in data_files]
dates = list(set(dates))
merge_out = [dd + '_merged.tif' for dd in dates]

for dd,o in zip(dates,merge_out): 
    
    filenamesList = [ff for ff in data_files if dd in ff][::-1]
    out = merged_f + os.sep + o
    
    subprocess.call(
        [sys.executable,"gdal_merge.py", "-co", "BIGTIFF=YES", "-co", "compress=LZW" ,"-a_nodata", "nan","-o", out, *filenamesList]
    )
    # g = gdal.Warp(out, filenamesList,format="GTiff",
    #           **kwargs) # if you want
    # g = gdal.Warp(out, filenamesList, resampleAlg="MAX",format="GTiff",
    #           options=["COMPRESS=LZW", "TILED=YES"]) # if you want
    # g = None
    #merge_tiffs(filenamesList, out, overwrite=True)
    

time = pd.to_datetime(dates)
reference_time = pd.Timestamp("1982-04-30")
rds = rio.open_rasterio(data_files[0])



xx = np.array(rds.x)
yy = np.flip(np.array(rds.y))

albedo = np.ones((len(yy), len(xx),len(data_files))) * np.nan

for ii,ff in enumerate(data_files):
    
    
    
    rds = rio.open_rasterio(ff)
    albedo[:,:,ii] = np.flip(np.array(rds))
    
    
ds = xr.Dataset(
    data_vars=dict(
        albedo=(["y", "x", "time"], albedo),
    ),
    coords=dict(
        xx=(["x"], xx),
        yy=(["y"], yy),
        time=time,
        reference_time=reference_time,
    ),
    attrs=dict(description="Albedo data Greenland"),
)

fig, axes = plt.subplots(figsize=[11,8]) #Creating the basis for the plot


def animate(time):
    axes.clear()
    ds.isel(time=time).albedo.plot(ax=axes, add_colorbar= False)
    

ani = animation.FuncAnimation(fig, animate, len(data_files), interval=200, blit=False)

mld = ds.isel(time=0).albedo.plot(ax=axes, add_colorbar= False)
cbar = fig.colorbar(mld)
cbar.set_label('Albedo [unitless]')
fig.suptitle("Greenland Albedo 1982", fontsize= 18)

#ani.save('animation.gif', writer='imagemagick', fps = 2) #Save animation as gif-file

ani.save('animation.gif', writer='imagemagick', fps = 2) #Save animation as gif-file