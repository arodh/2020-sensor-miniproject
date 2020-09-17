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
# imnport this library to use Stats functions
import statistics


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

    rooms = ["lab1", "class1", "office"]
    datatypes = ["temperature", "occupancy", "co2"]

# Median and Variance section of Temp and Occupancy

    print("Median and Variance Data:")

    for datatype in datatypes:
        df = data[datatype]
        for room in rooms:
            list = df[room]
            list = list.dropna()
            median = statistics.median(list)
            variance = statistics.variance (list)
            if datatype != "co2":
                print("The median " + str(datatype) + " of room " + str(room)+ " is "+ str(median))
                print("The variance of the " + str(datatype) + " of room " + str(room)+ " is "+ str(median))

    print("\n")

# probability distribution plot for each sensor in one room section
    print("Probability Distributions Plot for each Sensor:")
    for datatype in datatypes:
        df=pandas.DataFrame(data[datatype])
        Chart_Title = "Probabillity Distruction Function for " + str(datatype)
        df.plot.kde(title = Chart_Title)

    print("\n")

# Mean and Variance of the Time Interval Data

    print("Mean and Variance of Time Interval:")
    for datatype in datatypes:
        df1=data[datatype]
        Tdict={}
        for room in rooms:
            list = df[room]
            list = list.dropna()
            Tdiff=[0]*list.size
            for x in range (0, list.size):
                if x !=0:
                    Tdiff[x-1]=float(list.index[x].timestamp()-list.index[x-1].timestamp())
            Tdict[room]=Tdiff
            mean = statistics.mean(Tdiff)
            variance = statistics.variance(Tdiff)

            print("mean time differance of " +str(datatype) + " in " +str(room)+ " is " + str(mean))
            print("variance of time differances of " +str(datatype) + " in " +str(room)+ " is " + str(variance))
            
        rooms = rooms.get(datatypes)   
        print("\n")    
        print("Probability Distribution Functions of the Time Interval")
        Prob_Dis = dict(class1 = np.array(Tdict["class1"]), office = np.array(Tdict["office"]),lab1 = np.array(Tdict["lab1"]))
        df2=pandas.DataFrame(dict([(k,pandas.Series(v))for k, v in Prob_Dis.items()]))
        Title  = " Probability Distribution Function of the Time Interval for " + str(datatype)
        df2.plot.kde(title=Title)
        



    # for k in data:
    #     # data[k].plot()
    #     time = data[k].index
    #     data[k].hist()
    #     plt.figure()
    #     plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
    #     plt.xlabel("Time (seconds)")

    plt.show()
