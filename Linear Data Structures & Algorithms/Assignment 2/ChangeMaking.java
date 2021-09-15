import java.lang.invoke.LambdaMetafactory;

/**
* Classical Change making problem with an unlimited amount of coins of each type. <br> 
* Version 2: Selection function with more elaborated policy: First biggest-coin.<br> 
* Depending on the type of coins, it can lead to an optimal solution.<br>
* The class encapsulates all the functions of the Greedy schema<br>
*/

public class ChangeMaking {

	//---------------------------------------
	//	Constructor
	//---------------------------------------
	/**
	 * Constructor of the class. Do not edit it.
	 */
	public ChangeMaking(){}

	
	// -------------------------------------------------------------------
	// 1. selectionFunctionFirstCandidate--> It selects the first candidate 
	// -------------------------------------------------------------------
	/**
	 * Given a current solution that is not a final solution, this function
	 * selects the new candidate to be added to it.<br>
	 * The policy followed is very simple: Just pick the first unused item.
	 * 
	 * @param candidates:
	 *            The MyList stating whether a candidate has been selected so
	 *            far or not.
	 * @return: The index of first candidate to be selected.
	 */
	public int selectionFunctionFirstCandidate(MyList<Integer> candidates) {
		int scenario = 0;
		int res = 0;

		if (candidates.length() == 0) { //Rule 1. MyList is empty
			scenario = 1; }

		if (candidates.length() >= 1) { //Rule 2. MyList is non-empty
			scenario = 2; }


		switch (scenario) {

			case 1: //Rule 1. MyList is empty
				break;

			case 2: //Rule 2. MyList is non-empty
				res = candidates.getElement(0); // return element at index 0
				break;
		}
		return res;
	}


		
	//-------------------------------------------------------------------
	// 1. selectionFunction --> It selects the next candidate to be considered.  
	//-------------------------------------------------------------------	
	/**
	 * Given a current solution that is not a final solution, this function selects the new candidate to be added to it.<br> 
	 * The policy followed is more elaborated: Pick the best coin according to the objective function of minimizing the number
	 * of coins that make the change of the amount. 
	 * @param candidates: List of candidates
	 * @return: The index of candidate to be selected.
	 */	
	public int selectionFunctionBestCandidate(MyList<Integer> candidates) {
		int scenario = 0;
		int res = 0;

		if (candidates.length() == 0) { //Rule 1. MyList is empty
			scenario = 1; }

		if (candidates.length() >= 1) { //Rule 2. MyList is non-empty
			scenario = 2; }


		switch (scenario) {
			case 1: //Rule 1. MyList is empty
				break;

			case 2: //Rule 2. MyList is non-empty
				int i0 = candidates.getElement(0); // get element at index 0
				candidates.removeElement(0); // remove element at index 0
				res = selectionFunctionBestCandidate(candidates); // recursively call the function with the new list less the first element in the old list
				candidates.addElement(0, i0); // add i0 back at position 0 to undo any damage done
				if (i0 > res){ res = i0; } // if element at index 0 is greater than res, set res to i0 to get the largest element in the list
				break;
		}
		return res;
	}
	//-------------------------------------------------------------------
	// 2. feasibilityTest --> It selects if a candidate can be added to the solution.   
	//-------------------------------------------------------------------	
	/**
	 * Given a current solution and a selected candidate, this function 
	 * states whether the candidate must be added to the solution or discarded.<br> 
	 * @param candidateValue: The value of the candidate coin selected. 
	 * @param amount: The amount of change we want to generate.
	 * @param changeGenerated: The quantity of change we have generated so far. 
		 * @return: Whether the candidate fits or not into the solution.
	 */

	public boolean feasibilityTest(int candidateValue, int amount, int changeGenerated){
		int scenario = 0;
		boolean res = false;
		amount-= changeGenerated; //take the change that has been already generated from the total amount
		
		if (candidateValue <= amount) { //the proposed value fits into the total amount less the change generated thus far
			scenario = 1;
		} else { scenario = 2; } //the proposed value does not fit into the total amount less the change generated thus far

		switch (scenario) {
			case 1:
				res = true; // return true, the value fits into the amount
				break;

			case 2: // return false, the value does not fit into the amount
				break;
		}
		return res;
	}
	
	// -------------------------------------------------------------------
	// 5. solutionTest --> It selects if the current solution is the final
	// solution
	// -------------------------------------------------------------------
	/**
	 * Given a current solution, this function states whether it is a final
	 * solution or it can still be improved.<br>
	 * To determine it, it checks whether there is (at least) one item not
	 * picked before that fits into the knapsack.
	 * 
	 * @param nbCandidates:
	 *            number of candidates that have not been yet selected by the
	 *            selection function
	 * @return: Whether the current solution is the final solution.
	 */
	public boolean solutionTest(MyList<Integer> candidates) { // check if all possible solutions have been exhausted
		int scenario = 0;
		boolean res = false;

		if (candidates.length() == 0) { //Rule 1. MyList is empty
			scenario = 1; }

		if (candidates.length() >= 1) { //Rule 2. MyList is non-empty
			scenario = 2; }

		switch (scenario) {
			case 1:
				res = true; // candidate list is empty, all possible solutions have been exhausted, return true
				break;
			case 2:
				break; // candidate list is not empty, return false
		}
		return res;
	}


	//-------------------------------------------------------------------
	// 4. objectiveFunction --> This function computes the value of the final solution.  
	//-------------------------------------------------------------------	
	/**
	 * Given the final solution to the problem, this function 
	 * computes its objective function value according to:<br>
	 * How many coins are used in the solution.<br>
	 * @param sol: The MyList containing the solution to the problem. 
	 * @return: The objective function value of such solution.
	 */	
	public int  objectiveFunction(MyList<Integer> sol){
		int scenario = 0;
		int res = 0;

		if (sol.length() == 0) { //Rule 1. MyList is empty
			scenario = 1; }

		if (sol.length() >= 1) { //Rule 2. MyList is non-empty
			scenario = 2; }

		switch (scenario) {
			case 1:
				break;

			case 2:
				int i0 = sol.getElement(0); //set i0 to first element
				sol.removeElement(0); // remove first element
				res = objectiveFunction(sol); // recursively call the function passing the new list, which is the old list less the element in index 0
				sol.addElement(0, i0); // reverse the removal of elements to undo any damage
				res++; // increment counter
				break;
		}
		return res;
	}
	
	//-------------------------------------------------------------------
	// 5. solve --> This function solves the problem using a greedy algorithm.  
	//-------------------------------------------------------------------	
	/**
	 * Given an instance of the GP1 problem, this function solves it using 
	 * a greedy algorithm.<br> 
	 * @param typeSelectFunc:
	 *            Type of selection function to choose.
	 * @param coinValues: A MyList containing the value of each type of coin supported.
	 * @param amount: The amount of change we want to generate.
	 * @return: A MyList containing the amount of coins of each type being selected.
	 */	
	public MyList<Integer> solve(int typeSelectFunc, MyList<Integer> coinValues, int amount){
		int scenario = 0;
		int changeGenerated = 0; // counter that is incremented if coin is selected
		int coin; // coin is chosen from the coins list using typeSelectFunc
		MyList<Integer> res = new MyDynamicList<Integer>(); // results list
		MyList<Integer> coins = new MyDynamicList<Integer>(); // temp list that is a replica of coinValues to not damage coinValues


		for(int i=0; i < coinValues.length(); i++) { // take all elements in list coinValues and add them to list coins so as not to destroy the coinValues list
			int element = coinValues.getElement(i); // get each element in coinValues
			coins.addElement(i, element); } // add that element to coins list

		if (typeSelectFunc == 1 && amount >= 1) { // using firstCandidate
			scenario = 1;
		}

		if (typeSelectFunc == 2 && amount >= 1) { // using bestCandidate
			scenario = 2;
		}


		switch(scenario){

			case 1:
				while (!solutionTest(coins)) { // check that the coins list is not empty,
					coin = selectionFunctionFirstCandidate(coins); // get first element
					boolean isFeasible = feasibilityTest(coin, amount, changeGenerated); // check if that coin will fit
					if (isFeasible) { // if chosen coin fits
						System.out.println("Chosen coin: " + coin); // print chosen coin
						int oldAmount = amount - changeGenerated; // calculate old amount,
						changeGenerated += coin; // increment changeGenerated by chosen coin amount
						int newAmount = amount - changeGenerated; // calculate new amount
						System.out.print("Accuracy: " + oldAmount + " - " + coin + " = " + newAmount + "\n"); // print accuracy sum
						res.addElement(0, coin); // add coin to results list
						System.out.print("Coins used so far: "); // for loop to print all coins in res thus far
						for (int i = res.length() -1; i >= 0; i--) { // traverse res backwards
							System.out.print( res.getElement(i) + ", "); // print res backwards
						}
						System.out.println("\nNumber of Coins: " + objectiveFunction(res) +"\n"); // use objectiveFunction to count the number of coins in res

					} else { // if chosen coin does not fit
						coins.removeElement(0); // remove that coin from the temporary list
					}
				}
				break;

			case 2:
				while (!solutionTest(coins)) { // check if there are still possible solutions in the coins list
					coin = selectionFunctionBestCandidate(coins); // get first element
					boolean isFeasible = feasibilityTest(coin, amount, changeGenerated); // check if that coin will fit
					if (isFeasible) { // if chosen coin fits
						System.out.println("Chosen coin: " + coin); // print chosen coin
						int oldAmount = amount - changeGenerated; // calculate old amount,
						changeGenerated += coin; // increment changeGenerated by chosen coin amount
						int newAmount = amount - changeGenerated; // calculate new amount
						System.out.print("Accuracy: " + oldAmount + " - " + coin + " = " + newAmount + "\n"); // print accuracy
						res.addElement(0, coin); // add coin to results list
						System.out.print("Coins used so far: "); // for loop to print all coins in res thus far
						for (int i = res.length() -1; i >= 0; i--) { // traverse res backwards
							System.out.print( res.getElement(i) + ", "); // print res backwards
						}
						System.out.println("\nNumber of Coins: " + objectiveFunction(res) +"\n"); // use objectiveFunction to count the number of coins in res

					} else { // if chosen coin does not fit
						for (int i=0; i < coins.length(); i++) { //find the position of the current chosen coin
							if (coins.getElement(i) == coin) { // search coin list for chosen coin that doesn't fit
								coins.removeElement(i); // remove the current coin that doesn't fit
							}
						}
					}
				}
				break;

			default: // coinValues list is empty
				break;

		}
		return coinValues; // I FORGOT TO UPDATE THIS TO RES
	}
}
