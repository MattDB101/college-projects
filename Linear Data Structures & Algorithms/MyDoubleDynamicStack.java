//Matthew Byrne, R00173315, SD2-A.

/**
* ADT MyStack: Private Part<br>. 
* The class implements all the operations available in MyStack<br>
*/
public class MyDoubleDynamicStack<T> implements MyStack<T> {

	//--------------------------------------------------
	// Attributes
	//--------------------------------------------------
	private int numItems; //declare numItems variable
	private MyDoubleLinkedNode<T> head; // declare head from class MyDoubleLinkedNode
	//-------------------------------------------------------------------
	// Basic Operation --> Check if myStack is empty: myCreateEmpty
	//-------------------------------------------------------------------	
	//public myStack myCreateEmpty(){}

	public MyDoubleDynamicStack(){
		numItems = 0; //set numItems to 0
		head = null; //set head to null
	}

	//-------------------------------------------------------------------
	// Basic Operation --> Check if myStack is empty: isEmpty
	//-------------------------------------------------------------------	

	public boolean isEmpty(){
		//-----------------------------
		//Output Variable --> InitialValue
		//-----------------------------
		boolean res = true;

		//-----------------------------
		//SET OF OPS
		//-----------------------------

		//-----------------------------
		// I. SCENARIO IDENTIFICATION
		//-----------------------------
		int scenario = 0;
		if(numItems == 0){
			scenario = 1; // stack is empty
		} else {
			scenario = 2; // stack is not empty
		}

		//-----------------------------
		// II. SCENARIO IMPLEMENTATION 
		//-----------------------------
		switch(scenario){
		case 1:
			res = true;
			break;

		case 2:
			res = false;
			break;

		}
		//-----------------------------
		//Output Variable --> Return FinalValue
		//-----------------------------
		return res;
	}

	//-------------------------------------------------------------------
	// Basic Operation (Partial) --> Get first element from front of MyStack: first
	//-------------------------------------------------------------------

	public T first(){
		T res = null; // setting result to null
		int scenario = 0;
		if(isEmpty()){ // stack is empty
			scenario = 1;
		} else { // stack is not empty
			scenario = 2;
		}

		switch(scenario) {
			case 1:
				System.out.println("The stack is empty");
				break;

			case 2:
				MyDoubleLinkedNode<T> current = head; //set current to the top of the stack
				res = current.getInfo(); //setting result to current
		}
		return res;
	}

	//-------------------------------------------------------------------
	// Basic Operation --> Add element to back of MyStack: addByFirst 
	//-------------------------------------------------------------------

	public void addByFirst(T element){
		int scenario = 0;
		if(isEmpty()){ //stack is empty
			scenario = 1;
		} else { //stack is not empty
			scenario = 2;
		}

		switch(scenario) {
			case 1: // if stack is empty
				head = new MyDoubleLinkedNode<T>(null, element,null); //stack is empty, create new node with the given element and set head to it.
				numItems++; //increment numItems by 1
				break;

			case 2: // if stack is empty
				MyDoubleLinkedNode<T> current = head; //set current node to head
				MyDoubleLinkedNode<T> newNode = new MyDoubleLinkedNode<T>(null, element, current); //create a new node and passing it the element
				head = newNode; //set new node to top of stack
				newNode.setRight(current); //using setRight to put newNode ahead of previous current
				numItems++; //increment numItems by 1
				break;
		}
	}


	public void removeByFirst(){
		int scenario = 0;
		if(isEmpty()){ //stack is empty
			scenario = 1;
		} else { //stack is not empty
			scenario = 2;
		}

		switch(scenario) {
			case 1:
				System.out.println("The stack is empty");
				break;

			case 2:
				head = head.getRight(); //unreference current head
				numItems--; //decrement numItems by 1
				break;
		}
	}
	//-------------------------------------------------------------------
	// Basic Operation (Partial) --> Get first element from front of MyStack: last
	//-------------------------------------------------------------------

	public T last(){
		T res = null; //setting result to null
		int scenario = 0;
		if(isEmpty()){ //stack is empty
			scenario = 1;
		} else { //stack is not empty
			scenario = 2;
		}

		switch(scenario) {
			case 1:
				System.out.println("The stack is empty");
				break;

			case 2:
				MyDoubleLinkedNode<T> current = head; //set current node to head
				for(int i = 1; i < numItems; i++) { //for loop to get the last item in the stack
					current = current.getRight(); //set current to last item
				}
				res = current.getInfo(); //set result to current
		}
		return res;
	}

	//-------------------------------------------------------------------
	// Basic Operation --> Add element to back of MyStack: addByLast 
	//-------------------------------------------------------------------

	public void addByLast(T element){
		int scenario = 0;
		if(isEmpty()){ //stack is empty
			scenario = 1;
		} else { //stack is not empty
			scenario = 2;
		}


		switch(scenario) {
			case 1:
				head = new MyDoubleLinkedNode<T>(null, element, null); //stack is empty, create new node with the given element and set head to it.
				numItems++; //increment numItems by 1.
				break;

			case 2:
				MyDoubleLinkedNode<T> current = head; //set current node to head
				for(int i = 1; i < numItems; i++) { //for loop to get last item in stack
					current = current.getRight(); } //set current to last item
				MyDoubleLinkedNode<T> newNode = new MyDoubleLinkedNode<T>(current, element,null); //create a new node and passing it the element
				current.setRight(newNode); //adding newNode behind the current last item, making the newNode now the last item.
				numItems++; //increment numItems by 1.
				break;
		}
	}
	
	//-------------------------------------------------------------------
	// Basic Operation (Partial) --> Remove element from front of MyStack: removeByFirst 
	//-------------------------------------------------------------------	

	public void removeByLast(){
		//-----------------------------
		//SET OF OPS
		//-----------------------------


		//-----------------------------
		// I. SCENARIO IDENTIFICATION
		//-----------------------------
		int scenario = 0;
		if(isEmpty()){ //stack is empty
			scenario = 1;
		} else { //stack is not empty
			scenario = 2;
		}

		//-----------------------------
		// II. SCENARIO IMPLEMENTATION
		//-----------------------------
		switch(scenario) {
			case 1:
				System.out.println("The stack is empty");
				break;

			case 2:
				MyDoubleLinkedNode<T> current = head; //set current node to head
				for (int i = 1; i < numItems; i++) { //for loop to get last item in stack
					current = current.getRight(); }
				current.setInfo(null); //setting current, which is the last item in the stack to null.
				numItems--; //dencrement numItems by 1.
		}
	}
}


