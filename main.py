from letter_tree import build_tree_from_file
from board import *
from solver import SolveState

board = Board(15)
rack = ['c', 'a', 't', 's', 'r', 'e']
score, letters_left = board.place_word("cats", (7, 7), 'across', rack)
# print score for cats and the letters left in the rack
print("For cats: ", score, letters_left)
score, letters_left = board.place_word("ears", (6, 8), 'down', rack)
# print score for ears and the letters left in the rack
print("For ears: ", score, letters_left)
score, letters_left = board.place_word("tea", (1, 1), 'down', rack)
# print score for off and the letters left in the rack
print("For tea: ", score, letters_left)
lexicon_tree = build_tree_from_file("lexicon/lexicon_basic.txt")
solver = SolveState(lexicon_tree, board, rack)
solver.find_all_options()
print(board, end='\n\n')
print("Legal moves:")
for move in solver.found_moves:
    print(move)
board.visualize("assets/scoring_board_test.png")
