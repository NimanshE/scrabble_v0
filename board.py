from dawg import *
import regex as re
import random
import copy
from PIL import Image, ImageDraw, ImageFont


class Square:
    # default behavior is blank square, no score modifier, all cross-checks valid
    def __init__(self, letter=None, modifier="Normal", sentinel=1):
        self.letter = letter
        self.cross_checks_0 = [sentinel] * 26
        self.cross_checks_1 = [sentinel] * 26
        self.cross_checks = self.cross_checks_0
        self.modifier = modifier
        self.visible = True
        if sentinel == 0:
            self.visible = False

    def __str__(self):
        if not self.visible:
            return ""
        if not self.letter:
            return "_"
        else:
            return self.letter

    # maintain two separate cross-check lists depending on if the board is transpose or not
    def check_switch(self, is_transpose):
        if is_transpose:
            self.cross_checks = self.cross_checks_1
        else:
            self.cross_checks = self.cross_checks_0


class ScrabbleBoard:
    def __init__(self):
        self.size = 15
        self.board = [[Square() for _ in range(self.size)] for _ in range(self.size)]
        self.point_dict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4,
                           "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3,
                           "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8,
                           "Y": 8, "Z": 10, "%": 0}
        self.is_transpose = False
        self.upper_cross_check = []
        self.lower_cross_check = []

    def place_word(self, word, row, col, direction):
        if direction == 'across':
            for i, letter in enumerate(word):
                if col + i < self.size:
                    self.board[row][col + i].letter = letter
        elif direction == 'down':
            for i, letter in enumerate(word):
                if row + i < self.size:
                    self.board[row + i][col].letter = letter

    def _transpose(self):
        self.board = [list(row) for row in zip(*self.board)]
        self.is_transpose = not self.is_transpose

    def _update_cross_checks(self):
        while self.upper_cross_check:
            curr_square, lower_letter, lower_row, lower_col = self.upper_cross_check.pop()
            curr_square.check_switch(self.is_transpose)

            chr_val = 65
            for i, ind in enumerate(curr_square.cross_checks):
                if ind == 1:
                    test_node = lower_letter  # Simplified for this context
                    if chr(chr_val) != test_node:
                        curr_square.cross_checks[i] = 0
                chr_val += 1

        while self.lower_cross_check:
            curr_square, upper_letter, upper_row, upper_col = self.lower_cross_check.pop()
            curr_square.check_switch(self.is_transpose)

            chr_val = 65
            for i, ind in enumerate(curr_square.cross_checks):
                if ind == 1:
                    test_node = upper_letter  # Simplified for this context
                    if chr(chr_val) != test_node:
                        curr_square.cross_checks[i] = 0
                chr_val += 1

    def visualize(self, filename='scrabble_board.png'):
        cell_size = 40
        img_size = (self.size + 1) * cell_size  # Increase size to accommodate row and column numbers
        img = Image.new('RGB', (img_size, img_size), color='beige')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Draw the board with letters
        for i in range(self.size):
            for j in range(self.size):
                x, y = (j + 1) * cell_size, (i + 1) * cell_size
                draw.rectangle([x, y, x + cell_size, y + cell_size], outline='black')
                if self.board[i][j].letter:
                    draw.text((x + cell_size // 4, y + cell_size // 4), self.board[i][j].letter.upper(), fill='black', font=font)

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