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


filer = open('data.txt')
def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open('data.txt', "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

            temp = []
         
     #sorts objects by labels along the given axis       
    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    data = load_data('data.txt')

# there should be a loop that only retains the temperature points I want,(the points that arent outliers)
#from this file you then analyze it 
#I should then print out the bad data to see what time of temperatures the simulation is producing.
#then with the good data I can find the temp median and variance 
#The bottom code is where I'm having trouble in sesperating the ooutliers from the temp data i want

good_temp=[]
bad_temp=[]
filer = open('data.txt')
data = load_data('data.txt')
onestd = statistics.pstdev(data)

for k in data:
  if ((k-statistics.mean(data))>=onestd*3):
    bad_temp.append(k)
    print('Bad Temperatures:')
    print(bad_temp)
  else:
    good_temp.append(k)
    
    
for k in good_temp:
    if k == 'temperature':
            print('Temperatures')
            print('')
            print('For Office:')
            print('Median: ' + str(data[k]['office'].median()))
            print('Variance: ' + str(data[k]['office'].var()))
    if k == 'temperature':
            print('For lab1:')
            print('Median: ' + str(data[k]['lab1'].median()))
            print('Variance: ' + str(data[k]['lab1'].var()))  
    if k == 'temperature':
            print('For class1:')
            print('Median: ' + str(data[k]['class1'].median()))
            print('Variance: ' + str(data[k]['class1'].var()))
