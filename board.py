from enum import Enum
from PIL import Image, ImageDraw, ImageFont
from dawg import *


class Modifier(Enum):
    NORMAL = ("Normal", "white")
    DOUBLE_LETTER = ("2LS", "cyan")
    TRIPLE_LETTER = ("3LS", "blue")
    DOUBLE_WORD = ("2WS", "pink")
    TRIPLE_WORD = ("3WS", "red")


class Square:

    def __init__(self, letter=None, modifier=Modifier.NORMAL):
        self.letter = letter
        self.modifier = modifier
        self.across_cross_check = list("abcdefghijklmnopqrstuvwxyz")
        self.down_cross_check = list("abcdefghijklmnopqrstuvwxyz")

    def __str__(self):
        if not self.letter:
            return "_"
        else:
            return self.letter


class ScrabbleBoard:
    points_dict = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
                   'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
                   'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
                   'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}


    def __init__(self, dawg_root):
        self.size = 15
        self.board = [[Square() for _ in range(self.size)] for _ in range(self.size)]
        self._setup_board()
        self.dawg_root = dawg_root

    def _setup_board(self):
        # Set up triple word squares
        for i, j in [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]:
            self.board[i][j].modifier = Modifier.TRIPLE_WORD

        # Set up double word squares
        for i, j in [(1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10),
                     (13, 1), (12, 2), (11, 3), (10, 4), (13, 13), (12, 12), (11, 11), (10, 10)]:
            self.board[i][j].modifier = Modifier.DOUBLE_WORD

        # Set up triple letter squares
        for i, j in [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5),
                     (13, 9)]:
            self.board[i][j].modifier = Modifier.TRIPLE_LETTER

        # Set up double letter squares
        for i, j in [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14),
                     (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11),
                     (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14),
                     (12, 6), (12, 8), (14, 3), (14, 11)]:
            self.board[i][j].modifier = Modifier.DOUBLE_LETTER

    def place_word(self, word, row, col, direction):
        word = word.upper()

        if direction not in ['across', 'down']:
            raise ValueError("Direction must be 'across' or 'down'")

        if direction == 'across':
            if col + len(word) > self.size:
                raise ValueError("Word doesn't fit on the board")
            for i, letter in enumerate(word):
                self.board[row][col + i].letter = letter
        else:  # down
            if row + len(word) > self.size:
                raise ValueError("Word doesn't fit on the board")
            for i, letter in enumerate(word):
                self.board[row + i][col].letter = letter

    def naive_score(self, word, row, col, direction):
        word = word.upper()

        score = 0
        word_multiplier = 1
        for i, letter in enumerate(word):
            square = self.board[row + i][col] if direction == 'down' else self.board[row][col + i]
            letter_multiplier = 1
            if square.modifier == Modifier.DOUBLE_LETTER:
                letter_multiplier = 2
            elif square.modifier == Modifier.TRIPLE_LETTER:
                letter_multiplier = 3
            elif square.modifier == Modifier.DOUBLE_WORD:
                word_multiplier *= 2
            elif square.modifier == Modifier.TRIPLE_WORD:
                word_multiplier *= 3
            score += self.points_dict[letter] * letter_multiplier
        return score * word_multiplier

    def get_anchor_squares(self):
        anchor_squares = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].letter is None:
                    # Check adjacent squares
                    adjacent = [
                        (i - 1, j), (i + 1, j),  # Up and down
                        (i, j - 1), (i, j + 1)  # Left and right
                    ]
                    for adj_i, adj_j in adjacent:
                        if 0 <= adj_i < self.size and 0 <= adj_j < self.size:
                            if self.board[adj_i][adj_j].letter is not None:
                                anchor_squares.append((i, j))
                                break
        return anchor_squares

    def update_cross_checks(self):
        def get_valid_letters(prefix, suffix, direction):
            valid_letters = []
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                word = prefix + letter + suffix
                if is_word_in_dawg(word, self.dawg_root):
                    valid_letters.append(letter)
            return valid_letters

        def update_direction(i, j, direction):
            if direction == 'across':
                prefix = ''.join([self.board[i][k].letter for k in range(j) if self.board[i][k].letter])
                suffix = ''.join([self.board[i][k].letter for k in range(j + 1, self.size) if self.board[i][k].letter])
                self.board[i][j].across_cross_check = get_valid_letters(prefix, suffix, 'across')
            else:  # down
                prefix = ''.join([self.board[k][j].letter for k in range(i) if self.board[k][j].letter])
                suffix = ''.join([self.board[k][j].letter for k in range(i + 1, self.size) if self.board[k][j].letter])
                self.board[i][j].down_cross_check = get_valid_letters(prefix, suffix, 'down')

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].letter is None:
                    update_direction(i, j, 'across')
                    update_direction(i, j, 'down')

    def visualize(self, filename='scrabble_board.png'):
        cell_size = 40
        img_size = (self.size + 1) * cell_size
        img = Image.new('RGB', (img_size, img_size), color='beige')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        for i in range(self.size):
            for j in range(self.size):
                x, y = (j + 1) * cell_size, (i + 1) * cell_size
                square = self.board[i][j]

                # Draw modifier circle
                if square.modifier != Modifier.NORMAL:
                    draw.ellipse([x + 5, y + 5, x + cell_size - 5, y + cell_size - 5],
                                 fill=square.modifier.value[1])

                # Draw cell border
                draw.rectangle([x, y, x + cell_size, y + cell_size], outline='black')

                # Draw letter
                if square.letter:
                    draw.text((x + cell_size // 4, y + cell_size // 4),
                              square.letter.upper(), fill='black', font=font)

        # Draw row numbers
        for i in range(self.size):
            y = (i + 1) * cell_size
            draw.text((cell_size // 4, y + cell_size // 4), str(i), fill='black', font=font)

        # Draw column numbers
        for j in range(self.size):
            x = (j + 1) * cell_size
            draw.text((x + cell_size // 4, cell_size // 4), str(j), fill='black', font=font)

        img.save(filename)
        print(f"Board saved to '{filename}'")


# Example usage
if __name__ == "__main__":
    lexicon_type = "lexicon/lexicon_ref"

    dawg_root = build_dawg_from_file(lexicon_type)

    board = ScrabbleBoard(dawg_root)
    cats_points = board.naive_score("cats", 7, 7, "across")
    board.place_word("cats", 7, 7, "across")
    print(f"Score for 'cats': {cats_points}")

    ears_points = board.naive_score("ears", 6, 8, "down")
    board.place_word("ears", 6, 8, "down")
    print(f"Score for 'ears': {ears_points}")

    # print the anchor squares
    anchor_squares = board.get_anchor_squares()
    print(f"Anchor squares: {anchor_squares}")

    # print the cross checks for the anchor squares before updating
    for i, j in anchor_squares:
        print(f"({i}, {j}): across: {board.board[i][j].across_cross_check}, down: {board.board[i][j].down_cross_check}")

    # update the cross checks
    board.update_cross_checks()

    # print the cross checks for the anchor squares after updating
    for i, j in anchor_squares:
        print(f"({i}, {j}): across: {board.board[i][j].across_cross_check}, down: {board.board[i][j].down_cross_check}")

    board.visualize(filename="script_viz.png")