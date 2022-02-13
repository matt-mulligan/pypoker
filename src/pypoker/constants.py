from enum import Enum

"""
General Enums
"""


class OutsCalculationMethod(Enum):
    Implicit = "implicit"
    ExplicitPartial = "explicit_partial"
    ExplicitFull = "explicit_full"


"""
Card Construct Constants
"""
CARD_ANY_VALUE = "ANY_VALUE"
CARD_ANY_SUIT = "ANY_SUIT"


class CardRank(Enum):
    Two = "2"
    Three = "3"
    Four = "4"
    Five = "5"
    Six = "6"
    Seven = "7"
    Eight = "8"
    Nine = "9"
    Ten = "T"
    Jack = "J"
    Queen = "Q"
    King = "K"
    Ace = "A"
    Any = "ANY_VALUE"


CARD_RANK_VALUES = [e.value for e in CardRank]


class CardSuit(Enum):
    Hearts = "H"
    Diamonds = "D"
    Spades = "S"
    Clubs = "C"
    Any = "ANY_SUIT"


CARD_SUIT_VALUES = [e.value for e in CardSuit]

"""
Hand Construct Constants
"""


class HandType(Enum):
    """
    Grouping class used as a parent to all game specific hand type enum classes
    """


"""
Texas Hold'em Constants
"""


class TexasHoldemHandType(HandType, Enum):
    StraightFlush = "Straight Flush"
    Quads = "Quads"
    FullHouse = "Full House"
    Flush = "Flush"
    Straight = "Straight"
    Trips = "Trips"
    TwoPair = "Two Pair"
    Pair = "Pair"
    HighCard = "High Card"


class TexasHoldemHandStrength(Enum):
    StraightFlush = 9
    Quads = 8
    FullHouse = 7
    Flush = 6
    Straight = 5
    Trips = 4
    TwoPair = 3
    Pair = 2
    HighCard = 1


class TexasHoldemHandTiebreakerArgs(Enum):
    StraightFlush = 1
    Quads = 2
    FullHouse = 2
    Flush = 5
    Straight = 1
    Trips = 3
    TwoPair = 3
    Pair = 4
    HighCard = 5


class TexasHoldemHandNumCards(Enum):
    StraightFlush = (5, 5)
    Quads = (4, 5)
    FullHouse = (5, 5)
    Flush = (5, 5)
    Straight = (5, 5)
    Trips = (3, 5)
    TwoPair = (4, 5)
    Pair = (2, 5)
    HighCard = (1, 5)


"""
Game filtered constants
"""


class GameTypes(Enum):
    TexasHoldem = "Texas Hold'em"


class GameHandTypes(Enum):
    TexasHoldem = TexasHoldemHandType


class GameHandStrengths(Enum):
    TexasHoldem = TexasHoldemHandStrength


class GameHandNumCards(Enum):
    TexasHoldem = TexasHoldemHandNumCards


class GameHandTiebreakerArgs(Enum):
    TexasHoldem = TexasHoldemHandTiebreakerArgs
