#include <stdio.h>
#include <stdlib.h>

#include <string.h>
#define WALL 'w'
#define POTION '#'
#define NEEDED_POTIONS 3

struct maze_location
{
	int row;
	int col;
};

struct maze
{
	char **a;	// 2D array supporting maze
	unsigned int w;	// width
	unsigned int h;	// height
	unsigned int cell_size;	// number of chars per cell; walls are 1 char
};

/**
 *Represents a cell in the 2D matrix.
 */
struct cell
{
	unsigned int x;

	unsigned int y;

};

/**
 *Stack structure using a list of cells.
 *At element 0 in the list we have NULL.
 *Elements start from 1 onwards.
 *top_of_stack represents the index of the top of the stack
 *in the cell_list.
 */
struct stack
{
	struct cell * cell_list;

	unsigned int top_of_stack;

	unsigned int capacity;

};

/**
 *Initialises the stack by allocating memory for the internal list
 */
void
init_stack(struct stack *stack, unsigned int capacity)
{
	stack->cell_list =
		(struct cell *) malloc(sizeof(struct cell) *(capacity + 1));

	stack->top_of_stack = 0;

	stack->capacity = capacity;

}

void

free_stack(struct stack *stack)
{
	free(stack->cell_list);

}

/**
 *Returns the element at the top of the stack and removes it
 *from the stack.
 *If the stack is empty, returns NULL
 */
struct cell
stack_pop(struct stack *stack)
{
	struct cell cell = stack->cell_list[stack->top_of_stack];

	if (stack->top_of_stack > 0)

		stack->top_of_stack--;

	return cell;

}

/**
 *Pushes an element to the top of the stack.
 *If the stack is already full (reached capacity), returns -1.
 *Otherwise returns 0.
 */
int
stack_push(struct stack *stack, struct cell cell)
{
	if (stack->top_of_stack == stack->capacity)

		return -1;

	stack->top_of_stack++;

	stack->cell_list[stack->top_of_stack] = cell;

	return 0;

}

int
stack_isempty(struct stack *stack)
{
	return stack->top_of_stack == 0;

}

//-----------------------------------------------------------------------------

void
mark_visited(struct maze *maze, struct cell cell)
{
	maze->a[cell.y][cell.x] = 'v';

}

/**
 *Convert a cell coordinate to a matrix index.
 *The matrix also contains the wall elements and a cell might span
 *multiple matrix cells.
 */
int
cell_to_matrix_idx(struct maze *m, int cell)
{
	return (m->cell_size + 1) *cell + (m->cell_size / 2) + 1;

}

/**
 *Convert maze dimension to matrix dimension.
 */
int
maze_dimension_to_matrix(struct maze *m, int dimension)
{
	return (m->cell_size + 1) *dimension + 1;

}

/**
 *Returns the index of the previous cell (cell - 1)
 */
int
matrix_idx_prev_cell(struct maze *m, int cell_num)
{
	return cell_num - (m->cell_size + 1);

}

/**
 *Returns the index of the next cell (cell + 1)
 */
int
matrix_idx_next_cell(struct maze *m, int cell_num)
{
	return cell_num + (m->cell_size + 1);

}

/**
 *Returns into neighbours the unvisited neighbour cells of the given cell.
 *Returns the number of neighbours.
 *neighbours must be able to hold 4 cells.
 */
int
get_available_neighbours(struct maze *maze, struct cell cell,
	struct cell *neighbours)
{
	int num_neighbrs = 0;

	// Check above
	if ((cell.y > cell_to_matrix_idx(maze, 0)) &&
		(maze->a[matrix_idx_prev_cell(maze, cell.y)][cell.x] != 'v'))

	{
		neighbours[num_neighbrs].x = cell.x;

		neighbours[num_neighbrs].y = matrix_idx_prev_cell(maze, cell.y);

		num_neighbrs++;
	}

	// Check left
	if ((cell.x > cell_to_matrix_idx(maze, 0)) &&
		(maze->a[cell.y][matrix_idx_prev_cell(maze, cell.x)] != 'v'))

	{
		neighbours[num_neighbrs].x = matrix_idx_prev_cell(maze, cell.x);

		neighbours[num_neighbrs].y = cell.y;

		num_neighbrs++;
	}

	// Check right
	if ((cell.x < cell_to_matrix_idx(maze, maze->w - 1)) &&
		(maze->a[cell.y][matrix_idx_next_cell(maze, cell.x)] != 'v'))

	{
		neighbours[num_neighbrs].x = matrix_idx_next_cell(maze, cell.x);

		neighbours[num_neighbrs].y = cell.y;

		num_neighbrs++;
	}

	// Check below
	if ((cell.y < cell_to_matrix_idx(maze, maze->h - 1)) &&
		(maze->a[matrix_idx_next_cell(maze, cell.y)][cell.x] != 'v'))

	{
		neighbours[num_neighbrs].x = cell.x;

		neighbours[num_neighbrs].y = matrix_idx_next_cell(maze, cell.y);

		num_neighbrs++;
	}

	return num_neighbrs;

}

/**
 *Removes a wall between two cells.
 */
void
remove_wall(struct maze *maze, struct cell a, struct cell b)
{
	int i;

	if (a.y == b.y)

	{
		for (i = 0; i < maze->cell_size; i++)

			maze->a[a.y - maze->cell_size / 2 + i][a.x -
				(((int) a.x -
					(int) b.x)) / 2
			] = ' ';
	}
	else

	{
		for (i = 0; i < maze->cell_size; i++)

			maze->a[a.y - (((int) a.y - (int) b.y)) / 2][a.x -

				maze->cell_size / 2 +

				i
			] = ' ';
	}
}

/**
 *Fill all matrix elements corresponding to the cell
 */
void
fill_cell(struct maze *maze, struct cell c, char value)
{
	int i, j;

	for (i = 0; i < maze->cell_size; i++)

		for (j = 0; j < maze->cell_size; j++)

			maze->a[c.y - maze->cell_size / 2 + i][c.x - maze->cell_size / 2 +
				j
			] =
			value;

}

/**
 *This function generates a maze of width x height cells.
 *Each cell is a square of cell_size x cell_size characters.
 *The maze is randomly generated based on the supplied rand_seed.
 *Use the same rand_seed value to obtain the same maze.
 *
 *The function returns a struct maze variable containing:
 *- the maze represented as a 2D array (field a)
 *- the width (number of columns) of the array (field w)
 *- the height (number of rows) of the array (field h).
 *In the array, walls are represented with a 'w' character, while
 *pathways are represented with spaces (' ').
 *The edges of the array consist of walls, with the exception
 *of two openings, one on the left side (column 0) and one on
 *the right (column w-1) of the array. These should be used
 *as entry and exit.
 */
struct maze
generate_maze(unsigned int width, unsigned int height,
	unsigned int cell_size, int rand_seed)
{
	int row, col, i;

	struct stack stack;

	struct cell cell;

	struct cell neighbours[4];	// to hold neighbours of a cell
	int num_neighbs;

	struct maze maze;

	maze.w = width;

	maze.h = height;

	maze.cell_size = cell_size;

	maze.a =
		(char **) malloc(sizeof(char*) *

			maze_dimension_to_matrix(&maze, height));

	// Initialise RNG
	srandom(rand_seed);

	// Initialise stack
	init_stack(&stack, width *height);

	// Initialise the matrix with walls
	for (row = 0; row<maze_dimension_to_matrix(&maze, height); row++)

	{
		maze.a[row] =
			(char*) malloc(maze_dimension_to_matrix(&maze, width));

		memset(maze.a[row], WALL, maze_dimension_to_matrix(&maze, width));
	}

	// Select a random position on a border.
	// Border means x=0 or y=0 or x=2*width+1 or y=2*height+1
	cell.x = cell_to_matrix_idx(&maze, 0);

	cell.y = cell_to_matrix_idx(&maze, random() % height);

	mark_visited(&maze, cell);

	stack_push(&stack, cell);

	while (!stack_isempty(&stack))

	{
		// Take the top of stack
		cell = stack_pop(&stack);

		// Get the list of non-visited neighbours
		num_neighbs = get_available_neighbours(&maze, cell, neighbours);

		if (num_neighbs > 0)

		{

			struct cell next;

			// Push current cell on the stack
			stack_push(&stack, cell);

			// Select one random neighbour
			next = neighbours[random() % num_neighbs];

			// Mark it visited
			mark_visited(&maze, next);

			// Break down the wall between the cells
			remove_wall(&maze, cell, next);

			// Push new cell on the stack
			stack_push(&stack, next);
		}
	}

	// Finally, replace 'v' with spaces
	for (row = 0; row<maze_dimension_to_matrix(&maze, height); row++)

		for (col = 0; col<maze_dimension_to_matrix(&maze, width); col++)

			if (maze.a[row][col] == 'v')

	{
		cell.y = row;

		cell.x = col;

		fill_cell(&maze, cell, ' ');
	}

	// Select an entry point in the top right corner.
	// The first border cell that is available.
	for (row = 0; row<maze_dimension_to_matrix(&maze, height); row++)

		if (maze.a[row][1] == ' ')

	{
		maze.a[row][0] = ' ';

		break;
	}

	// Select the exit point
	for (row = maze_dimension_to_matrix(&maze, height) - 1; row >= 0; row--)

		if (maze.a[row][cell_to_matrix_idx(&maze, width - 1)] == ' ')

	{
		maze.a[row][maze_dimension_to_matrix(&maze, width) - 1] = ' ';

		break;
	}

	maze.w = maze_dimension_to_matrix(&maze, maze.w);

	maze.h = maze_dimension_to_matrix(&maze, maze.h);

	// Add the potions inside the maze at three random locations
	for (i = 0; i < NEEDED_POTIONS; i++)

	{
		do

		{

			row = random() % (maze.h - 1);

			col = random() % (maze.w - 1);
		}

		while (maze.a[row][col] != ' ');

		maze.a[row][col] = POTION;
	}

	return maze;

}

void printMaze(struct maze maze, int potionsFound, int fog, struct maze_location currentIndex)
{
	int row, col, sr, sc, er, ec;

	if (fog % 2 != 0) {
		sr = currentIndex.row - (fog / 2);
		sc = currentIndex.col - (fog / 2);
		er = currentIndex.row + (fog / 2) + 1;
		ec = currentIndex.col + (fog / 2) + 1;
		if (sr < 0){sr = 0;}
		if (sc < 0){sc = 0;}
		if (er > maze.h){er = maze.h;}
		if (ec > maze.w){ec = maze.w;}
		for (row = sr; row < er; row++)
		{
			for (col = sc; col < ec; col++)
			{
				printf("%c", maze.a[row][col]);
			}

			printf("\n\n");
		}
	} else if (fog % 2 == 0) {
		sr = currentIndex.row - (fog / 2)+1;
		sc = currentIndex.col - (fog / 2)+1;
		er = currentIndex.row + (fog / 2) + 1;
		ec = currentIndex.col + (fog / 2) + 1;
		if (sr < 0){sr = 0;}
		if (sc < 0){sc = 0;}
		if (er > maze.h){er = maze.h;}
		if (ec > maze.w){ec = maze.w;}
		for (row = sr; row < er; row++)
		{
			for (col = sc; col < ec; col++)
			{
				printf("%c", maze.a[row][col]);
			}

			printf("\n\n");
		}
	}

	if (fog == 0)
	{
		for (row = 0; row < maze.h; row++)
		{
			for (col = 0; col < maze.w; col++)
			{
				printf("%c", maze.a[row][col]);
			}

			printf("\n\n");
		}
	}
}

void main()
{
	int width, height, cellSize, randSeed, i, p, ii;
	int potionsFound = 0;
	int fog = 0;
	struct maze maze;

	// GET USER'S INPUT.
	do {
		printf("\nEnter the maze width (Min. 20): ");
		scanf("%d", &width);
	}
	while (width < 20);

	do {
		printf("\nEnter the maze height (Min. 3): ");
		scanf("%d", &height);
	}
	while (height < 3);

	do {
		printf("\nEnter the cell size (Min. 1, Must be odd): ");
		scanf("%d", &cellSize);
	}
	while (cellSize % 2 == 0 || cellSize < 1);

	do {
		printf("\nEnter a random seed: ");
		scanf("%d", &randSeed);
		getchar();
	}
	while (randSeed < 0);

	do {
		printf("\nEnter Fog Depth (0 = No Fog): ");
		scanf("%d", &fog);
		getchar();
	}
	while (fog < 0);

	// GENERATE THE MAZE.
	maze = generate_maze(width, height, cellSize, randSeed);
	struct maze_location startIndex;
	struct maze_location currentIndex;
	struct maze_location endIndex;

	// FIND STARTING POSITION.
	for (i = 0; i < maze.h; i++)
	{
		if (maze.a[i][0] != WALL)
		{
			maze.a[i][0] = '@';
			startIndex.row = i;
			startIndex.col = 0;
			currentIndex.row = i;
			currentIndex.col = 0;
			break;
		}
	}

	// FIND END POSITION.
	for (ii = 0; ii < maze.h; ii++)
	{
		if (maze.a[ii][maze.w - 1] != WALL)
		{
			endIndex.row = ii;
			endIndex.col = maze.w - 1;
			break;
		}
	}

	printMaze(maze, potionsFound, fog, currentIndex);
	char move;

	while (1)
	{
		if (currentIndex.row == endIndex.row && currentIndex.col == endIndex.col && potionsFound == NEEDED_POTIONS)
		{

			printMaze(maze, potionsFound, fog, currentIndex);
			printf("Congratulations, You win!");
			break;
		}

		printf("\n");
		scanf("%c", &move);

		if (potionsFound < NEEDED_POTIONS)
		{
			printf("Potions: ");
			for (p = 0;
				(NEEDED_POTIONS - potionsFound) - p; p++)
			{
				putchar(POTION);
			}
			putchar('\n');
		}
		else
		{
			printf("You've found all the potions, now make your way to the exit.\n");
		}

		switch (move)
		{
            
            case 'W':
			case 'w':

				if (maze.a[currentIndex.row - 1][currentIndex.col] != WALL)
				{
					if (maze.a[currentIndex.row - 1][currentIndex.col] == POTION)
					{
						potionsFound++;
					}

					maze.a[currentIndex.row][currentIndex.col] = ' ';
					maze.a[currentIndex.row - 1][currentIndex.col] = '@';
					currentIndex.row = currentIndex.row - 1;
				}
				printMaze(maze, potionsFound, fog, currentIndex);
				break;
            
            case 'A':
			case 'a':

				if (maze.a[currentIndex.row][currentIndex.col - 1] != WALL)
				{
					if (maze.a[currentIndex.row][currentIndex.col - 1] == POTION)
					{
						potionsFound++;
					}
					if (currentIndex.row == startIndex.row && currentIndex.col - 1 == startIndex.col - 1)
					{
						printMaze(maze, potionsFound, fog, currentIndex);
						printf("Not so fast, you can't go that way!");
						break;
					}

					maze.a[currentIndex.row][currentIndex.col] = ' ';
					maze.a[currentIndex.row][currentIndex.col - 1] = '@';
					currentIndex.col = currentIndex.col - 1;
				}
				printMaze(maze, potionsFound, fog, currentIndex);
				break;
            
            case 'S':
			case 's':

				if (maze.a[currentIndex.row + 1][currentIndex.col] != WALL)
				{
					if (maze.a[currentIndex.row + 1][currentIndex.col] == POTION)
					{
						potionsFound++;
					}

					maze.a[currentIndex.row][currentIndex.col] = ' ';
					maze.a[currentIndex.row + 1][currentIndex.col] = '@';
					currentIndex.row = currentIndex.row + 1;
				}
				printMaze(maze, potionsFound, fog, currentIndex);
				break;
            
            case 'D':
			case 'd':

				if (maze.a[currentIndex.row][currentIndex.col + 1] != WALL)
				{
					if (maze.a[currentIndex.row][currentIndex.col + 1] == POTION)
					{
						potionsFound++;
					}
					if (currentIndex.row == endIndex.row && currentIndex.col + 1 == endIndex.col && potionsFound != NEEDED_POTIONS)
					{
						printMaze(maze, potionsFound, fog, currentIndex);
						printf("You haven't found all the potions yet! ");
						break;
					}

					maze.a[currentIndex.row][currentIndex.col] = ' ';
					maze.a[currentIndex.row][currentIndex.col + 1] = '@';
					currentIndex.col = currentIndex.col + 1;
				}
				printMaze(maze, potionsFound, fog, currentIndex);
				break;

			default:

				printMaze(maze, potionsFound, fog, currentIndex);
				break;
		}
	}
}
