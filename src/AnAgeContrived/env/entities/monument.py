from env.entities.monumentTile import MonumentTile

class Monument:
    def __init__(self, name, monumentTiles):
        self.name = name
        self.tiles = monumentTiles # list of MonumentTile objects
        self.completed_tiles = [] # list of completed MonumentTile objects

    def isCompleted(self):
        return len(self.tiles) == 0 # if there are no tiles left, the monument is completed

    def getTopTile(self):
        return self.tiles[len(self.tiles)-1] # returns the top tile