"""
HAND_SOLVER.UTIL MODULE

This module holds small utility functions that are used throughout the hand solver package.
functions are a good candiate for this package if they are used by both the the functions logic and
class implementations.
"""
import collections
from itertools import combinations
from typing import List

from pypoker.constructs import Card


def hand_all_same_suit(hand):
    """
    This method will check if all cards in the hand have the same suit.

    :param hand: List of Card objects
    :return: Boolean, True if all cards in hand have the same suit, False otherwise.
    """

    suit = hand[0].suit
    return all(card.suit == suit for card in hand)


def hand_values_continuous(hand, allow_ace_low=True):
    """
    This private method will check if the cards provided in the hand are a straight
    (their values are continuous without gaps)
    This method does not assert the number of cards in the hand.

    :param hand: List of Card objects representing the players hand
    :param allow_ace_low: Boolean indicating if for this assessment you should allow Ace cards to be a low value (1) as well
    :return: Boolean. True of the ard values are continuous, False if not
    """

    hand.sort(key=lambda card: card.value, reverse=False)
    card_value_list = [card.value for card in hand]
    normal_values_continuous = all(
        a + 1 == b for a, b in zip(card_value_list, card_value_list[1:])
    )

    card_values_ace_low = [value if value != 14 else 1 for value in card_value_list]
    card_values_ace_low.sort(reverse=False)
    ace_low_continuous = all(
        a + 1 == b for a, b in zip(card_values_ace_low, card_values_ace_low[1:])
    )

    if allow_ace_low:
        return normal_values_continuous or ace_low_continuous
    else:
        return normal_values_continuous


def hand_highest_value_tuple(hand, tuple_length):
    """
    This method will check if the hand provided has a tuple of any value of card of the specified length.
    this method can be used to check if the hand has a pair (tuple_length=2), trips (tuple_length=3) or
    quads (tuple_length=4).

    if hand has multiple tuples of the specified length, the maximum is returned.
    e.g. tuple_length = 2 and hand is 7,9,10,9,7 then 9 is returned for tuple_card_value

    if a card value has more occurences than the specified tuple length, ot will still be returned.
    e.g. hand = [7,4,7,7,8], tuple length = 2, method returns (True, 7)

    :param hand: List of Card objects
    :param tuple_length: Int definign if looking for pairs(2) trips(3) or quads(4)
    :return: Int of the highest value tuple in the hand, return None if no tuple present in hand
    """

    card_values = [card.value for card in hand]
    occurances = collections.Counter(card_values)

    matches = [key for key, value in occurances.items() if value >= tuple_length]
    return None if not matches else max(matches)


def hand_is_ace_low_straight(hand: List[Card]):
    """
    This public method will check if the hand you have provided is an ace low straight (5, 4, 3, 2, A).

    :param hand: list of card objects rperesenting a players hand
    :return: Boolean indiciating if the hand is an ace low straight
    """

    hand.sort(key=lambda card: card.value, reverse=True)
    card_values = [card.value for card in hand]
    return card_values == [14, 5, 4, 3, 2]


def order_hands_highest_card(hands: List[List[Card]], winner_only=False):
    """
    Shared hand comparison method that orders hands based on their highest card.

    :param hands: List[Card] cards in a players hand
    :return: List of List[Card] ordered by high card
    """

    for hand_obj in hands:
        hand_obj.sort(key=lambda card: card.value, reverse=True)

    hands.sort(key=lambda hand: tuple(card.value for card in hand), reverse=True)
    return hands[0] if winner_only else hands


def hands_have_same_card_values(hand_a, hand_b):
    """
    shared hand comparison method that checks if the two hands have the same value cards
    :param hand_a:
    :param hand_b:
    :return:
    """

    hand_a.sort(key=lambda card: card.value, reverse=True)
    hand_b.sort(key=lambda card: card.value, reverse=True)
    return all(card_a.value == card_b.value for card_a, card_b in zip(hand_a, hand_b))


def get_all_combinations(
    hole_cards: List[Card], board_cards: List[Card], hand_size: int
):
    """
    This private method will get all possible hand combinations for a

    :param hole_cards: List of Card objects representing the players hole
    :param board_cards: List of Card objects representing the communal cards
    :param hand_size: Int representing what size hands to produce.

    :return: list of card objects
    """

    all_cards = hole_cards.copy()
    all_cards.extend(board_cards)
    all_combinations = [
        list(cards) for cards in list(combinations(all_cards, hand_size))
    ]

    return all_combinations
