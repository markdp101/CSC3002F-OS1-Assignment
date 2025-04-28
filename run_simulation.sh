#!/bin/bash

# Author: Mark Du Preez - DPRMAR021
# CSC3002F OS1 Process Scheduling Assignment 2025

# To install required python libaries if not already installed: matplotlib, numpy and pandas.
# Uncomment the below:
# pip3 install matplotlib
# pip3 install numpy
# pip3 install pandas

# Clean all files.
make clean
rm -f *raw_data*.txt *Plot.jpeg quantum.txt

# Compile program.
make
# First determine best time quantum.
# Run the simulation 20 times, each time with a different scheduling algorithm:
# Number of patrons = 150 (Should set to 100 for actual runs)
# Scheduler = [0, 1, 2] ([FCFS, SJF, RR])
# Context switch = 1 (Must still be experimented with)
# Time quantum = 80 (Experimentally found to be 80)
# Random seed = 5

for i in $(seq 0 9)
do
    for j in $(seq 5 5 150)
    do
        make run ARGS="150 2 1 ${j} 5" > quantum_${j}_raw_data_${i}.txt
    done
done
python3 dataprocessing.py 10 1 > quantum.txt

quantum=$(tail -n 1 quantum.txt)

for i in $(seq 0 19)
do
    for j in 0 1 2
    do
        make run ARGS="150 ${j} 1 ${quantum} 5" > scheduler_${j}_raw_data_${i}.txt
    done
done

python3 dataprocessing.py 19