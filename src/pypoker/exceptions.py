class PyPokerError(Exception):
    """
    Base PyPoker Exception Class.
    All other exceptions to inherit from this class
    """


class InvalidGameError(PyPokerError):
    """
    Error thrown when pypoker is given a game type that isn't supported.
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
