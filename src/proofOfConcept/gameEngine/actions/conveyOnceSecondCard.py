from gameEngine.command import Command
from gameEngine.convey import Convey

class ConveyOnceSecondCard(Command):

    def __init__(self, player, board):
        super().__init__(player, board)

    def execute(self):
        Convey.convey(self.player.transmuter, 1, 1)