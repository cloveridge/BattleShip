
from game import *
from player import *


if __name__ == "__main__":
	size = 10
	letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
	players = []
	for num in range(1, 3):
		cls()
		print("************************")
		print("*Welcome to Battleship!*")
		print("************************\n\n")

		print("Player {}:".format(num))
		# Establish players here, for all games.
		new_player = Player(size, letters)
		players.append(new_player)

	while True:
		# Start a new game here.
		winner = None
		winner = Game(players[0], players[1]).winner

		# Increase wins and display totals.
		players[winner].win()

		print("{}'s wins: {}".format(players[0].name, players[0].wins))
		print("{}'s wins: {}".format(players[1].name, players[1].wins))

		if "y" not in input("\nPlay again?\n>"):
			break

	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print("Thanks for playing!")
