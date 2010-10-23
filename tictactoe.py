"""
Interactive Tic-Tac-Toe
Paul Bissex, October 2010
More info: http://github.com/cmheisel/Tic-Tac-Toe
"""
import random

class Board(object):
	"""A Tic-Tac-Toe board."""
	piece_chars = { None: ".", 'X': "X", 'O': "O" }

	def __init__(self):
		self.cells = [None] * 9

	def __str__(self):
		row1 = " | ".join(self.piece_chars[c] for c in self.cells[0:3])
		row2 = " | ".join(self.piece_chars[c] for c in self.cells[3:6])
		row3 = " | ".join(self.piece_chars[c] for c in self.cells[6:9])
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
		return self.cells[x + y * 3]

	def winner(self):
		"""
		Determine the winner if any. Return "X", "O", or None.
		"""
		# Winning board states represented as bitmasks
		winner = None
		winning_bitstrings = [
			"111000000", "000111000", "000000111", 
			"100100100", "010010010", "001001001", 
			"100010001", "001010100"]
		pieces = "XO"
		for piece in pieces:
			other_piece = pieces[1 - pieces.find(piece)]
			bitmask_map = { None: "0", piece: "1", other_piece: "0"}
			board_bitstring = "".join(bitmask_map[c] for c in self.cells)
			board_bitvalue = int(board_bitstring, 2)
			for winning_bitstring in winning_bitstrings:
				winning_bitmask = int(winning_bitstring, 2)
				if (board_bitvalue & winning_bitmask) == winning_bitmask:
					winner = piece
		return winner

	def finished(self):
		"""
		Is board full, or is there a winner?
		"""
		return self.winner() or all(self.cells)

	def let_computer_move(self):
		"""
		Make next move.
		"""
		# stubbed -- random
		x, y = random.randint(0, 2), random.randint(0, 2)
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

	def play_turn(self):
		"""
		Play a turn of the game.
		"""
		if not self.finished():
			self.let_human_move()
		if not self.finished():
			self.let_computer_move()


def play():
	"""
	Play the game, interactively.
	"""
	board = Board()
	while not board.finished():
		print board
		board.play_turn()
	print "\nGAME OVER"
	print board
	if board.winner():
		print "Winner: %s" % board.winner()
	else:
		print "No winner!"


if __name__ == "__main__":
	play()