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

# Run the simulation 30 times, each time with a different scheduling algorithm:
# Number of patrons = 100 (Fixed for assignment --> Decided sample size)
# Scheduler = [0, 1, 2] ([FCFS, SJF, RR])
# Context switch = 5 (Justified in report as a reasonable context switch for a barman)
# Time quantum = 80 (Experimentally found to be 80)
# Random seed = 5

for i in $(seq 0 29)
do
    for j in 0 1 2
    do
        make run ARGS="100 ${j} 5 80 5" > scheduler_${j}_raw_data_${i}.txt
    done
done

python3 dataprocessing.py 30