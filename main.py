from letter_tree import *
from board import *
from solver import *

board = Board(15)
board.place_word("cats", (7, 7), 'across')
board.place_word("ears", (6, 8), 'down')
board.place_word("off", (1, 1), 'down')
rack = ['e', 'f', 'f', 'e', 'c', 't']
lexicon_tree = build_tree_from_file("lexicon/lexicon_basic.txt")
solver = SolveState(lexicon_tree, board, rack)
print(board, end='\n\n')
solver.find_all_options()