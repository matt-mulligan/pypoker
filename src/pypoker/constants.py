"""
Texas Hold'em Constants
"""

TH_HAND_STRAIGHT_FLUSH = "Straight Flush"
TH_HAND_QUADS = "Quads"
TH_HAND_FULL_HOUSE = "Full House"
TH_HAND_FLUSH = "Flush"
TH_HAND_STRAIGHT = "Straight"
TH_HAND_TRIPS = "Trips"
TH_HAND_TWO_PAIR = "Two Pair"
TH_HAND_PAIR = "Pair"
TH_HAND_HIGH_CARD = "High Card"

TH_HANDS_ORDERED = [
    TH_HAND_STRAIGHT_FLUSH,
    TH_HAND_QUADS,
    TH_HAND_FULL_HOUSE,
    TH_HAND_FLUSH,
    TH_HAND_STRAIGHT,
    TH_HAND_TRIPS,
    TH_HAND_TWO_PAIR,
    TH_HAND_PAIR,
    TH_HAND_HIGH_CARD,
]

TH_HAND_STRENGTHS = {
    TH_HAND_STRAIGHT_FLUSH: 9,
    TH_HAND_QUADS: 8,
    TH_HAND_FULL_HOUSE: 7,
    TH_HAND_FLUSH: 6,
    TH_HAND_STRAIGHT: 5,
    TH_HAND_TRIPS: 4,
    TH_HAND_TWO_PAIR: 3,
    TH_HAND_PAIR: 2,
    TH_HAND_HIGH_CARD: 1,
}

TH_HAND_TIEBREAKER_ARGS = {
    TH_HAND_STRAIGHT_FLUSH: 1,
    TH_HAND_QUADS: 2,
    TH_HAND_FULL_HOUSE: 2,
    TH_HAND_FLUSH: 5,
    TH_HAND_STRAIGHT: 1,
    TH_HAND_TRIPS: 3,
    TH_HAND_TWO_PAIR: 3,
    TH_HAND_PAIR: 4,
    TH_HAND_HIGH_CARD: 5,
}

TH_HAND_NUM_CARDS = {
    TH_HAND_STRAIGHT_FLUSH: (5, 5),
    TH_HAND_QUADS: (4, 5),
    TH_HAND_FULL_HOUSE: (5, 5),
    TH_HAND_FLUSH: (5, 5),
    TH_HAND_STRAIGHT: (5, 5),
    TH_HAND_TRIPS: (3, 5),
    TH_HAND_TWO_PAIR: (4, 5),
    TH_HAND_PAIR: (2, 5),
    TH_HAND_HIGH_CARD: (1, 5),
}


"""
Game filtered constants
"""
GAME_TEXAS_HOLDEM = "Texas Hold'em"
GAME_TYPES = [GAME_TEXAS_HOLDEM]

GAME_HAND_TYPES = {
    GAME_TEXAS_HOLDEM: TH_HANDS_ORDERED
}

GAME_HAND_STRENGTHS = {
    GAME_TEXAS_HOLDEM: TH_HAND_STRENGTHS
}

GAME_HAND_NUM_CARDS = {
    GAME_TEXAS_HOLDEM: TH_HAND_NUM_CARDS
}

GAME_HAND_TIEBREAKERS_ARGS = {
    GAME_TEXAS_HOLDEM: TH_HAND_TIEBREAKER_ARGS
}