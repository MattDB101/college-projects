import string, copy

"""

As with all my project's, I start by breaking the requirements into simple segments.
The key goals in the script are as follows;

1. Interactively ask the user for a list.
2. Define two functions checkQMark & checkLetterCounts, both of which are passed the list defined by the user.
3. In the checkQMark function, loop through each word in the list and use the "in" keyword to check for ?'s.
4. In the checkLetterCounts function, set all letters to lower case, then loop through the alphabet checking if a given letter occurs in all the words in a list, then add that letter to a list.

First, asking the user for a list. As I have some past experience with Python, this is pretty trivial. A simple infinite loop until the user asks to stop.

Next, defining the two functions, I didn't immediately remember the syntax for this, so I checked the slides from lecture 12 which covered this topic.

To check for question marks, all I had to do was loop through the list and then use the "in" keyword, I had recently used this keyword in my solution to Lab 08.

Next, the checkLetterCounts function, I did have some trouble in creating this function.
To begin, I copied the passed list into a new list case so as to not affect the user's strings this was covered in lecture 12.
Then I looped through the new list and set all elements to be lower case, which was covered in lecture 16. The code used to loop through all elements of the list was covered in lecture 12.
I then loop through each letter of the alphabet, I went online to find an elegant way of doing this, I found that the string library will do exactly what I need. (https://www.kite.com/python/answers/how-to-make-a-list-of-the-alphabet-in-python)
Next, I needed to loop through the letter of words in the list, I found this problem gave me some trouble.
I thought it would be better to try and use list comprehension for this problem, the issue being that I didn't know about the all() function.
I researched online for a way to check all items in a list python, and I found the all W3 schools page for the all() function. (https://www.w3schools.com/python/ref_func_all.asp_)
After identifying the common letters I append them to a list, this makes printing and identifying the number of common letters a simple task.

"""


def checkQMark(list):  # Function takes a list.
    qCount = 0
    print("\nQuestion mark check:\n")
    for word in list:  # Loop through contents of passed list.
        if "?" in word:  # Check if current word contains a "?".
            print(word, "contains a question mark.")
            qCount += 1  # Increment the word containing ? counter.
    if qCount == 0:  # If no words contain a ? tell the user.
        print("No words in the list contains a \"?\".")


def checkLetterCounts(list):  # Function takes a list.
    commonLetters = []  # Create an empty list that will be populated with characters that are in all words of the passed list.
    listLC = copy.copy(list)  # Create a copy if the passed list.
    for i in range(len(listLC)):
        listLC[i] = listLC[
            i].lower()  # Set new list to be lowercase so as to include matches that aren't of the same case.

    print("\nCommon character check:")

    for letter in string.ascii_lowercase:  # Loop through all characters in the alphabet
        if all(letter in word for word in listLC):  # Check if the letter can be found in every word in the passed list.
            commonLetters.append(letter)  # If the letter does occur in every word in the passed list, add it to the commonLetters list.

    for letter in commonLetters:  # Loop through all the letters in the commonLetters list.
        print("\nCharacter", letter, "appears in all items.")  # Print the letter.
        for word in listLC:  # Loop through the words in the passed list.
            print(word, "contains the letter ", letter, word.count(letter),"time(s).")  # Print the number of times the selected letter occurs in the selected word.
    if len(commonLetters) == 0:  # If no words share a letter tell the user.
        print("\nNo words in the share a letter.")


def main():
    list = []  # Given list of strings.
    while True:  # Infinitely take words until the user says to stop
        userInput = input("\nPlease input a word to be added to the list of words, press enter without typing anything to stop adding words: ")
        if len(list) == 0 and userInput == "":  # If the user requests to enter 0 words.
            print("Please input at least 1 word.")
        elif len(list) > 0 and userInput == "":  # If the user requests to stop enter words.
            break
        else:
            list.append(userInput)  # If they haven't asked to stop, add the given word.

    checkQMark(list)  # Call ? count function.
    checkLetterCounts(list)  # Call common letter function.


main()
