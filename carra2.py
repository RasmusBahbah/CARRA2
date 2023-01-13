# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:26:47 2023

@author: rabni
"""

import os
from pyproj import CRS,Transformer
from scipy.spatial import KDTree
import xarray as xr
import numpy as np
from rasterio.transform import Affine
import rasterio
import urllib.request
import pandas as pd
import glob
import netCDF4 as nc 
import sys
import warnings
import datetime as dt
warnings.filterwarnings("ignore", category=FutureWarning)

def opentiff(filename):
    
   "Input: Filename of GeoTIFF File "
   "Output: xgrid,ygrid, data paramater of Tiff, the data projection"
   
   
   da = xr.open_rasterio(filename)
   proj = CRS.from_string(da.crs)
   
   
   transform = Affine(*da.transform)
   elevation = np.array(da.variable[0],dtype=np.float32)
   nx,ny = da.sizes['x'],da.sizes['y']
   x,y = np.meshgrid(np.arange(nx,dtype=np.float32), np.arange(ny,dtype=np.float32)) * transform
   
   return x,y,elevation,proj


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
    
    return None 


def reproject(raw_lon,raw_lat):
    
    WGSProj = CRS.from_string("+init=EPSG:4326")
    PolarProj = CRS.from_string("+init=EPSG:3413")
    
    wgs_data = Transformer.from_proj(WGSProj, PolarProj)
    
    xx, yy = wgs_data.transform(raw_lon,raw_lat)
   
    return xx,yy

class AVHRR():
    
    def __init__(self,date):
            
        self.date = date
        self.base_folder = os.getcwd()
        
    def get_data(self,polar = None):
      
        
        if not os.path.exists(self.base_folder + os.sep + 'rawdata'):

            os.mkdir(self.base_folder + os.sep + 'rawdata')
        
        data_folder = self.base_folder + os.sep + 'rawdata' + os.sep + self.date
        
        if not os.path.exists(data_folder):
                
            os.mkdir(data_folder)
            
        os.chdir(data_folder)
        
        
        base_url = 'https://www.ncei.noaa.gov/data/avhrr-polar-pathfinder-extended/access/nhem'
        
        date_1 = dt.datetime.strptime(self.date, "%Y%m%d")
        
        procdatesplus = [(date_1 + delta).strftime("%Y%m%d") for delta in \
                         [dt.timedelta(days=int(d)) for d in np.arange(0,6)]]
        
        procdates = ['20190624','20190625','20190618'] + procdatesplus
        
        check = 0
        
        for d in procdates: 
            if check == 0:
                try: 
                    file = 'Polar-APP-X_v02r00_Nhem_0400_d' + self.date + '_c' + d + '.nc'
                    urllib.request.urlretrieve(base_url + "/" + self.date[:4] +  "/" + file, file)
                    check = 1
                except:
                    pass
        
        
        os.chdir(self.base_folder)
        
        ncfile = nc.Dataset(data_folder + os.sep + file)
        
        if polar is None: 
            
            raw_alb = np.array(ncfile["cdr_surface_albedo"])[0]
            raw_alb[raw_alb == 9999] = np.nan
            raw_lon = np.array(ncfile["longitude"])
            raw_lat = np.array(ncfile["latitude"])
            ncfile.close()
            
            if not any(~(np.isnan(raw_alb.ravel()))):
                print('No surface albedo data was available'+\
                              'on the given date')
                sys.exit()
            
            
            return raw_lon,raw_lat,raw_alb
            
        else: 
            
            raw_alb = np.array(ncfile["cdr_surface_albedo"])[0]
            raw_x,raw_y = reproject(np.array(ncfile["longitude"]),np.array(ncfile["latitude"]))
            raw_alb[raw_alb == 9999] = np.nan
            ncfile.close()
           
            
            if not any(~(np.isnan(raw_alb.ravel()))):
                print('No surface albedo data was available'+\
                              'on the given date')
                sys.exit()
                
            return raw_x,raw_y,raw_alb
        
             
        
    def proc(self,raw_data = None, area = None,res = 2500):
                    
        if not raw_data:
            xx,yy,albedo = self.get_data(polar = 1)
        else: 
            xx = raw_data[0]
            yy = raw_data[1]
            albedo = raw_data[2]
        
        res_proc = [1000,2500,5000]
        
        if res not in res_proc: 
            
            print('Specified resolution is not available. ' + \
                          'Please use one of these options ' + str(res_proc))
            sys.exit()
        
        mask_list = glob.glob(self.base_folder + os.sep + 'masks' + os.sep + '*.csv')
        grid_list = glob.glob(self.base_folder + os.sep + 'masks' + os.sep + '*' + str(res) + 'm.tif')
        
        if area:
            mask_list = [m for m in mask_list if m.split(os.sep)[-1].split('_')[0] in area]
            grid_list = [g for g in grid_list if g.split(os.sep)[-1].split('_')[0] in area]
        
        eps = (2 * 10**-5) # Shape Parameter
        
        data = {}
        
        for m,g in zip(mask_list,grid_list):
            
            a = m.split(os.sep)[-1].split('_')[0]
            
            df = pd.read_csv(m)
            min_x = int(df['MINX']) 
            max_x = int(df['MAXX'])
            min_y = int(df['MINY']) 
            max_y = int(df['MAXY']) 
            
            #print("min y: ",int(min_y))
            bbmsk =  (xx <= max_x) & (xx >= min_x)\
                   & (yy >= min_y) & (yy <= max_y)
                      
            xx_filt = xx[bbmsk]
            yy_filt = yy[bbmsk]
            alb_filt = albedo[bbmsk]
            
            
            #x_range = np.arange(min_x,max_x,res,dtype=np.float32)
            #y_range = np.arange(min_y,max_y,res,dtype=np.float32)
            
            #x_grid,y_grid = np.meshgrid(x_range,y_range)
            
            x_grid,y_grid,z_grid,gridproj = opentiff(g)            
            
            datagrid = np.ones_like(z_grid) * z_grid
            
            tree = KDTree(np.transpose(np.array([xx_filt,yy_filt])))
            
            
            print('Interpolating for ' + a)
            
            for i,(xmid,ymid) in enumerate(zip(x_grid.ravel(),y_grid.ravel())):
                
                dd, ii = tree.query([xmid,ymid],k = 20,p = 2)
                
                dd = dd[~np.isnan(alb_filt.ravel()[ii])]
                ii = ii[~np.isnan(alb_filt.ravel()[ii])]
                
                
                if (len(ii) == 0) or (datagrid.ravel()[i] != 220):
                    
                    
                    datagrid.ravel()[i] = np.nan
                    
                   
                else: 

                    
                    w = np.exp(-(eps * dd)**2)
                   
                    datagrid.ravel()[i] = np.average(alb_filt.ravel()[ii], weights = w)
            
            
            data[a] = {"x" : x_grid,\
                          "y" : y_grid,\
                          "albedo" : datagrid}
        return data
        
    def export_to_tif(self,output = None, path = 'default'):    
        
        
        crs = CRS.from_string("+init=EPSG:3413")
        
        
        if output is None: 
            
            output = self.proc()
            
            
        if path == 'default':
            pathoutput = self.base_folder + os.sep + "output"
            if not os.path.exists(pathoutput):
                os.mkdir(pathoutput)
            path = self.base_folder + os.sep + "output" + os.sep + self.date
            

        if not os.path.exists(path):
            os.mkdir(path)
            
        for a in output:
            
            x = output[a]["x"]
            y = output[a]["y"]
            z = output[a]["albedo"]
            
            res = int((x[0,1] - x[0,0]) + (x[0,0] - x[1,0]))
            
            filename = self.date + "_" + a + "_" + str(res) + "m_AVHRR.tif"
            
            exporttiff(x, y, z, crs, path, filename)
        
        return
        
    
            
        
    def export_to_csv(self,output = None, path = 'default'):
        
        if output is None: 
            
            output = self.proc()
            
        if path == 'default':
            path = self.base_folder + os.sep + "output" + os.sep + self.date
        
        if not os.path.exists(path):
            os.mkdir(path)
            
        for a in output: 
            
            
            x = output[a]["x"]
            y = output[a]["y"]
            z = output[a]["albedo"]
            
            res = int((x[0,1] - x[0,0]) + (x[0,0] - x[1,0]))
            
            filename = self.date + "_" + a + "_" + str(res) + "m_AVHRR.csv"
            
            df = pd.DataFrame({'x' : x,\
                               'y' : y,\
                               'albedo' : z})
                
            df.to_csv(path + os.sep + filename)

        
        return   
            
    def export_to_nc(self,output = None, path = 'default'):
        
        if output is None: 
            
            output = self.proc()
            
        if path == 'default':
            
            path = self.base_folder + os.sep + "output" + os.sep + self.date
        
        if not os.path.exists(path):
            os.mkdir(path)
            
        for a in output: 
            
            
            x = output[a]["x"]
            y = output[a]["y"]
            z = output[a]["albedo"]
            
            res = int((x[0,1] - x[0,0]) + (x[0,0] - x[1,0]))
            
            filename = self.date + "_" + a + "_" + str(res) + "m_AVHRR.nc"
            
            
            ds = nc.Dataset(path + os.sep + filename, 'w', format='NETCDF4')
            
            ds.createDimension('id1', np.shape(x)[0])
            ds.createDimension('id2', np.shape(x)[1])
            
            x_out = ds.createVariable('x', 'f4', ('id1', 'id2'), zlib=True)
            y_out = ds.createVariable('y', 'f4', ('id1', 'id2'), zlib=True)
            alb_out = ds.createVariable('albedo', 'f4', ('id1', 'id2'), zlib=True)
                
            x_out[:,:] = x
            y_out[:,:] = y
            alb_out[:,:] = z
        
            ds.close()
            
            
        return
