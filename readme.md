# The Reverse Sweeper of Axobot's Tic Tac Toe

This is a console bot which aims at beating the [Tic Tac Toe game](https://github.com/Axobot-org/Axobot/blob/main/modules/tictactoe/tictactoe.py) of [Axobot](https://github.com/Axobot-org/Axobot)
The bot uses the meanmax algorithm to determine the best move to make. (and yes the joke is intended)
The goal is to either guarantee a win against it or finish the game as fast as possible when no win is possible.

## How to run the bot

To run the bot, you need to have Python installed on your machine.
You can download Python from [here](https://www.python.org/downloads/).

After installing Python, you can run the bot by executing the following command in the terminal:

```bash
python main.py <verbose>
```

The `<verbose>` flag is optional and can be used to print the game board after each move. The `<verbose>` flag can be `1` or `0`.

## How to use the bot

The bot will prompt you with a menu to choose the mode.

1. Use the bot interactively
2. Given a list of moves, get the best move for the bot

### Interactive mode

In this mode, you can queue axobot against this bot. The bot will prompt you to give what axobot has played and then you'll be given the move the bot makes.

### Given a list of moves

In this mode, you can give the bot a list of moves (separated by spaces) and the bot will give you the best move to make and the expected outcome of the game.
