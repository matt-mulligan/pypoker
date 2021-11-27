"""
pypoker.engine.texas_holdem module
----------------------------------

module containing the poker engine for the texas holdem game type.
inherits from the BasePokerEngine class.
"""
from itertools import combinations
from typing import List

from pypoker.constants import TH_HANDS_ORDERED, TH_HAND_STRAIGHT_FLUSH, TH_HAND_QUADS, TH_HAND_FULL_HOUSE, \
    TH_HAND_FLUSH, TH_HAND_STRAIGHT, TH_HAND_TRIPS, TH_HAND_TWO_PAIR, TH_HAND_PAIR, TH_HAND_HIGH_CARD, GAME_TEXAS_HOLDEM
from pypoker.constructs import Card, Hand
from pypoker.engine2 import BasePokerEngine
from pypoker.player import BasePlayer


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
    def make_straight_flush_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible straight flush hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each straight flush hand possible.
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
        straight_flushes = [val for sublist in straight_flushes for val in sublist]

        hands = []
        for cards in straight_flushes:
            tiebreaker = [max([card.value for card in cards])]
            if tiebreaker == [14] and any(card.value == 5 for card in cards):
                tiebreaker = [5]
            hands.append(Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, cards, tiebreaker))

        return sorted(hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_quads_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible quads hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each quad hand possible.
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
            if not other_cards:  # manages for the usecase of only getting 4 cards of the same value and no kickers
                quad_hands.append(
                    Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, quad_cards, [quad_value, None])
                )
            else:
                quad_hands.extend([
                    Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, quad_cards + [card], [quad_value, card.value])
                    for card in other_cards
                ])

        return sorted(quad_hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_full_house_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible full house hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each full house hand possible.
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
                Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, trip_combo + pair_combo, [trip_value, pair_combo[0].value])
                for trip_combo in trip_combos for pair_combo in pair_combos
                if pair_combo[0].value != trip_value
            ]

            full_houses.extend(hands)

        return sorted(full_houses, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_flush_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible flush hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each flush hand possible.
        """

        if len(available_cards) < 5:
            return []

        suits_grouped = self.group_cards_by_suit(available_cards)
        eligible_suits = [cards for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return []

        flushes = [self.find_all_unique_card_combos(cards, 5) for cards in eligible_suits]
        flushes = [val for sublist in flushes for val in sublist]
        flushes = [
            Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, cards, sorted([card.value for card in cards], reverse=True))
            for cards in flushes
        ]

        return sorted(flushes, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_straight_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible straight hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each straight hand possible.
        """

        if len(available_cards) < 5:
            return []

        straights = self.find_consecutive_value_cards(available_cards, treat_ace_low=True, run_size=5)

        hands = []
        for cards in straights:
            tiebreaker = [max([card.value for card in cards])]
            if tiebreaker == [14] and any(card.value == 5 for card in cards):
                tiebreaker = [5]
            hands.append(Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, cards, tiebreaker))

        return sorted(hands, key=lambda hand: hand.tiebreakers, reverse=True)

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

    def make_two_pair_hands(self, available_cards: List[Card], include_kickers: bool = True) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible two-pair hands with the given cards, optionally including kickers.
        Note that this method will build ONLY two-pair hands, and exclude any hands that feature two-pairs but
        technically is a stronger hand. for example, if given three queens(QH-QS-QC), two aces(AH-AS) and a four(4S),
        this method would return you hands that do not feature all three queens as this would instead be trips or
        full houses and they are stronger hands than two-pair

        :param available_cards: List of card objects available to use.
        :param include_kickers: Boolean indicating if the returned hands should include the kicker cards or
            if the combinations should just be the cards required to make the two-pair.
            Note that setting this to true will return many more hands as it builds all hands possible with kickers.
        :return: List of lists of card objects representing all of the two-pairs that could be made.
        """

        if len(available_cards) < 4:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = {
            key: cards for key, cards in value_grouped_cards.items() if len(cards) >= 2
        }

        if len(eligible_values) < 2:
            return []

        two_pair_values = list(eligible_values.keys())
        two_pair_value_combos = [list(value) for value in combinations(two_pair_values, 2)]

        two_pair_hands = []
        for two_pair_value_list in two_pair_value_combos:
            two_pair_value_a = two_pair_value_list[0]
            two_pair_value_b = two_pair_value_list[1]

            two_pairs_a = self.find_all_unique_card_combos(eligible_values[two_pair_value_a], 2)
            two_pairs_b = self.find_all_unique_card_combos(eligible_values[two_pair_value_b], 2)
            two_pair_sets = [a + b for a in two_pairs_a for b in two_pairs_b]

            kicker_cards = [cards for value, cards in value_grouped_cards.items() if value not in two_pair_value_list]
            kicker_cards = [val for sublist in kicker_cards for val in sublist]

            if not include_kickers or not kicker_cards:
                two_pair_hands.extend(two_pair_sets)
                continue

            for two_pair_cards in two_pair_sets:
                two_pair_hands.extend([two_pair_cards + [kicker] for kicker in kicker_cards])

        return two_pair_hands

    def make_pair_hands(self, available_cards: List[Card], include_kickers: bool = True) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible pair hands with the given cards, optionally including kickers.
        Note that this method will build ONLY pair hands, and exclude any hands that feature a pair but
        technically is a stronger hand. for example, if given three queens(QH-QS-QC), two aces(AH-AS) and a four(4S),
        this method would return you hands that do not feature a pair of aces and a pair of queens as this would
        instead be a two-pair hand and they are stronger hands than pairs

        :param available_cards: List of card objects available to use.
        :param include_kickers: Boolean indicating if the returned hands should include the kicker cards or
            if the combinations should just be the cards required to make the pair.
            Note that setting this to true will return many more hands as it builds all hands possible with kickers.
        :return: List of lists of card objects representing all of the pairs that could be made.
        """

        if len(available_cards) < 2:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = {
            key: cards for key, cards in value_grouped_cards.items() if len(cards) >= 2
        }

        if not eligible_values:
            return []

        pair_hands = []
        for pair_value, pair_cards in eligible_values.items():
            pairs = self.find_all_unique_card_combos(pair_cards, 2)
            kicker_cards = [card for card in available_cards if card.value != pair_value]

            if not include_kickers or not kicker_cards:
                pair_hands.extend(pairs)
                continue

            kicker_sets = self.find_all_unique_card_combos(kicker_cards, 3)
            kicker_sets = [kicker_set for kicker_set in kicker_sets if self.check_all_card_values_unique(kicker_set)]

            if kicker_sets:
                pair_hands.extend([pair_set + kicker_set for pair_set in pairs for kicker_set in kicker_sets])
                continue

            kicker_sets = self.find_all_unique_card_combos(kicker_cards, 2)
            kicker_sets = [kicker_set for kicker_set in kicker_sets if self.check_all_card_values_unique(kicker_set)]

            if kicker_sets:
                pair_hands.extend([pair_set + kicker_set for pair_set in pairs for kicker_set in kicker_sets])
                continue

            pair_hands.extend([pair_set + [card] for pair_set in pairs for card in kicker_cards])

        return pair_hands
