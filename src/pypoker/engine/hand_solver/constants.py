"""
Shared constants library for the hand_solver package
"""

BEST_HAND = "best_hand"
HAND_TITLE = "hand_title"
HAND_RANK = "hand_rank"
HAND_DESCRIPTION = "hand_description"
TEST_METHOD = "test_method"
RANK_METHOD = "rank_method"
FIND_BEST_METHOD = "find_best_method"
DESCRIPTION_METHOD = "hand_description_method"
OUTS_METHOD = "outs_method"
OUT_STRING = "out_string"
OUTS_TB_METHOD = "outs_tb_method"

TIEBREAKER = "tiebreaker"
PLAYING_BOARD = "playing_board"

SUIT_HEARTS = "Hearts"
SUIT_SPADES = "Spades"
SUIT_DIAMONDS = "Diamonds"
SUIT_CLUBS = "Clubs"

CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


GAME_TYPE_TEXAS_HOLDEM = "Texas Holdem"
GAME_TYPES = [GAME_TYPE_TEXAS_HOLDEM]

HAND_TYPE_STRAIGHT_FLUSH = "Straight Flush"
HAND_TYPE_QUADS = "Quads"
HAND_TYPE_FULL_HOUSE = "Full House"
HAND_TYPE_FLUSH = "Flush"
HAND_TYPE_STRAIGHT = "Straight"
HAND_TYPE_TRIPS = "Trips"
HAND_TYPE_TWO_PAIR = "Two Pair"
HAND_TYPE_PAIR = "Pair"
HAND_TYPE_HIGH_CARD = "High Card"
TEXAS_HOLDEM_HAND_TYPES = [
    HAND_TYPE_STRAIGHT_FLUSH,
    HAND_TYPE_QUADS,
    HAND_TYPE_FULL_HOUSE,
    HAND_TYPE_FLUSH,
    HAND_TYPE_STRAIGHT,
    HAND_TYPE_TRIPS,
    HAND_TYPE_TWO_PAIR,
    HAND_TYPE_PAIR,
    HAND_TYPE_HIGH_CARD,
]

TB_DRAWS_KWARGS_ALL = "all"
TB_DRAWS_KWARGS_TIEBREAKER = "tiebreaker"
TB_DRAWS_KWAGRS = {
    HAND_TYPE_STRAIGHT_FLUSH: TB_DRAWS_KWARGS_TIEBREAKER,
    HAND_TYPE_QUADS: TB_DRAWS_KWARGS_ALL,
    HAND_TYPE_FULL_HOUSE: TB_DRAWS_KWARGS_TIEBREAKER,
    HAND_TYPE_FLUSH: TB_DRAWS_KWARGS_ALL,
    HAND_TYPE_STRAIGHT: TB_DRAWS_KWARGS_TIEBREAKER,
    HAND_TYPE_TRIPS: TB_DRAWS_KWARGS_ALL,
    HAND_TYPE_TWO_PAIR: TB_DRAWS_KWARGS_ALL,
    HAND_TYPE_PAIR: TB_DRAWS_KWARGS_ALL,
    HAND_TYPE_HIGH_CARD: TB_DRAWS_KWARGS_ALL,
}
