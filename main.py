from letter_tree import build_tree_from_file
from board import *
from solver import SolveState

board = Board(15)
board.place_word("cats", (7, 7), 'across')
board.place_word("ears", (6, 8), 'down')
board.place_word("off", (1, 1), 'down')
rack = ['e', 'f', 'f', 'e', 'c', 't']
lexicon_tree = build_tree_from_file("lexicon/lexicon_basic.txt")
solver = SolveState(lexicon_tree, board, rack)
solver.find_all_options()
print(board, end='\n\n')
print("Legal moves:")
for move in solver.found_moves:
    print(move)
