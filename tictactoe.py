"""
Interactive Tic-Tac-Toe
Paul Bissex, October 2010
More info: http://github.com/cmheisel/Tic-Tac-Toe
"""
import random

class Board(object):
	"""A Tic-Tac-Toe board."""
	
	def __init__(self):
		self.cells = [None] * 9
		
	def set_cell(self, x, y, piece):
		"""
		Set the cell at x, y (0-indexed from top left) to the indicated piece.
		Piece should be an "X" or "O" character or None. 
		"""
		self.cells[x + y * 3] = piece
	
	def get_cell(self, x, y):
		"""Return contents of the indicated cell"""
		return self.cells[x + y * 3]
			
	def __str__(self):
		return str(self.cells)
		
	def winner(self):
		"""Determine the winner -- X or O or None"""
		# XXX stubbed -- it's over when board is full
		if all(self.cells):
			return True

	def best_next_move(self, letter):
		"""X,Y coordinates of the best next move for given letter."""
		# XXX stubbed -- random
		position = (1, 1)
		while self.get_cell(*position) is not None:
			position = (random.randint(0, 3), random.randint(0, 3))
		return position
		
	def let_human_move(self, letter):
		"""Ask human where it wants to move, and make the change."""
		move_string = raw_input("Your move (X Y)? ")
		x, y = int(move_string.split()[0]), int(move_string.split()[1])
		self.set_cell(x, y, letter)
		
	def play(self):
		"""Play a game."""
		while not self.winner():
			self.let_human_move("X")
			print self
			x, y = self.best_next_move("O")
			self.set_cell(x, y, "O")
			print self

def play():
	"""Play the game, interactively."""
	board = Board()
	board.play()

if __name__ == "__main__":
	play()