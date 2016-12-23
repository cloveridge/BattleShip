from board import Board


class Player:
    """A player in the game.

    Each player has a name, wins, and a game board they own.
    """
    name = ""
    wins = 0

    def __init__(self, size, letters):
        self.set_name()
        self.wins = 0
        self.board = Board(size, letters)

    def set_name(self):
        """Sets the player's name"""
        while True:
            self.name = input("What is your name?\n>").capitalize()
            if self.name != "":
                break
        print("Welcome, Admiral {}!".format(self.name))
        input("[Press Enter]")

    def win(self):
        """Adds a win to the player's count"""
        self.wins += 1
