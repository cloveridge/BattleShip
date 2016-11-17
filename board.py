class Board:
    VERTICAL_SHIP = '|'
    HORIZONTAL_SHIP = '-'
    EMPTY = 'O'
    MISS = '.'
    HIT = '*'
    SUNK = '#'

    columns = []
    spaces = {}
    guesses = []

    def __init__(self, letters, size):
        for let in letters:
            for num in range(1, size + 1):
                self.spaces["{}{}".format(let, num)] = self.EMPTY
        self.columns = letters
        self.size = size

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
                    if self.spaces.get(col + str(num)) in self.guesses:
                        row += " {}".format(self.spaces.get(col + str(num)))
                    else:
                        row += " {}".format(self.EMPTY)
            print(row)
