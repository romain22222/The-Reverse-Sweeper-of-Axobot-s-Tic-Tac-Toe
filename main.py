# My goal is to make a tic-tac-toe bot whose goal is to win against the axobot bot.
# Here is its strategy:
# Suppose the board is as follows:
# 1 2 3
# 4 5 6
# 7 8 9
# The bot will first check if a move can be made to win the game (i.e. if there are two of its own pieces or two of the opponent's pieces in a row, column, or diagonal and the third space is empty).
# If so, it will make that move.
# Else, it chooses a random empty space to place its piece.
# Assuming this strategy, I will write the code for the bot to abuse its strategy and win against the axobot bot.
import sys

# I want to represent the game as a list of 9 elements, where the position represents where the piece is placed by the bot, and the value represents the optimal move for my bot (ie the move that will lead to a win or the fastest game if not winnable).

winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
verbose = 0


def check_winner(board):
	for combination in winning_combinations:
		if board[combination[0]] == board[combination[1]] and board[combination[0]] == board[combination[2]] and board[combination[0]] != 0:
			return 1
	return 0


def mean(lst):
	return sum(lst) / len(lst)


class Tree:
	def __init__(self, current_moves: list[int]):
		# current moves
		self.current_moves = current_moves.copy()
		# available moves
		self.available_moves = set(range(9)) - set(current_moves)
		# current board state
		self.board = [0] * 9
		for i in range(len(current_moves)):
			self.board[current_moves[i]] = i % 2 + 1
		# next possible move trees
		self.next_moves: list['Tree'] = [None for _ in range(9)]
		# depth of the current tree
		self.depth = len(current_moves)
		# list of moves which will lead to an immediate win
		self.forced_win = set()
		# list of moves which are forced to be played to avoid a loss
		self.forced_anti_loss = set()
		# move to be played by the axobot bot, -1 if random move
		self.axobotMove = -1
		# evaluation of the current position when reached by the axobot bot
		self.evalPosWhenReachedByAxobot = 0
		# evaluation of the current position when reached by this bot
		self.evalPosWhenReachedByBot = 0
		# move to be played by this bot
		self.botMove = -1

	def populate_tree(self):
		if check_winner(self.board):
			self.evalPosWhenReachedByAxobot = 1
			self.evalPosWhenReachedByBot = -1
			return
		if self.available_moves == set():
			self.evalPosWhenReachedByAxobot = 0
			self.evalPosWhenReachedByBot = 0
			return
		for move in self.available_moves:
			self.next_moves[move] = Tree(self.current_moves + [move])
			self.next_moves[move].populate_tree()
			if check_winner(self.next_moves[move].board):
				self.forced_win.add(move)
			if check_winner([self.depth % 2 + (0 if self.depth % 2 else 2) if i == move else self.board[i] for i in range(9)]):
				self.forced_anti_loss.add(move)

		if self.forced_win.union(self.forced_anti_loss):
			self.axobotMove = max(self.forced_win.union(self.forced_anti_loss))
			self.evalPosWhenReachedByAxobot = self.next_moves[self.axobotMove].evalPosWhenReachedByBot
		else:
			self.evalPosWhenReachedByAxobot = mean([self.next_moves[move].evalPosWhenReachedByBot for move in self.available_moves])

		self.evalPosWhenReachedByBot = max([self.next_moves[move].evalPosWhenReachedByAxobot for move in self.available_moves])
		for move in self.available_moves:
			if self.next_moves[move].evalPosWhenReachedByAxobot == self.evalPosWhenReachedByBot:
				self.botMove = move
				break


def print_board(tree):
	if not verbose:
		return
	print("--------------------")
	print_current_board = ["-" if i == 0 else ("X" if i == 1 else "O") for i in tree.board]
	print("Current board:")
	print(print_current_board[0], print_current_board[1], print_current_board[2])
	print(print_current_board[3], print_current_board[4], print_current_board[5])
	print(print_current_board[6], print_current_board[7], print_current_board[8])
	print("(if will play) Bot move: ", tree.botMove + 1)
	print("(if will play) Axobot move: ", tree.axobotMove + 1 if tree.axobotMove != -1 else "Random")
	print("Detected forced win moves: ", tree.forced_win)
	print("Detected forced anti-loss moves: ", tree.forced_anti_loss)
	print("Evaluation of the current position when reached by this bot:")
	for i in range(3):
		for j in range(3):
			print(tree.next_moves[i * 3 + j].evalPosWhenReachedByAxobot if i * 3 + j in tree.available_moves else "-", end=" ")
		print()
	print("Evaluation of the current position when reached by the axobot bot:")
	for i in range(3):
		for j in range(3):
			print(((1 if i * 3 + j == tree.axobotMove else 0) if tree.axobotMove != -1 else 1/len(tree.available_moves)) if i * 3 + j in tree.available_moves else "-", end=" ")
		print()
	print("####################")


def main():
	mainTree = Tree([])
	mainTree.populate_tree()
	while True:
		print("1. Propose first being bot or axobot")
		print("2. Assuming the current player is you and given the current move list, show the best move")
		print("3. Exit")
		choice = int(input("Enter your choice: "))
		tree = mainTree
		if choice == 1:
			first_player = input("Enter the first player (you (y) or axobot(a)): ")
			move = -1
			if first_player == "a":
				while move not in tree.available_moves:
					move = int(input("Enter the first move: "))-1
				tree = tree.next_moves[move]
			print_board(tree)
			print("Best move: ", tree.botMove + 1)
			print("Winrate: ", tree.evalPosWhenReachedByBot)
			tree = tree.next_moves[tree.botMove]
			print_board(tree)
			while True:
				while move not in tree.available_moves:
					move = int(input("Enter axobot move's response: ")) - 1
				tree = tree.next_moves[move]
				if check_winner(tree.board) or len(tree.available_moves) == 0:
					print("Game over, axobot wins!" if check_winner(tree.board) else "Game over, it's a draw!")
					break
				print_board(tree)
				print("Best move: ", tree.botMove + 1)
				print("Winrate: ", tree.evalPosWhenReachedByBot)
				tree = tree.next_moves[tree.botMove]
				if check_winner(tree.board) or len(tree.available_moves) == 0:
					print("Game over, you wins!" if check_winner(tree.board) else "Game over, it's a draw!")
					break
				print_board(tree)
		elif choice == 2:
			current_moves = list(map(int, input("Enter the current move list: ").split()))
			for move in current_moves:
				tree = tree.next_moves[move]
			print("Best move: ", tree.botMove)
			print("Winrate: ", tree.evalPosWhenReachedByBot)
			print_board(tree)
		elif choice == 3:
			break
		else:
			print("Invalid choice")


if __name__ == "__main__":
	# one possible argument is whether there is a verbose output
	if len(sys.argv) > 1:
		verbose = int(sys.argv[1]) != 0
	main()
