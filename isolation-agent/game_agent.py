"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from random import randint

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player using a weighting of the player and opponent's remaining
    legal moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if type(player) == CustomPlayer:
        psi = player.psi
    else:
        print('Score got an object that is not a player')
        psi = 20
    num_moves = game.move_count

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - min(10,num_moves/psi)*opp_moves)


def weighted_improved_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player using a weighting of the player and opponent's remaining
    legal moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if type(player) == CustomPlayer:
        psi = player.psi
    else:
        print('Score got an object that is not a player')
        psi = 20

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - psi*opp_moves)

def blanks_score(game, player):
    """Calculate the heuristic value of a game state using the legal moves for
    each player and the number of remaining blank spaces.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


    blanks = len(game.get_blank_spaces())
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)/blanks

class ReflectionPlayer:
    """Player that reflects the movement of the other player """

    def get_move(self, game, legal_moves, time_left):
        """Reflect the movement of the other player"""

        self.time_left = time_left

        if game.move_count == 1:
            last_move = game.get_player_location(game.inactive_player)
            ref_move = (last_move[1], last_move[0])
            if ref_move in legal_moves:
                return ref_move
            else:
                return (-1,-1)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.openings = {
            'best':[(2,3),(3,4),(4,3),(3,2)],
            'second':[(r,c) for r in range(2,5) for c in range(2,5)]
        }
        self.psi = 10

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # Set search method
        if self.method == 'minimax':
            search_fn = self.minimax
        else:
            search_fn = self.alphabeta

        # Check if this is the first move
        if game.move_count <= 1:
            # if self.first_move != None:
            #     if self.first_move in legal_moves:
            #         return self.first_move
            #     else:
            #         raise ValueError
            #         return (-1, -1)
            for move in self.openings['best']:
                if move in legal_moves:
                    return move

            for move in self.openings['second']:
                if move in legal_moves:
                    return move

            return legal_moves[randint(0, len(legal_moves) - 1)]
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if not legal_moves:
                return (-1,-1)
            else:
                if self.iterative:
                    depth = 1
                    while True:
                        best_move = search_fn(game, depth)
                        depth += 1
                else:
                    depth = self.search_depth
                    return search_fn(game, depth)[1]

        except Timeout:
            # Handle any actions required at timeout, if necessary
            try:
                # Return the best move from the last completed search iteration
                return best_move[1]
            except NameError:
                # Ran out of time before search finished, return random legal move
                return legal_moves[randint(0, len(legal_moves) - 1)]

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Get the legal moves
        legal_moves = game.get_legal_moves()
        if legal_moves:
            # Check if max depth has been reached
            if depth == 0:
                # Apply heuristic to score moves
                return (self.score(game, self), game.get_player_location(self))
            # Max depth not reached, call minimax again
            else:
                # Call minimax for each remaining move to get scores of branch
                scores = []
                for m in legal_moves:
                    new_game = game.forecast_move(m)
                    score = self.minimax(new_game, depth-1, not maximizing_player)
                    scores.append((score[0], m))

            # Return score based on maximizing criteria
            if maximizing_player:
                return max(scores)
            else:
                return min(scores)
        else:
            # No valid moves remain
            if maximizing_player:
                return (-float('inf'), (-1,-1))
            else:
                return (float('inf'), (-1,-1))


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Get the legal moves
        legal_moves = game.get_legal_moves()
        if legal_moves:
            # Check if max depth has been reached
            if depth == 0:
                # Apply heuristic to score move
                return (self.score(game, self), game.get_player_location(self))

            if maximizing_player:
                best_score = (float('-inf'),(-1,-1))
                for m in legal_moves:
                    new_game = game.forecast_move(m)
                    score = self.alphabeta(new_game, depth-1, alpha, beta, False)
                    score = (score[0], m)
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score[0])
                    if beta <= alpha:
                        # Trim this branch
                        break

                return best_score
            else:
                best_score = (float('inf'),(-1,-1))
                for m in legal_moves:
                    new_game = game.forecast_move(m)
                    score = self.alphabeta(new_game, depth-1, alpha, beta, True)
                    score = (score[0], m)
                    best_score = min(best_score, score)
                    beta = min(beta, best_score[0])
                    if beta <= alpha:
                        break

                return best_score


        else:
            # No valid moves remain
            if maximizing_player:
                return (-float('inf'), (-1,-1))
            else:
                return (float('inf'), (-1,-1))
