# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 11:40:50 2023

@author: rabni
"""


import argparse
from pyproj import CRS,Transformer
import sys 
import logging
import time
import datetime
import glob
import os
import numpy as np
from scipy.ndimage import gaussian_filter
from rasterio.transform import Affine
import rasterio
import warnings
import xarray as xr
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
from multiprocessing import set_start_method,get_context
if sys.version_info < (3, 4):
    raise "must use python 3.6 or greater"
 
    
if not os.path.exists("logs"):
        os.makedirs("logs")
        
logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f'logs/monthlymaps_{time.strftime("%Y_%m_%d",time.localtime())}.log'),
            logging.StreamHandler()
        ])

def parse_arguments():
        parser = argparse.ArgumentParser(description='Date range excicuteable for the CARRA2 Module')
        parser.add_argument("-mo","--month", type=str,help="Please input the month(s) you want process")
        parser.add_argument("-re","--res", type=int,choices=[1000,2500,5000],default=2500,help="Please input the resolution of the input")
        parser.add_argument("-ar","--area", type=str,default=None,help="Please input the areas you want to process")
        parser.add_argument("-c","--cores", type=int,default=4,help="Please input the number of cores you want to use")
        args = parser.parse_args()
        return args
    
    

def multimaps(month,res,area,monthlyfolder):
    
    logging.info("Processing: " + month)
    folders = os.listdir()
    folders = [f for f in folders if month in f]
    
    files = [glob.glob(f + os.sep + "*.tif") for f in folders]
    files = [item for sublist in files for item in sublist]
    files = [fi for fi in files if str(res) in fi]
    
    
    
    outputfolder = monthlyfolder + os.sep + month
    if not os.path.exists(outputfolder):
        os.mkdir(outputfolder)
    
    for a in area: 
        logging.info(f"Starting on {a} in {month}")
        filesarea = [fa for fa in files if a in fa]
        start = 1
        
        if filesarea:
        
            start = 1
            
            
            for i,f in enumerate(filesarea): 
                
                x,y,z,crs = opentiff(f)
                #print(np.nanmean(z)) 
                if start == 1: 
                    
                    data = np.tile(z * np.nan, (len(files), 1, 1))
                    
                    start = 0
                    
                data[i,:,:] = z
                
            
            m,n = np.shape(data[0,:,:])
            
            mergemean = np.array([[np.nanmean(data[:,i,j]) for j in range(n)] for i in range(m)])
            mergemean[mergemean == 0] = np.nan
            sigma = np.nanstd(mergemean.ravel())
             
            if len(mergemean[~np.isnan(mergemean)]) > 0:
                
                mergemean = gaussian_filter(mergemean, sigma)
                name = month + "_" + a + "_" + str(res) + "_monthlymean.tif"  
                exporttiff(x,y,mergemean,CRS.from_string("+init=EPSG:3413"),outputfolder,name)
            
            logging.info(f"{a} in {month} has been exported")
            
        else: 
            
            logging.info(f"{a} in {month} had no data")

def exporttiff(x,y,z,crs,path,filename):
    
    "Input: xgrid,ygrid, data paramater, the data projection, export path, name of tif file"
    
    resx = (x[0,1] - x[0,0])
    resy = (y[1,0] - y[0,0])
    transform = Affine.translation((x.ravel()[0]),(y.ravel()[0])) * Affine.scale(resx, resy)
    
    if resx == 0:
        resx = (x[0,0] - x[1,0])
        resy = (y[0,0] - y[0,1])
        transform = Affine.translation((y.ravel()[0]),(x.ravel()[0])) * Affine.scale(resx, resy)
    
    with rasterio.open(
    path + os.sep + filename,
    'w',
    driver='GTiff',
    height=z.shape[0],
    width=z.shape[1],
    count=1,
    dtype=z.dtype,
    crs=crs,
    transform=transform,
    ) as dst:
        dst.write(z, 1)
    
    dst.close()
    
    return None 
 
def opentiff(filename):
    
   "Input: Filename of GeoTIFF File "
   "Output: xgrid,ygrid, data paramater of Tiff, the data projection"
   
   da = xr.open_rasterio(filename)
   proj = CRS.from_string(da.crs)
   
   
   transform = Affine(*da.transform)
   elevation = np.array(da.variable[0],dtype=np.float32)
   nx,ny = da.sizes['x'],da.sizes['y']
   x,y = np.meshgrid(np.arange(nx,dtype=np.float32), np.arange(ny,dtype=np.float32)) * transform
   
   da.close()
   
   return x,y,elevation,proj


if __name__ == "__main__":
    
    args = parse_arguments() 
    
    basefolder = os.getcwd() 
    
    thisyear = datetime.date.today().year

    months = [str(y)+m for m in [args.month] for y in list(np.arange(1982,thisyear)) ]
    if args.area == None:
        args.area = ["Greenland","Iceland","AlaskaYukon","Svalbard","Norway",\
                     "NovayaZemlya","SevernayaZemlya","SouthernArcticCanada",\
                     "SouthernArcticCanada"]
    else:
        args.area = [args.area]
    
    res = [args.res for i in range(len(months))]
    area = [args.area for i in range(len(months))]
    
    logging.info("Number of Months: " + str(len(months)))
    
    os.chdir("output")
    
    monthlyfolder = basefolder + os.sep + "monthlymaps"
    
    if not os.path.exists(monthlyfolder):
        os.mkdir(monthlyfolder)
   
    monthlyfolder = [monthlyfolder for i in range(len(months))] 
   
    set_start_method("spawn")
    
    with get_context("spawn").Pool(args.cores) as p:       
            p.starmap(multimaps,zip(months,res,area,monthlyfolder))
    
    logging.info("Processing Done!")
    