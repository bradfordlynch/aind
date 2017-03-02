import numpy as np
from sample_players import *
from isolation import Board

def runTrial(player1, player2, game, numTrials=1000):
    wins = 0
    avg_depth = 0

    for i in range(numTrials):
        new_game = game.copy()
        winner, history, outcome = new_game.play()
        if winner == player1:
            wins += 1
        avg_depth += len(history)

    return wins/numTrials, avg_depth/numTrials



if __name__ == "__main__":
    width = 7
    height = 7
    probs = np.empty((width,height))
    dpths = np.empty_like(probs)
    for i in range(probs.shape[0]):
        for j in range(probs.shape[1]):
            player1 = GreedyPlayer()
            player2 = RandomPlayer()
            game = Board(player1, player2, width, height)
            game.apply_move((i,j))
            game.apply_move(player2.get_move(game, game.get_legal_moves(player2), lambda: 200))
            prob, depth = runTrial(player1, player2, game, 100)
            probs[i,j] = prob
            dpths[i,j] = depth

    print(probs)
    print(dpths)
