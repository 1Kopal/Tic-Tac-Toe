"""
Interactive Tic-Tac-Toe
Paul Bissex, October 2010
More info: http://github.com/cmheisel/Tic-Tac-Toe
"""
import copy
import random

def debug(text):
	print "XXX: %s" % text

class Board(object):
	"""A Tic-Tac-Toe board."""
	piece_chars = { None: ".", 'X': "X", 'O': "O" }

	def __init__(self):
		self.cells = [None] * 9
		self.hpiece = "X"
		self.cpiece = "O"

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

	def cell_empty(self, x, y):
		"""Is the cell empty?"""
		return self.get_cell(x, y) == None

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

	def winning_move(self, piece):
		"""
		Return a winning move for the given piece if possible, or Return None, None
		"""
		possible = self.possible_moves()
		for x, y in possible:
			lookahead = copy.deepcopy(self)
			lookahead.set_cell(x, y, piece)
			if lookahead.winner() == piece:
				return x, y
		
	def possible_moves(self):
		"""
		A list of possible current moves, in (x, y) form
		"""
		open = []
		for x in range(3):
			for y in range(3):
				if self.cell_empty(x, y):
					open.append((x, y))
		return open

	def x_move(self):
		if self.hpiece == "X":
			self.human_move()
		else:
			self.computer_move()

	def o_move(self):
		if self.hpiece == "O":
			self.human_move()
		else:
			self.computer_move()
			
	def human_move(self):
		"""
		Ask the human for a move, and make it.
		"""
		print self
		legal_move = False
		while not legal_move:
			try:
				move = int(raw_input("Your move (1-9)? ")) - 1
				y = move / 3
				x = move % 3
				if self.get_cell(x, y):
					raise ValueError
				self.set_cell(x, y, self.hpiece)
				legal_move = True
			except ValueError:
				print "Already a piece there."
			except IndexError:
				print "No such square."

	def computer_move(self):
		# Win...
		if self.winning_move(self.cpiece):
			debug("found a winning computer move")
			x, y = self.winning_move(self.cpiece)
			self.set_cell(x, y, self.cpiece)
		# ...or block a win...
		elif self.winning_move(self.hpiece):
			debug("found a winning human move")
			x, y = self.winning_move(self.hpiece)
			self.set_cell(x, y, self.cpiece)
		# ...or take the center...
		elif self.cell_empty(1, 1):
			debug("found empty center")
			self.set_cell(1, 1, self.cpiece)
		# ...or just move anywhere.
		else:
			debug("random move")
			x, y = random.choice(self.possible_moves())
			self.set_cell(x, y, self.cpiece)

	def play_turn(self):
		"""
		Play a turn of the game.
		"""
		if not self.finished():
			self.x_move()
		if not self.finished():
			self.o_move()


def play():
	"""
	Play the game, interactively.
	"""
	board = Board()
	while not board.finished():
		board.play_turn()
	print "\nGAME OVER\n"
	print board
	if board.winner():
		print "\nWinner: %s" % board.winner()
	else:
		print "\nNo winner!"


if __name__ == "__main__":
	play()