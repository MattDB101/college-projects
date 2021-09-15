"""

I start by breaking the requirements into simple segments.
The key goals in the script are as follows;

1. Get an positive integer from the user and handle any exceptions that may occur.
2. Determine whether this number is odd, even or equal to 1.
3. Perform the required operation depending on the value.
4. Recursively call the function until the final value of 1 is achieved.

First, getting a number from the user, just like with the last task, I used a try except to handle any exceptions that might arise from the user's input, this was covered in lecture 12.

The first step is to determine which of the operations to perform, I decided to do this just by checking the number with modulus division to see the remainder when divided by 2.

When the number is even (because the sequence will always end proceeded by a 2), I needed to check whether or not the number was equal to 1, since this means the recursion is finished and the function should not be called again.
Next, simply call the function recursively, passing in the new number and then return said number to the function that called this instance of the function.
I didn't need to perform much research in order to complete this task as I have used recursive functions in Java before.

"""

"""  
This version of the function prints the returned number unlike my solution below that prints the number, then returns it. 
The Reason I chose to not use this version is because it will print the sequence in reverse order.

def reducer(number):  # Function takes an int.

    if number % 2 == 0:  # If the number is even.
        number /= 2  # Divide the number by 2.
        if number != 1:  # If the number isn't 1 the sequence isn't complete.
            print(reducer(number))  # Recursively call the function.
        return int(number)  # Return the modified number to the function that called this instance of the function.

    else:  # If the number is odd.
        number = number * 3 + 1  # Multiply the number by 3, then add 1.
        print(reducer(number))  # Recursively call the function.
        return int(number)  # Return the modified number to the function that called this instance of the function.

"""


def reducer(number):  # Function takes an int.

    if number % 2 == 0:  # If the number is even.
        number /= 2  # Divide the number by 2.
        print(int(number))
        if number != 1:  # If the number isn't 1 the sequence isn't complete.
            reducer(number)  # Recursively call the function.
        return int(number)  # Return the modified number to the function that called this instance of the function.

    else:  # If the number is odd.
        number = number * 3 + 1  # Multiply the number by 3, then add 1.
        print(int(number))
        reducer(number)  # Recursively call the function.
        return int(number)  # Return the modified number to the function that called this instance of the function.


def main():
    number = 0  # Initialize number to 0.

    while True:
        try:
            while number <= 1:  # Ask the user for a number until the given number is at-least 1.
                number = int(input("Please input a number (Must be greater than 1): "))
            break  # If the number the user has input satisfies the constraint, break out of the loop.

        except ValueError:
            print("Please input only numerical characters.")
            pass
        except:
            print("Unexpected error!")
            pass

    reducer(number)  # Call the reducer function and pass the taken number.


main()
