//M. M. Kuttel 2025 mkuttel@gmail.com
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

	// Cumulative waiting time for process/patron.
	private long averageWaitingTime;

	// Response time for process/patron.
	private long responseTime;

	// Array of longs representing waiting times for a particular drink/job.
	private Long[] waitingTimes;

	private long turnaroundTime;

	private DrinkOrder [] drinksOrder;
	
	Patron( int ID,  CountDownLatch startSignal, Barman aBarman, long seed) {
		this.ID=ID;
		this.startSignal=startSignal;
		this.theBarman=aBarman;
		this.numberOfDrinks=5; // number of drinks is fixed
		// Array of waiting times for each CPU burst
		this.averageWaitingTime = 0;
		this.waitingTimes = new Long [numberOfDrinks];
		this.responseTime = 0;
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

			long startTurnaroundTime = System.currentTimeMillis();
			
	        for(int i=0;i<numberOfDrinks;i++) {
	        	drinksOrder[i]=new DrinkOrder(this.ID); //order a drink (=CPU burst)	        
	        	//drinksOrder[i]=new DrinkOrder(this.ID,i); //fixed drink order (=CPU burst), useful for testing
				System.out.println("Order placed by " + drinksOrder[i].toString()); //output in standard format  - do not change this
				theBarman.placeDrinkOrder(drinksOrder[i]);
				long startWaitingTime = System.currentTimeMillis();
				drinksOrder[i].waitForOrder();
				long endWaitingTime = System.currentTimeMillis();
				waitingTimes[i] += endWaitingTime - startWaitingTime;
				averageWaitingTime += (endWaitingTime - startWaitingTime)/numberOfDrinks;
				if (i == 0) {
					responseTime = endWaitingTime - startWaitingTime;
				}
				System.out.println("Drinking patron " + drinksOrder[i].toString());
				sleep(drinksOrder[i].getImbibingTime()); //drinking drink = "IO"
			}

			long endTurnaroundTime = System.currentTimeMillis();

			turnaroundTime = endTurnaroundTime - startTurnaroundTime;

			System.out.println("Patron "+ this.ID + " completed ");


			
		} catch (InterruptedException e1) {  //do nothing
		}
}

// Return reference to array of waiting times for particular patron.
public Long[] getWaitingTimes () {
	return waitingTimes;
}

// Return average waiting time for a particular patron.
public long getAverageWaitingTime() {
	return averageWaitingTime;
}

// Return the response time for a particular patron.
public long getResponseTime () {
	return responseTime;
}

// Return the turnaround time for a particular patron.
public long getTurnaroundTime() {
	return turnaroundTime;
}

}