# Author: Mark Du Preez - DPRMAR021
# CSC3002F OS1 Process Scheduling Assignment 2025
# Used to process raw output from simulation, extract relevant performant metrics and plot that.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import math

def main ():
    if (len(sys.argv) == 2):
        runMainExperiment(int(sys.argv[1]))
    else:
        runTimeQuantumExperiment(int(sys.argv[1]))
    # runTimeQuantumExperiment()

def extractRawData(fileName):
    # Open simulation raw data file and extract data.
    with open(fileName, 'r') as rawData:
        # Skip all the simulation output and get to the raw data.
        while rawData.readline().strip() != "------Bar closed------":
            continue
        
        # Extract the length of execution.
        totalExecutionTime = int(rawData.readline().strip())

        # Get number of patrons.
        numPatrons = int(rawData.readline().strip())
        # Initialize numpy array for patrons.
        patrons = np.arange(numPatrons)

        # Extract patron turnaround times into numpy array.
        patronTurnaroundTimes = np.array(list(map(int, rawData.readline().split())))

        # Extract patron response times into numpy array.
        patronResponseTimes = np.array(list(map(int, rawData.readline().split())))

        # Extract drink response times.
        drinkResponseTimes = []

        # Extracting response times per drink for each drink into a 2D numpy array.
        for i in range(numPatrons):
            drinkResponseTimes.append(list(map(int, rawData.readline().split())))

        drinkResponseTimes = np.array(drinkResponseTimes)

        # Extracting drink execution times per drink for each patron into a 2D numpy array.
        drinkExecutionTimes = []

        for i in range(numPatrons):
            drinkExecutionTimes.append(list(map(int, rawData.readline().split())))
        
        drinkExecutionTimes = np.array(drinkExecutionTimes)

        # Compute CPU utilization

        totalDrinkPrepTime = np.sum(drinkExecutionTimes)

        cpuUtilisation = (totalDrinkPrepTime / totalExecutionTime)*100

        # Computing patron waiting times.

        # Drink waiting time = drink response time - drink execution time
        # Time spent in ready queue.
        # Use element wise subtraction (2D Matrix) then sum all elements in a row (sum all drink waiting times for each patron to get total patron waiting time).
        drinkWaitingTimes = drinkResponseTimes - drinkExecutionTimes
        patronWaitingTimes = np.sum(drinkWaitingTimes, axis = 1)

        # drinkExecutionTimes = np.sum(drinkExecutionTimes, axis=1)
        # patronWaitingTimes = patronTurnaroundTimes - drinkExecutionTimes

        # Extracting patron completion times for throughput calculation.
        patronCompletionTimes = np.array(list(map(int, rawData.readline().split())))

        # Calculating throughput using sliding window.
        # Average Burst Time = 
        # Size of sliding window.
        windowSize = 3000

        # Initialize a numpy array to hold throughput at different times (t) in program.
        throughputs = np.full(totalExecutionTime, np.nan)

        # Set initial window boundaries at time, t = 0.
        windowStart = 0
        windowEnd = windowSize - 1

        while (windowEnd <= totalExecutionTime):
            throughputs[windowStart + (windowSize // 2)] = np.sum((patronCompletionTimes >= windowStart) & (patronCompletionTimes <= windowEnd))
            windowStart += 1
            windowEnd += 1

        # # Compute mean, median and variance of patron waiting times.
        # meanWaitingTime = np.mean(patronWaitingTimes)
        # medianWaitingTime = np.median(patronWaitingTimes)
        # varWaitingTime = np.var(patronWaitingTimes)

        # # Compute mean, median and variance of patron response times.
        # meanResponseTime = np.mean(patronResponseTimes)
        # medianResponseTime = np.median(patronResponseTimes)
        # varResponseTime = np.var(patronResponseTimes)

        # # Compute mean, median and variance of patron turnaround times.
        # meanTurnaroundTime = np.mean(patronTurnaroundTimes)
        # medianTurnaroundTime = np.median(patronTurnaroundTimes)
        # varTurnaroundTime = np.var(patronTurnaroundTimes)

        return patrons, cpuUtilisation, pd.Series(throughputs), patronTurnaroundTimes, patronWaitingTimes, patronResponseTimes
    
def plotThroughput(fcfsThroughput, sjfThroughput, rrThroughput):
    plt.plot(fcfsThroughput, label='First-Come First-Serve')
    plt.plot(sjfThroughput, label='Shortest-Job_First')
    plt.plot(rrThroughput, label='Round-Robin')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Throughput (Processes completed per second)')

    plt.title('Throughput for different CPU scheduling algorithms')

    plt.legend()

    plt.savefig("ThroughputPlot.jpeg", dpi=300)

    plt.clf()

def plotTurnaroundTime(patrons, fcfsTurnaroundTimes, sjfTurnaroundTimes, rrTurnaroundTimes):
    plt.plot(patrons, fcfsTurnaroundTimes, label='First-Come First-Serve')
    plt.plot(patrons, sjfTurnaroundTimes, label='Shortest-Job First')
    plt.plot(patrons, rrTurnaroundTimes, label='Round-Robin')

    plt.xlabel('Processes')
    plt.ylabel('Turnaround Time (seconds)')

    plt.title('Turnaround times of processes for different scheduling algorithms')

    plt.legend()

    plt.savefig('TurnaroundPlot.jpeg', dpi=300)

    plt.clf()

def plotWaitingTime(patrons, fcfsWaitingTimes, sjfWaitingTimes, rrWaitingTimes):
    plt.plot(patrons, fcfsWaitingTimes, label='First-Come First-Serve')
    plt.plot(patrons, sjfWaitingTimes, label='Shortest-Job First')
    plt.plot(patrons, rrWaitingTimes, label='Round-Robin')

    plt.xlabel('Processes')
    plt.ylabel('Waiting Time (seconds)')

    plt.title('Waiting times of processes for different scheduling algorithms')

    plt.legend()

    plt.savefig('WaitingTimesPlot.jpeg', dpi=300)

    plt.clf()

def plotResponseTime(patrons, fcfsResponseTimes, sjfResponseTimes, rrResponseTimes):
    plt.plot(patrons, fcfsResponseTimes, label='First-Come First-Serve')
    plt.plot(patrons, sjfResponseTimes, label='Shortest-Job First')
    plt.plot(patrons, rrResponseTimes, label='Round-Robin')

    plt.xlabel('Processes')
    plt.ylabel('Response Time (seconds)')

    plt.title('Response times of processes for different scheduling algorithms')

    plt.legend()

    plt.savefig('ResponseTimesPlot.jpeg', dpi=300)

    plt.clf()

def plotCPUUtilisation(fcfsCPUUtilisation, sjfCPUUtilisation, rrCPUUtilisation):
    x = ['First-Come First-Serve','Shortest-Job First','Round-Robin']
    heights = [fcfsCPUUtilisation, sjfCPUUtilisation, rrCPUUtilisation]

    plt.bar(x, heights)

    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('CPU Utilisation')

    plt.title('CPU Utilisation for different scheduling algorithms')

    # plt.legend()

    plt.savefig('CPUUtilisationPlot.jpeg', dpi=300)

    plt.clf()

def getCMASeries(throughputs):
    # Performing CMA on throughput time series to smooth it with window size 3000.
    # timeSeriesThroughput = pd.Series(throughputs)

    cmaThroughput = throughputs.rolling(window=1000, center=True).mean()

    return cmaThroughput

def runMainExperiment(numRepetitions):
    patrons, fcfsCPUUtilisation, fcfsThroughput, fcfsTurnaroundTimes, fcfsWaitingTimes, fcfsResponseTimes = extractRawData("scheduler_0_raw_data_0.txt")
    patrons, sjfCPUUtilisation, sjfThroughput, sjfTurnaroundTimes, sjfWaitingTimes, sjfResponseTimes = extractRawData("scheduler_1_raw_data_0.txt")
    patrons, rrCPUUtilisation, rrThroughput, rrTurnaroundTimes, rrWaitingTimes, rrResponseTimes = extractRawData("scheduler_2_raw_data_0.txt")

    # 3 runs (repetitions of the experiment).
    for i in range(1, numRepetitions):
        patronsi, fcfsCPUUtilisationi, fcfsThroughputi, fcfsTurnaroundTimesi, fcfsWaitingTimesi, fcfsResponseTimesi = extractRawData("scheduler_0_raw_data_" + str(i) + ".txt")
        patronsi, sjfCPUUtilisationi, sjfThroughputi, sjfTurnaroundTimesi, sjfWaitingTimesi, sjfResponseTimesi = extractRawData("scheduler_1_raw_data_" + str(i) + ".txt")
        patronsi, rrCPUUtilisationi, rrThroughputi, rrTurnaroundTimesi, rrWaitingTimesi, rrResponseTimesi = extractRawData("scheduler_2_raw_data_" + str(i) + ".txt")

        # Average CPU utilisation.
        fcfsCPUUtilisation = (fcfsCPUUtilisation + fcfsCPUUtilisationi)/2
        sjfCPUUtilisation = (sjfCPUUtilisation + sjfCPUUtilisationi)/2
        rrCPUUtilisation = (rrCPUUtilisation + rrCPUUtilisationi)/2

        # Average Throughput.
        fcfsThroughput = (fcfsThroughput + fcfsThroughputi)/2
        sjfThroughput = (sjfThroughput + sjfThroughputi)/2
        rrThroughput = (rrThroughput + rrThroughputi)/2

        # Average Turnaround time.
        fcfsTurnaroundTimes = (fcfsTurnaroundTimes + fcfsTurnaroundTimesi)/2
        sjfTurnaroundTimes = (sjfTurnaroundTimes + sjfTurnaroundTimesi)/2
        rrTurnaroundTimes = (rrTurnaroundTimes + rrTurnaroundTimesi)/2

        # Average Waiting time.
        fcfsWaitingTimes = (fcfsWaitingTimes + fcfsWaitingTimesi)/2
        sjfWaitingTimes = (sjfWaitingTimes + sjfWaitingTimesi)/2
        rrWaitingTimes = (rrWaitingTimes + rrWaitingTimesi)/2

        # Average Response time.
        fcfsResponseTimes = (fcfsResponseTimes + fcfsResponseTimesi)/2
        sjfResponseTimes = (sjfResponseTimes + sjfResponseTimesi)/2
        rrResponseTimes = (rrResponseTimes + rrResponseTimesi)/2

    # plotThroughput(getCMASeries(fcfsThroughput), getCMASeries(sjfThroughput), getCMASeries(rrThroughput))
    plotThroughput(getCMASeries(fcfsThroughput), getCMASeries(sjfThroughput), getCMASeries(rrThroughput))
    plotTurnaroundTime(patrons, fcfsTurnaroundTimes, sjfTurnaroundTimes, rrTurnaroundTimes)
    plotWaitingTime(patrons, fcfsWaitingTimes, sjfWaitingTimes, rrWaitingTimes)
    plotResponseTime(patrons, fcfsResponseTimes, sjfResponseTimes, rrResponseTimes)
    plotCPUUtilisation(fcfsCPUUtilisation, sjfCPUUtilisation, rrCPUUtilisation)

def runTimeQuantumExperiment(numRepetitions):
    quanta = np.arange(5, 151, 5)
    averageTurnaroundTime = []
    averageResponseTime = []

    for i in quanta:
        averageTurnaroundPerQuantum = []
        averageResponsePerQuantum = []

        for j in range(numRepetitions):
            averageTurnaround, averageResponse = extractAverageMetricsPerQuantum(i, j)
            averageTurnaroundPerQuantum.append(averageTurnaround)
            averageResponsePerQuantum.append(averageResponse)
        
        averageTurnaroundTime.append(np.array(averageTurnaroundPerQuantum).mean())
        averageResponseTime.append(np.array(averageResponsePerQuantum).mean())

    averageTurnaroundTime = np.array(averageTurnaroundTime)
    averageResponseTime = np.array(averageResponseTime)

    minTurnaroundTime = np.min(averageTurnaroundTime)
    minResponseTime = np.min(averageResponseTime)

    minTurnaroundQuantum = np.argmin(averageTurnaroundTime)
    minResponseQuantum = np.argmin(averageResponseTime)

    print("Best time quantum for turnaround time: ", quanta[minTurnaroundQuantum])
    print("Best time quantum for response time: ", quanta[minResponseQuantum])

    minTimeQuantum = int((quanta[minTurnaroundQuantum] + quanta[minResponseQuantum])/2)

    print("Best overall time quantum: " + str(minTimeQuantum))
    print(str(minTimeQuantum))

    plt.plot(quanta, averageTurnaroundTime)
    plt.scatter(quanta[minTurnaroundQuantum], minTurnaroundTime, color='red', s=20, zorder=5)

    plt.xlabel('Time Quantum')
    plt.ylabel('Average Turnaround Time (seconds)')

    plt.title('Average Turnaround times for different time quanta')

    # plt.legend()

    plt.savefig('TurnaroundTimeQuantumPlot.jpeg', dpi=300)

    plt.clf()

    plt.plot(quanta, averageResponseTime)
    plt.scatter(quanta[minResponseQuantum], minResponseTime, color='red', s=20, zorder=5)


    plt.xlabel('Time Quantum')
    plt.ylabel('Average Response Time (seconds)')

    plt.title('Average Response times for different time quanta')

    # plt.legend()

    plt.savefig('ResponseTimeQuantumPlot.jpeg', dpi=300)

    plt.clf()

def extractAverageMetricsPerQuantum(quantum, index):
    # Open simulation raw data file and extract data.
    with open("quantum_" + str(quantum) + "_raw_data_" + str(index) + ".txt", 'r') as rawData:
        # Skip all the simulation output and get to the raw data.
        while rawData.readline().strip() != "------Bar closed------":
            continue
        
        # Extract the length of execution.
        totalExecutionTime = int(rawData.readline().strip())

        # Get number of patrons.
        numPatrons = int(rawData.readline().strip())
        # Initialize numpy array for patrons.
        patrons = np.arange(numPatrons)

        # Extract patron turnaround times into numpy array.
        patronTurnaroundTimes = np.array(list(map(int, rawData.readline().split())))

        # Extract patron response times into numpy array.
        patronResponseTimes = np.array(list(map(int, rawData.readline().split())))

        # Extract drink response times.
        drinkResponseTimes = []

        # Extracting response times per drink for each drink into a 2D numpy array.
        for i in range(numPatrons):
            drinkResponseTimes.append(list(map(int, rawData.readline().split())))

        drinkResponseTimes = np.array(drinkResponseTimes)

        return patronTurnaroundTimes.mean(), drinkResponseTimes.mean()
    
if __name__ == "__main__":
    main()