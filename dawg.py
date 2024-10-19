import pickle
from graphviz import Digraph
import os


# Define a node to be stored in DAWG
class Node:
    next_id = 0

    def __init__(self):
        self.is_terminal = False
        self.id = Node.next_id
        Node.next_id += 1
        self.children = {}

    def __str__(self):
        out = [f"Node {self.id}\nChildren:\n"]
        letter_child_dict = self.children.items()
        for letter, child in letter_child_dict:
            out.append(f" {letter} -> {child.id}\n")
        return " ".join(out)

    def __repr__(self):
        out = []
        if self.is_terminal:
            out.append("1")
        else:
            out.append("0")
        for key, val in self.children.items():
            out.append(key)
            out.append(str(val.id))
        return "_".join(out)

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()


# returns length of common prefix
def length_common_prefix(prev_word, word):
    shared_prefix_length = 0
    for letter1, letter2 in (zip(prev_word, word)):
        if letter1 == letter2:
            shared_prefix_length += 1
        else:
            return shared_prefix_length
    return shared_prefix_length


# minimization function
def minimize(curr_node, common_prefix_length, minimized_nodes, non_minimized_nodes):
    for _ in range(len(non_minimized_nodes), common_prefix_length, -1):
        parent, letter, child = non_minimized_nodes.pop()
        if child in minimized_nodes:
            parent.children[letter] = minimized_nodes[child]
        else:
            minimized_nodes[child] = child
        curr_node = parent
    return curr_node


# function to build dawg from given lexicon
def build_dawg(lexicon):
    root = Node()
    minimized_nodes = {root: root}
    non_minimized_nodes = []
    curr_node = root
    prev_word = ""
    for i, word in enumerate(lexicon):
        common_prefix_length = length_common_prefix(prev_word, word)
        if non_minimized_nodes:
            curr_node = minimize(curr_node, common_prefix_length, minimized_nodes, non_minimized_nodes)
        for letter in word[common_prefix_length:]:
            next_node = Node()
            curr_node.children[letter] = next_node
            non_minimized_nodes.append((curr_node, letter, next_node))
            curr_node = next_node
        curr_node.is_terminal = True
        prev_word = word
    minimize(curr_node, 0, minimized_nodes, non_minimized_nodes)
    return root


def build_dawg_from_file(file_name):
    base_name = os.path.splitext(file_name)[0]
    pickle_file = f"{base_name}.pickle"
    text_file = f"{base_name}.txt"

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as file:
            return pickle.load(file)
    else:
        lexicon = open(text_file, "r").readlines()
        lexicon = [word.strip("\n").upper() for word in lexicon]
        dawg = build_dawg(lexicon)

        # Save the built DAWG as a pickle file
        with open(pickle_file, "wb") as file:
            pickle.dump(dawg, file)

        return dawg


# check if word is in dawg
def is_word_in_dawg(word, curr_node):
    word = word.upper()
    for letter in word:
        if letter in curr_node.children:
            curr_node = curr_node.children[letter]
        else:
            return False
    if curr_node.is_terminal:
        return True
    else:
        return False


def visualize_dawg(dawg, filename="dawg_visualization"):
    dot = Digraph(comment="DAWG Visualization")
    dot.attr(rankdir="LR", dpi="300")
    dot.attr('node', shape='circle', width='0.3', height='0.3', style='filled', color='black', fillcolor='white')

    def add_nodes_edges(node, visited=None):
        if visited is None:
            visited = set()
        if id(node) in visited:
            return
        visited.add(id(node))
        node_id = str(id(node))
        if node.is_terminal:
            dot.node(node_id, shape="doublecircle", fillcolor="lightblue", label="")
        else:
            dot.node(node_id, label="")
        for char, child in node.children.items():
            add_nodes_edges(child, visited)
            dot.edge(node_id, str(id(child)), label=char, fontsize='14', fontweight='bold')

    add_nodes_edges(dawg)
    dot.attr(size='40,40')
    dot.render(filename, view=True, format="png", cleanup=True)


def traverse_dawg(node, visited=None):
    if visited is None:
        visited = set()

    if id(node) in visited:
        return

    visited.add(id(node))
    yield node

    for child in node.children.values():
        yield from traverse_dawg(child, visited)

if __name__ == "__main__":
    file_name = input("Enter the name of the lexicon file (without extension): ")

    # Check for pickle file first
    pickle_file = f"{file_name}.pickle"
    if os.path.exists(pickle_file):
        print(f"Loading DAWG from pickle file: {pickle_file}")
        with open(pickle_file, "rb") as file:
            root = pickle.load(file)

        # Count nodes in the loaded DAWG
        node_count = sum(1 for _ in traverse_dawg(root))
        print(f"Number of nodes in the loaded DAWG: {node_count}")
    else:
        # If pickle file doesn't exist, look for text file
        text_file = f"{file_name}.txt"
        if os.path.exists(text_file):
            print(f"Building DAWG from text file: {text_file}")
            with open(text_file, 'r') as file:
                lexicon = [word.strip().upper() for word in file]
            print(f"Number of words in the lexicon: {len(lexicon)}")

            root = build_dawg(lexicon)

            # Save the built DAWG as a pickle file
            with open(pickle_file, "wb") as file:
                pickle.dump(root, file)
            print(f"DAWG saved as pickle file: {pickle_file}")
        else:
            print(f"Error: Neither {pickle_file} nor {text_file} found.")
            exit(1)


    #visualize the DAWG
    visualize = input("Do you want to visualize the DAWG? (y/n): ").lower()
    if visualize == 'y':
        visualize_dawg(root, f"{file_name}_dawg_visualization")