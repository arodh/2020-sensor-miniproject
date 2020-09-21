#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

filer = open('data.txt')
def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}
#I will be leaving myself notes like this to try an understand what is happening
#r is a command for the opening a file for reading
#Json.loads  will take a string and returns a json object

    with open('data.txt', "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

            temp = []


#so i neeed to make a loop that goes through all the info and organizes it 
#there are python commands that can calculate the mean and variance for you  

        occu = []          
     #sorts objects by labels along the given axis       
    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    data = load_data('data.txt')

    for k in data:
        if k == 'temperature':
            print('Temperatures')
            print('')
            print('For Office:')
            print('Median: ' + str(data[k]['office'].median()))
            print('Variance: ' + str(data[k]['office'].var()))
        if k == 'occupancy':
            print('')
            print('Occupancies')
            print('')
            print('For office:')
            print('Median: ' + str(data[k]['office'].median()))
            print('Variance: ' + str(data[k]['office'].var()))
        if k == 'temperature':
            print('For lab1:')
            print('Median: ' + str(data[k]['lab1'].median()))
            print('Variance: ' + str(data[k]['lab1'].var()))
        if k == 'occupancy':
            print('For lab1:')
            print('Median: ' + str(data[k]['lab1'].median()))
            print('Variance: ' + str(data[k]['lab1'].var()))
        if k == 'temperature':
            print('For class1:')
            print('Median: ' + str(data[k]['class1'].median()))
            print('Variance: ' + str(data[k]['class1'].var()))
        if k == 'occupancy':
            print('For class1:')
            print('Median: ' + str(data[k]['class1'].median()))
            print('Variance: ' + str(data[k]['class1'].var()))

plt.figure()
data[k]['office'].plot.density()
plt.title('Probability Density Functions for ' + k)
if k == 'temperature':
    plt.xlabel('Temperature/°C')
if k == 'co2':       
    plt.xlabel('co2 level')
    
    plt.figure()
    data[k]['lab1'].plot.density()
    plt.title('Probability density Functions for Occupancy')
    plt.xlabel('Amt of people')

    time = data['temperature'].index
    time_series = pandas.Series([t.total_seconds() for t in (time[1:] - time[:-1])])
    print('')
    print('Time Interval across all Rooms:')
    print('')
    print('Time Interval Mean: ' + str(time_series.mean()))
    print('Time Interval Variance: ' + str(time_series.var()))
    print('')
    plt.figure()
    time_series.plot.density()
    plt.title('Probability Density Function For Time Interval')
    plt.xlabel('Time (seconds)')

    plt.show()   
