from typing import List, Dict

from pypoker.deck import Card
from pypoker.poker_engine.hand_solver.base import BaseHandSolver
from pypoker.poker_engine.hand_solver.constants import HAND_TITLE, HAND_RANK, TEST_METHOD, BEST_HAND, FIND_BEST_METHOD, \
    HAND_DESCRIPTION, HAND_DESCRIPTION_METHOD


class TexasHoldemHandSolver(BaseHandSolver):
    """
    The Texas Hold'em implementation of the BaseHandSolver class.
    Responsible for determining a players best hand
    """

    def __init__(self):
        self._hand_ranks = [
            {
                HAND_TITLE: "Straight Flush", HAND_RANK: 1, FIND_BEST_METHOD: self._find_best_straight_flush,
                TEST_METHOD: self._test_straight_flush, HAND_DESCRIPTION_METHOD: self._hand_description_straight_flush
            },
            {
                HAND_TITLE: "Quads", HAND_RANK: 2, FIND_BEST_METHOD: self._find_best_quads,
                TEST_METHOD: self._test_quads, HAND_DESCRIPTION_METHOD: self._hand_description_quads
            },
            {
                HAND_TITLE: "Full House", HAND_RANK: 3, FIND_BEST_METHOD: self._find_best_full_house,
                TEST_METHOD: self._test_full_house, HAND_DESCRIPTION_METHOD: self._hand_description_full_house
            },
            {
                HAND_TITLE: "Flush", HAND_RANK: 4, FIND_BEST_METHOD: self._find_best_flush,
                TEST_METHOD: self._test_flush, HAND_DESCRIPTION_METHOD: self._hand_description_flush
            },
            {
                HAND_TITLE: "Straight", HAND_RANK: 5, FIND_BEST_METHOD: self._find_best_straight,
                TEST_METHOD: self._test_straight, HAND_DESCRIPTION_METHOD: self._hand_description_straight
            },
            {
                HAND_TITLE: "Trips", HAND_RANK: 6, FIND_BEST_METHOD: self._find_best_trips,
                TEST_METHOD: self._test_trips, HAND_DESCRIPTION_METHOD: self._hand_description_trips
            },
            {
                HAND_TITLE: "Two Pair", HAND_RANK: 7, FIND_BEST_METHOD: self._find_best_two_pair,
                TEST_METHOD: self._test_two_pair, HAND_DESCRIPTION_METHOD: self._hand_description_two_pair
            },
            {
                HAND_TITLE: "Pair", HAND_RANK: 8, FIND_BEST_METHOD: self._find_best_pair,
                TEST_METHOD: self._test_pair, HAND_DESCRIPTION_METHOD: self._hand_description_pair
            },
            {
                HAND_TITLE: "High Card", HAND_RANK: 9, FIND_BEST_METHOD: self._find_best_high_card,
                TEST_METHOD: self._test_high_card, HAND_DESCRIPTION_METHOD: self._hand_description_high_card
            }
        ]

    ########################
    #  PUBLIC API METHODS  #
    ########################

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
            best_hand = hand_type[FIND_BEST_METHOD](hole_cards, board_cards)

            if best_hand:
                return {
                    BEST_HAND: best_hand,
                    HAND_TITLE: hand_type[HAND_TITLE],
                    HAND_RANK: hand_type[HAND_RANK],
                    HAND_DESCRIPTION: hand_type[HAND_DESCRIPTION_METHOD](best_hand)
                }

    def rank_hands(self, hands: Dict[str, List[Card]]):
        pass

    #################################
    #  FIND BEST HAND TYPE METHODS  #
    #################################

    def _find_best_straight_flush(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a straight flush hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [hand for hand in all_hands if self._test_straight_flush(hand)]

        if not matched_hands:
            return None

        return self.order_hands_highest_card(matched_hands, winner_only=True)

    def _find_best_quads(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a quads hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [
            (hand, self.hand_highest_value_tuple(hand, 4)) for hand in all_hands if self._test_quads(hand)
        ]

        if not matched_hands:
            return None

        matched_hands.sort(key=lambda tup: tup[1], reverse=True)
        top_quads_value = matched_hands[0][1]
        top_quads_hands = filter(lambda tup: tup[1] == top_quads_value, matched_hands)

        return self.order_hands_highest_card([tup[0] for tup in top_quads_hands], winner_only=True)

    def _find_best_full_house(self, hole_cards: List[Card], board_cards: List[Card]):
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
            return None

        matched_hands.sort(key=lambda tup: (tup[1], tup[2]), reverse=True)
        return matched_hands[0][0]

    def _find_best_flush(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a flush hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [hand for hand in all_hands if self._test_flush(hand)]

        if not matched_hands:
            return None

        return self.order_hands_highest_card(matched_hands, winner_only=True)

    def _find_best_straight(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a straight hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        matched_hands = [hand for hand in all_hands if self._test_straight(hand)]

        if not matched_hands:
            return None

        return self.order_hands_highest_card(matched_hands, winner_only=True)

    def _find_best_trips(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a trips hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)

        matched_hands = [
            (hand, self.hand_highest_value_tuple(hand, 3)) for hand in all_hands if self._test_trips(hand)
        ]

        if not matched_hands:
            return None

        matched_hands.sort(key=lambda tup: tup[1], reverse=True)
        top_trips = matched_hands[0][1]
        top_trips_hands = filter(lambda tup: tup[1] == top_trips, matched_hands)

        return self.order_hands_highest_card([tup[0] for tup in top_trips_hands], winner_only=True)

    def _find_best_two_pair(self, hole_cards: List[Card], board_cards: List[Card]):
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
            return None

        matched_hands.sort(key=lambda tup: (tup[1], tup[2], tup[3]), reverse=True)
        return matched_hands[0][0]

    def _find_best_pair(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a pair hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)

        matched_hands = [
            (hand, self.hand_highest_value_tuple(hand, 2)) for hand in all_hands if self._test_pair(hand)
        ]

        if not matched_hands:
            return None

        matched_hands.sort(key=lambda tup: tup[1], reverse=True)
        top_pair_value = matched_hands[0][1]
        top_pair_hands = filter(lambda tup: tup[1] == top_pair_value, matched_hands)

        return self.order_hands_highest_card([tup[0] for tup in top_pair_hands], winner_only=True)

    def _find_best_high_card(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Evaluation method to check if a high card hand can be made from the current set of hole and board cards.

        :param hole_cards:
        :param board_cards:
        :return: (Bool: indicating if the hand can be made, List[Card]: the best possible straight flush,
        None if cannot be made)
        """

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        return self.order_hands_highest_card(all_hands, winner_only=True)

    ############################
    #  TEST HAND TYPE METHODS  #
    ############################

    def _test_straight_flush(self, hand: List[Card]):
        """
        Private method to test if a hand is a straight flush hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return self.hand_all_same_suit(hand) and self.hand_values_continuous(hand)

    def _test_quads(self, hand: List[Card]):
        """
        Private method to test if a hand is a quads hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return bool(self.hand_highest_value_tuple(hand, 4))

    def _test_full_house(self, hand: List[Card]):
        """
        Private method to test if a hand is a quads hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        trips_value = self.hand_highest_value_tuple(hand, 3)
        remaining_cards = filter(lambda card: card.value != trips_value, hand)
        pair_value = self.hand_highest_value_tuple(remaining_cards, 2)

        return bool(trips_value and pair_value)

    def _test_flush(self, hand: List[Card]):
        """
        Private method to test if a hand is a flush hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return self.hand_all_same_suit(hand)

    def _test_straight(self, hand: List[Card]):
        """
        Private method to test if a hand is a straight hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return self.hand_values_continuous(hand)

    def _test_trips(self, hand: List[Card]):
        """
        Private method to test if a hand is a trips hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return bool(self.hand_highest_value_tuple(hand, 3))

    def _test_two_pair(self, hand: List[Card]):
        """
        Private method to test if a hand is a two pair hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        high_pair_value = self.hand_highest_value_tuple(hand, 2)
        remaining_cards = list(filter(lambda card: card.value != high_pair_value, hand))
        low_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)

        return bool(high_pair_value and low_pair_value)

    def _test_pair(self, hand: List[Card]):
        """
        Private method to test if a hand is a two pair hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return bool(self.hand_highest_value_tuple(hand, 2))

    @staticmethod
    def _test_high_card(hand: List[Card]):
        """
        Private method to test if a hand is a two pair hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return True

    ##############################
    #  HAND DESCRIPTION METHODS  #
    ##############################

    @staticmethod
    def _hand_description_straight_flush(hand: List[Card]):
        """
        Private method that produces the proper hand description for a straight flush hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        return f"Straight Flush ({hand[0].rank} to {hand[4].rank} of {hand[0].suit})"

    def _hand_description_quads(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a quads hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        quads_value = self.hand_highest_value_tuple(hand, 4)
        quads_rank = list(filter(lambda card: card.value == quads_value, hand))[0].rank
        kicker_rank = list(filter(lambda card: card.value != quads_value, hand))[0].rank
        return f"Quads ({quads_rank}s with {kicker_rank} kicker)"

    def _hand_description_full_house(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a full house hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        trips_value = self.hand_highest_value_tuple(hand, 3)
        trips_rank = list(filter(lambda card: card.value == trips_value, hand))[0].rank
        remaining_cards = filter(lambda card: card.value != trips_value, hand)
        pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
        pair_rank = list(filter(lambda card: card.value == pair_value, hand))[0].rank
        return f"Full House ({trips_rank}s full of {pair_rank}s)"

    @staticmethod
    def _hand_description_flush(hand: List[Card]):
        """
        Private method that produces the proper hand description for flush hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        return f"Flush ({hand[0].suit} with cards {hand[0].rank}, {hand[1].rank}, {hand[2].rank}, " \
               f"{hand[3].rank}, {hand[4].rank})"

    @staticmethod
    def _hand_description_straight(hand: List[Card]):
        """
        Private method that produces the proper hand description for straight hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        return f"Straight ({hand[0].rank} to {hand[4].rank})"

    def _hand_description_trips(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a quads hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        trips_value = self.hand_highest_value_tuple(hand, 3)
        trips_rank = list(filter(lambda card: card.value == trips_value, hand))[0].rank
        kickers = list(filter(lambda card: card.value != trips_value, hand))
        kickers.sort(key=lambda card: card.value, reverse=True)
        return f"Trips ({trips_rank}s with kickers {kickers[0].rank}, {kickers[1].rank})"

    def _hand_description_two_pair(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a two pair hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        higher_pair_value = self.hand_highest_value_tuple(hand, 2)
        higher_pair_rank = list(filter(lambda card: card.value == higher_pair_value, hand))[0].rank

        remaining_cards = list(filter(lambda card: card.value != higher_pair_value, hand))
        lower_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
        lower_pair_rank = list(filter(lambda card: card.value == lower_pair_value, remaining_cards))[0].rank

        kicker_rank = list(filter(lambda card: card.value != lower_pair_value, remaining_cards))[0].rank

        return f"Two Pair ({higher_pair_rank}s and {lower_pair_rank}s with kicker {kicker_rank})"

    def _hand_description_pair(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a pair hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        pair_value = self.hand_highest_value_tuple(hand, 2)
        pair_rank = list(filter(lambda card: card.value == pair_value, hand))[0].rank

        kickers = list(filter(lambda card: card.value != pair_value, hand))
        kickers.sort(key=lambda card: card.value, reverse=True)

        return f"Pair ({pair_rank}s with kickers {kickers[0].rank}, {kickers[1].rank}, {kickers[2].rank})"

    @staticmethod
    def _hand_description_high_card(hand: List[Card]):
        """
        Private method that produces the proper hand description for a high card hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)

        return f"High Card ({hand[0].rank}, {hand[1].rank}, {hand[2].rank}, {hand[3].rank}, {hand[4].rank})"
