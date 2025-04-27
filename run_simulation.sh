#!/bin/bash

# Clean all files.
make clean
rm -f *raw_data.txt

# Compile program.
make

# Run the simulation 3 times, each time with a different scheduling algorithm:
# Number of patrons = 30 (Should set to 100 for actual runs)
# Scheduler = [0, 1, 2] ([FCFS, SJF, RR])
# Context switch = 1 (Must still be experimented with)
# Time quantum = 70 (Must still be experimented with)
# Random seed = 5

for i in 0 1 2
do
    make run ARGS="30 ${i} 1 70 5" > scheduler_${i}_raw_data.txt
done