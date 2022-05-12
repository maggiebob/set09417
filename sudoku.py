# 
# Written by Maggie Woodward 40456404
# For SET09417 Coursework Spring 2022
# 

from pprint import pprint
import random
import curses
import time
from curses import wrapper
import numpy

def shuffle_list():
	
# 	create a randomly ordered list of the numbers 1-9
# 	used to randomly order guesses and initial sub-grids
	list = [1,2,3,4,5,6,7,8,9]
	random.shuffle(list)
	return list

def find_space(gameboard):
	# find the index of the next empty space (represented by 0)
	# could use shuffle_list to switch up solve order

	for r in range(9):
		for c in range(9):
			if gameboard[r][c] == 0:
				return r, c
				
	return None, None  # if no spaces in the puzzle are zero

def is_valid(gameboard, guess, row, col):
	# checks validity of each guess, following sudoku rules
	
	# check if guess exists in row
	row_vals = gameboard[row]
	if guess in row_vals:
		return False # if we've repeated, then our guess is not valid!
	
	# check if guess exists in column
	col_vals = [gameboard[i][col] for i in range(9)]
	if guess in col_vals:
		return False
	
	# get index of first space for current 3x3 subgrid
	r_start = (row // 3) * 3 
	c_start = (col // 3) * 3
	
	# check if guess exists in subgrid
	for r in range(r_start, r_start + 3):
		for c in range(c_start, c_start + 3):
			if gameboard[r][c] == guess:
				return False
	
	return True

def solve_sudoku(gameboard):
	# my backtracking algorithm! Created following https://youtu.be/tvP_FZ-D9Ng
	
	# get index of next empty space, if none, grid is complete
	row, col = find_space(gameboard)
	if row is None:
		return True
	
	# guess numbers 1-9 (in random order) and if guess is valid, enter in to grid
	guess_list = shuffle_list()
	for guess in guess_list:
		if is_valid(gameboard, guess, row, col):
			gameboard[row][col] = guess
			if solve_sudoku(gameboard): # recursion
				return True
		
		# if no valid solutions with this guess, backtrack
		gameboard[row][col] = 0
	
	# if puzzle unsolvable, return False. Can use this as exit
	return False
	
def list_spaces(gameboard):

	spaces_list = []
	
	for x in range(9):
		for y in range(9):
			if gameboard[x][y] == 0:
				spaces_list.append([x, y])

	return spaces_list
    
def generate_gameboard():
	# create 9x9 array, randomly complete diagonal subgrids
	# Tighten this up later!
		
# 	gameboard = []
	
	list1 = shuffle_list()
	list2 = shuffle_list()
	list3 = shuffle_list()
	
# 	i = 0
# 	for y in range (0,3):
# 		for x in range (0,3):
# 			gameboard[x][y] = list1[i]
# 			i += 1
#  
# 	i = 0
# 	for y in range (3,6):
# 		for x in range (3,6):
# 			gameboard[x][y] = list2[i]
# 			i += 1
#  
# 	i = 0
# 	for y in range (6,9):
# 		for x in range (6,9):
# 			gameboard[x][y] = list3[i]
# 			i += 1
# 			
# 	for y in range(9):
# 		for x in range (9):
# 			if gameboard[x][y] is None:
# 				gameboard[x][y] = 0

	
	gameboard = [
		[list1[0], list1[1], list1[2], 0, 0, 0, 0, 0, 0],
		[list1[3], list1[4], list1[5], 0, 0, 0, 0, 0, 0],
		[list1[6], list1[7], list1[8], 0, 0, 0, 0, 0, 0],
		[0, 0, 0, list2[0], list2[1], list2[2], 0, 0, 0],
		[0, 0, 0, list2[3], list2[4], list2[5], 0, 0, 0],
		[0, 0, 0, list2[6], list2[7], list2[8], 0, 0, 0],
		[0, 0, 0, 0, 0, 0, list3[0], list3[1], list3[2]],
		[0, 0, 0, 0, 0, 0, list3[3], list3[4], list3[5]],
		[0, 0, 0, 0, 0, 0, list3[6], list3[7], list3[8]],
	]
	
	solve_sudoku(gameboard)
	
	return gameboard
	
def generate_game(diff):
# need to use the backtracking algorithm to check each removal still leaves solvable game

	game = generate_gameboard()
	
	if diff == 1:
		removals = 36
	elif diff == 2:
		removals = 46
	elif diff == 3:
		removals = 52
	else:
		return
		
	i = 0
	while i < removals:
		r = random.randint(0,8)
		c = random.randint(0,8)
		if game[r][c] != 0:
			game[r][c] = 0
			i += 1
		
	return game
	
def print_game (window, crnt_board):

	# draw vertical lines
	for y in range(18):
		window.addch(y, 5, "|")
		window.addch(y, 11, "|")
	# draw horizontal lines
	for x in range(18):
		window.addch(5, x, "-")
		window.addch(11, x, "-")

	for y in range(9):
		for x in range(9):
			window.addstr(x*2, y*2, str(crnt_board[x][y]))
			window.refresh()
			
def save_game(gameboard):

#	function to save current game
	game = open("saved_game.csv", "w")
	
	for row in gameboard:
		numpy.savetxt(game, row, fmt='%i')
		
	game.close()

def load_game():

#	function to load existing game
	gameboard = numpy.loadtxt("saved_game.csv", dtype=int).reshape(9,9)
	
	return gameboard

def playgame (window):

# 	player instructions
	window.addstr(20, 1, "(a): New game easy (b): New game medium (c): New game difficult")
	window.addstr(21, 1, "(l): load (p): save (q): quit (s): solve")
	window.addstr(22, 1, "Use arrow keys to navigate board")
	window.addstr(23, 1, "Enter numbers 1-9 over any zeros")
			
	y = 0
	x = 0
	window.move(y,x)
			
	while True:
		c = window.getch()
# 		window.printstr(3, 30, str(c)) #input checker for ASCII conversion
# 		launch new game of selected difficulty
		if c == ord('a'):
			this_game = generate_game(1)
			print_game(window, this_game)
			spaces = list_spaces(this_game)
			moves =[]
			moves.append(this_game)
		elif c == ord('b'):
			this_game = generate_game(2)
			print_game(window, this_game)
			spaces = list_spaces(this_game)
			moves = []
			moves.append(this_game)
		elif c == ord('c'):
			this_game = generate_game(3)
			print_game(window, this_game)
			spaces = list_spaces(this_game)
			moves = []
			moves.append(this_game)
# 			Load an existing gameboard
		elif c == ord('l'):
			this_game = load_game()
			print_game(window, this_game)
			spaces = list_spaces(this_game)
			moves = []
			moves.append(this_game)
# 			Save the current gameboard
		elif c == ord('p'):
			save_game(this_game)
			window.addstr(24, 5, "The game has been saved")
			window.clrtoeol()
			window.move(y, x)
			
# 			other instructions
		if c == ord('q'): # quit the game
			break
		if c == ord('s'): # solve the game using the built in solver
			solve_sudoku(this_game)
			print_game(window, this_game)
			window.addstr(24, 5, "The game has been solved")
			window.clrtoeol()
			window.move(y, x)
# 			Below is meant to be my undo function, but while the moves stack works
# 			this doesn't seem to update playboard back to the previous
# 		if c == ord('u'):
# 			moves.pop()
# 			playboard = moves[-1]
# 			print_game(window, playboard)
			
# 			cursor movements
		elif c == curses.KEY_RIGHT:
			if x<16:
				x += 2
			window.move(y, x)
		elif c == curses.KEY_LEFT:
			if x>1:
				x -= 2
			window.move(y, x)
		elif c == curses.KEY_UP:
			if y>1:
				y -= 2
			window.move(y, x)
		elif c == curses.KEY_DOWN:
			if y<16:
				y += 2
			window.move(y, x)
			
# 			validating and entering guesses
		elif c in range(48,57): # ascii codes for 0-9
			if [y/2, x/2] in spaces: # only allows user to update indexes that start as 0
				if is_valid(this_game, int(chr(c)), int(y/2), int(x/2)): #validation
					this_game[int(y/2)][int(x/2)] = int(chr(c))
					print_game(window, this_game)
					moves.append(this_game)
					window.move(y, x)
				else: # error message if invalid
					window.addstr(24, 5, "Invalid move")
					window.clrtoeol()
					window.move(y, x)
			else: # error message if non-editable
				window.addstr(24,5, "Cannot change existing number")
				window.clrtoeol()
				window.move(y, x)

if __name__ == '__main__':

	print("Launching Sudoku")
	curses.wrapper(playgame)
	print("The game has been ended")
    