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
rm -f *raw_data*.txt *Plot.jpeg

# Compile program.
make

for i in $(seq 0 9)
do
    for j in $(seq 5 5 150)
    do
        make run ARGS="100 2 5 ${j} 5" > quantum_${j}_raw_data_${i}.txt
    done
done

python3 dataprocessing.py 10 1 > quantum.txt