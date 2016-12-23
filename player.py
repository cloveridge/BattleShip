from board import *


class Player:
    name = ""
    wins = 0

    def __init__(self, size, letters):
        self.set_name()
        self.wins = 0
        self.board = Board(size, letters)

    def set_name(self):
        while True:
            self.name = input("What is your name?\n>").capitalize()
            if self.name != "":
                break
        print("Welcome, Admiral {}!".format(self.name))
        input("[Press Enter]")

    def win(self):
        self.wins += 1
