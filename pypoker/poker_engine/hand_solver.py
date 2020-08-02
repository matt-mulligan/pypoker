"""
Hand Solver

This module provides a class that can be used to solve winners and probabilities of poker hands.
"""

from itertools import combinations

############################
#  MODULE LEVEL CONSTANTS  #
############################

FORMAT_TEXAS_HOLDEM = "texas_holdem"
GAME_FORMATS = [FORMAT_TEXAS_HOLDEM]


class PokerHandSolver(object):

    def __init__(self):
        self.texas_holdem_hand_orders = [
            {"name": "Straight Flush", "method": self._hand_check_texas_holdem_straight_flush},
            {"name": "Quads", "method": self._hand_check_texas_holdem_quads},
            {"name": "Full House", "method": self._hand_check_texas_holdem_full_house}
        ]

    ########################
    #  PUBLIC API METHODS  #
    ########################

    def find_player_best_hand(self, player_cards, board_cards, game_format=FORMAT_TEXAS_HOLDEM):
        """
        This public method will return the best possible hand for the player.

        :param player_cards: List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :param game_format: String. represents the type of poker game that is being played
        :return: tuple(Hand Name, [hand_cards])
        """

        for hand_type in self.texas_holdem_hand_orders:
            has_hand_type, cards = hand_type["method"](player_cards, board_cards)

            if has_hand_type:
                return hand_type["name"], cards

    # def find_winner(self, player_hands, board_cards, game_format=FORMAT_TEXAS_HOLDEM):
    #     """
    #     This public method will determine which player has won the hand of poker based on the game format.
    #     The hand should be played out to completion. to find each players odds use hand_solver.find_odds()
    #
    #     :param player_hands: Dictionary in the format of KEY="player_name", VALUE=List of Card Objects
    #     :param board_cards: List of Card objects representing the communal cards
    #     :param game_format: String. represents the type of poker game that is being played
    #     :return: Tuple in format of (PLAYER_NAME, WINNING_HAND)
    #     """
    #
    # def find_odds(self, player_hands, board_cards, game_format=FORMAT_TEXAS_HOLDEM):
    #     """
    #     This public method will determine each players changes of winning the hand given the current situation.
    #
    #     :param player_hands: Dictionary in the format of KEY="player_name", VALUE=List of Card Objects
    #     :param board_cards: List of Card objects representing the communal cards
    #     :param game_format: String. represents the type of poker game that is being played
    #     :return: Dictionary in format of KEY=PLAYER_NAME, VALUE=WIN_PERCENTAGE
    #     """
    #
    # def find_outs(self, target_player_hand, other_players_hands, board_cards, game_format=FORMAT_TEXAS_HOLDEM):
    #     """
    #     This public API will give the possible outs combinations for the target player when playing against the other
    #     players in the current game situation described by the board cards.
    #
    #     :param target_player_hand: Dictionary in the format of KEY="player_name", VALUE=List of Card Objects
    #     :param other_players_hands: Dictionary in the format of KEY="player_name", VALUE=List of Card Objects
    #     :param board_cards: List of Card objects representing the communal cards
    #     :param game_format: String. represents the type of poker game that is being played
    #     :return: List of card objects that would result in the target player winning.
    #     """

    #############################################
    #  PRIVATE TEXAS HOLDEM HAND CHECK METHODS  #
    #############################################

    def _hand_check_texas_holdem_straight_flush(self, player_cards, board_cards):
        """
        This private method will check if the given player has a Texas holdem royal straight flush hand.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)
            if not self._hand_all_same_suit(hand):
                continue
            if not self._hand_values_continuous(hand):
                continue
            matched_hands.append(hand)

        if not matched_hands:
            return False, None

        best_hand = self._find_hand_with_highest_card(matched_hands) if len(matched_hands) > 1 else matched_hands[0]
        return True, best_hand

    def _hand_check_texas_holdem_quads(self, player_cards, board_cards):
        """
        This private method will check if the given player has a Texas holdem four of a kind hand.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)
            has_quads, quad_value = self._hand_has_value_tuple(hand, 4)
            if has_quads:
                matched_hands.append({"cards": hand, "quad_value": quad_value})

        if not matched_hands:
            return False, None

        best_hand = self._find_hand_with_highest_quad(matched_hands) if len(matched_hands) > 1 else matched_hands[0]["cards"]
        return True, best_hand

    def _hand_check_texas_holdem_full_house(self, player_cards, board_cards):
        """
        This private method will check if the given player has a Texas holdem full house.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)

            hand_has_trips, trips_value = self._hand_has_value_tuple(hand, 3)
            if not hand_has_trips:
                continue

            remaining_cards = self._filter_hand_by_value(hand, trips_value)
            hand_has_pair, pair_value = self._hand_has_value_tuple(remaining_cards, 2)

            if hand_has_pair:
                matched_hands.append({"cards": hand, "trips_value": trips_value, "pair_value": pair_value})

        if not matched_hands:
            return False, None

        best_hand = self._find_hand_with_highest_full_house(matched_hands) if len(matched_hands) > 1 else matched_hands[0]["cards"]
        return True, best_hand

    ##########################################
    #  PRIVATE HAND CHARACTERISTICS METHODS  #
    ##########################################

    @staticmethod
    def _hand_all_same_suit(hand):
        """
        This method will check if all cards in the hand have the same suit.

        :param hand: List of Card objects
        :return: Boolean, True if all cards in hand have the same suit, False otherwise.
        """

        suit = hand[0].suit
        return True if all(card.suit == suit for card in hand) else False

    @staticmethod
    def _hand_values_continuous(hand):
        """
        This private method will check if the cards provided in the hand are a straight
        (their values are continuous without gaps)
        This method does not assert the number of cards in the hand.

        :param hand: List of Card objects representing the players hand
        :return: Boolean. True of the ard values are continuous, False if not
        """

        hand.sort(key=lambda card: card.value, reverse=False)
        card_value_list = [card.value for card in hand]
        return all(a + 1 == b for a, b in zip(card_value_list, card_value_list[1:]))

    @staticmethod
    def _hand_has_value_tuple(hand, tuple_length):
        """
        This private method will check if the hand provided has a tuple of any value of card of the specified length.
        this method can be used to check if the hand has a pair (tuple_length=2), trips (tuple_length=3) or
        quads (tuple_length=4).

        if hand has multiple tuples of the specified length, the maximum is returned.
        e.g. tuple_length = 2 and hand is 7,9,10,9,7 then 9 is returned for tuple_card_value

        :param hand: List of Card objects
        :param tuple_length: Int definign if looking for pairs(2) trips(3) or quads(4)
        :return: tuple of (BOOLEAN: hand_has_tuple, INT: tuple_card_value)
        """

        card_values = {}
        for card in hand:
            if card.value not in card_values.keys():
                card_values[card.value] = 1
            else:
                card_values[card.value] += 1

        meets_criteria = [value for value, count in card_values.items() if count == tuple_length]

        if not meets_criteria:
            return False, None

        return True, max(meets_criteria)

    ######################################
    #  PRIVATE HAND TIE-BREAKER METHODS  #
    ######################################
    @staticmethod
    def _find_hand_with_highest_card(hands):
        """
        This private method will compare the hands provided to find the one that has the highest card.
        if the highest card is a tie, it will continue down the list.
        if all cards are a tie then all matching hands returned.

        :return: the hand(s) with the highest card
        """

        hands_data = []
        for hand in hands:
            hand.sort(key=lambda card: card.value, reverse=True)
            hands_data.append(hand)

        for card_index in range(len(hands[0])):
            hand_vals = [hand[card_index].value for hand in hands_data]
            max_val = max(hand_vals)

            new_hands_data = [hand for hand in hands_data if hand[card_index].value == max_val]
            if len(new_hands_data) == 1:
                return new_hands_data[0]

            hands_data = new_hands_data

        # two hands that tie, just take the first one
        return hands_data[0]

    def _find_hand_with_highest_quad(self, quads_hands):
        """
        This private method will find the highest quad hand
        :param quads_hands: List of dicts containing {cards, quad_value}
        :return:
        """

        sorted_quads = sorted(quads_hands, key=lambda hand_info: hand_info["quad_value"], reverse=True)
        highest_quads_value = sorted_quads[0]["quad_value"]
        highest_quads = [hand_info["cards"] for hand_info in sorted_quads if hand_info["quad_value"] == highest_quads_value]
        return highest_quads[0] if len(highest_quads) == 1 else self._find_hand_with_highest_card(highest_quads)

    @staticmethod
    def _find_hand_with_highest_full_house(hands):
        """
        THis private method will check all hands passed to it
        :param hands:
        :return:
        """

        sorted_hands = sorted(hands, key=lambda hand: (hand["trips_value"], hand["pair_value"]), reverse=True)
        return sorted_hands[0]["cards"]

    ############################
    #  PRIVATE HELPER METHODS  #
    ############################

    @staticmethod
    def _get_hand_combinations(player_cards, board_cards, hand_size):
        """
        This private method will get all possible hand combinations for a

        :param player_cards: List of Card objects representing the players cards
        :param board_cards: List of Card objects representing the communal cards
        :param hand_size: Int representing what size hands to produce.

        :return: Generator object containing all hand combinations. An empty list is returned if the hand_size is
        greater than the number of all cards provided
        """

        all_cards = player_cards.copy()
        all_cards.extend(board_cards)
        return combinations(all_cards, hand_size)

    @staticmethod
    def _filter_hand_by_value(hand, filter_value):
        """
        This private method will filter the cards within hand based on the value.
        any card that matches the passed value argument will be filtered out of the hand.

        :param hand: List of Card objects
        :param filter_value: Int of the value to filter out of the hand
        :return: List of Card objects
        """

        return [card for card in hand if card.value != filter_value]
