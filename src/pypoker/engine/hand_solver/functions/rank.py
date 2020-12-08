"""
FUNCTIONS.RANK MODULE

this module contains the implementation of all hand ranking logic for hands of the same type
"""
from typing import List, Dict

from pypoker.deck import Card
from pypoker.engine.hand_solver.constants import GAME_TYPE_TEXAS_HOLDEM, HAND_TYPE_STRAIGHT_FLUSH, \
    HAND_TYPE_QUADS, HAND_TYPE_FULL_HOUSE, HAND_TYPE_FLUSH, HAND_TYPE_STRAIGHT, HAND_TYPE_TRIPS, HAND_TYPE_TWO_PAIR, \
    HAND_TYPE_PAIR, HAND_TYPE_HIGH_CARD
from pypoker.engine.hand_solver.functions.shared import _check_game_type, _check_hand_type, _check_kwargs
from pypoker.engine.hand_solver.utils import hand_is_ace_low_straight, order_hands_highest_card, \
    hands_have_same_card_values, hand_highest_value_tuple


###################
#  PUBLIC METHOD  #
###################
def rank_hand_type(game_type: str, hand_type: str, **kwargs: Dict) -> Dict:
    """
    Public method that ranks hands of a specific type against each other

    :param game_type: indicates what type of poker game you are playing. Tested against constants.GAME_TYPES
    :param hand_type: indicates the hand type you are testing for. Tested against constants.<GAME_TYPE>_HAND_TYPES
    :param kwargs: Unbounded keyword arguments list required for the implementation of the rank_hand_type method you
                   are using. Arguments passed to this command are be validated before calling underlying implementation
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    rank_key = f"{game_type}-{hand_type}"

    kwargs_required_keys, rank_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}": (["hands"], _rank_straight_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}": (["hands"], _rank_quads),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}": (["hands"], _rank_full_house),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}": (["hands"], _rank_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}": (["hands"], _rank_straight),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}": (["hands"], _rank_trips),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}": (["hands"], _rank_two_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}": (["hands"], _rank_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}": (["hands"], _rank_high_card),
    }[rank_key]

    _check_kwargs(kwargs, kwargs_required_keys)
    return rank_method(**kwargs)


###################################################
#  PRIVATE IMPLEMENTATION METHODS - TEXAS HOLDEM  #
###################################################
def _rank_straight_flush(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best straight flush hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a straight flush hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    ordered_hands = order_hands_highest_card(hands)
    ordered_hands = _reorder_ace_low_straight_hands(ordered_hands)

    ranked_hands = {1: [ordered_hands[0]]}

    for hand in ordered_hands[1:]:
        current_rank = max(ranked_hands.keys())

        if hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
            ranked_hands[current_rank].append(hand)
        else:
            current_rank += 1
            ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_quads(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best quads hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a quads hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    hands_quads = [(hand, hand_highest_value_tuple(hand, 4)) for hand in hands]
    quad_values = list(set([tup[1] for tup in hands_quads]))
    quad_values.sort(reverse=True)

    ranked_hands = dict()

    for quad_value in quad_values:
        quad_value_hands = filter(
            lambda hand_tuple: hand_tuple[1] == quad_value, hands_quads
        )
        quad_value_hands = order_hands_highest_card(
            [tup[0] for tup in quad_value_hands]
        )

        current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
        ranked_hands[current_rank] = [quad_value_hands[0]]

        for hand in quad_value_hands[1:]:
            if hands_have_same_card_values(
                    hand, ranked_hands[current_rank][0]
            ):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_full_house(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best full house hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a full house hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    ordered_hands = []

    for hand in hands:
        trips_value = hand_highest_value_tuple(hand, 3)
        remaining_cards = filter(lambda card: card.value != trips_value, hand)
        pair_value = hand_highest_value_tuple(remaining_cards, 2)
        ordered_hands.append((hand, trips_value, pair_value))

    ordered_hands.sort(key=lambda tup: (tup[1], tup[2]), reverse=True)

    current_rank = 1
    ranked_hands = {current_rank: [ordered_hands[0][0]]}
    current_trip = ordered_hands[0][1]
    current_pair = ordered_hands[0][2]

    for hand, trip, pair in ordered_hands[1:]:
        if current_trip == trip and current_pair == pair:
            ranked_hands[current_rank].append(hand)
        else:
            current_rank += 1
            current_trip = trip
            current_pair = pair
            ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_flush(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best flush hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a flush hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    ordered_hands = order_hands_highest_card(hands)
    ranked_hands = {1: [ordered_hands[0]]}

    for hand in ordered_hands[1:]:
        current_rank = max(ranked_hands.keys())

        if hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
            ranked_hands[current_rank].append(hand)
        else:
            current_rank += 1
            ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_straight(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best straight hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a straight hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    ordered_hands = order_hands_highest_card(hands)
    ordered_hands = _reorder_ace_low_straight_hands(ordered_hands)
    ranked_hands = {1: [ordered_hands[0]]}

    for hand in ordered_hands[1:]:
        current_rank = max(ranked_hands.keys())

        if hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
            ranked_hands[current_rank].append(hand)
        else:
            current_rank += 1
            ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_trips(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best trips hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a trips hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    hands_trips = [(hand, hand_highest_value_tuple(hand, 3)) for hand in hands]
    trips_values = list(set([tup[1] for tup in hands_trips]))
    trips_values.sort(reverse=True)

    ranked_hands = dict()

    for trips_value in trips_values:
        trips_value_hands = filter(
            lambda hand_tuple: hand_tuple[1] == trips_value, hands_trips
        )
        trips_value_hands = order_hands_highest_card(
            [tup[0] for tup in trips_value_hands]
        )

        current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
        ranked_hands[current_rank] = [trips_value_hands[0]]

        for hand in trips_value_hands[1:]:
            if hands_have_same_card_values(
                    hand, ranked_hands[current_rank][0]
            ):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_two_pair(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best two pair hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a two pair hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    hands_two_pair_kicker = []

    for hand in hands:
        high_pair_value = hand_highest_value_tuple(hand, 2)
        remaining_cards = filter(lambda card: card.value != high_pair_value, hand)
        low_pair_value = hand_highest_value_tuple(remaining_cards, 2)
        kicker_value = list(
            filter(
                lambda card: card.value != high_pair_value
                             and card.value != low_pair_value,
                hand,
            )
        )[0].value
        hands_two_pair_kicker.append(
            (hand, high_pair_value, low_pair_value, kicker_value)
        )

    hands_two_pair_kicker.sort(
        key=lambda tup: (tup[1], tup[2], tup[3]), reverse=True
    )

    current_rank = 1
    current_high_pair = hands_two_pair_kicker[0][1]
    current_low_pair = hands_two_pair_kicker[0][2]
    current_kicker = hands_two_pair_kicker[0][3]
    ranked_hands = {current_rank: [hands_two_pair_kicker[0][0]]}

    for hand, high_pair, low_pair, kicker in hands_two_pair_kicker[1:]:
        if (
                high_pair == current_high_pair
                and low_pair == current_low_pair
                and kicker == current_kicker
        ):
            ranked_hands[current_rank].append(hand)
        else:
            current_rank += 1
            current_high_pair = high_pair
            current_low_pair = low_pair
            current_kicker = kicker
            ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_pair(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best pair hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a pair hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    hands_pair = [(hand, hand_highest_value_tuple(hand, 2)) for hand in hands]
    pair_values = list(set([tup[1] for tup in hands_pair]))
    pair_values.sort(reverse=True)

    ranked_hands = dict()

    for pair_value in pair_values:
        pair_value_hands = filter(
            lambda hand_tuple: hand_tuple[1] == pair_value, hands_pair
        )
        pair_value_hands = order_hands_highest_card(
            [tup[0] for tup in pair_value_hands]
        )

        current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
        ranked_hands[current_rank] = [pair_value_hands[0]]

        for hand in pair_value_hands[1:]:
            if hands_have_same_card_values(
                    hand, ranked_hands[current_rank][0]
            ):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

    return ranked_hands


def _rank_high_card(hands: List[List[Card]]):
    """
    Private tiebreaker method to determine the best high card hand in the list of hands

    :param hands: List of list of cards. each internal list of cards represents a high card hand
    :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
        If there are tied hands, then multiple hands will appear as the value for that rank.
    """

    ordered_hands = order_hands_highest_card(hands)
    ranked_hands = {1: [ordered_hands[0]]}

    for hand in ordered_hands[1:]:
        current_rank = max(ranked_hands.keys())

        if hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
            ranked_hands[current_rank].append(hand)
        else:
            current_rank += 1
            ranked_hands[current_rank] = [hand]

    return ranked_hands


#########################
#  MISC HELPER METHODS  #
#########################
def _reorder_ace_low_straight_hands(ordered_hands):
    """
    Private helper method to reorder ace low straight hands to end of ordered hands list
    :param ordered_hands:
    :return:
    """

    ace_low_straight_hands = [
        True if hand_is_ace_low_straight(hand) else False
        for hand in ordered_hands
    ]
    ace_low_straight_index_hand = [
        (index, ordered_hands[index])
        for index, is_ace_low_straight in enumerate(ace_low_straight_hands)
        if is_ace_low_straight
    ]
    ace_low_straight_index_hand.sort(key=lambda tup: tup[0], reverse=True)

    for index, hand in ace_low_straight_index_hand:
        del ordered_hands[index]
        ordered_hands.append(hand)

    return ordered_hands
