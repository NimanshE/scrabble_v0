class LetterTreeNode:
    def __init__(self, is_word):
        self.is_word = is_word
        self.children = dict()

class LetterTree:
    def __init__(self, words):
        self.root = LetterTreeNode(False)
        for word in words:
            current_node = self.root
            for letter in word:
                if letter not in current_node.children.keys():
                    current_node.children[letter] = LetterTreeNode(False)
                current_node = current_node.children[letter]
            current_node.is_word = True

    def lookup(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node.children.keys():
                return None
            current_node = current_node.children[letter]
        return current_node

    def is_word(self, word):
        word_node = self.lookup(word)
        if word_node is None:
            return False
        return word_node.is_word

def build_tree_from_file(file_name = 'lexicon/lexicon_basic.txt'):
    with open(file_name, 'rt') as file:
        words = []
        for line in file:
            word = line.strip()
            words.append(word)
    return LetterTree(words)
