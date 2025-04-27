//M. M. Kuttel 2025 mkuttel@gmail.com
package barScheduling;

import java.util.Random;
import java.util.Comparator;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.PriorityBlockingQueue;

/*
 Barman Thread class.
 */

public class Barman extends Thread {
	

	private CountDownLatch startSignal;
	private BlockingQueue<DrinkOrder> orderQueue;
	int schedAlg =0;
	int q=10000; //really big if not set, so FCFS
	private int switchTime;

	// Used to keep track of the number of patrons/processes.
	private int numPatrons;

	private int numDrinks = 5;

	// Used to keep track of execution times for the drink orders per processes.
	// Number of drinks per patron is fixed.
	private Long[][] executionTimes;

	// Keep track of completed drinks per patron where each index represents a patron and holds the count of completed drinks.
	private int[] completedOrders;

	// Used to keep track of the start time of the program.
	private long startTotalTime;

	// Used to keep track of the end time of the program.
	private long endTotalTime;

	// Used to keep track of patron completion times.
	private Long[] patronCompletionTimes;

	// private long processingTime = 0;
	// private long totalTime = 0;
	
	
	// Modified constructor to get number of total patrons for recording purposes.
	Barman(  CountDownLatch startSignal,int sAlg,int numPatrons) {
		//which scheduling algorithm to use
		this.schedAlg=sAlg;
		// SJF is option 1

		this.numPatrons = numPatrons;

		// Initialize 2D array where each row is a patron with the columns holding the execution times.
		executionTimes = new Long[numPatrons][numDrinks];

		for (int i = 0; i < numPatrons; ++i) {
			for (int j = 0; j < 5; ++j) {
				executionTimes[i][j] = 0L;
			}
		}

		// Initialize the counter array for orders completed for patrons.
		completedOrders = new int[numPatrons];
		for (int i = 0; i < numPatrons; ++i) {
			completedOrders[i] = 0;
		}

		// Initialize barman start and end times.
		startTotalTime = 0;
		endTotalTime = 0;

		// Initialize array of patron/processes completed order time.
		patronCompletionTimes = new Long [numPatrons];

		if (schedAlg==1) this.orderQueue = new PriorityBlockingQueue<>(5000, Comparator.comparingInt(DrinkOrder::getExecutionTime));
		else this.orderQueue = new LinkedBlockingQueue<>(); //FCFS & RR
	    this.startSignal=startSignal;
	}
	
	Barman(  CountDownLatch startSignal,int sAlg,int numPatrons,int quantum, int sTime) { //overloading constructor for RR which needs q
		this(startSignal, sAlg, numPatrons);
		q=quantum;
		switchTime=sTime;
	}

	public void placeDrinkOrder(DrinkOrder order) throws InterruptedException {
        orderQueue.put(order);
    }
	
	public void run() {
		int interrupts=0;
		try {
			DrinkOrder currentOrder;
			
			startSignal.countDown(); //barman ready
			startSignal.await(); //check latch - don't start until told to do so

			startTotalTime = System.currentTimeMillis();

			if ((schedAlg==0)||(schedAlg==1)) { //FCFS and non-preemptive SJF
				while(true) {
					currentOrder=orderQueue.take();

					// Start recording the execution time --> drink is starting to be made.
					long startExecutionTime = System.currentTimeMillis();

					System.out.println("---Barman preparing drink for patron "+ currentOrder.toString());
					sleep(currentOrder.getExecutionTime()); //processing order (="CPU burst")

					// Finish recording the execution time --> drink is completed.
					long endExecutionTime = System.currentTimeMillis();

					System.out.println("---Barman has made drink for patron "+ currentOrder.toString());
					currentOrder.orderDone();

					// Do the computation after order is done to minimally effect recorded waiting and response times for patrons.

					// Getting the patrons id for particular drink order.
					String string = currentOrder.toString();

					// Extract and cast to integer the patron ID.
					int patronID = Integer.parseInt(string.substring(0, string.indexOf(":")));

					// Store execution time for nth drink order for particular patron.
					executionTimes[patronID][completedOrders[patronID]] = endExecutionTime - startExecutionTime;
					++completedOrders[patronID];

					// Assuming (built-in logic of simulator) fixed drinks per patron.
					// Record the time all patron's orders/CPU bursts are completed relative to the start time (making zero-relative).
					if (completedOrders[patronID] == 5) {
						patronCompletionTimes[patronID] = endExecutionTime - startTotalTime;
					}

					sleep(switchTime);//cost for switching orders
				}
			}
			else { // RR 
				int burst=0;
				int timeLeft=0;
				System.out.println("---Barman started with q= "+q);

				// The following recording of execution times for drinks works on the logic fixed into the program that a patron orders and receives one drink at a time.

				while(true) {
					System.out.println("---Barman waiting for next order ");
					currentOrder=orderQueue.take();

					// Getting the patrons id for particular drink order.
					String string = currentOrder.toString();

					// Extract and cast to integer the patron ID.
					int patronID = Integer.parseInt(string.substring(0, string.indexOf(":")));

					// Start recording the execution time --> drink is starting to be made.
					long startExecutionTime = System.currentTimeMillis();

					System.out.println("---Barman preparing drink for patron "+ currentOrder.toString() );
					burst=currentOrder.getExecutionTime();
					if(burst<=q) { //within the quantum
						sleep(burst); //processing complete order ="CPU burst"
						System.out.println("---Barman has made drink for patron "+ currentOrder.toString());

						// Finish recording the execution time --> drink is completed.
						long endExecutionTime = System.currentTimeMillis();

						currentOrder.orderDone();

						// Do the computation after order is done to minimally effect recorded waiting and response times for patrons.

						// Store execution time for nth drink order for particular patron.
						executionTimes[patronID][completedOrders[patronID]] = endExecutionTime - startExecutionTime;
						++completedOrders[patronID];

						// Assuming (built-in logic of simulator) fixed drinks per patron.
						// Record the time all patron's orders/CPU bursts are completed relative to the start time (making zero-relative).
						if (completedOrders[patronID] == 5) {
							patronCompletionTimes[patronID] = endExecutionTime - startTotalTime;
						}

					}
					else {
						sleep(q);

						// Finish recording the execution time --> drink is completed.
						long endExecutionTime = System.currentTimeMillis();

						timeLeft=burst-q;

						// Increment execution time for nth drink order for particular patron.
						executionTimes[patronID][completedOrders[patronID]] += endExecutionTime - startExecutionTime;

						// If particular order is done move onto the next order for that particular patron.
						if (timeLeft == 0) {
							++completedOrders[patronID];

							// Assuming (built-in logic of simulator) fixed drinks per patron.
							// Record the time all patron's orders/CPU bursts are completed relative to the start time (making zero-relative).
							if (completedOrders[patronID] == 5) {
							patronCompletionTimes[patronID] = endExecutionTime - startTotalTime;
							}
						}

						System.out.println("--INTERRUPT---preparation of drink for patron "+ currentOrder.toString()+ " time left=" + timeLeft);
						interrupts++;
						currentOrder.setRemainingPreparationTime(timeLeft);
						orderQueue.put(currentOrder); //put back on queue at end
					}
					sleep(switchTime);//switching orders
				}
			}
				
		} catch (InterruptedException e1) {
			// Record the end of the barman taking orders. Last patron's order is completed.
			endTotalTime = System.currentTimeMillis();
			System.out.println("---Barman is packing up ");
			System.out.println("---number interrupts="+interrupts);
		}
	}

	// Returns the total length that the barman was processing orders (total execution time of CPU).
	public long getOperationLength() {
		return endTotalTime - startTotalTime;
	}

	// Return the execution times of drink orders for particular patron.
	public Long[][] getExecutionTimes() {
		return executionTimes;
	}

	// Return the completion time of patrons (last drink order completed).
	public Long[] getPatronCompletionTimes() {
		return patronCompletionTimes;
	}
}


