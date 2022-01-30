from player import Player

# Let a human play the game :)
class InteractivePlayer(Player):
    def __init__(self):
        super().__init__(True)
    def guess_impl(self):
        return input().strip().upper()