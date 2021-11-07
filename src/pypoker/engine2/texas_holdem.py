"""
pypoker.engine.texas_holdem module
----------------------------------

module containing the poker engine for the texas holdem game type.
inherits from the BasePokerEngine class.
"""
import itertools
from typing import List

from pypoker.deck import Card, CARD_SUITS
from pypoker.engine2 import BasePokerEngine
from pypoker.exceptions import InvalidHandError
from pypoker.player import BasePlayer


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
    TH_HAND_HIGH_CARD
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
    TH_HAND_HIGH_CARD: 1
}


class TexasHoldemPokerEngine(BasePokerEngine):
    """
    concrete implementation of the PokerEngine class for Texas Hold'em game type
    """

    # Concrete Implementation of public methods
    def find_player_best_hand(self, player: BasePlayer, board: List[Card], **kwargs):
        """
        Find a given players best possible hand with the current cards available.

        :param player: the Player object to find the best hand for
        :param board: list containing the current board cards. If preflop then this list should be empty
        """

        available_cards = player.hole_cards + board

        for hand_type in TH_HANDS_ORDERED:
            made_hands = {
                TH_HAND_STRAIGHT_FLUSH: self.make_straight_flush_hands,
                TH_HAND_QUADS: self._make_quads_hands,
                TH_HAND_FULL_HOUSE: self._make_full_house_hands,
                TH_HAND_FLUSH: self._make_flush_hands,
                TH_HAND_STRAIGHT: self._make_make_straight_hands,
                TH_HAND_TRIPS: self._make_trips_hands,
                TH_HAND_TWO_PAIR: self._make_two_pair_hands,
                TH_HAND_PAIR: self._make_pair_hands,
                TH_HAND_HIGH_CARD: self._make_high_card_hands
            }[hand_type](available_cards)

            if made_hands:
                return made_hands[0]

    # Public make_hands_of_type methods
    def make_straight_flush_hands(self, available_cards: List[Card]):
        """
        Texas Holdem Poker Engine hand maker method
        tests to see if any straight flush hands can be made from the given set of cards
        """

        if len(available_cards) < 5:
            return []

        suits_grouped = {suit: [card for card in available_cards if card.suit == suit] for suit in CARD_SUITS}
        eligible_suits = [cards for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return []

        for cards in eligible_suits:
            cards = sorted(cards, key=lambda card: card.value)
            runs = self.find_runs_of_cards(cards, treat_ace_low=True, run_size=5)




    # Public test_hand_is_type methods
    @staticmethod
    def hand_is_straight_flush(hand: List[Card]):
        """
        Texas Holdem Poker Engine hand tester method
        tests to see if the given hand is a straight flush

        :param hand: List of cards representing a players hand.
        """

        if len(hand) > 5:
            raise InvalidHandError(
                f"Texas Hold'em poker hands can have a maximum of 5 cards. Hand provided has {len(hand)}"
            )

        if len(hand) < 5:
            return False

        suits_grouped = {suit: [card for card in hand if card.suit == suit] for suit in CARD_SUITS}
        eligible_suits = [cards.value for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return False

        for cards in eligible_suits:
            return sorted(cards) == list(range(min(cards), max(cards) + 1))
