import re
import os


def cls():
    """Clears the screen using the system, or printing 100 newlines"""
    try:
        os.system("clear")
    finally:
        print("\n"*100)


def input_filter(text):
    """Takes text, removes whitespace, and returns it"""
    return re.sub('s', "", text)


class Game:
    """The Game class, which directs the flow of the game for two players.

    Each game instance has 2 players, and after establishing all elements,
    runs the game loop. The game loop ends when a winner has been declared,
    the winner is reported to the application, and the Game object is destroyed.
    """
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

        self.run_game()

    def run_game(self):
        """The game loop which runs until a winner has been declared.

        Each player takes turns making guesses until one of them has guessed
        all of the other player's ships.
        """
        while True:
            # Alternate turns
            self.switch_players()

            while True:
                # Loop until a good guess has been made
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
                    # A good guess has been made
                    break


            if self.players[abs(self.current - 1)].board.ship_spaces == 0:
                # If other player has no ships left, break and set a winner.
                self.winner = self.current

                cls()
                message = "* We have a winner! *"
                print("*"*len(message))
                print(message)
                print("*"*len(message))
                print("\nAdmiral {} won!\n".format(self.players[
                                                       self.current].name))

                # Display both full boards for review.
                self.players[abs(self.current - 1)].board.display_full_board()
                print("\n" + ("==" * (len(self.letters) + 1)) + "\n")
                self.players[self.current].board.display_full_board()
                input("\n[Press Enter] when finished reviewing the game.")
                break

            else:
                # If there are ships left, recap the turn
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
        """Changes the 1/0 player list index to its inverse"""
        cls()
        print("{}, please step away.".format(self.players[self.current].name))
        self.current = abs(self.current - 1)
        input("{}, [Press Enter].".format(self.players[self.current].name))

    def place_ships(self):
        """Places each ship in SHIP_INFO"""
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
