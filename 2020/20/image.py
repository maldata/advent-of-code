from tile import BorderEdges


class Image:
    def __init__(self, tiles):
        self.tiles = tiles
        self.placed_tiles = {}
        self._tiles_per_side = 12

        # These are lists separating the tiles into groups based on
        # how many sides they share with other tiles.
        self._centers = []
        self._sides = []
        self._corners = []

        # This is a big-ass dictionary that maps border strings to tile IDs
        self._edge_lookup = {}
        self._populate_num_shared_borders()

    def _populate_num_shared_borders(self):
        """
        Create a list of all the tile IDs. Take each one in the list and compare it
        to all the other ones.
        """
        all_tile_ids = list(self.tiles)
        for target_tile_id in all_tile_ids:
            target_tile = self.tiles[target_tile_id]

            # Run through all the other tiles. Note that Tile::num_shared_borders()
            # will populate the number of shared sides of the one that calls it,
            # not the one that is used as the argument.
            for comparison_id in all_tile_ids:
                if comparison_id != target_tile_id:
                    comp_tile = self.tiles[comparison_id]
                    target_tile.num_shared_borders(comp_tile)

            # Based on the number of border matches, classify the tile as center/side/corner
            if target_tile.border_matches == 4:
                self._centers.append(target_tile_id)
            elif target_tile.border_matches == 3:
                self._sides.append(target_tile_id)
            elif target_tile.border_matches == 2:
                self._corners.append(target_tile_id)
            else:
                print('Oh no! Tile ID {0} has {1} border matches!'.format(target_tile_id, target_tile.border_matches))

            # As long as we're at it, let's take the four borders of this tile
            # (and the reverse of each) and use them as keys in the edge lookup dictionary.
            for b in target_tile.borders:
                b_rev = b[::-1]
                if b in self._edge_lookup:
                    self._edge_lookup[b].append(target_tile_id)
                    self._edge_lookup[b_rev].append(target_tile_id)
                else:
                    self._edge_lookup[b] = [target_tile_id]
                    self._edge_lookup[b_rev] = [target_tile_id]

    def place_tiles(self):
        # Pick a corner tile arbitrarily. Orient it to sit in the top left corner. That is,
        # the edge strings that only exist on this tile need to be on the top & left of the tile.
        arbitrary_corner_id = self._corners[0]
        arbitrary_corner = self.tiles[arbitrary_corner_id]
        while True:
            top_border_str = arbitrary_corner.borders[BorderEdges.TOP.value]
            left_border_str = arbitrary_corner.borders[BorderEdges.LEFT.value]
            tiles_with_top_str = self._edge_lookup[top_border_str]
            tiles_with_left_str = self._edge_lookup[left_border_str]

            if len(tiles_with_top_str) == 1 and len(tiles_with_left_str) == 1:
                break
            else:
                arbitrary_corner.rotate(1)

        # i will be our row index, j will be our column index. So we go left to right, top to bottom.
        for i in range(self._tiles_per_side):
            for j in range(self._tiles_per_side):
                if i == 0 and j == 0:
                    # We already got this one set up correctly, so just set it
                    self.placed_tiles[(i, j)] = arbitrary_corner_id
                elif j == 0:
                    # If it's the first tile in a row (other than (0, 0)), use the one above
                    # it to identify the tile, then orient to match the tile above
                    tile_above_id = self.placed_tiles[(i - 1, j)]
                    tile_above = self.tiles[tile_above_id]

                    # bottom string of above tile... this is what we search for
                    target_border_str = tile_above.borders[BorderEdges.BOTTOM.value]
                    print('Tile above {0} has bottom border {1}'.format(tile_above_id, target_border_str))

                    # Get all tiles with that string
                    matching_tile_ids = self._edge_lookup[target_border_str]
                    print('Tiles with that string: {0}'.format(matching_tile_ids))

                    # Filter the tile above out of the list of matching tiles
                    matching_tile_id = filter(lambda x: x != tile_above_id, matching_tile_ids)
                    matching_tile_id = list(matching_tile_id)[0]
                    print('Picked {0}'.format(matching_tile_id))

                    # So now we have the tile ID that goes in this position
                    matching_tile = self.tiles[matching_tile_id]

                    # Orient it so the edge that doesn't match anything is on the left
                    while True:
                        left_border_str = matching_tile.borders[BorderEdges.LEFT.value]
                        tiles_with_left_str = self._edge_lookup[left_border_str]
                        if len(tiles_with_left_str) == 1:
                            break
                        else:
                            matching_tile.rotate()

                    # Now you still might need to flip it, if the top edge of the new tile
                    # is backward relative to the tile above. If so, we flip it along the
                    # vertical axis, putting the outer edge on the inside, then rotate twice.
                    if matching_tile.borders[BorderEdges.TOP.value] != target_border_str:
                        matching_tile.flip()
                        matching_tile.rotate(2)

                    self.placed_tiles[(i, j)] = matching_tile_id
                else:
                    # For everything else, align it with the one on the left
                    left_tile_id = self.placed_tiles[(i, j - 1)]
                    left_tile = self.tiles[left_tile_id]

                    # right string of left tile
                    target_border_str = left_tile.borders[BorderEdges.RIGHT.value]

                    # Get all tiles with that string
                    matching_tile_ids = self._edge_lookup[target_border_str]

                    # Filter the tile above out of the list of matching tiles
                    matching_tile_id = filter(lambda x: x != left_tile_id, matching_tile_ids)
                    matching_tile_id = list(matching_tile_id)[0]

                    # So now we have the tile ID that goes in this position
                    matching_tile = self.tiles[matching_tile_id]

                    # Orient it so the target_border_str is on the left
                    while True:
                        if matching_tile.borders[BorderEdges.LEFT.value] == target_border_str:
                            break
                        elif matching_tile.borders[BorderEdges.LEFT.value][::-1] == target_border_str:
                            matching_tile.flip()
                            matching_tile.rotate(2)
                            break
                        else:
                            matching_tile.rotate()

                    self.placed_tiles[(i, j)] = matching_tile_id

    def print_with_borders(self):
        square_size = 12
        num_lines = 10
        for i in range(square_size):
            for k in range(num_lines):
                full_line = ''
                for j in range(square_size):
                    tile_id = self.placed_tiles[(i, j)]
                    tile = self.tiles[tile_id]
                    full_line = full_line + tile.lines[k] + ' '
                print(full_line)
            print()