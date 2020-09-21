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
      time = datetime.fromisoformat(r[room]["time"])
      temperature[time] = {room: r[room]["temperature"][0]}
      
  data = {temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index()}
  return data

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
    
