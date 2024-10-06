from dawg import *
from board import *
import os

lexicon_type = "lexicon/lexicon_ref"

pickle_file = f"{lexicon_type}.pickle"
lexicon_file = f"{lexicon_type}.txt"

if os.path.exists(pickle_file):
    try:
        with open(pickle_file, "rb") as to_load:
            dawg = pickle.load(to_load)
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        dawg = build_dawg_from_file(lexicon_file)
else:
    if os.path.exists(lexicon_file):
        dawg = build_dawg_from_file(lexicon_file)
    else:
        raise FileNotFoundError(f"Neither {pickle_file} nor {lexicon_file} exists.")

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