"""
FUNCTIONS.RANK MODULE

this module contains the implementation of all hand ranking logic for hands of the same type
"""

from typing import List, Dict

from pypoker.deck import Card
from pypoker.engine.hand_solver.constants import (
    GAME_TYPE_TEXAS_HOLDEM,
    HAND_TYPE_STRAIGHT_FLUSH,
    HAND_TYPE_QUADS,
    HAND_TYPE_FULL_HOUSE,
    HAND_TYPE_FLUSH,
    HAND_TYPE_STRAIGHT,
    HAND_TYPE_TRIPS,
    HAND_TYPE_TWO_PAIR,
    HAND_TYPE_PAIR,
    HAND_TYPE_HIGH_CARD,
)
from pypoker.engine.hand_solver.functions.shared import (
    _check_game_type,
    _check_hand_type,
    _check_kwargs,
)
from pypoker.engine.hand_solver.utils import (
    hand_is_ace_low_straight,
    hand_highest_value_tuple,
)


###################
#  PUBLIC METHOD  #
###################
def describe_hand(game_type: str, hand_type: str, **kwargs: Dict) -> str:
    """
    Public method that gives a string representation of a hand type

    :param game_type: indicates what type of poker game you are playing. Tested against constants.GAME_TYPES
    :param hand_type: indicates the hand type you are testing for. Tested against constants.<GAME_TYPE>_HAND_TYPES
    :param kwargs: Unbounded keyword arguments list required for the implementation of the rank_hand_type method you
                   are using. Arguments passed to this command are be validated before calling underlying implementation
    :return: String describing the characteristics of the hand
    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    rank_key = f"{game_type}-{hand_type}"

    kwargs_required_keys, describe_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}": (
            ["hand"],
            _hand_description_straight_flush,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}": (
            ["hand"],
            _hand_description_quads,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}": (
            ["hand"],
            _hand_description_full_house,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}": (
            ["hand"],
            _hand_description_flush,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}": (
            ["hand"],
            _hand_description_straight,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}": (
            ["hand"],
            _hand_description_trips,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}": (
            ["hand"],
            _hand_description_two_pair,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}": (
            ["hand"],
            _hand_description_pair,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}": (
            ["hand"],
            _hand_description_high_card,
        ),
    }[rank_key]

    _check_kwargs(kwargs, kwargs_required_keys)
    return describe_method(**kwargs)


###################################################
#  PRIVATE IMPLEMENTATION METHODS - TEXAS HOLDEM  #
###################################################
def _hand_description_straight_flush(hand: List[Card]):
    """
    Private method that produces the proper hand description for a straight flush hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    hand.sort(key=lambda card: card.value, reverse=True)
    if hand_is_ace_low_straight(hand):
        return f"Straight Flush ({hand[1].rank} to {hand[0].rank})"
    else:
        return f"Straight Flush ({hand[0].rank} to {hand[4].rank})"


def _hand_description_quads(hand: List[Card]):
    """
    Private method that produces the proper hand description for a quads hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    quads_value = hand_highest_value_tuple(hand, 4)
    quads_rank = list(filter(lambda card: card.value == quads_value, hand))[0].rank
    kicker = list(filter(lambda card: card.value != quads_value, hand))
    if kicker:
        return f"Quads ({quads_rank}s with {kicker[0].rank} kicker)"
    else:
        return f"Quads ({quads_rank}s)"


def _hand_description_full_house(hand: List[Card]):
    """
    Private method that produces the proper hand description for a full house hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    trips_value = hand_highest_value_tuple(hand, 3)
    trips_rank = list(filter(lambda card: card.value == trips_value, hand))[0].rank
    remaining_cards = filter(lambda card: card.value != trips_value, hand)
    pair_value = hand_highest_value_tuple(remaining_cards, 2)
    pair_rank = list(filter(lambda card: card.value == pair_value, hand))[0].rank
    return f"Full House ({trips_rank}s full of {pair_rank}s)"


def _hand_description_flush(hand: List[Card]):
    """
    Private method that produces the proper hand description for flush hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    hand.sort(key=lambda card: card.value, reverse=True)
    return f"Flush ({hand[0].rank}, {hand[1].rank}, {hand[2].rank}, {hand[3].rank}, {hand[4].rank})"


def _hand_description_straight(hand: List[Card]):
    """
    Private method that produces the proper hand description for straight hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    hand.sort(key=lambda card: card.value, reverse=True)
    if hand_is_ace_low_straight(hand):
        return f"Straight ({hand[1].rank} to {hand[0].rank})"
    else:
        return f"Straight ({hand[0].rank} to {hand[4].rank})"


def _hand_description_trips(hand: List[Card]):
    """
    Private method that produces the proper hand description for a quads hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    trips_value = hand_highest_value_tuple(hand, 3)
    trips_rank = list(filter(lambda card: card.value == trips_value, hand))[0].rank
    kickers = list(filter(lambda card: card.value != trips_value, hand))

    if not kickers:
        return f"Trips ({trips_rank}s)"

    kickers.sort(key=lambda card: card.value, reverse=True)
    kickers_rank = [card.rank for card in kickers]
    return f"Trips ({trips_rank}s with kickers {', '.join(kickers_rank)})"


def _hand_description_two_pair(hand: List[Card]):
    """
    Private method that produces the proper hand description for a two pair hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    higher_pair_value = hand_highest_value_tuple(hand, 2)
    higher_pair_rank = list(filter(lambda card: card.value == higher_pair_value, hand))[
        0
    ].rank

    remaining_cards = list(filter(lambda card: card.value != higher_pair_value, hand))
    lower_pair_value = hand_highest_value_tuple(remaining_cards, 2)
    lower_pair_rank = list(
        filter(lambda card: card.value == lower_pair_value, remaining_cards)
    )[0].rank

    kicker = list(filter(lambda card: card.value != lower_pair_value, remaining_cards))

    if kicker:
        return f"Two Pair ({higher_pair_rank}s and {lower_pair_rank}s with kicker {kicker[0].rank})"
    else:
        return f"Two Pair ({higher_pair_rank}s and {lower_pair_rank}s)"


def _hand_description_pair(hand: List[Card]):
    """
    Private method that produces the proper hand description for a pair hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    pair_value = hand_highest_value_tuple(hand, 2)
    pair_rank = list(filter(lambda card: card.value == pair_value, hand))[0].rank

    kickers = list(filter(lambda card: card.value != pair_value, hand))

    if kickers:
        kickers.sort(key=lambda card: card.value, reverse=True)
        kickers = [kicker.rank for kicker in kickers]
        return f"Pair ({pair_rank}s with kickers {', '.join(kickers)})"
    else:
        return f"Pair ({pair_rank}s)"


def _hand_description_high_card(hand: List[Card]):
    """
    Private method that produces the proper hand description for a high card hand.

    :param hand: List of Card objects representing a players hand
    :return: String of the hand description
    """

    hand.sort(key=lambda card: card.value, reverse=True)
    ranks = [card.rank for card in hand]

    return f"High Card ({', '.join(ranks)})"
