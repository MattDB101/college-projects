#include <stdio.h> //Standard IO functions
#include <stdlib.h> //Standard Library functions

struct Student{
    char fName[10];
    char init[2];
    char lName[10];
    int year;
    char course[10];
    char group;
    int avg;
};


struct Node {
    struct Student *data;
    struct Node *next;
};


int fscanfMB(FILE *file, const char *fString, char *fName, char *init, char *lName, int *year, char *course, char *group, int *avg) {

    if(feof(file)) {
        return 1;
    }

    int fStrIndex = 0; // format string index.
    int strIndex = 0; // tracker of current "word" in the read line
    int strCount = 0; // tracker of which string's in the fString pattern have been read so far.
    int intCount = 0; // tracker of which int's in the fString pattern have been read so far.
    int matchedParams = 0; // how many "things" have been read from the line.
    char line[100]; // line read from the file.
    char *ptr; // used in strtol.
    long ret;  // number from using strtol.

    fgets(line, 100, file); // get line from file.

	while (fString[fStrIndex] != '\0') { // loop through characters of format string.

		if (fString[fStrIndex] == '%') { // if the current characters is the placeholder, advance to the next character.
			fStrIndex++;

			if (fString[fStrIndex] == 's') { // if formatString is of type string.
				int i = 0;
				char tempString[100];
				int index = 0;

				for (i = strIndex; line[i] != ' '; i++) {  // get characters of current string and load them into the temp string.
					if (line[i] == '\0' || line[i] == '\n')
						break;
					tempString[index++] = line[i]; // load tempString.
					strIndex++;
				}
				tempString[index] = '\0';

				if (strCount == 0) { // read string is the student's first name.
					for (i = 0; tempString[i] != '\0'; i++) {
						fName[i] = tempString[i]; // unload tempString.
					}
					fName[i] = '\0';

				}

				else if (strCount == 1) { // read string is the student's initial.
                    			init[0] = tempString[1]; // unload the character that is actually of use.
					init[i] = '\0';
				}

				else if (strCount == 2) { // read string is the student's last name.
					for (i = 0; tempString[i] != '\0'; i++) {
						lName[i] = tempString[i]; // unload tempString.
					}
					lName[i] = '\0';
				}

				else if (strCount == 3) { // read string is the student's course name.
					for (i = 0; tempString[i] != '\0'; i++) {
						course[i] = tempString[i]; // unload tempString.
					}
					course[i] = '\0';
				}

				strCount++;
				matchedParams++;
			}

			else if (fString[fStrIndex] == 'd') { // if formatString is of type decimal int.

				if (intCount == 0) { // read string is the student's year.
                   			 ret = strtol(&line[strIndex], &ptr, 10); // get long int from current string
					*year = ret;
					if (ret !=0) { // student's year cannot be 0.
                       				matchedParams++;
					}
				}

				else if (intCount == 1) { // read string is the student's average.
					ret = strtol(&line[strIndex], &ptr, 10); // get long int from current string
					*avg = ret;
					matchedParams++;
				}

				strIndex++;
				intCount++;
			}

			else if (fString[fStrIndex] == 'c') { // if formatString is of type char.
				*group = line[strIndex];
				strIndex++;
				matchedParams++;
			}
		}

        else{strIndex++;} // if not %

		fStrIndex++;
	}
	return matchedParams;
}


int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Please provide a single file.");
        exit(1);
    }
	
	int menu = 1;
	while(menu != 0){
		printf("Enter 1 to load data.\n");
		printf("Enter 0 to exit.\n");
		printf(">>> ");
		scanf("%d", &menu);
		
		if(menu==0){
            exit(0);
		}

        else if (menu == 1) {
			int done = 0;
			FILE *file = fopen(argv[1], "r");
			struct Node *node;
            struct Node *cursor;
            struct Node list_head;
			node = malloc(sizeof(struct Node));

			while (done != 1) {
				node->data = malloc(sizeof(struct Student));
				node->next = NULL;
				struct Student *student = node->data;
				done = fscanfMB(file, "%s %s %s %d %s %c %d", student->fName, student->init, student->lName, &student->year, student->course, &student->group, &student->avg);
				if (done == 7) {
					printf("Student added: %s %s %s %d %s %c %d \n", student->fName, student->init, student->lName, student->year, student->course, student->group, student->avg);
				}
				node->next = malloc(sizeof(struct Node));
                node = node->next;
				free(student);

			}
            fclose(file);
            printf("\n");
        }
		
        else {
            printf("Please select either 1 or 0.\n\n");
		}
		
	}
	return 0; //return from main
}
