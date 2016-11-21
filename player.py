from board import Board


class Player:
    name = ""
    wins = 0
    ship_spaces = 0
    board = {}
    display_board = {}

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", self.get_name()).capitalize()
        self.wins = 0
        self.size = kwargs.get("BOARD_SIZE", 10)
        self.letters = kwargs.get("LETTERS", ["A", "B", "C", "D", "E",
                                              "F", "G", "H", "I", "J"])
        self.create_board()

    def get_name(self):
        name = input("What is your name?\n>").capitalize()
        print("Welcome, Admiral {}!".format(name))
        input("[Press Enter]")
        return name

    def create_board(self):
        self.board = None
        self.board = Board(self.letters, self.size)

    def win(self):
        self.wins += 1

    def ship_spacing_check(self, ship_size, loc, direction):
        """
        Makes sure the player's new ship will fit in the selected placement
        :param ship_size: The length of the ship
        :param loc: The ship's starting spot
        :param direction: vertical or horizontal (Read as "v" or "h")
        :return: True for valid placement
        """
        col = self.letters.index(loc[0])
        row = int(loc[1:])

        if direction == "v":
            # Make sure the ship will fit
            for spot in range(0, ship_size):
                if int(row) + spot > self.size - 1 \
                or self.board.spaces.get(
                self.letters[col] + str(row + spot)) != Board.EMPTY \
                or self.board.spaces.get(
                self.letters[col] + str(row + spot)) is None:
                    print("The ship won't fit vertically! Try a new spot.")
                    input("[Press Enter]")
                    return False
        else:
            # Attempt a horizontal placement
            for spot in range(0, ship_size):
                if col + spot > len(self.letters) - 1 \
                or self.board.spaces.get(
                self.letters[col + spot] + str(row)) != Board.EMPTY \
                or self.board.spaces.get(
                self.letters[col + spot] + str(row)) is None:
                    print("The ship won't fit horizontally! Try a new spot.")
                    input("[Press Enter]")
                    return False
        return True

    def place_ship(self, ship_size, loc):
        """
        attempts to place the ship on the board. If successful,
        returns 1, otherwise, it reports an error and returns 0.
        """

        # Verifies each space the ship would take is open and exists
        if self.board.spaces.get(loc) is None:
            print("{} isn't a valid space on the board!".format(loc.upper()))
            print("Please try again, with a space like \"A1\"")
            input("[Press Enter]")
            return False
        elif self.board.spaces.get(loc) != Board.EMPTY:
            print("{} is already taken!".format(loc.upper()))
            input("[Press Enter]")
            return False

        drctn = input("[v]ertical or [h]orizontal?\n>").lower()[0]

        col = self.letters.index(loc[0])
        row = int(loc[1:])

        if not self.ship_spacing_check(ship_size, loc, drctn):
            return False
        else:
            # Place the ships
            if drctn == "v":
                # Vertical placement
                for spot in range(0, ship_size):
                    self.board.spaces[
                        self.letters[col] + str(row + spot)
                        ] = self.board.VERTICAL_SHIP
            else:
                # Horizontal placement
                for spot in range(0, ship_size):
                    self.board.spaces[
                        self.letters[col + spot] + str(row)
                        ] = self.board.HORIZONTAL_SHIP
            self.ship_spaces += ship_size
            return True

    def guess(self, guess):
        guess = guess.capitalize()
        # Checks to make sure the input is in the proper format
        if guess[0] not in self.letters or not guess[1].isnumeric():
            print("{} is not valid. Try something like\"A1\"".format(guess))
            input("[Press Enter]")
            return False
        # Checks to make sure the space is on the board
        elif self.board.spaces[guess] is None:
            print("{} is not a space! Try something like\"A1\"".format(guess))
            input("[Press Enter]")
            return False

        elif self.board.spaces[guess] != self.board.HIT \
        or self.board.spaces[guess] != self.board.MISS:
            print("{} has already been guessed!".format(guess))
            input("[Press Enter]")
            return False
        elif self.board.spaces[guess] == self.board.EMPTY:
            self.board.spaces[guess] = self.board.MISS
            self.board.guesses.append(guess)
            print("It's a miss!")
            input("[Press Enter]")
            return True
        else:
            self.board.spaces[guess] = self.board.HIT
            self.board.guesses.append(guess)
            self.ship_spaces -= 1
            print("{} a direct hit!")
            input("[Press Enter]")
            return True
