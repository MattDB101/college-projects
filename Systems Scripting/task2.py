import random
NUMOFITEMS = 12

"""

Again, I start by breaking the requirements into simple segments.
The key goals in the script are as follows;

1. Interactively ask the user for a list of 12 or more items.
2. Get an number between 2 and 6 from the user and handle any exceptions that may occur.
3. Define  remove(), pass the list and number taken from the user. Generate x numbers between 1 & 4, where x is the number input by the user, and then remove the element at that generated index. 
4. Return the list as a tuple.

First, asking the user for a list. I used the same code from task 1 with some slight alterations.

Next, getting a number from the user, I used a try except to handle any exceptions that might arise from the user's input, this was a topic that was covered in lecture 12.

I then created the remove() function, when calling this function I pass a copy of the original list so as to not affect the list permanently.
I used a simple loop to generate the random numbers, I did so using the random library. I have used this library in the past, but in order to remember the syntax I checked the example from lecture 11.
After generating the random index, I removed the element at that index from the list.

Once I had removed the elements all that was left to do was to return the list as a tuple, I was already familiar with returning a value from a function, the return statement was covered in lecture 12. 
I didn't remember how to convert the list to a tuple, so I checked the slides from lecture 13 and found an example.

"""


def remove(list, numIndexes):  # Function takes a list and an int.
    for i in range(numIndexes):  # Loop passed number of times.
        index = random.randint(0, 3)  # Generate a number between 0-3.
        list.pop(index)  # Remove the element in the randomly generated numbers position.-
    return tuple(list)  # Return the list as a tuple.


def main():
    list = []  # Create an empty list.
    numIndexes = 0

    while True:  # Infinitely take items until the user says to stop
        userInput = input("\nPlease input an item to be added to the list, press enter without typing anything to stop adding items (Min. 12): ")
        if len(list) < NUMOFITEMS and userInput == "":  # If the user requests to enter 0 items.
            print(f"Please input at least 12 items, so far you've entered {len(list)} item(s).")
        elif len(list) >= NUMOFITEMS and userInput == "":  # If the user requests to stop enter items.
            break
        else:
            list.append(userInput)  # If they haven't asked to stop, add the given word.

    while True:
        try:
            while int(numIndexes) < 2 or int(numIndexes) > 6:  # Ask the user for a number between 2 & 6.
                numIndexes = int(input("Please enter the number of items to be deleted (Must be between 2 & 6): "))
            break  # If the number the user has input satisfies the constraint, break out of the loop.
        except ValueError:  # If the user's input causes an error, continue the infinite loop.
            print("Please input only numerical characters.")
            pass
        except:
            print("Unexpected error!")
            pass

    resTuple = remove(list.copy(), numIndexes)  # Call the function with a copy of the list so as to not delete elements permanently.

    print(
        f"\nSample program output when {numIndexes} items were randomly deleted:\n"  # Print the number of indexes that were deleted.
        f"Result tuple: {resTuple}\n"  # Print the result of deleting elements in random indexes.
        f"Original List: {list}")  # Print the original list.


main()
