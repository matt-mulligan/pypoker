from typing import List, Dict

from pypoker.deck import Card, Deck
from pypoker.poker_engine.hand_solver.base import BaseHandSolver
from pypoker.poker_engine.hand_solver.constants import HAND_TITLE, HAND_RANK, TEST_METHOD, BEST_HAND, \
    HAND_DESCRIPTION, DESCRIPTION_METHOD, RANK_METHOD


class TexasHoldemHandSolver(BaseHandSolver):
    """
    The Texas Hold'em implementation of the BaseHandSolver class.
    Responsible for determining a players best hand
    """

    def __init__(self):
        self._hand_rankings = [
            {
                HAND_TITLE: "Straight Flush", HAND_RANK: 1, TEST_METHOD: self._test_straight_flush,
                RANK_METHOD: self._rank_straight_flush, DESCRIPTION_METHOD: self._hand_description_straight_flush
            },
            {
                HAND_TITLE: "Quads", HAND_RANK: 2, TEST_METHOD: self._test_quads,
                RANK_METHOD: self._rank_quads, DESCRIPTION_METHOD: self._hand_description_quads
            },
            {
                HAND_TITLE: "Full House", HAND_RANK: 3, TEST_METHOD: self._test_full_house,
                RANK_METHOD: self._rank_full_house, DESCRIPTION_METHOD: self._hand_description_full_house
            },
            {
                HAND_TITLE: "Flush", HAND_RANK: 4, TEST_METHOD: self._test_flush,
                RANK_METHOD: self._rank_flush, DESCRIPTION_METHOD: self._hand_description_flush
            },
            {
                HAND_TITLE: "Straight", HAND_RANK: 5, TEST_METHOD: self._test_straight,
                RANK_METHOD: self._rank_straight, DESCRIPTION_METHOD: self._hand_description_straight
            },
            {
                HAND_TITLE: "Trips", HAND_RANK: 6, TEST_METHOD: self._test_trips,
                RANK_METHOD: self._rank_trips, DESCRIPTION_METHOD: self._hand_description_trips
            },
            {
                HAND_TITLE: "Two Pair", HAND_RANK: 7, TEST_METHOD: self._test_two_pair,
                RANK_METHOD: self._rank_two_pair, DESCRIPTION_METHOD: self._hand_description_two_pair
            },
            {
                HAND_TITLE: "Pair", HAND_RANK: 8, TEST_METHOD: self._test_pair,
                RANK_METHOD: self._rank_pair, DESCRIPTION_METHOD: self._hand_description_pair
            },
            {
                HAND_TITLE: "High Card", HAND_RANK: 9, TEST_METHOD: self._test_high_card,
                RANK_METHOD: self._rank_high_card, DESCRIPTION_METHOD: self._hand_description_high_card
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

        all_hands = self.get_all_combinations(hole_cards, board_cards, 5)
        for hand_type in self._hand_rankings:
            matched_hands = [hand for hand in all_hands if hand_type[TEST_METHOD](hand)]

            if matched_hands:
                best_hand = hand_type[RANK_METHOD](matched_hands)[1][0]
                return {
                    BEST_HAND: best_hand,
                    HAND_TITLE: hand_type[HAND_TITLE],
                    HAND_RANK: hand_type[HAND_RANK],
                    HAND_DESCRIPTION: hand_type[DESCRIPTION_METHOD](best_hand)
                }

    def rank_hands(self, players_hands: Dict[str, List[Card]]):
        """
        Public method that will rank players texas hold'em hands against each other

        :param players_hands: Dict in format of
        {
            "PLAYER_NAME": [LIST_OF_CARDS]
        }

        :return: dict in the following format:
        {
            <RANK>: {
                "players": ["LIST OF PLAYER NAMES"],
                "hand_description": "HAND_DESCRIPTION"
            }
        }
        """

        player_hands_by_rank = self._group_player_hands_by_rank(players_hands)
        ranks = sorted(list(player_hands_by_rank.keys()))

        current_rank = 0
        ranked_player_hands = dict()

        for rank in ranks:
            hands = list(player_hands_by_rank[rank].values())
            subranked_hands = self._hand_rankings[rank - 1][RANK_METHOD](hands)
            subranked_players = self._link_subranked_hands_to_players(subranked_hands, players_hands)

            for players in subranked_players.values():
                current_rank += 1
                hand_desc = self._hand_rankings[rank - 1][DESCRIPTION_METHOD](players_hands[players[0]])
                ranked_player_hands[current_rank] = {
                    "players": players,
                    "hand_description": hand_desc
                }

        return ranked_player_hands

    def find_odds(self, player_cards: Dict[str, List[Card]], board_cards: List[Card]):
        """
        Abstract method to implement to find the odds of all players winning from the current situation.

        :param player_cards: Dictionary, of player names and their hole cards
        :param board_cards: List of cards representing the current board cards
        :return: Dictionary of player names and their likelyhood of winning from this situation.
        """

        unused_cards = self._determine_unused_cards(player_cards, board_cards)
        possible_boards = self.get_all_combinations(board_cards, unused_cards, 5, always_use_hole_cards=True)
        wins = self._find_all_winners(player_cards, possible_boards)
        return self._calculate_win_percentage(wins, len(possible_boards))

    #######################
    #  TEST HAND METHODS  #
    #######################

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

    #######################
    #  RANK HAND METHODS  #
    #######################

    def _rank_straight_flush(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best straight flush hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a straight flush hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ordered_hands = self._reorder_ace_low_straight_hands(ordered_hands)

        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_quads(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best quads hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a quads hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_quads = [(hand, self.hand_highest_value_tuple(hand, 4)) for hand in hands]
        quad_values = list(set([tup[1] for tup in hands_quads]))
        quad_values.sort(reverse=True)

        ranked_hands = dict()

        for quad_value in quad_values:
            quad_value_hands = filter(lambda hand_tuple: hand_tuple[1] == quad_value, hands_quads)
            quad_value_hands = self.order_hands_highest_card([tup[0] for tup in quad_value_hands])

            current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
            ranked_hands[current_rank] = [quad_value_hands[0]]

            for hand in quad_value_hands[1:]:
                if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                    ranked_hands[current_rank].append(hand)
                else:
                    current_rank += 1
                    ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_full_house(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best full house hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a full house hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = []

        for hand in hands:
            trips_value = self.hand_highest_value_tuple(hand, 3)
            remaining_cards = filter(lambda card: card.value != trips_value, hand)
            pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
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

    def _rank_flush(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best flush hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a flush hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_straight(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best straight hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a straight hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ordered_hands = self._reorder_ace_low_straight_hands(ordered_hands)
        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_trips(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best trips hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a trips hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_trips = [(hand, self.hand_highest_value_tuple(hand, 3)) for hand in hands]
        trips_values = list(set([tup[1] for tup in hands_trips]))
        trips_values.sort(reverse=True)

        ranked_hands = dict()

        for trips_value in trips_values:
            trips_value_hands = filter(lambda hand_tuple: hand_tuple[1] == trips_value, hands_trips)
            trips_value_hands = self.order_hands_highest_card([tup[0] for tup in trips_value_hands])

            current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
            ranked_hands[current_rank] = [trips_value_hands[0]]

            for hand in trips_value_hands[1:]:
                if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                    ranked_hands[current_rank].append(hand)
                else:
                    current_rank += 1
                    ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_two_pair(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best two pair hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a two pair hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_two_pair_kicker = []

        for hand in hands:
            high_pair_value = self.hand_highest_value_tuple(hand, 2)
            remaining_cards = filter(lambda card: card.value != high_pair_value, hand)
            low_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
            kicker_value = list(
                filter(lambda card: card.value != high_pair_value and card.value != low_pair_value, hand)
            )[0].value
            hands_two_pair_kicker.append((hand, high_pair_value, low_pair_value, kicker_value))

        hands_two_pair_kicker.sort(key=lambda tup: (tup[1], tup[2], tup[3]), reverse=True)

        current_rank = 1
        current_high_pair = hands_two_pair_kicker[0][1]
        current_low_pair = hands_two_pair_kicker[0][2]
        current_kicker = hands_two_pair_kicker[0][3]
        ranked_hands = {current_rank: [hands_two_pair_kicker[0][0]]}

        for hand, high_pair, low_pair, kicker in hands_two_pair_kicker[1:]:
            if high_pair == current_high_pair and low_pair == current_low_pair and kicker == current_kicker:
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                current_high_pair = high_pair
                current_low_pair = low_pair
                current_kicker = kicker
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_pair(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best pair hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a pair hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_pair = [(hand, self.hand_highest_value_tuple(hand, 2)) for hand in hands]
        pair_values = list(set([tup[1] for tup in hands_pair]))
        pair_values.sort(reverse=True)

        ranked_hands = dict()

        for pair_value in pair_values:
            pair_value_hands = filter(lambda hand_tuple: hand_tuple[1] == pair_value, hands_pair)
            pair_value_hands = self.order_hands_highest_card([tup[0] for tup in pair_value_hands])

            current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
            ranked_hands[current_rank] = [pair_value_hands[0]]

            for hand in pair_value_hands[1:]:
                if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                    ranked_hands[current_rank].append(hand)
                else:
                    current_rank += 1
                    ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_high_card(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best high card hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a high card hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    ##############################
    #  HAND DESCRIPTION METHODS  #
    ##############################

    def _hand_description_straight_flush(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a straight flush hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        if self.hand_is_ace_low_straight(hand):
            return f"Straight Flush ({hand[1].rank} to {hand[0].rank})"
        else:
            return f"Straight Flush ({hand[0].rank} to {hand[4].rank})"

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
        return f"Flush ({hand[0].rank}, {hand[1].rank}, {hand[2].rank}, {hand[3].rank}, {hand[4].rank})"

    def _hand_description_straight(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for straight hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        if self.hand_is_ace_low_straight(hand):
            return f"Straight ({hand[1].rank} to {hand[0].rank})"
        else:
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

    #########################
    #  MISC HELPER METHODS  #
    #########################

    def _reorder_ace_low_straight_hands(self, ordered_hands):
        """
        Private helper method to reorder ace low straight hands to end of ordered hands list
        :param ordered_hands:
        :return:
        """

        ace_low_straight_hands = [True if self.hand_is_ace_low_straight(hand) else False for hand in ordered_hands]
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

    def _group_player_hands_by_rank(self, players_hands):
        """
        Helper method that will group player hands together by their hand ranks.

        :param players_hands: Dict in format of {PLAYER_NAME: [LIST_OF_CARDS]}
        :return: dictionary in format of {RANK: {PLAYER: [LIST_OF_CARDS]}}
        """

        player_hands_by_rank = dict()
        for player, hand in players_hands.items():
            for hand_type in self._hand_rankings:
                if hand_type[TEST_METHOD](hand):
                    if hand_type[HAND_RANK] not in player_hands_by_rank.keys():
                        player_hands_by_rank[hand_type[HAND_RANK]] = {player: hand}
                    else:
                        player_hands_by_rank[hand_type[HAND_RANK]][player] = hand
                    break
        return player_hands_by_rank

    @staticmethod
    def _link_subranked_hands_to_players(subranked_hands, players_hands):
        """
        Helper method to link player names (found in players_hands dict) back to their hand within the subranked_hands
        dict

        :param subranked_hands: Dict in form of {SUBRANK: [LIST_OF_HANDS]}
        :param players_hands: Dict in format of {PLAYER: [LIST_OF_CARDS]}
        :return:
        """
        for hand in players_hands.values():
            hand.sort(key=lambda card: card.value, reverse=True)

        linked_subrank_players = dict()
        for subrank, subrank_hands in subranked_hands.items():
            for hand in subrank_hands:
                hand.sort(key=lambda card: card.value, reverse=True)

            matched_players = [player for player, player_hand in players_hands.items() if player_hand in subrank_hands]
            linked_subrank_players[subrank] = matched_players

        return linked_subrank_players

    @staticmethod
    def _determine_unused_cards(player_cards, board_cards):
        """
        private helper method that finds all of the possible remaining cards based on the hole and boaard cards
        that are known.

        :param player_cards: Dictionary, of player names and their hole cards
        :param board_cards: List of cards representing the current board cards
        :return:
        """

        used_cards = board_cards.copy()
        for cards in player_cards.values():
            used_cards.extend(cards)

        return [card for card in Deck().cards_all if card not in used_cards]

    def _find_all_winners(self, player_cards, possible_boards):
        """
        Private helper method to assess the winner of each set of board cards.

        :param player_cards: Dictionary, of player names and their hole cards
        :param possible_boards: list of all possible board card combinations to test against
        :return:
        """

        wins = dict()
        for board in possible_boards:
            best_hands = {
                player: self.find_best_hand(hole_cards, board)[BEST_HAND]
                for player, hole_cards in player_cards.items()
            }

            ranked_hands = self.rank_hands(best_hands)
            winners = sorted(ranked_hands[1]["players"])
            winners_key = "---".join(winners)

            if winners_key in wins.keys():
                wins[winners_key] += 1
            else:
                wins[winners_key] = 1
        return wins

    @staticmethod
    def _calculate_win_percentage(wins, games_played):
        """
        private method to calculate each players win percentage.

        :param games_played: number of games played to build the wins dictionary
        :param wins: dictionary containing player names and their win total.
        Ties are represented as players names seperated by '---'
        :return: dictionary of player names and their win percentage
        """

        player_odds = dict()
        for winner, win_count in wins:
            name = f"Tie ({winner.split('---')})" if "---" in winner else winner
            win_percentage = win_count / games_played
            player_odds[name] = win_percentage
        return player_odds