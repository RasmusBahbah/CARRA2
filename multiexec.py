# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:34:21 2023

@author: rabni
"""

import argparse
import pandas as pd
import sys 
import carra2py
from multiprocessing import set_start_method,get_context
if sys.version_info < (3, 4):
    raise "must use python 3.6 or greater"
    

def parse_arguments():
        parser = argparse.ArgumentParser(description='Date range excicuteable for the CARRA2 Module')
        parser.add_argument("-st","--sday", type=str,help="Please input the start day")
        parser.add_argument("-en","--eday", type=str,help="Please input the end day")
        parser.add_argument("-re","--res", type=int,choices=[1000,2500,5000],default=2500,help="Please input the resolution of the output")
        parser.add_argument("-ar","--area", type=str,default=None,help="Please input the areas you want to process")
        parser.add_argument("-o","--output", type=str,default="tif",choices=["tif","csv","nc"],help="Please specify the out format")
        parser.add_argument("-c","--cores", type=int,default=4,help="Please input the number of cores you want to use")
        parser.add_argument("-se","--season", type=str,default="default",help="Please input the season or month you want to process")
        args = parser.parse_args()
        return args
    
    
def multicarra2(date,res,area,out):
  
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
    
    args = parse_arguments() 
    
    if args.season == "default":
        months = ["06","07","08","09"]
    elif (args.season).isnumeric():
        months = [args.season]
    else: 
        months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        
    dates = pd.date_range(start=args.sday,end=args.eday).to_pydatetime().tolist()
    dates = [d.strftime("%Y%m%d") for d in dates]
    dates = [d for d in dates if d[4:6] in [ m for m in months]]
    res = [args.res for i in range(len(dates))]
    area = [args.area for i in range(len(dates))]
    out = [args.output for i in range(len(dates))]
    
    print("Processing for date range: " + args.sday + " to " + args.eday)
    print("Number of Days: " + str(len(dates)))
   
    set_start_method("spawn")
    
    with get_context("spawn").Pool(args.cores) as p:       
            p.starmap(multicarra2,zip(dates,res,area,out))
    
    print("Processing Done!")