#!/usr/bin/env python
"""
Interactive Tic-Tac-Toe
Paul Bissex, October 2010
More info: http://github.com/cmheisel/Tic-Tac-Toe
"""
import optparse
import random

class Board(object):
	"""A Tic-Tac-Toe board."""

	def __init__(self):
		self.hpiece = "X"
		self.cpiece = "O"
		self.corner_cells = [(0, 0), (2, 0), (0, 2), (2, 2)]
		self.side_cells = [(1, 0), (0, 1), (2, 1), (1, 2)]
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


	# Board mechanics

	def clear(self):
		"""Set the board to a blank state."""
		self.cells = [None] * 9
		self.moves = []  # instant replay for --test

	def set_cell(self, x, y, piece):
		"""
		Set the cell at x, y (0-indexed from top left) to the indicated piece.
		Piece should be an "X" or "O" character or None. 
		"""
		self.cells[x + y * 3] = piece
		if piece is not None:  # record move for --test
			self.moves.append((piece, 1+x+y*3))

	def get_cell(self, x, y):
		"""Return contents of the indicated cell"""
		return self.cells[x + y * 3]

	def cell_empty(self, x, y):
		"""Is the cell empty?"""
		return self.get_cell(x, y) is None

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

	def finished(self):
		"""Is the board full, or is there a winner?"""
		return self.winner() or all(self.cells)

	def winner(self):
		"""Determine the winner if any. Return "X", "O", or None."""
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


	# Computer tactics

	def winning_moves(self, piece):
		"""
		Return a winning move for the given piece if possible, or return empty list
		"""
		moves = []
		for x, y in self.possible_moves():
			self.set_cell(x, y, piece)
			if self.winner() == piece:
				moves.append((x, y))
			# Undo the tested move
			self.set_cell(x, y, None)
			self.moves = self.moves[:-1]  # clean up list for --test
		return moves
		
	def opposite_corner(self, x, y):
		"""Return the cell coordinates diagonally opposite the given cell."""
		if (x, y) in self.corner_cells:
			opp_x = 2 - x
			opp_y = 2 - y
		return opp_x, opp_y

	def empty_corners(self, opposite=None):
		"""
		Which corner squares are empty? If "opposite" is provided ("X" or "O"), 
		look for open corner cells opposite that piece.
		"""
		empty = [cell for cell in self.corner_cells if self.cell_empty(*cell)]
		if opposite:
			empty_opposite = []
			for x, y in empty:
				if self.get_cell(*self.opposite_corner(x, y)) == opposite:
					empty_opposite.append((x, y))
			return empty_opposite
		else:
			return empty
		
	def empty_sides(self):
		"""Which side squares are empty?"""
		empty = [cell for cell in self.side_cells if self.cell_empty(*cell)]
		return empty
		
	def tucked_corner(self, piece):
		"""Find an open corner "tucked" between two pieces on adjacent sides"""
		top = self.get_cell(*self.side_cells[0]) == piece
		left = self.get_cell(*self.side_cells[1]) == piece
		right = self.get_cell(*self.side_cells[2]) == piece
		bottom = self.get_cell(*self.side_cells[3]) == piece
		if top and left and self.cell_empty(0, 0):
			return 0, 0
		if top and right and self.cell_empty(2, 0):
			return 2, 0
		if bottom and left and self.cell_empty(0, 2):
			return 0, 2
		if bottom and right and self.cell_empty(2, 2):
			return 2, 2
			
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

	def computer_move(self):
		# Win...
		if self.winning_moves(self.cpiece):
			x, y = random.choice(self.winning_moves(self.cpiece))
			self.set_cell(x, y, self.cpiece)
		# ...or block a win...
		elif self.winning_moves(self.hpiece):
			x, y = random.choice(self.winning_moves(self.hpiece))
			self.set_cell(x, y, self.cpiece)
		# ...or take the center...
		elif self.cell_empty(1, 1):
			self.set_cell(1, 1, self.cpiece)
		# ...or foil a possible fork...
		elif len([c for c in self.corner_cells if self.get_cell(*c) == self.hpiece]) > 1:
			x, y = random.choice(self.empty_sides())
			self.set_cell(x, y, self.cpiece)
		# ...or take a corner: 
		# 1. between two human pieces on sides ("tucked") or
		# 2. opposite human piece in corner or
		# 3. randomly
		elif self.empty_corners():
			if self.tucked_corner(self.hpiece):
				x, y = self.tucked_corner(self.hpiece)
			elif self.empty_corners(opposite=self.hpiece):
				x, y = random.choice(self.empty_corners(opposite=self.hpiece))
			else:
				x, y = random.choice(self.empty_corners())
			self.set_cell(x, y, self.cpiece)
		# ...or move at random.
		else:
			x, y = random.choice(self.possible_moves())
			self.set_cell(x, y, self.cpiece)


	# Game play
	
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
	wins = { None: 0, "X": 0, "O": 0 }
	for i in range(rounds):
		print "Game %d" % i
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
			print board.moves
		wins[board.winner()] += 1
	print "WINS:", wins

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("-t", "--test", help="Rounds of brute-force testing to run")
	options, args = parser.parse_args()
	board = Board()
	if options.test:
		test(board, int(options.test))
	else:
		play(board)
		