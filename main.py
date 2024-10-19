from board import *
from dawg import *

lexicon_type = "lexicon/lexicon_full"

dawg = build_dawg_from_file(lexicon_type)

# check sample words to see if they are in the dawg
checklist = ["eats", "sleeps", "pants", "dog"]

for word in checklist:
    if is_word_in_dawg(word, dawg):
        print(f"{word} is in the lexicon")
    else:
        print(f"{word} is not in the lexicon")

board = ScrabbleBoard()

# place some words on the board
board.place_word("cats", 7, 7, 'across')
board.place_word("ears", 6, 8, 'down')
board.visualize()

anchor_squares = board.get_anchor_squares()

print(f"Anchor squares: {anchor_squares}")
