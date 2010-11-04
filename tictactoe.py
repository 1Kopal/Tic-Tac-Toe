#!/usr/bin/env python
"""
Interactive Tic-Tac-Toe
Paul Bissex, October 2010
More info: http://github.com/cmheisel/Tic-Tac-Toe
"""
import copy
import optparse
import random

class Board(object):
	"""A Tic-Tac-Toe board."""

	def __init__(self):
		self.hpiece = "X"
		self.cpiece = "O"
		self.clear()

	def __str__(self):
		piece_chars = { None: ".", 'X': "X", 'O': "O" }
		row1 = " | ".join(piece_chars[c] for c in self.cells[0:3])
		row2 = " | ".join(piece_chars[c] for c in self.cells[3:6])
		row3 = " | ".join(piece_chars[c] for c in self.cells[6:9])
		board = " %s \n-----------\n %s \n-----------\n %s " % (row1, row2, row3)
		return board

	def __repr__(self):
		pieces = [str(c) for c in self.cells]
		return "".join(pieces)

	def clear(self):
		"""Set the board to a blank state."""
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

	def cell_empty(self, x, y):
		"""Is the cell empty?"""
		return self.get_cell(x, y) == None

	def winner(self):
		"""Determine the winner if any. Return "X", "O", or None."""
		# If less than 5 moves have been made, there's no winner
		if self.cells.count(None) >= 5:
			return None
		# Winning board states represented as bitmasks
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
					return piece  # We have a winner!

	def finished(self):
		"""
		Is board full, or is there a winner?
		"""
		return self.winner() or all(self.cells)

	def winning_moves(self, piece):
		"""
		Return a winning move for the given piece if possible, or Return None, None
		"""
		moves = []
		for x, y in self.possible_moves():
			self.set_cell(x, y, piece)
			if self.winner() == piece:
				moves.append((x, y))
			# Undo the tested move
			self.set_cell(x, y, None)
			
		return moves

	def fork_move(self, piece):
		"""
		Return a move which would create a "fork", i.e. two possible winning moves
		for the given piece.
		"""
		for x, y in self.possible_moves():
			self.set_cell(x, y, piece)
			if len(self.winning_moves(piece)) >= 2:
				return x, y
			# Undo the tested move
			self.set_cell(x, y, None)
		
	def possible_moves(self):
		"""
		A list of all possible current moves, in (x, y) form
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
		if self.winning_moves(self.cpiece):
			x, y = random.choice(self.winning_moves(self.cpiece))
			self.set_cell(x, y, self.cpiece)
		# ...or block a win...
		elif self.winning_moves(self.hpiece):
			x, y = random.choice(self.winning_moves(self.hpiece))
			self.set_cell(x, y, self.cpiece)
		# ...or create a fork...
		elif self.fork_move(self.cpiece):
			x, y = self.fork_move(self.cpiece)
			self.set_cell(x, y, self.cpiece)
		# ...or block a human fork...
		elif self.fork_move(self.hpiece):
			x, y = self.fork_move(self.hpiece)
			self.set_cell(x, y, self.cpiece)
		# ...or take the center...
		elif self.cell_empty(1, 1):
			self.set_cell(1, 1, self.cpiece)
		# ...or move at random.
		else:
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


def play(board):
	"""
	Play the game, interactively.
	"""
	while not board.finished():
		board.play_turn()
	print "\nGAME OVER\n"
	print board
	if board.winner():
		print "\nWinner: %s" % board.winner()
	else:
		print "\nNo winner!"

def test(board, rounds):
	"""
	Test the computer player by brute force. "Human" moves randomly.
	"""
	for i in range(rounds):
 		board.clear()
		while not board.finished():
			# Random "human" move
			x, y = random.choice(board.possible_moves())
			board.set_cell(x, y, board.hpiece)
			# Computer move
			if not board.finished():
				board.computer_move()
		if board.winner() == board.hpiece:
			print "Unauthorized human victory!"
			print board

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("-t", "--test", help="Rounds of brute-force testing to run")
	options, args = parser.parse_args()
	board = Board()
	if options.test:
		test(board, int(options.test))
	else:
		play(board)
		