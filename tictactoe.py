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

	def __str__(self):
		map = { None: ".", 'X': "X", 'O': "O" }
		row1 = " | ".join(map[c] for c in self.cells[0:3])
		row2 = " | ".join(map[c] for c in self.cells[3:6])
		row3 = " | ".join(map[c] for c in self.cells[6:9])
		board = " %s \n-----------\n %s \n-----------\n %s " % (row1, row2, row3)
		return board

	def __repr__(self):
		pieces = [str(c) for c in self.cells]
		return "".join(pieces)

	def set_cell(self, x, y, piece):
		"""
		Set the cell at x, y (0-indexed from top left) to the indicated piece.
		Piece should be an "X" or "O" character or None. 
		"""
		self.cells[x + y * 3] = piece

	def get_cell(self, x, y):
		"""Return contents of the indicated cell"""
		try:
			return self.cells[x + y * 3]
		except IndexError:
			raise IndexError, "Out of range: %s %s" % (x, y)

	def winner(self):
		"""
		Determine the winner if any. Return "X", "O", or None.
		"""
		# stubbed -- detects full board
		return all(self.cells)

	def let_computer_move(self):
		"""
		Make next move.
		"""
		# stubbed -- random
		x, y = 1, 1
		while self.get_cell(x, y) is not None:
			x, y = random.randint(0, 2), random.randint(0, 2)
		self.set_cell(x, y, "O")

	def let_human_move(self):
		"""Ask human where it wants to move, and make the change."""
		legal_move = False
		while not legal_move:
			try:
				move = int(raw_input("Your move (1-9)? ")) - 1
				y = move / 3
				x = move % 3
				if self.get_cell(x, y):
					raise ValueError
				self.set_cell(x, y, "X")
				legal_move = True
			except ValueError:
				print "Already a piece there."
			except IndexError:
				print "No such square."

	def play(self):
		"""Play a game."""
		while not self.winner():
			print self
			self.let_human_move()
			self.let_computer_move()

def play():
	"""Play the game, interactively."""
	board = Board()
	board.play()


if __name__ == "__main__":
	play()