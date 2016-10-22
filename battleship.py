"""
Author: Christian Loveridge
Creation Date: 10/09/2016
My take on the classic game of Battleship! Two players place their "ships" on 10x10 grids, then take turns guessing
exactly where the other player's ships are. The one to hit all of the other player's ships first, wins the game.
"""

import os


# Create a menu
# Generate a new game
# Create 2 boards
# Let player 1 place their ships (Show only their board)
# players get 5 ships--have a list of ships
# Verify placed ships are not overlapping
# Let player 2 place their ships too (Show only their board)
# Start the game
# Players take turns
# Parse players' moves
# Record hits and misses (Detailed Reports)
# Verbose errors
# When all ships are sunk for one player, game over.


def cls():
	# os.system("cls")
	os.system("clear")


def test():
	board = [(letter + str(number)) for number in range(1, 11) for letter in "abcdefghij"]
	taken_places = []
	hits = []
	misses = []
	draw_board(board, taken_places, hits, misses)


def draw_board(board, objects):
	"""
	Renders the game board.
	:param board: A dictionary whose keys are letter-number references ("A1") which hold values.
	:param objects: A dictionary of lists--letters for the header, board labels for hits/misses/ships/empty spaces.
	:return: nothing.
	"""
	board_size = objects["size"]
	letters = objects["letters"]
	board_objects = objects["board_objects"]

	printrow = "  "
	for letter in letters:
		printrow += " " + letter.upper()

	print(printrow)

	for num in range(1, board_size + 1):
		printrow = ""
		if num < 10:
			printrow = " " + str(num)
		else:
			printrow = str(num)
		for let in letters:
			printrow += " " + board.get(let + str(num), "O")

		print(printrow)
	print("")


def place_ship(board, ship, objects):
	"""
	Self-explanatory function.
	:param board: A dictionary whose keys are letter-number references ("A1") which hold values
	:param ship: A tuple with a ship's name and size
	:param objects: A dictionary of lists--letters for the header, board labels for hits/misses/ships/empty spaces.
	:return: a new, updated board with the new ship placed in it.
	"""
	ship_name, ship_size = ship
	new_board = board
	board_size = objects["size"]
	letters = objects["letters"]
	board_objects = objects["board_objects"]

	# Loop which makes sure they place their ships correctly
	while True:
		starting_place = ""
		direction = ""
		can_be_horizontal = True
		can_be_vertical = True

		while starting_place == "":
			cls()
			print("Captain {}, please place your {} ({} spaces):\n".format(objects.get("current_player"), ship_name, ship_size))
			draw_board(board, objects)
			starting_place = str(input("> : ")).lower().strip()
			if len(starting_place) < 2 or len(starting_place) > 3 or board.get(starting_place) is None:
				print("\"{}\" didn't work. Please type a valid cell address with letter and number, like \"A1\"".format(starting_place))
				input("[Press Enter]")
				starting_place = ""
				continue
			elif board[starting_place] != board_objects.get("EMPTY"):
				print(
					"\"{}\" is not available. Please type a valid cell address with letter and number, like \"A1\"".format(starting_place))
				input("[Press Enter]")
				starting_place = ""
				continue

		letter, number = starting_place[0].lower().strip(), int(starting_place[1:])

		# check to see if ships can be placed vertical or horizontal
		for let in letters[letters.index(letter):letters.index(letter) + ship_size]:
			if board.get(let + str(number)) != board_objects.get("EMPTY") or letters.index(letter) + ship_size > len(letters):
				can_be_horizontal = False

		for num in range(number, number + ship_size):
			if board.get(letter + str(num)) != board_objects.get("EMPTY") or board.get(letter + str(num)) is None:
				can_be_vertical = False

		if can_be_vertical and can_be_horizontal:
			dir_input = ""
			while dir_input == "":
				dir_input = input("[V]ertical or [H]orizontal? ([R]ight/[D]own from {})\n".format(starting_place.upper())).lower().strip()
				if dir_input[0] == "v" or dir_input[0] == "d":
					direction = "v"
				elif dir_input[0] == "h" or dir_input[0] == "r":
					direction = "h"
				else:
					dir_input = ""
					print("Sorry, \"{}\" wasn't a valid input. Please follow the prompts.".format(dir_input))
					input("[Press Enter]")
					cls()
					print("Please place your {} ({} spaces):\n".format(ship_name, ship_size))
					draw_board(board, objects)
					continue
		elif can_be_vertical:
			direction = "v"
		elif can_be_horizontal:
			direction = "h"
		else:
			print("The {} won't fit there--it's {} spaces long!".format(ship_name, ship_size))
			input("[Press Enter]")
			continue

		if direction == "h":
			for let in letters[letters.index(letter):letters.index(letter) + ship_size]:
				board[let + str(number)] = board_objects.get("HORIZONTAL_SHIP", "-")
		else:
			for num in range(number, number + ship_size):
				board[letter + str(num)] = board_objects.get("VERTICAL_SHIP", "|")

		break

	return new_board


def game_setup(objects):
	"""
	Creates the game boards and places the ships
	:param objects:
	:return:
	"""
	ships = objects.get("ships")
	board_objects = objects.get("board_objects")
	players = objects["players"]
	player_1 = players[0]
	player_2 = players[1]

	cls()

	# Create the boards
	for number in range(1, BOARD_SIZE + 1):
		for letter in LETTERS:
			objects["player_1_board"][letter + str(number)] = board_objects.get("EMPTY", "O")
			objects["player_2_board"][letter + str(number)] = board_objects.get("EMPTY", "O")

	input("{}, please step away.\n[{}, press Enter]".format(player_2, player_1))

	objects["current_player"] = player_1

	# Place all ships for player one
	for ship in objects.get("ships"):
		objects["player_1_board"] = place_ship(objects["player_1_board"], ship, objects)

	cls()
	draw_board(objects["player_1_board"], objects)
	print("Ships placed!\n")
	input("[Press Enter]")
	cls()
	input("{}, please step away.\n[{}, press Enter]".format(player_1, player_2))
	objects["current_player"] = player_2

	# Place all ships for player two
	for ship in ships:
		objects["player_2_board"] = place_ship(objects["player_2_board"], ship, objects)

	cls()
	draw_board(objects["player_2_board"], objects)
	print("Ships placed!")

	return objects


def validate_guess(board, board_objects, guess):
	"""
	Makes sure a guess is actually on the board, and it hasn't been guessed before.
	:param board:
	:param board_objects:
	:param guess:
	:return:
	"""
	if board.get(guess) is None:
		print("That's not a valid reference!")
		return False
	elif board.get(guess) == board_objects["HIT"] or board.get(guess) == board_objects["MISS"]:
		print("You've already guessed that space!")
		return False
	else:
		return True


def start_game(objects):
	"""
	The main game loop. Players take turns guessing where the other player's ships are
	until there are no more ships on the board.
	:param objects:
	:return:
	"""
	board_objects = objects.get("board_objects")
	size = objects.get("size")
	letters = objects.get("letters")
	players = objects.get("players")
	player_1 = players[0]
	player_2 = players[1]
	winner = ""
	player_1_ship_spaces = 0
	player_2_ship_spaces = 0

	input("[Press Enter]")
	cls()

	objects["current_player"] = player_2

	# Sets the counter for the players' ships
	for ship in objects.get("ships"):
		player_1_ship_spaces += ship[1]

	player_2_ship_spaces = player_1_ship_spaces

	print("Let's play Battleship!\n\n")

	while player_1_ship_spaces and player_2_ship_spaces:

		# Resets the per-turn game boards
		display_board = {}
		guessing_board = {}
		my_board = {}

		# Copies the game board for the current player into "current_board"
		if objects.get("current_player") == player_1:
			objects["current_player"] = player_2
			for number in range(1, BOARD_SIZE + 1):
				for letter in LETTERS:
					guessing_board[letter + str(number)] = objects["player_1_board"][letter + str(number)]
					my_board[letter + str(number)] = objects["player_2_board"][letter + str(number)]
		else:
			objects["current_player"] = player_1
			for number in range(1, BOARD_SIZE + 1):
				for letter in LETTERS:
					guessing_board[letter + str(number)] = objects["player_2_board"][letter + str(number)]
					my_board[letter + str(number)] = objects["player_1_board"][letter + str(number)]

		print("Captain {}, it's your turn!".format(objects["current_player"]))
		input("[Press Enter]")
		cls()

		# Create the display board so no ships appear
		for number in range(1, BOARD_SIZE + 1):
			for letter in LETTERS:
				if guessing_board[letter + str(number)] == board_objects.get("VERTICAL_SHIP") or guessing_board[letter + str(number)] == board_objects.get("HORIZONTAL_SHIP"):
					display_board[letter + str(number)] = board_objects.get("EMPTY")
				else:
					display_board[letter + str(number)] = guessing_board[letter + str(number)]

		draw_board(display_board, objects)
		draw_board(my_board, objects)

		# Loop to guess a cell, verify legitimacy, and produce an outcome on the board
		valid_attack_cell = ""
		guess_outcome = ""
		while valid_attack_cell == "":
			valid_attack_cell = input("Captain {}, choose a cell to attack! (Like \"A1\")\n".format(objects["current_player"])).lower().strip()
			if validate_guess(guessing_board, board_objects, valid_attack_cell):
				if guessing_board[valid_attack_cell] == board_objects["EMPTY"]:
					guess_outcome = "miss"
					guessing_board[valid_attack_cell] = board_objects["MISS"]
					display_board[valid_attack_cell] = board_objects["MISS"]
				else:
					guess_outcome = "direct hit"
					guessing_board[valid_attack_cell] = board_objects["HIT"]
					display_board[valid_attack_cell] = board_objects["HIT"]
					if objects["current_player"] == player_1:
						player_2_ship_spaces -= 1
					else:
						player_1_ship_spaces -= 1
			else:
				valid_attack_cell = ""

		cls()
		draw_board(display_board, objects)
		draw_board(my_board, objects)
		print("{} was a {}!\n".format(valid_attack_cell, guess_outcome))

		if objects["current_player"] == player_1:
			for number in range(1, BOARD_SIZE + 1):
				for letter in LETTERS:
					objects["player_2_board"][letter + str(number)] = guessing_board[letter + str(number)]
		else:
			for number in range(1, BOARD_SIZE + 1):
				for letter in LETTERS:
					objects["player_1_board"][letter + str(number)] = guessing_board[letter + str(number)]

	if player_2_ship_spaces:
		winner = player_2
	else:
		winner = player_1

	return winner


if __name__ == "__main__":
	print("***************")
	print("* Ship Battle *")
	print("***************")
	player_1_name = input("\nPlayer 1, enter your name:\n> ")
	player_2_name = input("Player 2, enter your name:\n> ")

	SHIP_INFO = [
		("Aircraft Carrier", 5),
		("Battleship", 4),
		("Submarine", 3),
		("Cruiser", 3),
		("Patrol Boat", 2)
	]

	BOARD_OBJECTS = {
		"VERTICAL_SHIP": "|",
		"HORIZONTAL_SHIP": "-",
		"EMPTY": "O",
		"MISS": ".",
		"HIT": "*",
		"SUNK": "#",
	}

	BOARD_SIZE = 10
	LETTERS = "abcdefghij"

	# Create a dictionary, comprised of all dictionaries--This is passed to/from functions
	OBJ_DICT = {
		"ships": SHIP_INFO,
		"board_objects": BOARD_OBJECTS,
		"player_1_board": {},
		"player_2_board": {},
		"size": BOARD_SIZE,
		"letters": LETTERS,
		"players": [player_1_name, player_2_name],
		"current_player": ""
	}

	play_again = True
	player_1_wins = 0
	player_2_wins = 0

	while play_again:
		OBJ_DICT = game_setup(OBJ_DICT)
		winner = start_game(OBJ_DICT)

		input("[Press Enter]")
		cls()
		print("{} wins!".format(winner))

		print("\n{}'s board:".format(player_1_name))
		draw_board(OBJ_DICT["player_1_board"], OBJ_DICT)
		print("\n{}'s board:".format(player_2_name))
		draw_board(OBJ_DICT["player_2_board"], OBJ_DICT)

		if winner == player_1_name:
			player_1_wins += 1
		else:
			player_2_wins += 1
		print("{}'s wins: {}".format(player_1_name, player_1_wins))
		print("{}'s wins: {}".format(player_2_name, player_2_wins))
		input("[Press Enter]")

		if "y" not in input("Play again? ").lower().strip():
			play_again = False
