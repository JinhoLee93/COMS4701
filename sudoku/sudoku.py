#!/usr/bin/env python
#coding:utf-8

#Jinho Lee (jl5027)
#sudoku.py

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import time
import statistics
import sys

TIME_TAKEN = 0
BOARD_NUMBER = 0
MIN = 0
MAX = 0
STANDARD_DEVIATION = []
ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    backtrack(board)
    solved_board = board

    return solved_board

def backtrack(board):
    # Traverses through the board assigning new values
    # and deleting conflicting values.

    zeroes = find_zeroes(board)

    if len(zeroes) == 0:
        return True

    rv = find_rv(board)
    mrv = []

    for square in zeroes:
        mrv.append(len(rv[square]))

    # Minimum remaining values in the ascending order
    mrv_index = mrv.index(min(mrv))
    pos = zeroes[mrv_index]
    domain = rv[pos]

    # Backtracking loop
    while len(domain) != 0:
        value = domain[0]
        domain.remove(value)
        if forward_checking(rv, value, pos):
            board[pos] = value
            if backtrack(board):
                return True
            else:
                board[pos] = 0

    return False

def forward_checking(rv, num, pos):
    # Check each row
    row = ROW.find(pos[0])
    col = COL.find(pos[1])

    for i in range(len(COL)):
        if rv[pos[0] + COL[i]] == num and pos[0] != i:
            return False

    # Check each column
    for i in range(len(ROW)):
        if rv[ROW[i] + pos[1]] == num and pos[1] != i:
            return False

    # Traverse through the 3x3 box by the given row and column.
    box_row = row // 3
    box_col = col // 3

    for i in range(3):
        for j in range(3):
            x = rv[ROW[box_row * 3 + i] + COL[box_col * 3 + j]]
            if len(x) == 1:
                if x[0] == num:
                    return False

    return True

def find_zeroes(board):
    # Return a list of rows and columns with 0 value.
    zeroes = []

    for pos, val in board.items():
        if val == 0:
            zeroes.append(pos)

    return zeroes

def find_rv(board):
    # Find remaining values by the given row and column
    rv = {}

    # Initiating the set
    for i in range(len(ROW)):
        for j in range(len(COL)):
            rv[ROW[i] + COL[j]] = [k for k in range(1, 10)]

    # Finiding non-zero remaining values and remove them from the entire domains
    for i in range(len(ROW)):
        for j in range(len(COL)):
            if board[ROW[i] + COL[j]] != 0:
                value = board[ROW[i] + COL[j]]
                rv = remove_value(rv, value, i, j)

    return rv

def remove_value(rv, value, r, c):
    # Helper function that removes remaining values from the list of domains.
    # For already taken indices
    rv[ROW[r] + COL[c]] = [0]

    # ValueError exception catch inspired by
    # https://stackoverflow.com/questions/9915339

    # Remove remaining values in the given row.
    for i in range(len(ROW)):
        values = rv[ROW[r] + COL[i]]
        try:
            values.remove(value)
        except ValueError:
            pass

    # Remove remaining values in the given column.
    for i in range(len(COL)):
        values = rv[ROW[i] + COL[c]]
        try:
            values.remove(value)
        except ValueError:
            pass

    # Traverse through the 3x3 box by the given row and column.
    box_row = r // 3
    box_col = c // 3
    for i in range(3):
        for j in range(3):
            values = rv[ROW[box_row * 3 + i] + COL[box_col * 3 + j]]
            try:
                values.remove(value)
            except ValueError:
                pass

    return rv

if __name__ == '__main__':
    #  Read boards from source.
    if len(sys.argv) == 1:
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            BOARD_NUMBER += 1
            print_board(board)
            start_time = time.time()
            # Solve with backtracking
            solved_board = backtracking(board)
            end_time = time.time()
            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)
            runtime = end_time - start_time
            if BOARD_NUMBER == 1:
                first_run = runtime
                MIN = first_run
            TIME_TAKEN += runtime
            STANDARD_DEVIATION.append(runtime)
            print("Time taken for board", BOARD_NUMBER, ": %.3f second(s)" %runtime)
            if MIN > runtime:
                MIN = runtime
            if MAX < runtime:
                MAX = runtime
            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

    elif len(sys.argv) == 2:
        line = sys.argv[1]
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        board = {ROW[r] + COL[c]: int(line[9 * r + c])
            for r in range(9) for c in range(9)}

        BOARD_NUMBER += 1
        print_board(board)
        start_time = time.time()
        solved_board = backtracking(board)
        end_time = time.time()
        print_board(solved_board)
        runtime = end_time - start_time
        if BOARD_NUMBER == 1:
            first_run = runtime
            MIN = first_run
        TIME_TAKEN += runtime
        STANDARD_DEVIATION.append(runtime)
        print("Time taken for board", BOARD_NUMBER, ": %.3f second(s)" % runtime)
        if MIN > runtime:
            MIN = runtime
        if MAX < runtime:
            MAX = runtime

        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:

        print("Invalid number of inputs")

    print("Time taken to process all the boards: %.3f seconds" %TIME_TAKEN)
    print("Max: %.3f seconds" %MAX)
    print("Min: %.3f seconds" %MIN)
    print("Mean: %.3f seconds" %(TIME_TAKEN/BOARD_NUMBER))
    if sys.argv == 1:
        print("Standard Deviation: %.3f seconds" %(statistics.stdev(STANDARD_DEVIATION)))
    else:
        print("Standard Deviation: None")
    print("Finishing all boards in file.")
