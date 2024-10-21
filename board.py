class Board:
    def __init__(self, size):
        self.size = size
        self._tiles = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(None)
            self._tiles.append(row)

    def __str__(self):
        return '\n'.join(''.join(x if x is not None else '_' for x in row) for row in self._tiles)

    def all_positions(self):
        result = []
        for row in range(self.size):
            for col in range(self.size):
                result.append((row, col))
        return result

    def get_tile(self, pos):
        row, col = pos
        return self._tiles[row][col]

    def set_tile(self, pos, tile):
        row, col = pos
        self._tiles[row][col] = tile

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

def sample_board():
    result = Board(7)
    result.place_word("cats", (1, 1), 'across')
    result.place_word("ears", (0, 2), 'down')
    return result

if __name__ == '__main__':
    board = Board(15)
    board.place_word("cats", (7, 7), 'across')
    board.place_word("ears", (6, 8), 'down')
    print(board)
