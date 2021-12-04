"""
Card Construct Constants
"""
from enum import Enum

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
CARD_RANK_NAMES = [e.name for e in CardRank]


class CardSuit(Enum):
    Hearts = "H"
    Diamonds = "D"
    Spades = "S"
    Clubs = "C"
    Any = "ANY_SUIT"


CARD_SUIT_VALUES = [e.value for e in CardSuit]
CARD_SUIT_NAMES = [e.name for e in CardSuit]

"""
Hand Construct Classes
"""


class HandType:
    """
    Grouping class used as a parent to all game specific hand type enum classes
    """


"""
Texas Hold'em Constants
"""


class TexasHoldemHands(HandType, Enum):
    StraightFlush = "Straight Flush"
    Quads = "Quads"
    FullHouse = "Full House"
    Flush = "Flush"
    Straight = "Straight"
    Trips = "Trips"
    TwoPair = "Two Pair"
    Pair = "Pair"
    HighCard = "High Card"


TH_HAND_STRENGTHS = {
    TexasHoldemHands.StraightFlush: 9,
    TexasHoldemHands.Quads: 8,
    TexasHoldemHands.FullHouse: 7,
    TexasHoldemHands.Flush: 6,
    TexasHoldemHands.Straight: 5,
    TexasHoldemHands.Trips: 4,
    TexasHoldemHands.TwoPair: 3,
    TexasHoldemHands.Pair: 2,
    TexasHoldemHands.HighCard: 1,
}

TH_HAND_TIEBREAKER_ARGS = {
    TexasHoldemHands.StraightFlush: 1,
    TexasHoldemHands.Quads: 2,
    TexasHoldemHands.FullHouse: 2,
    TexasHoldemHands.Flush: 5,
    TexasHoldemHands.Straight: 1,
    TexasHoldemHands.Trips: 3,
    TexasHoldemHands.TwoPair: 3,
    TexasHoldemHands.Pair: 4,
    TexasHoldemHands.HighCard: 5,
}

TH_HAND_NUM_CARDS = {
    TexasHoldemHands.StraightFlush: (5, 5),
    TexasHoldemHands.Quads: (4, 5),
    TexasHoldemHands.FullHouse: (5, 5),
    TexasHoldemHands.Flush: (5, 5),
    TexasHoldemHands.Straight: (5, 5),
    TexasHoldemHands.Trips: (3, 5),
    TexasHoldemHands.TwoPair: (4, 5),
    TexasHoldemHands.Pair: (2, 5),
    TexasHoldemHands.HighCard: (1, 5),
}


"""
Game filtered constants
"""
GAME_TEXAS_HOLDEM = "Texas Hold'em"
GAME_TYPES = [GAME_TEXAS_HOLDEM]

GAME_HAND_TYPES = {GAME_TEXAS_HOLDEM: TexasHoldemHands}

GAME_HAND_STRENGTHS = {GAME_TEXAS_HOLDEM: TH_HAND_STRENGTHS}

GAME_HAND_NUM_CARDS = {GAME_TEXAS_HOLDEM: TH_HAND_NUM_CARDS}

GAME_HAND_TIEBREAKERS_ARGS = {GAME_TEXAS_HOLDEM: TH_HAND_TIEBREAKER_ARGS}
