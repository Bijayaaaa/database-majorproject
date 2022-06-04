# source: https://www.askpython.com/python/examples/sudoku-solver-in-python
import random

M = 9
def puzzle(grid):
    # prints the suduko board with values
    for i in range(M):
        for j in range(M):
            print(grid[i][j],end = " ")
        print()
def solve(grid, row, col, num):
    # checks if num is suitable for grid[row][col]
    # returns True or False
    
    # checks if value already exist in row
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # checks if value already exist in column    
    for x in range(9):
        if grid[x][col] == num:
            return False
    
    # Checks the 3*3 rectangular box
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True # num. does not exist in row, column of the grid
 
def Suduko(grid, row, col):
    # main function to traverse through the grid
    # recursive function

    if (row == M - 1 and col == M):
        # puzzle solved <last element of grid>
        return True, grid
    if col == M:
        # go to next row, column = 0
        row += 1
        col = 0
    if grid[row][col] > 0:
        # position filled check next position
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1): 
        # fill empty grid witn val. 1 - 9 untill it satisfies the position
        if solve(grid, row, col, num):
            # num. satisfies the position <does not already exist in the row, column of the grid>
            grid[row][col] = num
            
            # check game over
            if Suduko(grid, row, col + 1):
                return True, grid # <check if solved>
        grid[row][col] = 0  # <Unsolvable suduko>
    return False

'''0 means the cells where no value is assigned'''
grid = [[2, 5, 0, 0, 3, 0, 9, 0, 1],
        [0, 1, 0, 0, 0, 4, 0, 0, 0],
        [4, 0, 7, 0, 0, 0, 2, 0, 8],
        [0, 0, 5, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 8, 1, 0, 0],
        [0, 4, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 3, 6, 0, 0, 7, 2],
        [0, 7, 0, 0, 0, 0, 0, 0, 3],
        [9, 0, 3, 0, 0, 0, 6, 0, 4]]
 
if (Suduko(grid, 0, 0)):
    puzzle(grid)
else:
    print("Solution does not exist:(")


def generate_suduko(drop_how_many=27):
    initial_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    _,initial_grid = Suduko(grid, 0, 0)
    for i in range(drop_how_many):
            row = random.choice(range(0,9))
            col = random.choice(range(0,9))
            initial_grid[row][col] = 0
    return initial_grid

print(generate_suduko())
# # genrates suduko game
# def next_number(row, col):
#     next_num_start = (3*row) % 9
#     next_num = (next_num_start + col + 1) % 9
#     if next_num == 0:
#         next_num = 1 
#     return next_num
#     # returns: [[1, 2, 3, 1, 2, 3, 1, 2, 3], [4, 5, 6, 4, 5, 6, 4, 5, 6], [7, 8, 1, 7, 8, 1, 7, 8, 1], [1, 2, 3, 1, 2, 3, 1, 2, 3], [4, 5, 6, 4, 5, 6, 4, 5, 6], [7, 8, 1, 7, 8, 1, 7, 8, 1], [1, 2, 3, 1, 2, 3, 1, 2, 3], [4, 5, 6, 4, 5, 6, 4, 5, 6], [7, 8, 1, 7, 8, 1, 7, 8, 1]]
# # def shuffle(grid):


# def generateSuduko():
#     values = [[i for i in range(9)]]* 9
#     grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
#     for i in range(9):
#         for j in range(9):
#             grid[i][j] = next_number(i, j)
#             print(f'grid[{i}][{j}] = {grid[i][j]}')
#     print(grid)
#     puzzle(grid)

# generateSuduko()
