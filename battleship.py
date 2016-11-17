
from game import *
from player import *


if __name__ == "__main__":
	players = []
	for num in range(1, 3):
		cls()
		print("************************")
		print("*Welcome to Battleship!*")
		print("************************\n\n")

		# Establish players here, for all games.
		new_player = Player()
		players.append(new_player)

	while True:
		# Start a new game here.
		winner = None
		winner = Game(players[0], players[1]).winner

		# Increase wins and display totals.
		if winner.winner == players[0]:
			players[0].win()
		else:
			players[1].win()

		print("{}'s wins: {}".format(players[0].name, players[0].wins))
		print("{}'s wins: {}".format(players[1].name, players[1].wins))

		if "y" not in input("\nPlay again?\n>"):
			break

	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print("Thanks for playing!")
