//M. M. Kuttel 2025 mkuttel@gmail.com

// Modified by Mark Du Preez (DPRMAR021) to record performance metrics for simulation.
// April 2025

package barScheduling;
// the main class, starts all threads and the simulation


import java.io.IOException;
import java.util.Random;
import java.util.concurrent.CountDownLatch;


public class SchedulingSimulation {
	static int noPatrons=10; //number of customers - default value if not provided on command line
	static int sched=0; //default scheduling algorithm, 0= FCFS, 1=SJF, 2=RR
	static int q=10000, s=0;
	static long seed=0;
	static CountDownLatch startSignal;	
	static Patron[] patrons; // array for customer threads
	static Barman Sarah;

	public static void main(String[] args) throws InterruptedException, IOException {

		//deal with command line arguments if provided
		if (args.length>=1) noPatrons=Integer.parseInt(args[0]);  //total people to enter room
		if (args.length>=2) sched=Integer.parseInt(args[1]); 	// alg to use
		if (args.length>=3) s=Integer.parseInt(args[2]);  //context switch 
		if(args.length>=4) q=Integer.parseInt(args[3]);  // time slice for RR
		if(args.length>=5) seed=Integer.parseInt(args[4]); // random number seed- set to compare apples with apples		
		

		startSignal= new CountDownLatch(noPatrons+2);//Barman and patrons and main method must be ready
		
		//create barman
        Sarah= new Barman(startSignal,sched,noPatrons,q,s); 
     	Sarah.start();
  
	    //create all the patrons, who all need access to Barman
		patrons = new Patron[noPatrons];
		for (int i=0;i<noPatrons;i++) {
			patrons[i] = new Patron(i,startSignal,Sarah,seed);
			patrons[i].start();
		}
		
		if (seed>0) DrinkOrder.random = new Random(seed);// for consistent Patron behaviour

		
		System.out.println("------Sarah the Barman Scheduling Simulation------");
		System.out.println("-------------- with "+ Integer.toString(noPatrons) + " patrons---------------");
		switch(sched) {
		  case 0:
			  System.out.println("-------------- and FCSF scheduling ---------------");
		    break;
		  case 1:
			  System.out.println("-------------- and SJF scheduling ---------------");
		    break;
		  case 2:
			  System.out.println("-------------- and RR scheduling with q="+q+"-------------");
		}
		
			
      	startSignal.countDown(); //main method ready
      	
      	// wait till all patrons done, otherwise race condition on the file closing!
      	for (int i=0;i<noPatrons;i++) {  
			patrons[i].join();
		}

    	System.out.println("------Waiting for Barman------");
    	Sarah.interrupt();   //tell Barman to close up
    	Sarah.join(); //wait till she has
      	System.out.println("------Bar closed------");

		// Start outputting raw data.

		// Length of barman execution (used for later processesing).
		System.out.println(Long.toString(Sarah.getOperationLength()));

		// Number of patrons.
		System.out.println(Integer.toString(noPatrons));

		// Outputting patron turnaround times in order of patron ID's (in order of arrival) seperating by ' ' (spaces).
		for (int i = 0; i < noPatrons; ++i) {
			System.out.print(Long.toString(patrons[i].getTurnaroundTime()) + " ");
		}

		System.out.println();

		// Outputting response time of PATRON (not drink orders which I use for later calculation).
		for (int i = 0; i < noPatrons; ++i) {
			System.out.print(Long.toString(patrons[i].getResponseTime()) + " ");
		}

		System.out.println();

		// Outputting response times per drink (not a performance metric, used for later calculations) in order of patrons in order of orders placed.
		for (int i = 0; i < noPatrons; ++i) {
			Long[] responseTimes = patrons[i].getResponseTimes();

			for (int j = 0; j < 5; ++j) {
				System.out.print(Long.toString(responseTimes[j]) + " ");
			}

			System.out.println();
		}

		// Outputting execution times for patron drink orders in order which they are received. Do this for each patron in order of their arrival (ID).
		Long[][] executionTimes = Sarah.getExecutionTimes();

		for (int i = 0; i < noPatrons; ++i) {
			for (int j = 0; j < 5; ++j) {
				System.out.print(Long.toString(executionTimes[i][j]) + " ");
			}

			System.out.println();
		}

		// Output patron completion times (time relative to start time of bar) in patron arrival order for later processing.
		Long[] patronCompletionTimes = Sarah.getPatronCompletionTimes();

		for (int i = 0; i < noPatrons; ++i) {
			System.out.print(Long.toString(patronCompletionTimes[i]) + " ");
		}

 	}
}