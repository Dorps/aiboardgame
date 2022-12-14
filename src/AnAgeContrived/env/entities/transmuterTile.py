class TransmuterTile:
    def __init__(self, top_size, bottom_size):
        self.top = [0, 0]  # put a max of 2 energies on top
        self.bottom = [0, 0]  # put a max of 2 energies on bottom
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.available_top_positions = top_size
        self.available_bottom_positions = bottom_size

    # fill the energy at the given position: position: 1 == top, position: 2 == bottom
    def fillTile(self, energy, position):
        if position > 2 or position < 1:
            print(
                'Position is wrong. Please enter a correct position between [1, 2]')
        elif position == 1:
            if self.top_size == 0:
                return print('No tile at the top')
            elif self.top_size == 1:
                if self.top[0] != 0:
                    return print('Tile already contains energy. Cannot fill this position')
                else:
                    self.top[0] = energy
            elif self.top_size == 2:
                if self.top[0] != 0:
                    if self.top[1] != 0:
                        return print('Tile already contains energy. Cannot fill this position')
                    else:
                        self.top[1] = energy
                else:
                    self.top[0] = energy
        elif position == 2:
            if self.bottom_size == 0:
                return print('No tile at the bottom')
            elif self.bottom_size == 1:
                if self.bottom[0] != 0:
                    return print('Tile already contains energy. Cannot fill this position')
                else:
                    self.bottom[0] = energy
            elif self.bottom_size == 2:
                if self.bottom[0] != 0:
                    if self.bottom[1] != 0:
                        return print('Tile already contains energy. Cannot fill this position')
                    else:
                        self.bottom[1] = energy
                else:
                    self.bottom[0] = energy

    def emptyTile(self):
        self.top = [0, 0]
        self.bottom = [0, 0]

    # have getter and setter methods for available positions

    def printTile(self):
        tile_string = ''
        tile_string += '---------------\n'
        tile_string += '|             |\n'
        if self.top_size == 0:
            tile_string += '|             |\n'
            tile_string += '|             |\n'
            tile_string += '|             |\n'
        elif self.top_size == 1:
            tile_string += '|     ---     |\n'
            tile_string += '|    | {} |    |\n'.format(self.top[0])
            tile_string += '|     ---     |\n'
        elif self.top_size == 2:
            tile_string += '|  ---   ---  |\n'
            tile_string += '| | {} | | {} | |\n'.format(
                self.bottom[0], self.bottom[1])
            tile_string += '|  ---   ---  |\n'
        tile_string += '|             |\n'
        tile_string += '|             |\n'
        if self.bottom_size == 0:
            tile_string += '|             |\n'
            tile_string += '|             |\n'
            tile_string += '|             |\n'
        elif self.bottom_size == 1:
            tile_string += '|     ---     |\n'
            tile_string += '|    | {} |    |\n'.format(self.top[0])
            tile_string += '|     ---     |\n'
        elif self.bottom_size == 2:
            tile_string += '|  ---   ---  |'
            tile_string += '| | {} | | {} | |\n'.format(
                self.bottom[0], self.bottom[1])
            tile_string += '|  ---   ---  |\n'
        tile_string += '|             |\n'
        tile_string += '---------------\n'

        return (
            tile_string
        ).format().splitlines()
