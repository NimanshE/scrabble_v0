from letter_tree import build_tree_from_file
from board import *
from solver import SolveState
from game import *

ai_player1 = GreedyAIPlayer("Greedy AI 1")
ai_player2 = GreedyAIPlayer("Greedy AI 2")

game = ScrabbleGame(ai_player1, ai_player2)
game.start_game()
