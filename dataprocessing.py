# Author: Mark Du Preez - DPRMAR021
# CSC3002F OS1 Process Scheduling Assignment 2025
# Used to process raw output from simulation, extract relevant performance metrics and plot that.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def main ():
    if (len(sys.argv) == 2):
        runMainExperiment(int(sys.argv[1]))
    else:
        runTimeQuantumExperiment(int(sys.argv[1]))

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

        # Extracting patron completion times for throughput calculation.
        patronCompletionTimes = np.array(list(map(int, rawData.readline().split())))

        # Calculating throughput using sliding window.
        # Size of sliding window. Used to smooth throughput more.
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

        return patrons, cpuUtilisation, pd.Series(throughputs), patronTurnaroundTimes, patronWaitingTimes, patronResponseTimes
    
def plotThroughput(fcfsThroughput, sjfThroughput, rrThroughput):
    plt.plot(fcfsThroughput, label='First-Come First-Serve')
    plt.plot(sjfThroughput, label='Shortest-Job_First')
    plt.plot(rrThroughput, label='Round-Robin')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Throughput (Processes/Patrons completed per second)')

    plt.title('Throughput for different CPU scheduling algorithms', loc='center')

    plt.legend()

    plt.savefig("ThroughputPlot.jpeg", dpi=300)

    plt.clf()

    algorithms = ['First-Come First-Serve', 'Shortest-Job First', 'Round-Robin']
    means = [np.mean(fcfsThroughput), np.mean(sjfThroughput), np.mean(rrThroughput)]
    medians = [fcfsThroughput.median(), sjfThroughput.median(), rrThroughput.median()]

    x = np.arange(len(algorithms))
    width = 0.35    

    # Create bar plot
    fig, ax = plt.subplots()

    bars1 = ax.bar(x - width/2, means, width, label='Mean')
    bars2 = ax.bar(x + width/2, medians, width, label='Median')

    # Add labels above each bar
    for i in range(len(x)):
        ax.text(x[i] - width/2, means[i] + 0.2, f'{means[i]:.2f}', ha='center', va='bottom')
        ax.text(x[i] + width/2, medians[i] + 0.2, f'{medians[i]:.2f}', ha='center', va='bottom')

    ax.set_xlabel('Scheduling Algorithm')
    ax.set_ylabel('Throughput (Processes/Patrons completed per second)')
    ax.set_title('Mean and Median Throughput for Scheduling Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15)
    ax.legend()

    plt.tight_layout()
    plt.savefig('MeanMedianThroughputPlot.jpeg', dpi=300)
    plt.clf()

def plotTurnaroundTime(patrons, fcfsTurnaroundTimes, sjfTurnaroundTimes, rrTurnaroundTimes):
    plt.plot(patrons, fcfsTurnaroundTimes, label='First-Come First-Serve')
    plt.plot(patrons, sjfTurnaroundTimes, label='Shortest-Job First')
    plt.plot(patrons, rrTurnaroundTimes, label='Round-Robin')

    plt.xlabel('Processes')
    plt.ylabel('Turnaround Time (seconds)')

    plt.title('Turnaround time of processes/patrons for different scheduling algorithms', loc='center')

    plt.legend()

    plt.savefig('TurnaroundPlot.jpeg', dpi=300)

    plt.clf()

    algorithms = ['First-Come First-Serve', 'Shortest-Job First', 'Round-Robin']
    means = [np.mean(fcfsTurnaroundTimes), np.mean(sjfTurnaroundTimes), np.mean(rrTurnaroundTimes)]
    medians = [np.median(fcfsTurnaroundTimes), np.median(sjfTurnaroundTimes), np.median(rrTurnaroundTimes)]

    x = np.arange(len(algorithms))
    width = 0.35    

    # Create bar plot
    fig, ax = plt.subplots()

    bars1 = ax.bar(x - width/2, means, width, label='Mean')
    bars2 = ax.bar(x + width/2, medians, width, label='Median')

    # Add labels above each bar
    for i in range(len(x)):
        ax.text(x[i] - width/2, means[i] + 0.2, f'{means[i]:.2f}', ha='center', va='bottom')
        ax.text(x[i] + width/2, medians[i] + 0.2, f'{medians[i]:.2f}', ha='center', va='bottom')

    ax.set_xlabel('Scheduling Algorithm')
    ax.set_ylabel('Turnaround Time (seconds)')
    ax.set_title('Mean and Median Turnaround Times for Scheduling Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15)
    ax.legend()

    plt.tight_layout()
    plt.savefig('MeanMedianTurnaroundTimesPlot.jpeg', dpi=300)
    plt.clf()

def plotWaitingTime(patrons, fcfsWaitingTimes, sjfWaitingTimes, rrWaitingTimes):
    plt.plot(patrons, fcfsWaitingTimes, label='First-Come First-Serve')
    plt.plot(patrons, sjfWaitingTimes, label='Shortest-Job First')
    plt.plot(patrons, rrWaitingTimes, label='Round-Robin')

    plt.xlabel('Processes')
    plt.ylabel('Waiting Time (seconds)')

    plt.title('Waiting times of processes/patrons for different scheduling algorithms', loc='center')
    
    plt.legend()

    plt.savefig('WaitingTimesPlot.jpeg', dpi=300)

    plt.clf()

    algorithms = ['First-Come First-Serve', 'Shortest-Job First', 'Round-Robin']
    means = [np.mean(fcfsWaitingTimes), np.mean(sjfWaitingTimes), np.mean(rrWaitingTimes)]
    medians = [np.median(fcfsWaitingTimes), np.median(sjfWaitingTimes), np.median(rrWaitingTimes)]

    x = np.arange(len(algorithms))
    width = 0.35    

    # Create bar plot
    fig, ax = plt.subplots()

    bars1 = ax.bar(x - width/2, means, width, label='Mean')
    bars2 = ax.bar(x + width/2, medians, width, label='Median')

    # Add labels above each bar
    for i in range(len(x)):
        ax.text(x[i] - width/2, means[i] + 0.2, f'{means[i]:.2f}', ha='center', va='bottom')
        ax.text(x[i] + width/2, medians[i] + 0.2, f'{medians[i]:.2f}', ha='center', va='bottom')

    ax.set_xlabel('Scheduling Algorithm')
    ax.set_ylabel('Waiting Time (seconds)')
    ax.set_title('Mean and Median Waiting Times for Scheduling Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15)
    ax.legend()

    plt.tight_layout()
    plt.savefig('MeanMedianWaitingTimesPlot.jpeg', dpi=300)
    plt.clf()

def plotResponseTime(patrons, fcfsResponseTimes, sjfResponseTimes, rrResponseTimes):
    plt.plot(patrons, fcfsResponseTimes, label='First-Come First-Serve')
    plt.plot(patrons, sjfResponseTimes, label='Shortest-Job First')
    plt.plot(patrons, rrResponseTimes, label='Round-Robin')

    plt.xlabel('Processes')
    plt.ylabel('Response Time (seconds)')

    plt.title('Response times of processes/patrons for different scheduling algorithms', loc='center')

    plt.legend()

    plt.savefig('ResponseTimesPlot.jpeg', dpi=300)

    plt.clf()

    algorithms = ['First-Come First-Serve', 'Shortest-Job First', 'Round-Robin']
    means = [np.mean(fcfsResponseTimes), np.mean(sjfResponseTimes), np.mean(rrResponseTimes)]
    medians = [np.median(fcfsResponseTimes), np.median(sjfResponseTimes), np.median(rrResponseTimes)]

    x = np.arange(len(algorithms))
    width = 0.35    

    # Create bar plot
    fig, ax = plt.subplots()

    bars1 = ax.bar(x - width/2, means, width, label='Mean')
    bars2 = ax.bar(x + width/2, medians, width, label='Median')

    # Add labels above each bar
    for i in range(len(x)):
        ax.text(x[i] - width/2, means[i] + 0.2, f'{means[i]:.2f}', ha='center', va='bottom')
        ax.text(x[i] + width/2, medians[i] + 0.2, f'{medians[i]:.2f}', ha='center', va='bottom')

    ax.set_xlabel('Scheduling Algorithm')
    ax.set_ylabel('Response Time (seconds)')
    ax.set_title('Mean and Median Response Times for Scheduling Algorithms')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15)
    ax.legend()

    plt.tight_layout()
    plt.savefig('MeanMedianResponseTimesPlot.jpeg', dpi=300)
    plt.clf()

def plotCPUUtilisation(fcfsCPUUtilisation, sjfCPUUtilisation, rrCPUUtilisation):
    x = ['First-Come First-Serve', 'Shortest-Job First', 'Round-Robin']
    heights = [fcfsCPUUtilisation, sjfCPUUtilisation, rrCPUUtilisation]

    plt.bar(x, heights)

    # Add labels above each bar
    for i, height in enumerate(heights):
        plt.text(i, height + 0.2, f'{height:.2f}%', ha='center', va='bottom')

    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('CPU Utilisation')
    plt.title('CPU Utilisation for different scheduling algorithms', loc='center')

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

    # Plotting average turnaround time for each quantum.

    plt.plot(quanta, averageTurnaroundTime)
    plt.scatter(quanta[minTurnaroundQuantum], minTurnaroundTime, color='red', s=20, zorder=5)

    plt.xlabel('Time Quantum')
    plt.ylabel('Average turnaround itme (seconds)')

    plt.title('Average turnaround times for different time quanta')

    plt.savefig('TurnaroundTimeQuantumPlot.jpeg', dpi=300)

    plt.clf()

    # Plotting average response time for each quantum.

    plt.plot(quanta, averageResponseTime)
    plt.scatter(quanta[minResponseQuantum], minResponseTime, color='red', s=20, zorder=5)

    plt.xlabel('Time Quantum')
    plt.ylabel('Average response time (seconds)')

    plt.title('Average response times for different time quanta')

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