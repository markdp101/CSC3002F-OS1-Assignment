//M. M. Kuttel 2025 mkuttel@gmail.com

// Modified by Mark Du Preez (DPRMAR021) to record performance metrics for simulation.
// April 2025
package barScheduling;


import java.util.Random;
import java.util.concurrent.CountDownLatch;

/*class for the patrons at the bar*/

public class Patron extends Thread {
	
	private Random random;// for variation in Patron behaviour
	private CountDownLatch startSignal; //all start at once, actually shared
	private Barman theBarman; //the Barman is actually shared though

	private int ID; //thread ID 
	private int numberOfDrinks;

	// Turnaround time for a process/patron (time from placing first drink order to when the 5 drinks are done being made).
	private long turnaroundTime;

	// Records the response time for each drink (time from when order was placed to when drink was received).
	private Long[] responseTimes;

	private DrinkOrder [] drinksOrder;
	
	Patron( int ID,  CountDownLatch startSignal, Barman aBarman, long seed) {
		this.ID=ID;
		this.startSignal=startSignal;
		this.theBarman=aBarman;
		this.numberOfDrinks=5; // number of drinks is fixed
		// Array of response times for each CPU burst
		this.responseTimes = new Long [numberOfDrinks];
		this.turnaroundTime = 0;
		drinksOrder=new DrinkOrder[numberOfDrinks];
		if (seed>0) random = new Random(seed);// for consistent Patron behaviour
		else random = new Random();
	}
	
	
//this is what the threads do	
	public void run() {
		try {
			
			//Do NOT change the block of code below - this is the arrival times
			startSignal.countDown(); //this patron is ready
			startSignal.await(); //wait till everyone is ready
			int arrivalTime = ID*50; //fixed arrival for testing
	        sleep(arrivalTime);// Patrons arrive at staggered  times depending on ID 
			System.out.println("+new thirsty Patron "+ this.ID +" arrived"); //Patron has actually arrived
			//End do not change

			long startTurnaroundTime = 0;
			long endTurnaroundTime = 0;
			
	        for(int i=0;i<numberOfDrinks;i++) {
	        	drinksOrder[i]=new DrinkOrder(this.ID); //order a drink (=CPU burst)	        
	        	//drinksOrder[i]=new DrinkOrder(this.ID,i); //fixed drink order (=CPU burst), useful for testing
				System.out.println("Order placed by " + drinksOrder[i].toString()); //output in standard format  - do not change this
				theBarman.placeDrinkOrder(drinksOrder[i]);

				// Recording the starting time for calculating turnaround time and response time 
				// (start timing from when first drink order is placed).
				if (i == 0) {
					startTurnaroundTime = System.currentTimeMillis();
				}

				// Starting timer for calculating waiting time per job.
				long startResponseTime = System.currentTimeMillis();
				drinksOrder[i].waitForOrder();

				// Record time when order was received.
				long endResponseTime = System.currentTimeMillis();

				// Compute response time and add it to the response times array which stores response times for each drink.
				// Response time for particular drink = Time from when order for particular drink was submitted till drink is received.
				this.responseTimes[i] = endResponseTime - startResponseTime;

				// Record the time at which the last drink is done being made.
				if (i == (numberOfDrinks - 1)) {
					endTurnaroundTime = endResponseTime;
				}

				System.out.println("Drinking patron " + drinksOrder[i].toString());
				sleep(drinksOrder[i].getImbibingTime()); //drinking drink = "IO"
			}

			// Compute and record turnaround time.
			this.turnaroundTime = endTurnaroundTime - startTurnaroundTime;

			System.out.println("Patron "+ this.ID + " completed ");

		} catch (InterruptedException e1) {  //do nothing
		}
}

// Return reference to array of waiting times for particular patron.
public Long[] getResponseTimes () {
	return responseTimes;
}

// Return the response time for process (response time of first drink).
public long getResponseTime () {
	return responseTimes[0];
}

// Return the turnaround time for a particular patron.
public long getTurnaroundTime() {
	return turnaroundTime;
}

}