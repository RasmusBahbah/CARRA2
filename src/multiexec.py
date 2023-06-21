# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:34:21 2023

@author: rabni
"""

import argparse
import pandas as pd
import sys 
import carra2py
import logging
import glob
import os
import time
from multiprocessing import set_start_method,get_context
# try:
#     set_start_method("spawn")
# except:
#     pass

if sys.version_info < (3, 4):
    raise "must use python 3.6 or greater"
    
base_f  = os.path.abspath('..')

if not os.path.exists(base_f + os.sep + "logs"):
        os.makedirs(base_f + os.sep + "logs")
        
log_f = base_f + os.sep + "logs"
logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(f'{log_f}' + os.sep + f'multiexec_{time.strftime("%Y_%m_%d",time.localtime())}.log'),
            logging.StreamHandler()
        ])

def parse_arguments():
        parser = argparse.ArgumentParser(description='Date range excicuteable for the CARRA2 Module')
        parser.add_argument("-st","--sday", type=str,help="Please input the start day")
        parser.add_argument("-en","--eday", type=str,help="Please input the end day")
        parser.add_argument("-re","--res", type=int,choices=[1000,2500,5000],default=2500,help="Please input the resolution of the output")
        parser.add_argument("-ar","--area", type=str,default='default',help="Please input the areas you want to process")
        parser.add_argument("-o","--output", type=str,default="tif",choices=["tif","csv","nc"],help="Please specify the out format")
        parser.add_argument("-c","--cores", type=int,default=4,help="Please input the number of cores you want to use")
        parser.add_argument("-se","--season", type=str,default="default",help="Please input the season or month you want to process")
        parser.add_argument("-m","--mode", type=str,default="local",choices=["local","global"],help="Please input the process mode")
        args = parser.parse_args()
        return args
    
def multicarra2_local(date,res,area,out):
  
    pathfinder = carra2py.AVHRR(date,block=True)
    data = pathfinder.proc(area=area,res=res)
    
    if data:    
        if out == 'tif':
            pathfinder.export_to_tif(output = data)
    
        elif out == 'nc':
            pathfinder.export_to_nc(output = data)
    
        else: 
            pathfinder.export_to_csv(output = data)
            
            
if __name__ == "__main__":
    
    
    carra_f = os.path.abspath('..')
    output_f = carra_f + os.sep + 'output'
    mask_list = glob.glob(carra_f + os.sep + 'masks' + os.sep + '*.csv')
    mask_list = [m for m in mask_list if 'Arctic' not in m]
    area_list = [m.split(os.sep)[-1].split('_')[0] for m in mask_list]
    
    args = parse_arguments() 
    
    if args.season == "default":
        months = ["03","04","05","06","07","08","09"]
    elif (args.season).isnumeric():
        months = [args.season]
    else: 
        months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        
    
    if args.area != "default":
        area_list = args.area
        
    
    dates = pd.date_range(start=args.sday,end=args.eday).to_pydatetime().tolist()
    dates = [d.strftime("%Y%m%d") for d in dates]
    dates = [d for d in dates if d[4:6] in [ m for m in months]]
    
    res_str = str(args.res)
    out_str = args.output
    mode = args.mode
    
    if os.path.exists(output_f) and mode == 'local': 
        
        f_done = glob.glob(output_f + os.sep + '**' + os.sep + f'*{res_str}m_AVHRR.{out_str}',recursive=True)
        f_done_id = [f.split(os.sep)[-1][:-16] for f in f_done]
        
        ids = [(d + '_' + a) for d in dates for a in area_list]
        ids_not_done = [i for i in ids if i not in f_done_id]
        dates_not_done_all =  [i[:8] for i in ids_not_done]
        dates_not_done = [d for d in dates if d in dates_not_done_all]
        
        area_not_done = [[a[9:] for a in ids_not_done if (a[:8] == d)] for d in dates_not_done]
        
    elif  os.path.exists(output_f) and mode == 'global':
        
       f_done = glob.glob(output_f + os.sep + '**' + os.sep + f'*Arctic_{res_str}m_AVHRR.{out_str}',recursive=True)
       f_done_dates = [f.split(os.sep)[-1][:8] for f in f_done]
      
       dates_not_done = [d for d in dates if d not in f_done_dates]
       area_not_done = ['Arctic' for d in dates_not_done]
    
    
    elif mode == 'local': 
        
        dates_not_done = dates
        area_not_done = [[a for a in area_list] for d in dates_not_done]
       
    elif mode == 'global':
        
       dates_not_done = dates
       area_not_done = ['Arctic' for d in dates_not_done]
       
       
      
       
    res = [args.res for i in range(len(dates_not_done))]
    area = area_not_done
    out = [args.output for i in range(len(dates_not_done))]
   
    
    logging.info(f"Processing for date range: {args.sday} to {args.eday}")
    logging.info(f"Number of Days: {len(dates_not_done)}") 
    logging.info(f"Mode: {mode}")
    logging.info(f"Number of Cores: {args.cores}")
    
    set_start_method("spawn")
    
    with get_context("spawn").Pool(args.cores) as p:       
            p.starmap(multicarra2_local,zip(dates_not_done,res,area,out))
            p.close()
            p.join()
    
        
        
    logging.info("Processing Done!")