from letter_tree import build_tree_from_file
from board import *
from solver import SolveState
from game import *
from adversarial_player import AdversarialAIPlayer
from dumb_human_player import DumbHumanPlayer

# ai_player1 = GreedyAIPlayer("Greedy AI")
human_player = DumbHumanPlayer("Human")
ai_player2 = AdversarialAIPlayer("Adversary AI")

game = ScrabbleGame(human_player, ai_player2)
game.start_game()
