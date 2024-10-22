from enum import Enum
from PIL import Image, ImageDraw, ImageFont

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

    def __str__(self):
        if not self.letter:
            return "_"
        else:
            return self.letter

class Board:
    def __init__(self, size):
        self.size = size
        self._tiles = [[Square() for _ in range(self.size)] for _ in range(self.size)]
        self._setup_board()

    def _setup_board(self):
        # Set up triple word squares
        for i, j in [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]:
            self._tiles[i][j].modifier = Modifier.TRIPLE_WORD

        # Set up double word squares
        for i, j in [(1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10),
                     (13, 1), (12, 2), (11, 3), (10, 4), (13, 13), (12, 12), (11, 11), (10, 10)]:
            self._tiles[i][j].modifier = Modifier.DOUBLE_WORD

        # Set up triple letter squares
        for i, j in [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5),
                     (13, 9)]:
            self._tiles[i][j].modifier = Modifier.TRIPLE_LETTER

        # Set up double letter squares
        for i, j in [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14),
                     (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11),
                     (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14),
                     (12, 6), (12, 8), (14, 3), (14, 11)]:
            self._tiles[i][j].modifier = Modifier.DOUBLE_LETTER

    def __str__(self):
        return '\n'.join(''.join(str(tile) for tile in row) for row in self._tiles)

    def all_positions(self):
        result = []
        for row in range(self.size):
            for col in range(self.size):
                result.append((row, col))
        return result

    def get_tile(self, pos):
        row, col = pos
        return self._tiles[row][col].letter

    def set_tile(self, pos, tile):
        row, col = pos
        self._tiles[row][col].letter = tile

    def place_word(self, word, pos, direction):
        row, col = pos
        for letter in word:
            self.set_tile((row, col), letter)
            if direction == 'across':
                col += 1
            else:
                row += 1

    def in_bounds(self, pos):
        row, col = pos
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, pos):
        return self.in_bounds(pos) and self.get_tile(pos) is None

    def is_filled(self, pos):
        return self.in_bounds(pos) and self.get_tile(pos) is not None

    def copy(self):
        result = Board(self.size)
        for pos in self.all_positions():
            result.set_tile(pos, self.get_tile(pos))
        return result

    def visualize(self, filename='scrabble_board.png'):
        cell_size = 40
        img_size = (self.size + 1) * cell_size
        img = Image.new('RGB', (img_size, img_size), color='beige')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        for i in range(self.size):
            for j in range(self.size):
                x, y = (j + 1) * cell_size, (i + 1) * cell_size
                square = self._tiles[i][j]

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

def sample_board():
    result = Board(15)
    result.place_word("cats", (7, 7), 'across')
    result.place_word("ears", (6, 8), 'down')
    result.place_word("off", (1, 1), 'down')
    return result

if __name__ == '__main__':
    board = Board(15)
    board.place_word("cats", (7, 7), 'across')
    board.place_word("ears", (6, 8), 'down')
    board.place_word("off", (1, 1), 'down')
    print(board)
    board.visualize()
