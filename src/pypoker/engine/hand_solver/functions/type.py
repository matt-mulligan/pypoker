"""
FUNCTIONS.TYPE MODULE

this module contains the implementation of all hand_test functions for each game/hand type
methods in this module test if the given hand is of the same type as the type specified.
"""
from typing import List

from pypoker.deck import Card
from pypoker.engine.hand_solver.functions.shared import _check_game_type, _check_hand_type, _check_kwargs
from pypoker.engine.hand_solver.utils import hand_all_same_suit, hand_values_continuous, hand_highest_value_tuple

from typing import Dict

from pypoker.engine.hand_solver.constants import GAME_TYPES, TEXAS_HOLDEM_HAND_TYPES, GAME_TYPE_TEXAS_HOLDEM, \
    HAND_TYPE_STRAIGHT_FLUSH, HAND_TYPE_QUADS, HAND_TYPE_FULL_HOUSE, HAND_TYPE_FLUSH, HAND_TYPE_STRAIGHT, \
    HAND_TYPE_TRIPS, HAND_TYPE_TWO_PAIR, HAND_TYPE_PAIR, HAND_TYPE_HIGH_CARD


###################
#  PUBLIC METHOD  #
###################
def hand_test(game_type: str, hand_type: str, **kwargs: Dict) -> bool:
    """
    Public method that tests if hand specified in kwargs qualifies as the type of hand specified in hand_type

    :param game_type: indicates what type of poker game you are playing. Tested against constants.GAME_TYPES
    :param hand_type: indicates the hand type you are testing for. Tested against constants.<GAME_TYPE>_HAND_TYPES
    :param kwargs: Unbounded keyword arguments list required for the implementation of the test_hands method you
                   are using. Arguments passed to this command are be validated before calling underlying implementation
    :return: Boolean indicating if the hand is actually of this type.
    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    test_key = f"{game_type}-{hand_type}"

    kwargs_required_keys, test_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}": (["hand"], _hand_test_straight_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}": (["hand"], _hand_test_quads),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}": (["hand"], _hand_test_full_house),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}": (["hand"], _hand_test_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}": (["hand"], _hand_test_straight),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}": (["hand"], _hand_test_trips),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}": (["hand"], _hand_test_two_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}": (["hand"], _hand_test_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}": (["hand"], _hand_test_high_card),
    }[test_key]

    _check_kwargs(kwargs, kwargs_required_keys)
    return test_method(**kwargs)


###################################################
#  PRIVATE IMPLEMENTATION METHODS - TEXAS HOLDEM  #
###################################################
def _hand_test_straight_flush(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a straight flush hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return (
            len(hand) == 5
            and hand_all_same_suit(hand)
            and hand_values_continuous(hand)
    )


def _hand_test_quads(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a quads hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return bool(hand_highest_value_tuple(hand, 4))


def _hand_test_full_house(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a quads hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    trips_value = hand_highest_value_tuple(hand, 3)
    remaining_cards = filter(lambda card: card.value != trips_value, hand)
    pair_value = hand_highest_value_tuple(remaining_cards, 2)

    return bool(trips_value and pair_value)


def _hand_test_flush(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a flush hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return len(hand) == 5 and hand_all_same_suit(hand)


def _hand_test_straight(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a straight hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return len(hand) == 5 and hand_values_continuous(hand)


def _hand_test_trips(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a trips hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return bool(hand_highest_value_tuple(hand, 3))


def _hand_test_two_pair(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a two pair hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    high_pair_value = hand_highest_value_tuple(hand, 2)
    remaining_cards = list(filter(lambda card: card.value != high_pair_value, hand))
    low_pair_value = hand_highest_value_tuple(remaining_cards, 2)

    return bool(high_pair_value and low_pair_value)


def _hand_test_pair(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a two pair hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return bool(hand_highest_value_tuple(hand, 2))


def _hand_test_high_card(hand: List[Card]) -> bool:
    """
    Private method to test if a hand is a two pair hand

    :param hand: List of Card objects representing a players hand
    :return: Boolean indicating if the hand is a straight flush
    """

    return True
