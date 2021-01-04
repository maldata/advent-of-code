from enum import Enum


class BorderEdges(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Tile:
    def __init__(self, tile_id, lines):
        self.id = tile_id
        self.lines = lines
        self.border_matches = 0
        self._cemented_pos = None

    @property
    def borders(self):
        """
        Returns a list of four strings (top, right, bottom, left). The order of characters
        in the string is always left-to-right or top-to-bottom.
        """
        top = self.lines[0]
        bottom = self.lines[-1]
        left = ''.join([line[0] for line in self.lines])
        right = ''.join([line[-1] for line in self.lines])
        return [top, right, bottom, left]

    def rotate(self, num_rotations=1):
        """
        Rotate the tile by 90 degrees per rotation.
        """
        if self._cemented_pos is not None:
            print('==> Trying to rotate cemented tile {0} at position {1}'.format(self.id, self._cemented_pos))

        for r in range(num_rotations):
            new_lines = []
            for i in range(len(self.lines)):
                new_line = ''.join([line[i] for line in self.lines])
                new_lines.append(new_line[::-1])
            self.lines = new_lines

    def flip(self):
        """
        Flip along the vertical axis by reversing all strings
        """
        if self._cemented_pos is not None:
            print('==> Trying to flip cemented tile {0} at position {1}'.format(self.id, self._cemented_pos))

        self.lines = [line[::-1] for line in self.lines]

    def cement(self, pos):
        self._cemented_pos = pos

    def num_shared_borders(self, other_tile):
        # We'll assume we put the other tile to the right of this one, rotate four times,
        # flip, and rotate 4 more times. Then rotate the other tile and repeat.
        for other_tile_side in range(4):
            for this_tile_side in range(4):
                if self.borders[BorderEdges.RIGHT.value] == other_tile.borders[BorderEdges.LEFT.value]:
                    self.border_matches = self.border_matches + 1
                self.rotate()

            self.flip()

            for this_tile_side in range(4):
                if self.borders[BorderEdges.RIGHT.value] == other_tile.borders[BorderEdges.LEFT.value]:
                    self.border_matches = self.border_matches + 1
                self.rotate()

            # Rotate the other one, but don't flip it (only need to flip one of the two)
            other_tile.rotate()
