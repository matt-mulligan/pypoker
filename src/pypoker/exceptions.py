class PyPokerError(Exception):
    """
    Base PyPoker Exception Class.
    All other exceptions to inherit from this class
    """


class InvalidGameError(PyPokerError):
    """
    Error thrown when pypoker is given a game type that isn't supported.
    """


class GameMismatchError(PyPokerError):
    """
    Error thrown when an unexpected value for game is given
    """


class InvalidHandTypeError(PyPokerError):
    """
    Error thrown when pypoker is given a hand type that isn't valid.
    """


class InvalidHandError(PyPokerError):
    """
    Error thrown when pypoker is expecting a list of cards representing a players hand but the hand isn't valid.
    e.g.
        too many cards for a valid hand
        duplicate cards for a game type that dosen't accept this
    """


class RankingError(PyPokerError):
    """
    Error thrown when trying to rank player hands but an error occurs, usually a player dosent have their hand attr set
    """


class OutsError(PyPokerError):
    """
    Error thrown when trying to find outs for a player
    """
