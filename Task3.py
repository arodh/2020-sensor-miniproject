#FOr this task you need to work with thte Temp data 
#So i have to filter out the bad temperatures that are too low or too high

#algorithm for detecting anomalies
import pandas 
from pathlib import Path 
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import statistics

def load_data(file:Path) ->T.Dict[str, pandas.DataFrame]:
  temperature = {}
  
  with open(file, "r") as f:
    for line in f:
      r = json.loads(line)
      room = list(r.keys())[0]
      temperature[time] = {room: r[room]["temperature"][0]}
      
  data = {"temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index()}
  return data

if __name__ == "__main__": 
  p = argparse.ArgumentParser(description="load and analyze IoT JSON data")
  p.add_argument("file", help="path to JSON data file") 
  P = p.parse_args() 
  
  file = Path(P.file).expanduser() 
  
  #Get data 
  data = load_data(file) 
  
  rooms = ["lab1", "class1","office"] 
  stds = 1.5 
  
  for room in rooms: 
    print("Finding anomalies: " + room) 
    temps = data["temperature"][room].dropna() 
    rmean = statistics.mean(temps) 
    rstdev = statistics.stdev(temps) 
    badsize=0 
    size=temps.size 
    print("Number of Data Points "+str(size)) 
    to_drop = [] 
    for x in range(0, temps.size): 
      limit = rstdev *stds 
      temp = temps.iloc[x] 
      dev = abs(temp - rmean) 
      
      if dev > limit: 
        badsize=badsize +1 
        print("Error: outlier") 
        print(" Temperature: " + str(temps[x])) 
        to_drop += [temps.index[x]] 
        temps = temps.drop(to_drop) 
        
        percent = (badsize/size)*100 
        print("Percent of Bad Data Points is " + str(percent)) 
        median = statistics.median(temps) 
        variance = statistics.variance (temps) 
        print("The median temperature is "+ str(median)) 
        print("The variance of the temperature is "+ str(variance)) #mean and variance print("\n")
        
'''
good_temp=[]
bad_temp=[]
filer = open('data.txt')
data = load_data('data.txt')
onestd = statistics.pstdev(data)

for k in data:
  if ((k-statistics.mean(data))>=onestd*3):
    bad_temp.append(k)
  else:
    good_temp.append(k)
'''    
