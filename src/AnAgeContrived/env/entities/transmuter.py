from .transmuterTile import TransmuterTile


class Transmuter:
    def __init__(self):

        t1 = TransmuterTile(1, 1)
        t2 = TransmuterTile(1, 1)
        t3 = TransmuterTile(1, 1)
        t4 = TransmuterTile(1, 1)
        t5 = TransmuterTile(2, 1)
        t6 = TransmuterTile(2, 1)
        t7 = TransmuterTile(2, 1)

        t1.fillTile(1, 1)
        t1.fillTile(1, 2)

        t2.fillTile(1, 1)
        t2.fillTile(1, 2)

        t3.fillTile(1, 1)
        t3.fillTile(1, 2)

        self.active_tiles = [t1, t2, t3, t4, t5]
        self.reserved_tiles = [t6, t7]
        self.action_tokens = []
        pass

    # gets all the tiles currently on the transmuter
    def getAllTiles(self):
        pass

    # returns the tile at the given position
    def getTile(self, position):
        pass

    # conveys the transmuter tiles only once, if convey 2 call method twice
    # Upgrade performance here
    def convey(self, reservedTileIndex):
        new_active_tiles = [None, None, None, None, None]
        new_active_tiles[0] = self.reserved_tiles[reservedTileIndex]
        for i in range(len(self.active_tiles)-1):
            new_active_tiles[i+1] = self.active_tiles[i]
        self.active_tiles[4].emptyTile()
        self.reserved_tiles[reservedTileIndex] = self.active_tiles[4]
        self.active_tiles = new_active_tiles

    # helper func to move the tiles after removing a tile

    def _moveAllTilesAhead(self):
        pass

    def isFull(self):
        pass

    def getState(self):
        w, h = 7, 4
        matrix = [[0 for x in range(w)] for y in range(h)]
        for i, tile in enumerate(self.active_tiles):
            matrix[0][i] = tile.top_size
            matrix[1][i] = tile.bottom_size
            matrix[2][i] = tile.top.count(1)
            matrix[3][i] = tile.bottom.count(1)

        for i, tile in enumerate(self.reserved_tiles):
            matrix[0][i+5] = tile.top_size
            matrix[1][i+5] = tile.bottom_size
            matrix[2][i+5] = tile.top.count(1)
            matrix[3][i+5] = tile.bottom.count(1)
        return matrix

    def printTransmuter(self):
        for lines in zip(*map(TransmuterTile.printTile, self.active_tiles)):
            print(*lines)

    def getTotalEnergyCells(self):
        sum = 0
        for tile in self.active_tiles:
            sum += tile.top.count(1)
            sum += tile.bottom.count(1)
        return sum

    def getTotalEmptyCells(self):
        sum = 0
        for tile in self.active_tiles:
            sum += tile.top.count(0)
            sum += tile.bottom.count(0)
        return sum
