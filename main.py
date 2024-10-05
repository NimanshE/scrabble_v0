from dawg import *

lexicon_file = 'lexicon_ref.txt'

dawg = build_dawg_from_file(lexicon_file)

# check sample words to see if they are in the dawg

checklist = ["eats", "sleeps", "pants", "dog"]

for word in checklist:
    if is_word_in_dawg(word, dawg):
        print(f"{word} is in the lexicon")
    else:
        print(f"{word} is not in the lexicon")