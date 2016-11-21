from player import Player
from board import Board
from copy import deepcopy
import re
import os


def cls():
    os.system("clear")

def input_filter(text):
    return re.sub('\s', "", text)

class Game:
    players = []
    SHIP_INFO = [
        #("Aircraft Carrier", 5),
        #("Battleship", 4),
        #("Submarine", 3),
        #("Cruiser", 3),
        ("Patrol Boat", 2)
    ]
    winner = None

    def __init__(self, player_1, player_2):
        self.current_player = player_2
        self.other_player = player_1

        # Set player 1's ships up
        self.place_ships()
        # Set player 2's ships up
        self.place_ships()

        # Run the regular game loop through here.
        while True:
            # Alternate turns
            self.switch_players()

            # Loop until a good guess has been made
            while True:
                cls()
                # Print quiet board for other player
                self.other_player.board.display_quiet_board()
                print("\n" + ("==" * (len(player_1.letters) + 1)) + "\n")

                # Print verbose board for current player
                self.current_player.board.display_full_board()

                print("{}, pick a space to attack!".format(
                    self.current_player.name))
                location = input_filter(input(">")).capitalize()
                if self.other_player.guess(location):
                    break

            # If no ships left, break
            if self.other_player.ship_spaces == 0:
                self.winner = self.current_player
                break
            # Otherwise recap the turn
            else:
                cls()
                print("{}'s turn summary:".format(self.current_player.name))
                # Print quiet board for other player
                self.other_player.board.display_quiet_board()
                print("\n" + ("==" * (len(player_1.letters) + 1)) + "\n")

                # Print verbose board for current player
                self.current_player.board.display_full_board()

    def switch_players(self):
        cls()
        print("{}, please step away.".format(self.current_player.name))
        input("{}, [Press Enter] when ready.".format(self.other_player.name))
        temp_val = deepcopy(self.current_player)
        temp_val.board = deepcopy(self.current_player.board)
        self.current_player.board = None
        self.current_player = None
        self.current_player = deepcopy(self.other_player)
        self.current_player.board = deepcopy(self.other_player.board)
        self.other_player.board = None
        self.other_player = None
        self.other_player = deepcopy(temp_val)
        self.other_player.board = deepcopy(temp_val.board)
        temp_val.board = None
        temp_val = None

    def place_ships(self):
        self.switch_players()
        for ship in self.SHIP_INFO:
            while True:
                cls()
                # Print the board
                self.current_player.board.display_full_board()
                print("{}, choose a space for your {} ({} spaces):".format(
                    self.current_player.name, ship[0], ship[1]
                ))
                # Get the input and attempt to place the ship
                location = input_filter(input(">")).capitalize()
                if self.current_player.place_ship(ship[1], location):
                    break
