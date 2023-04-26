# Algo-connect4

The file 'api.py' contains an API with one endpoint that returns the optimal column for a connect4 game based on an alpha-beta pruning algorithm.

# How to use
Either Follow these steps : 
- Make sure you have python and pip installed : `python --version` and `pip --version` (the version I used are python *3.10.10* and pip *23.0.1*)
- clone the repository
- run `pip install -r requirements.txt`
- run `python api.py`

Or use the provided containerized image in https://hub.docker.com/repository/docker/badrach/algo-connect4/general  \
You can use : `sudo docker run --network host -d badrach/algo-connect4:latest` after pulling the image to run it locally on the port 5000 *(localhost:5000)*.

There is only one end point : GET /move?b=

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
