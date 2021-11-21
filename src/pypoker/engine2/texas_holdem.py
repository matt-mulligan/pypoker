"""
pypoker.engine.texas_holdem module
----------------------------------

module containing the poker engine for the texas holdem game type.
inherits from the BasePokerEngine class.
"""
from itertools import product
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


class TexasHoldemPokerEngine(BasePokerEngine):
    """
    concrete implementation of the PokerEngine class for Texas Hold'em game type
    """

    # Concrete Implementation of public methods
    # -----------------------------------------
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
                TH_HAND_QUADS: self.make_quads_hands,
                TH_HAND_FULL_HOUSE: self.make_full_house_hands,
                TH_HAND_FLUSH: self.make_flush_hands,
                TH_HAND_STRAIGHT: self.make_straight_hands,
                TH_HAND_TRIPS: self.make_trips_hands,
                TH_HAND_TWO_PAIR: self.make_two_pair_hands,
                TH_HAND_PAIR: self.make_pair_hands,
                TH_HAND_HIGH_CARD: self.make_high_card_hands,
            }[hand_type](available_cards)

            if made_hands:
                return made_hands[0]

    # Public "Hand Maker" methods
    # ---------------------------
    def make_straight_flush_hands(
        self, available_cards: List[Card]
    ) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible straight flush hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: List of lists of card objects representing all of the straight flushes that could be made.
        """

        if len(available_cards) < 5:
            return []

        suits_grouped = self.group_cards_by_suit(available_cards)
        eligible_suits = [cards for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return []

        straight_flushes = [
            self.find_consecutive_value_cards(cards, treat_ace_low=True, run_size=5)
            for cards in eligible_suits
        ]
        return [val for sublist in straight_flushes for val in sublist]

    def make_quads_hands(self, available_cards: List[Card]) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible quads hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: List of lists of card objects representing all of the quads that could be made.
        """

        if len(available_cards) < 4:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = [
            key for key, cards in value_grouped_cards.items() if len(cards) == 4
        ]
        if not eligible_values:
            return []

        quad_hands = []
        for quad_value in eligible_values:
            quad_cards = value_grouped_cards[quad_value]
            other_cards = [card for card in available_cards if card.value != quad_value]
            if (
                not other_cards
            ):  # manages for the usecase of only getting 4 cards of the same value and no kickers
                quad_hands.append(quad_cards)
            else:
                quad_hands.extend([quad_cards + [card] for card in other_cards])

        return quad_hands

    def make_full_house_hands(self, available_cards: List[Card]) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible full house hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: List of lists of card objects representing all of the full houses that could be made.
        """

        if len(available_cards) < 5:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        trips_values = [
            key for key, cards in value_grouped_cards.items() if len(cards) >= 3
        ]
        pair_values = [
            key for key, cards in value_grouped_cards.items() if len(cards) >= 2
        ]

        pair_combos = [
            self.find_all_unique_card_combos(value_grouped_cards[value], 2)
            for value in pair_values
        ]
        pair_combos = [val for sublist in pair_combos for val in sublist]

        full_houses = []
        for trip_value in trips_values:
            trip_cards = value_grouped_cards[trip_value]
            trip_combos = self.find_all_unique_card_combos(trip_cards, 3)
            hands = [
                [
                    trip_combo + pair_combo
                    for pair_combo in pair_combos
                    if pair_combo[0].value != trip_value
                ]
                for trip_combo in trip_combos
            ]
            full_houses.extend([val for sublist in hands for val in sublist])

        return full_houses

    def make_flush_hands(self, available_cards: List[Card]) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible flush hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: List of lists of card objects representing all of the full houses that could be made.
        """

        if len(available_cards) < 5:
            return []

        suits_grouped = self.group_cards_by_suit(available_cards)
        eligible_suits = [cards for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return []

        flushes = [self.find_all_unique_card_combos(cards, 5) for cards in eligible_suits]
        return [val for sublist in flushes for val in sublist]

    def make_straight_hands(self, available_cards: List[Card]) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible straight hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: List of lists of card objects representing all of the straights that could be made.
        """

        if len(available_cards) < 5:
            return []

        return self.find_consecutive_value_cards(available_cards, treat_ace_low=True, run_size=5)

    def make_trips_hands(self, available_cards: List[Card], include_kickers: bool = True) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible trips hands with the given cards.
        Note that this method will build ONLY trips hands, and exclude any hands that feature three of a kind but
        technically is a stronger hand. for example, if given three queens(QH-QS-QC), two aces(AH-AS) and a four(4S),
        this method would return you only two possible trips hands, (QH-QS-QC-AH-4S) and (QH-QS-QC-AS-4S)
        The other option for a full hand here would give a full house instead, which means it is excluded from
        this method.

        :param available_cards: List of card objects available to use.
        :param include_kickers: Boolean indicating if the returned hands should include the kicker cards or
            if the combinations should just be the cards required to make the trips.
            Note that setting this to true will return many more hands as it builds all hands possible with kickers.
        :return: List of lists of card objects representing all of the trips that could be made.
        """

        if len(available_cards) < 3:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = {
            key: cards for key, cards in value_grouped_cards.items() if len(cards) >= 3
        }

        if not eligible_values:
            return []

        trip_hands = []
        for trip_value, trip_cards in eligible_values.items():
            trip_card_combos = self.find_all_unique_card_combos(trip_cards, 3)

            if not include_kickers:
                trip_hands.extend(trip_card_combos)
            else:
                kicker_cards = [cards for key, cards in value_grouped_cards.items() if key != trip_value]
                kicker_cards = [val for sublist in kicker_cards for val in sublist]
                kicker_cards_combos = self.find_all_unique_card_combos(kicker_cards, 2)

                kicker_cards_combos = [
                    card_combo for card_combo in kicker_cards_combos if card_combo[0].value != card_combo[1].value
                ]

                full_trip_hands = [
                    [trip_combo + kicker_combo for trip_combo in trip_card_combos]
                    for kicker_combo in kicker_cards_combos
                ]

                trip_hands.extend([val for sublist in full_trip_hands for val in sublist])

        return trip_hands




