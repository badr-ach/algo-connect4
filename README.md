# Algo-connect4

The file 'api.py' contains an API with one endpoint that returns the optimal column for a connect4 game based on an alpha-beta pruning algorithm.

# Quick Details

- Evaluation function is a simple function that counts the number of aligned tokens for each player and multiplies it by a coffecient.

- The board is represented as a bitstring for both players in order to optimize the code

- The depth of the tree is set to 7 to not bypass the limited speed of 2s on our machine. (At 8 we jump from a computation that hovers around 1s to  past 2s immediately)

- A must-play move is calculated before exploring the tree to block the enemy from connecting 4 tokens or to win instantly. (additional heuristic)

# References & Credits

http://blog.gamesolver.org/solving-connect-four/06-bitboard/
http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
https://www.gamedev.net/forums/topic/596955-trying-bit-boards-for-connect-4/

And many other code bites from stackoverflow...