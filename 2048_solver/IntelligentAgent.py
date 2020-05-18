import random
from BaseAI import BaseAI
import numpy as np
import math
from copy import deepcopy

class IntelligentAgent(BaseAI):
	def getMove(self, grid):
		# Selects a random move and returns it
		best_move, _ = self.maximize(grid)

		return best_move

	def evaluate(self, in_grid, emptiness):
		# Heuristics (Smoothness, monotonicity, and emptiness (free tiles)) inspired by
		# (https://stackoverflow.com/questions/22342854/ what-is-the-optimal-algorithm-for-the-game-2048)

		score = 0

		grid = in_grid.clone()
		np_grid = np.array(in_grid.map)

		# Sum of the values on the board
		# Also, I made it square of the sum to give it more weights.
		sum = np.sum(np.power(np_grid, 2))

		# The bigger smoothness the worse for the score.
		smoothness = 0

		# These smoothness and monotonicity loops below were inspired by
		# https://github.com/ovolve/2048-AI/blob/master/js/grid.js
		# whose writer wrote the answer in the StackOverflow thread above

		# Row smoothness
		for i in range(3):
			smoothness -= np.sum(np.abs(np_grid[:, i] - np_grid[:, i+1]))
		# Column smoothness
		for j in range(3):
			smoothness -= np.sum(np.abs(np_grid[j, :] - np_grid[j+1, :]))

		# Monotonicity
		mono_up = 0
		mono_down = 0
		mono_left = 0
		mono_right = 0

		# Monotonicity up and down
		for x in range(4):
			current = 0
			next = current + 1
			while next < 4:
				while next < 3 and not grid.map[next][x]:
					next += 1
				current_cell = grid.getCellValue((current, x))
				current_value = math.log(current_cell, 2) if current_cell else 0
				next_cell = grid.getCellValue((next, x))
				next_value = math.log(next_cell, 2) if next_cell else 0
				if current_value > next_value:
					mono_up += (next_value - current_value)
				elif next_value > current_value:
					mono_down += (current_value - next_value)
				current = next
				next += 1

		# Monotonicity right and left
		for y in range(4):
			current = 0
			next = current + 1
			while next < 4:
				while next < 3 and not grid.map[y][next]:
					next += 1
				current_cell = grid.getCellValue((y, current))
				current_value = math.log(current_cell, 2) if current_cell else 0
				next_cell = grid.getCellValue((y, next))
				next_value = math.log(next_cell, 2) if next_cell else 0
				if current_value > next_value:
					mono_left += (next_value - current_value)
				elif next_value > current_value:
					mono_right += (current_value - next_value)
				current = next
				next += 1

		# You cannot have both up and down or both left and right monotonicity.
		# So, I chose to add the maximum values from the two sets of
		# monotonicity (up and down and right and left).
		monotonicity = max(mono_up, mono_down) + max(mono_right, mono_left)

		# Weight values for emptiness and monotonicity.
		# These weight values were achieved by a series of numerous tests.
		emptiness_w = 10
		monotonicity_w = 1000

		emptiness_wd = emptiness * emptiness_w
		monotonicity_wd = monotonicity * monotonicity_w

		# Add them to the score.
		score += sum
		score += smoothness
		score += emptiness_wd
		score += monotonicity_wd

		return score

	# expectiminimax

	def maximize(self, in_grid, depth=0):
		best_score = float("-inf")
		best_move = None

		# Make a move
		available_moves = in_grid.getAvailableMoves()
		for i in range(len(available_moves)):
			move = available_moves[i][0]
			moved_board = in_grid.clone()
			moved_board.move(move)
			score = self.minimize(moved_board,depth+1)

			# Alpha-Beta Pruning
			if score >= best_score:
				best_score = score
				best_move = move

		return best_move, best_score

	def minimize(self, in_grid, depth):

		available_cells = in_grid.getAvailableCells()
		cells = len(available_cells)

		# Early exit by conditions.
		# These results were achieved by a series of tests.
		if cells >= 6 and depth >= 2:
			return self.evaluate(in_grid, cells)

		if cells >= 0 and depth >= 3:
			return self.evaluate(in_grid, cells)

		if cells == 0:
			_, score = self.maximize(in_grid, depth+1)
			return score

		minimized = 0

		# Putting a tile with 2 or 4 in an empty spot.
		for x, y in available_cells:
			for tile in [2, 4]:
				new_grid = in_grid.clone()
				new_grid.map[x][y] = tile
				_, score = self.maximize(new_grid, depth+1)

				if tile == 2:
					score *= 0.9 / cells
				else:
					score *= 0.1 / cells

				minimized += score

		return minimized