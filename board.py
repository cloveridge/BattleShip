class Board:
    EMPTY = 'O'
    VERTICAL_SHIP = '|'
    HORIZONTAL_SHIP = '-'
    MISS = '.'
    HIT = '*'
    SUNK = '#'

    def __init__(self, size, letters):

        self.guesses = []
        self.ship_spaces = 0
        self.columns = []
        self.spaces = {}

        # Set the parameters of the board
        self.columns = letters
        self.size = size

        # Create the board's dict
        self.reset_board()

    def display_full_board(self):
        # Displays the board
        for num in range(0, self.size + 1):
            row = ""

            # Print the column headers
            if num == 0:
                row = "  "
                for col in self.columns:
                    row += " {}".format(col)
            else:
                # print the row headers
                row = str(num).rjust(2)

                # print each space, with a preceding space
                for col in self.columns:
                    row += " {}".format(self.spaces.get(col + str(num)))

            print(row)

    def reset_board(self):
        self.guesses = []
        self.ship_spaces = 0

        for let in self.columns:
            for num in range(1, self.size + 1):
                self.spaces["{}{}".format(let, num)] = self.EMPTY

    def display_quiet_board(self):
        # Displays the board without ships

        for num in range(0, self.size + 1):
            row = ""

            # Queue the column headers
            if num == 0:
                row = "  "
                for col in self.columns:
                    row += " {}".format(col.upper())
            else:
                # Queue the row headers
                row = str(num).rjust(2)

                # Queue each board space, with a preceding space
                for col in self.columns:
                    if col + str(num) in self.guesses:
                        row += " {}".format(self.spaces.get(col + str(num)))
                    else:
                        row += " {}".format(self.EMPTY)
            print(row)

    def ship_spacing_check(self, ship_size, loc, direction):
        """
        Makes sure the player's new ship will fit in the selected placement
        :param ship_size: The length of the ship
        :param loc: The ship's starting spot
        :param direction: vertical or horizontal (Read as "v" or "h")
        :return: True for valid placement
        """
        col = self.columns.index(loc[0])
        row = int(loc[1:])

        if direction == "v":
            # Make sure the ship will fit
            for spot in range(0, ship_size):
                if int(row) + spot > self.size - 1 \
                    or self.spaces.get(
                            self.columns[col] + str(row + spot)) != \
                        Board.EMPTY \
                    or self.spaces.get(
                            self.columns[col] + str(row + spot)) is None:
                    print("The ship won't fit vertically! Try a new spot.")
                    input("[Press Enter]")
                    return False
        else:
            # Attempt a horizontal placement
            for spot in range(0, ship_size):
                if col + spot > len(self.columns) - 1 \
                    or self.spaces.get(
                            self.columns[col + spot] + str(row)) != \
                        Board.EMPTY \
                    or self.spaces.get(
                            self.columns[col + spot] + str(row)) is None:
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
        if self.spaces.get(loc) is None:
            print("{} isn't a valid space on the board!".format(loc.upper()))
            print("Please try again, with a space like \"A1\"")
            input("[Press Enter]")
            return False
        elif self.spaces.get(loc) != Board.EMPTY:
            print("{} is already taken!".format(loc.upper()))
            input("[Press Enter]")
            return False

        direction = ""

        while True:
            direction = input("[v]ertical or [h]orizontal?\n>").lower()
            if direction == "":
                print("Try again, with \"v\" or \"h\".")
            elif direction[0] == "v" or direction == "h":
                break
            else:
                print("Try again, with \"v\" or \"h\".")

        col = self.columns.index(loc[0])
        row = int(loc[1:])

        if not self.ship_spacing_check(ship_size, loc, direction):
            return False
        else:
            # Place the ships
            if direction == "v":
                # Vertical placement
                for spot in range(0, ship_size):
                    self.spaces[
                        self.columns[col] + str(row + spot)
                        ] = self.VERTICAL_SHIP
            else:
                # Horizontal placement
                for spot in range(0, ship_size):
                    self.spaces[
                        self.columns[col + spot] + str(row)
                        ] = self.HORIZONTAL_SHIP
            self.ship_spaces += ship_size
            return True

    def guess(self, guess):
        guess = guess.capitalize()
        # Checks to make sure the input is in the proper format
        if guess[0] not in self.columns or not guess[1].isnumeric():
            print("{} is not valid. Try something like\"A1\"".format(guess))
            input("[Press Enter]")
            return False
        # Checks to make sure the space is on the board
        elif self.spaces.get(guess) is None:
            print("{} is not a space! Try something like\"A1\"".format(guess))
            input("[Press Enter]")
            return False
        elif self.spaces[guess] == self.EMPTY:
            self.spaces[guess] = self.MISS
            self.guesses.append(guess)
            print("It's a miss!")
            input("[Press Enter]")
            return True

        elif guess in self.guesses:
            print("{} has already been guessed!".format(guess))
            input("[Press Enter]")
            return False

        else:
            self.spaces[guess] = self.HIT
            self.guesses.append(guess)
            self.ship_spaces -= 1
            print("{} was a direct hit!".format(guess))
            input("[Press Enter]")
            return True
