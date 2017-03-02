from random import randint
from game_agent import ReflectionPlayer, CustomPlayer
from sample_players import GreedyPlayer, RandomPlayer, open_move_score
from agent_test import makeEvalTable

if __name__ == "__main__":
    from isolation import Board

    h = 7
    w = 7

    value_table = [[0] * w for _ in range(h)]
    value_table[1][5] = 1  # depth 1 & 2
    value_table[4][3] = 2  # depth 3 & 4
    value_table[6][6] = 3  # depth 5
    heuristic = makeEvalTable(value_table)

    # create an isolation board (by default 7x7)
    player1 = CustomPlayer(score_fn=heuristic)
    player1.time_left = lambda: 1e3
    player1.iterative = False
    player2 = GreedyPlayer()
    game = Board(player1, player2)

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that .apply_move() changes the calling object
    game.apply_move((2, 3))
    game.apply_move((0, 0))

    # players take turns moving on the board, so player2 should be next to move
    assert(player1 == game.active_player)

    # get a list of the legal moves available to the active player
    #print(game.get_legal_moves())

    print('What algo thinks:')
    print(player1.minimax(game, 2))
    print()
    print('What should be there:')
    print('First state legal moves:')
    lms = game.get_legal_moves()
    #print(lms)
    print("\nCurrent state:\n{}".format(game.to_string()))
    print('Legal moves for subsequent states:')
    for m in lms:
        new_game = game.forecast_move(m)
        #print("\nMove {}, Score{}:\n{}".format(m, player1.score(new_game, player1),new_game.to_string()))
        #print(m, new_game.get_legal_moves())

    # get a successor of the current state by making a copy of the board and
    # applying a move. Notice that this does NOT change the calling object
    # (unlike .apply_move()).
    # new_game = game.forecast_move((1, 1))
    # assert(new_game.to_string() != game.to_string())
    # print("\nOld state:\n{}".format(game.to_string()))
    # # print("\nNew state:\n{}".format(new_game.to_string()))
    #
    # # play the remainder of the game automatically -- outcome can be "illegal
    # # move" or "timeout"; it should _always_ be "illegal move" in this example
    # winner, history, outcome = game.play()
    # print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    # print(game.to_string())
    # print("Move history:\n{!s}".format(history))
