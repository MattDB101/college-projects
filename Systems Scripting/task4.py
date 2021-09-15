import os, shutil, zipfile

NUMARCHIVES = 5  # Define a const that defines the number of backups that will be created.

"""

I start by breaking the requirements into simple segments.
The key goals in the script are as follows;

1. Interactively ask the user for the name of a folder to be created.
2. Create a function to create a directory with the name the user has passed, Inside that directory create sub-directories and file's as specified in the task.
3. Create a function to change the case of all files in the "docs" directory after confirming the "docs" directory exists.
4. Create another function to make 5 archives of the contents of the "docs" folder and then save these archives to the "backup" folder
5. Output the contents of the "backup" folder and one of the zip files. 

First, asking the user for a name. I used similar code from the previous task, using a try/except to catch if the user input's an illegal character.

The makeDir() function.
The first step was to check whether or not the passed directory name already exists, I had not used Python for any OS related tasks before and was unsure of the syntax to do so.
Using the slides from lecture 14, I was able to find the correct code to check if a directory exists. 
However, I later discovered that this code requires a try/except to catch any errors that may arise when trying to remove a file that is currently open.
Now that I could confirm that the folder existed, I needed to remove that directory and all sub-directories, I was able to find the solution in lecture 15's slides.
Next I needed to create the directory and all the sub directories, I had remembered from lecture 14 that the makedirs() function can mass-create directories. 
I decided that a good way to go about creating all necessary sub-directories would be to have lists of folders/files found in each level of the directory 
and having a variable that keeps track of the path that has been created so far, then simply using a loop to append the folder/file name onto that variable and passing this variable into the makedirs() function.
This solution required I join a path with a string, and I had remembered that this topic was discussed during a lecture, so I went back to lecture 14 to find the os.path.join() function.
After all the directories were created I just had to create the files inside the "docs" folder. As I had past experience with Python, I was able to remember the syntax to do so.

The rename() function.
First, I needed to confirm the existence of the "docs" folder, I used a combination of the .exists and the .join  functions from earlier for this.
Next, I used a loop to loop through all the files inside the "docs" directory, I was unsure how to do this, but I was able to find the listdir function from lecture 14.
I then needed to split the file into it's name and it's extension, I couldn't find a method to do this is the lecture notes, so I looked online for a solution. (https://www.geeksforgeeks.org/how-to-get-file-extension-in-python/)
After the file has been split I simply use .lower on the name and .upper on the extension.
As this was my first time working with the OS I didn't know how to rename file's, I checked the lecture notes and found the shutil.move() function from lecture 15.

The zip() function.
I created a variable that appends the archive number to the string "backup_" and I created the variables src and dest, these are the path's parent directories of the "docs" folder and the location of the backup.
Now that I had the source and destination directory as a variable I could use this information to create the backup.
I hadn't used the zipfile library before so I referred to lecture 15's slides for creating, writing to and reading zip files.
After creating the zipfile I needed to get all files and sub directories inside the source directory. To do this, I used os.walk from lecture 15 to iterate through all directories.
Because the src variable was set to be the parent directory of the "docs" folder, the walk function would iterate through folders that weren't supposed to be backed up. 
The solution used was just to check the name of the directory and then using the continue keyword to exit this iteration of the loop early.
Next I needed to get the path of each sub directory using path.join to append the directories name to the current path.
I then needed to get the path from the source path to the current directory, I was unsure how to do this so I checked lecture 15's slides and found that os.path.relpath(dirPath, src).
I now have all the information needed to write the directory to the zip file.
Now that all directories have been made, I can now write the files. The code for this is the same as the code described above.

After creating all 5 backups, I needed to output the contents of the backup directory and one of the archives.
A simple loop to iterate through all files in the backup directory completes the first part of this problem nicely.
To read the contents of the zip file I used a solution I found online to neatly print the contents.

"""


def makeDir(root):  # Function that takes a string that will become the name of the new directory.
    if os.path.exists(root):  # If a directory already exists with that name.
        while True:
            try:
                shutil.rmtree(root)  # Remove the directory along with everything inside of it.
                break
            except PermissionError:  # If the directory cannot be removed as a file inside it is currently open, prompt the user to close the offending file.
                input("Error: Cannot remove directory as file is currently in use, please close the open file and press any key to continue.")
            except:  # If there is any other general error when trying to remove the directory, warn the user and exit.
                print("Unexpected Error!")
                exit(1)

    childOfRoot = ["backup", "working"]  # A list of the directories inside the user given root directory.
    childOfWorking = ["pics", "movie", "docs"]  # A list of the directories inside the "Working" directory.
    childOfDocs = ["school", "party"]  # A list of the directories inside the "Docs" directory.
    filesOfDocs = ["CORONAVIRUS.txt", "DANGEROUS.txt", "KEEPSAFE.txt", "STAYHOME.txt",
                   "HYGIENE.txt"]  # A list of the files inside the "Docs" directory.
    filesOfDocsContents = [
        "The virus that causes COVID-19 is mainly transmitted through droplets generated when an infected person coughs, sneezes, or exhales.",
        "The disease can be fatal. Older people, and those with pre-existing medical conditions are more vulnerable.",
        "Maintain a two-metre distance between yourself and others at all times. Frequently wash your hands for at least 20 seconds with soap and water",
        "Work from home. Only essential workers should go to their workplace.",
        "Use soap and water or alcohol hand sanitiser to clean your hands regularly."]  # A list of strings that will become the contents of the files from the "filesOfDocs" directory.

    workingTree = root  # Create a variable and assign it the name of the folder the user has provided.
    for dir in childOfRoot:
        os.makedirs(os.path.join(workingTree, dir))  # Create the directory inside the root folder.
    workingTree = os.path.join(workingTree, "working")  # Change the workingTree variable to append the "working" directory to it.

    for dir in childOfWorking:
        os.makedirs(os.path.join(workingTree, dir))  # Create the directory inside the "working" folder.
    workingTree = os.path.join(workingTree, "docs")  # Change the workingTree variable to append the "working" directory to it.

    for dir in childOfDocs:
        os.makedirs(os.path.join(workingTree, dir))  # Create the directory inside the "docs" folder.

    os.chdir(workingTree)  # Change working directory to root/working/docs.

    fileNum = 0  # Initialize fileNum to 0.
    while fileNum < len(filesOfDocs):
        file = open(filesOfDocs[fileNum], "w")  # Create a file with the name being a string in the filesOfDocs list.
        file.write(filesOfDocsContents[fileNum])  # Write a string from the "filesOfDocsContents" list to the corresponding file position.
        fileNum += 1


def rename(root):  # Function that takes a string that is the name of the directory that was created by the user.
    if os.path.exists(os.path.join(root, "working", "docs")):  # Confirm that "root/working/docs" exists.
        os.chdir(os.path.join(root, "working", "docs"))  # Change working directory to "root/working/docs".
        for file in os.listdir():
            name, ext = os.path.splitext(file)  # Split the file name into it's title and it's extension.
            name = name.lower()  # Set the name to lower case.
            ext = ext.upper()  # Set the extension to upper case.
            shutil.move(file, name + ext)  # Rename the file to have the altered name

    else:
        print(os.path.join(root, "working", "docs"),
              " doesn't exist.")  # If "root/working/docs" does not exist, warn the user.


def zip(root):  # Function that takes a string that is the name of the directory that was created by the user.
    count = 0
    while count < NUMARCHIVES:
        archiveName = "backup_" + str(count + 1) + ".zip"  # The name of the backup changes depending on the number of times the backup has been made already.
        src = os.path.join(root, "working")  # The location of the of the directories to be backed-up.
        dest = os.path.join(root, "backup", archiveName)  # The location of the backup to be created.

        with zipfile.ZipFile(dest, 'w') as archive:  # Create a zipfile in the location specified
            for dirpath, dirnames, filenames in os.walk(src):
                for dirname in dirnames:  # For each child folder inside the source directory.
                    if dirname == "movie" or dirname == "pics":  # As the current src contains folders we DON'T want backed up, we must exclude them from the backup.
                        continue
                    dirPath = os.path.join(dirpath, dirname)  # Build the path to the child directory.
                    dest = os.path.relpath(dirPath, src)  # Get path to the dirPath from the source directory.
                    archive.write(dirPath, dest)  # Write the directory to the zip file.

                for filename in filenames:  # For each file inside the directory.
                    filePath = os.path.join(dirpath, filename)  # Build the path to the file.
                    dest = os.path.relpath(filePath, src)  # Get path to the dirPath from the source directory.
                    archive.write(filePath, dest)  # Write the file to the zip file.
        count += 1

    print("\nContents of backup directory:")
    for file in os.listdir(os.path.join(root, "backup")):  # for each zip file in the "backup" directory, print the name of the zip.
        print(file)

    print(f"\nContents of {archiveName}:")
    os.chdir(os.path.join(root, "backup"))  # Change working directory to the location of the "backup" directory.
    zip = zipfile.ZipFile(archiveName)  # read the zip file that was made last.
    for info in zip.infolist():  # print the contents of the zip file that was made last.
        print(info.filename)


def main():
    while True:
        try:
            root = input("Please input the new folders name: ")  # Take the name of the folder to be created from the user.
            makeDir(root)
            os.chdir(os.path.dirname(__file__))  # Set the current working directory back to the script's location.
            rename(root)
            os.chdir(os.path.dirname(__file__))  # Set the current working directory back to the script's location.
            zip(root)
            break  # If the number the user has input satisfies the constraint, break out of the loop.
        except:
            print("Please do not use any illegal characters for the directory name.")
            pass

main()
