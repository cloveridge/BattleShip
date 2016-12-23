from board import Board
import re
import os


def cls():
    os.system("clear")


def input_filter(text):
    return re.sub('s', "", text)


class Game:

    SHIP_INFO = [
        ("Aircraft Carrier", 5),
        ("Battleship", 4),
        ("Submarine", 3),
        ("Cruiser", 3),
        ("Patrol Boat", 2)
    ]
    winner = None

    def __init__(self, player_1, player_2):

        # Establish players
        self.players = []
        self.players.append(player_1)
        self.players.append(player_2)
        self.current = 0

        # Reset the boards from previous games
        self.players[self.current].board.reset_board()
        self.players[self.current + 1].board.reset_board()

        self.size = player_1.board.size
        self.letters = player_1.board.columns

        # Set player 1's ships up
        self.place_ships()

        # Set player 2's ships up
        self.switch_players()
        self.place_ships()

        self.game_loop()

    def game_loop(self):
        # Run the regular game loop through here.
        while True:
            # Alternate turns
            self.switch_players()

            # Loop until a good guess has been made
            while True:
                cls()
                # Print plain board for other player
                self.players[abs(self.current - 1)].board.display_quiet_board()
                print("\n" + ("==" * (len(self.letters) + 1)) + "\n")

                # Print detailed board for current player
                self.players[self.current].board.display_full_board()

                print("{}, pick a space to attack!".format(
                    self.players[self.current].name))
                location = input_filter(input(">")).capitalize()
                if location == "":
                    continue
                if self.players[abs(self.current - 1)].board.guess(location):
                    break


            if self.players[abs(self.current - 1)].board.ship_spaces == 0:
                # If no ships left, break
                self.winner = self.current

                cls()
                message = "* We have a winner! *"
                print("*"*len(message))
                print(message)
                print("*"*len(message))
                print("\nAdmiral {} won!\n".format(self.players[
                                                       self.current].name))

                self.players[abs(self.current - 1)].board.display_full_board()
                print("\n" + ("==" * (len(self.letters) + 1)) + "\n")
                self.players[self.current].board.display_full_board()
                input("\n[Press Enter] when finished reviewing the game.")
                break

            else:
                # Otherwise recap the turn
                cls()
                print("{}'s summary:".format(self.players[self.current].name))
                # Print quiet board for other player
                self.players[abs(self.current - 1)].board.display_quiet_board()
                print("\n" + ("==" * (len(self.letters) + 1)) + "\n")

                # Print verbose board for current player
                self.players[self.current].board.display_full_board()
                input("[Press Enter] when finished.")
                cls()

    def switch_players(self):
        cls()
        print("{}, please step away.".format(self.players[self.current].name))
        self.current = abs(self.current - 1)
        input("{}, [Press Enter].".format(self.players[self.current].name))

    def place_ships(self):
        for ship in self.SHIP_INFO:
            while True:
                cls()
                self.players[self.current].board.display_full_board()
                print("{}, choose a space for your {} ({} spaces):".format(
                    self.players[self.current].name, ship[0], ship[1]
                ))
                # Get the input and attempt to place the ship
                loc = input_filter(input(">")).capitalize()
                if self.players[self.current].board.place_ship(ship[1], loc):
                    break

        cls()
        print("Here is your board:")
        self.players[self.current].board.display_full_board()
        input("[Press Enter] when finished.")
