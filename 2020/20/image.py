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

        # y will be our row index (positive down), and x will be our
        # column index (positive right). So we go left to right, top to bottom.
        for y in range(self._tiles_per_side):
            for x in range(self._tiles_per_side):
                if x == 0 and y == 0:
                    # We already got this one set up correctly, so just set it
                    self.placed_tiles[(x, y)] = arbitrary_corner_id
                    arbitrary_corner.cement((x, y))
                elif x == 0:
                    # If it's the first tile in a row (other than (0, 0)), use the one above
                    # it to identify the tile, then orient to match the tile above
                    tile_above_id = self.placed_tiles[(x, y - 1)]
                    tile_above = self.tiles[tile_above_id]

                    # bottom string of above tile... this is what we search for
                    target_border_str = tile_above.borders[BorderEdges.BOTTOM.value]
                    print('Tile above ({0}) has bottom border {1}'.format(tile_above_id, target_border_str))

                    # Get all tiles with that string
                    matching_tile_ids = self._edge_lookup[target_border_str]
                    print('Tiles with that string: {0}'.format(matching_tile_ids))

                    # Filter the tile above out of the list of matching tiles
                    matching_tile_id = filter(lambda t: t != tile_above_id, matching_tile_ids)
                    matching_tile_id = list(matching_tile_id)[0]
                    print('Picked {0}'.format(matching_tile_id))

                    # So now we have the tile ID that goes in this position
                    matching_tile = self.tiles[matching_tile_id]

                    # Orient it to match the tile above
                    oriented_ok = matching_tile.orient_edge(target_border_str, BorderEdges.TOP)
                    if not oriented_ok:
                        print('Was not able to orient tile {0} so that string {1} was on top.'.format(matching_tile_id, target_border_str))
                        return
                    
                    self.placed_tiles[(x, y)] = matching_tile_id
                    matching_tile.cement((x, y))
                else:
                    # For everything else, align it with the one on the left
                    left_tile_id = self.placed_tiles[(x - 1, y)]
                    left_tile = self.tiles[left_tile_id]

                    # right string of left tile
                    target_border_str = left_tile.borders[BorderEdges.RIGHT.value]

                    # Get all tiles with that string
                    matching_tile_ids = self._edge_lookup[target_border_str]

                    # Filter the tile above out of the list of matching tiles
                    matching_tile_id = filter(lambda t: t != left_tile_id, matching_tile_ids)
                    matching_tile_id_list = list(matching_tile_id)
                    if len(matching_tile_id_list) > 2:
                        print('Uh oh. Target string {0} is available in {1} tiles.'.format(target_border_str, len(matching_tile_id_list)))
                    matching_tile_id = matching_tile_id_list[0]

                    # So now we have the tile ID that goes in this position
                    matching_tile = self.tiles[matching_tile_id]

                    # Orient it so the target_border_str is on the left
                    oriented_ok = matching_tile.orient_edge(target_border_str, BorderEdges.LEFT)
                    if not oriented_ok:
                        print('Was not able to orient tile {0} so that string {1} was on the left.'.format(matching_tile_id, target_border_str))
                        return
                    
                    self.placed_tiles[(x, y)] = matching_tile_id
                    matching_tile.cement((x, y))

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
