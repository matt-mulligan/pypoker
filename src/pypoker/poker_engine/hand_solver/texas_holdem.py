from typing import List

from pypoker.deck import Card
from pypoker.poker_engine.hand_solver.base import BaseHandSolver
from pypoker.poker_engine.hand_solver.constants import HAND_TITLE, HAND_RANK, HAND_TEST_METHOD, BEST_HAND


class TexasHoldemHandSolver(BaseHandSolver):
    """
    The Texas Hold'em implementation of the BaseHandSolver class.
    Responsible for determining a players best hand
    """

    def __init__(self):
        self._hand_ranks = [
            {HAND_TITLE: "Straight Flush", HAND_RANK: 1, HAND_TEST_METHOD: self._test_straight_flush},
            {HAND_TITLE: "Quads", HAND_RANK: 2, HAND_TEST_METHOD: self._test_quads},
            {HAND_TITLE: "Full House", HAND_RANK: 3, HAND_TEST_METHOD: self._test_full_house},
            {HAND_TITLE: "Flush", HAND_RANK: 4, HAND_TEST_METHOD: self._test_flush},
            {HAND_TITLE: "Straight", HAND_RANK: 5, HAND_TEST_METHOD: self._test_straight},
            {HAND_TITLE: "Trips", HAND_RANK: 6, HAND_TEST_METHOD: self._test_trips},
            {HAND_TITLE: "Two Pair", HAND_RANK: 7, HAND_TEST_METHOD: self._test_two_pair},
            {HAND_TITLE: "Pair", HAND_RANK: 8, HAND_TEST_METHOD: self._test_pair},
            {HAND_TITLE: "High Card", HAND_RANK: 9, HAND_TEST_METHOD: self._test_high_card}
        ]

    def find_best_hand(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Abstract method to implement to find a players best hand.

        :param hole_cards: List of card objects, representing the players hole cards
        :param board_cards: List of card objects, representing the board cards available to use.
        :return: dictionary of player hand information. including at least the following keys:
        {
            "best_hand": List of card objects representing the players best hand
            "hand_title": Str the english title of the best hand type the player has (Straight, Flush, Two Pair, etc)
            "hand_rank": Int ranking of the hand type, with 1 signifying the best type of hand (e.g. straight flush
                         would have a ranking of 1 in texas holdem)
        }
        child classes implementing this abstract method can choose to expand the dictionary where
        appropriate but must at minimum have the above keys
        """

        for hand_type in self._hand_ranks:
            is_hand_type, cards = hand_type[HAND_TEST_METHOD](hole_cards, board_cards)

            if is_hand_type:
                return {
                    BEST_HAND: cards,
                    HAND_TITLE: hand_type[HAND_TITLE],
                    HAND_RANK: hand_type[HAND_RANK]
                }

    def _test_straight_flush(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a straight flush hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [hand for hand in all_hands
                         if self.hand_all_same_suit(hand) and self.hand_values_continuous(hand)]

        if not matched_hands:
            return False, None

        return True, self.order_hands_highest_card(matched_hands, winner_only=True)

    def _test_quads(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a quads hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [
            (hand, self.hand_highest_value_tuple(hand, 4))
            for hand in all_hands
            if self.hand_highest_value_tuple(hand, 4)
        ]

        if not matched_hands:
            return False, None

        matched_hands.sort(key=lambda tup: tup[1], reverse=True)
        top_quads_value = matched_hands[0][1]
        top_quads_hands = filter(lambda tup: tup[1] == top_quads_value, matched_hands)

        return True, self.order_hands_highest_card([tup[0] for tup in top_quads_hands], winner_only=True)

    def _test_full_house(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a full house hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            trips_value = self.hand_highest_value_tuple(hand, 3)
            remaining_cards = filter(lambda card: card.value != trips_value, hand)
            pair_value = self.hand_highest_value_tuple(remaining_cards, 2)

            if trips_value and pair_value:
                matched_hands.append((hand, trips_value, pair_value))

        if not matched_hands:
            return False, None

        matched_hands.sort(key=lambda tup: (tup[1], tup[2]), reverse=True)
        return True, matched_hands[0][0]

    def _test_flush(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a flush hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [hand for hand in all_hands if self.hand_all_same_suit(hand)]

        if not matched_hands:
            return False, None

        return True, self.order_hands_highest_card(matched_hands, winner_only=True)

    def _test_straight(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a straight hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [hand for hand in all_hands if self.hand_values_continuous(hand)]

        if not matched_hands:
            return False, None

        return True, self.order_hands_highest_card(matched_hands, winner_only=True)

    def _test_trips(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a trips hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)

        matched_hands = [
            (hand, self.hand_highest_value_tuple(hand, 3))
            for hand in all_hands
            if self.hand_highest_value_tuple(hand, 3)
        ]

        if not matched_hands:
            return False, None

        matched_hands.sort(key=lambda tup: tup[1], reverse=True)
        top_trips = matched_hands[0][1]
        top_trips_hands = filter(lambda tup: tup[1] == top_trips, matched_hands)

        return True, self.order_hands_highest_card([tup[0] for tup in top_trips_hands], winner_only=True)

    def _test_two_pair(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a two pair hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            high_pair_value = self.hand_highest_value_tuple(hand, 2)
            remaining_cards = list(filter(lambda card: card.value != high_pair_value, hand))
            low_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)

            if high_pair_value and low_pair_value:
                kicker_value = list(filter(lambda card: card.value != low_pair_value, remaining_cards))[0].value
                matched_hands.append((hand, high_pair_value, low_pair_value, kicker_value))

        if not matched_hands:
            return False, None

        matched_hands.sort(key=lambda tup: (tup[1], tup[2], tup[3]), reverse=True)
        return True, matched_hands[0][0]

    def _test_pair(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a pair hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)

        matched_hands = [
            (hand, self.hand_highest_value_tuple(hand, 2))
            for hand in all_hands
            if self.hand_highest_value_tuple(hand, 2)
        ]

        if not matched_hands:
            return False, None

        matched_hands.sort(key=lambda tup: tup[1], reverse=True)
        top_pair_value = matched_hands[0][1]
        top_pair_hands = filter(lambda tup: tup[1] == top_pair_value, matched_hands)

        return True, self.order_hands_highest_card([tup[0] for tup in top_pair_hands], winner_only=True)

    def _test_high_card(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a high card hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        return True, self.order_hands_highest_card(all_hands, winner_only=True)
