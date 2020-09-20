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

HAND_TYPE_STRAIGHT_FLUSH = "Straight Flush"
HAND_TYPE_QUADS = "Quads"
HAND_TYPE_FULL_HOUSE = "Full House"
HAND_TYPE_FLUSH = "Flush"
HAND_TYPE_STRAIGHT = "Straight"
HAND_TYPE_TRIPS = "Trips"
HAND_TYPE_TWO_PAIR = "Two Pair"
HAND_TYPE_PAIR = "Pair"
HAND_TYPE_HIGH_CARD = "High Card"


class PokerHandSolver(object):

    def __init__(self):
        self.texas_holdem_hand_definitions = [
            {
                "name": HAND_TYPE_STRAIGHT_FLUSH,
                "strength": 9,
                "method": self._hand_check_texas_holdem_straight_flush,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_straight_flush
            },
            {
                "name": HAND_TYPE_QUADS,
                "strength": 8,
                "method": self._hand_check_texas_holdem_quads,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_quads
            },
            {
                "name": HAND_TYPE_FULL_HOUSE,
                "strength": 7,
                "method": self._hand_check_texas_holdem_full_house,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_full_house
            },
            {
                "name": HAND_TYPE_FLUSH,
                "strength": 6,
                "method": self._hand_check_texas_holdem_flush,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_flush
            },
            {
                "name": HAND_TYPE_STRAIGHT,
                "strength": 5,
                "method": self._hand_check_texas_holdem_straight,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_straight
            },
            {
                "name": HAND_TYPE_TRIPS,
                "strength": 4,
                "method": self._hand_check_texas_holdem_trips,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_trips
            },
            {
                "name": HAND_TYPE_TWO_PAIR,
                "strength": 3,
                "method": self._hand_check_texas_holdem_two_pair,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_two_pair
            },
            {
                "name": HAND_TYPE_PAIR,
                "strength": 2,
                "method": self._hand_check_texas_holdem_pair,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_pair
            },
            {
                "name": HAND_TYPE_HIGH_CARD,
                "strength": 1,
                "method": self._hand_check_texas_holdem_high_card,
                "tiebreaker": self._hand_tiebreaker_texas_holdem_high_card
            }
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

        for hand_type in self.texas_holdem_hand_definitions:
            has_hand_type, cards = hand_type["method"](player_cards, board_cards)

            if has_hand_type:
                return hand_type["name"], cards

    def rank_player_hands(self, players, board_cards, game_format=FORMAT_TEXAS_HOLDEM):
        """
        This public method will determine the order of the players hands.

        :param players: List of player dictionaries with the following keys
            {
                "name": NAME_OF_PLAYER,
                "player_cards": PLAYER_HOLE_CARDS
            }
        :param board_cards: List of Card objects representing the communal cards
        :param game_format: String. represents the type of poker game that is being played
        :return: Updated players list object with the following keys for each player dictionary
            {
                "name": NAME_OF_PLAYER,
                "player_cards": PLAYER HOLE CARDS
                "hand": CARDS OF PLAYERS BEST HAND
                "hand_type": BEST HAND TYPE PLAYER CAN MAKE,
                "hand_strength: THE RELATIVE STRENGTH OF THE HAND TYPE IN TEXAS HOLDEM (HIGHER IS BETTER)
                "hand_rank": PLAYER HAND RANKING COMPARED TO OTHER PLAYERS (LOWER IS BETTER)
                "hand_rank_tie": BOOL IF PLAYER HAND RANK IS A TIE WITH ANY OTHER PLAYERS
                "tiebreaker_rank": RANK GIVEN BY THE TIEBREAKER METHOD
            }
        """

        hand_strength_occurances = {}
        for player_dict in players:
            hand_type, hand = self.find_player_best_hand(player_dict["player_cards"], board_cards)
            hand_strength = self._find_hand_strength(hand_type)

            if hand_strength not in hand_strength_occurances.keys():
                hand_strength_occurances[hand_strength] = 1
            else:
                hand_strength_occurances[hand_strength] += 1

            player_dict["hand_type"] = hand_type
            player_dict["hand"] = hand
            player_dict["hand_strength"] = hand_strength

        #  Create final ordered list of players
        hand_rank = 1
        ranked_players = []

        for hand_strength in sorted(hand_strength_occurances.keys(), reverse=True):
            if hand_strength_occurances[hand_strength] == 1:
                for player in players:
                    if player["hand_strength"] == hand_strength:
                        player["hand_rank"] = hand_rank
                        player["hand_rank_tie"] = False
                        player["tiebreaker_rank"] = None
                        ranked_players.append(player)
                        hand_rank += 1
            else:
                tiebreak_players = [player for player in players if player["hand_strength"] == hand_strength]
                tiebreak_method = self._find_tiebreaker_method(tiebreak_players)
                tiebreak_ordered = tiebreak_method(tiebreak_players, winner_only=False)
                hand_rank = self._rank_tiebreak_players(hand_rank, ranked_players, tiebreak_ordered)

        return ranked_players

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
        This private method will check if the player can make a texas holdem hand containing a straight flush.
        If the player can make multiple hands with a straight flush in them, then the best hand is returned.

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
            matched_hands.append({"hand": hand})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_straight_flush(matched_hands) if len(matched_hands) > 1 \
            else matched_hands[0]
        return True, best_hand["hand"]

    def _hand_check_texas_holdem_quads(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing quads.
        If the player can make multiple hands with quads in them, then the best hand is returned.

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
                matched_hands.append({"hand": hand, "quad_value": quad_value})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_quads(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_full_house(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing a full house.
        If the player can make multiple hands with a full house in them, then the best hand is returned.

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
                matched_hands.append({"hand": hand, "trips_value": trips_value, "pair_value": pair_value})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_full_house(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_flush(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing a flush.
        If the player can make multiple hands with a flush in them, then the best hand is returned.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)
            if self._hand_all_same_suit(hand):
                matched_hands.append({"hand": hand})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_flush(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_straight(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing a straight.
        If the player can make multiple hands with a straight in them, then the best hand is returned.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)
            if self._hand_values_continuous(hand):
                matched_hands.append({"hand": hand})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_straight(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_trips(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing trips.
        If the player can make multiple hands with trips, then the best hand is returned.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)

            hand_has_trips, trips_value = self._hand_has_value_tuple(hand, 3)
            if hand_has_trips:
                matched_hands.append({"hand": hand, "trips_value": trips_value})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_trips(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_two_pair(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing two pairs.
        If the player can make multiple hands with two pairs in them, then the best hand is returned.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)

            hand_has_pair, larger_pair_value = self._hand_has_value_tuple(hand, 2)
            if not hand_has_pair:
                continue

            remaining_cards = self._filter_hand_by_value(hand, larger_pair_value)
            hand_has_pair, smaller_pair_value = self._hand_has_value_tuple(remaining_cards, 2)

            if hand_has_pair:
                matched_hands.append({"hand": hand, "larger_pair_value": larger_pair_value,
                                      "smaller_pair_value": smaller_pair_value})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_two_pair(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_pair(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing a pair.
        If the player can make multiple hands with a pair, then the best hand is returned.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)

            hand_has_pair, pair_value = self._hand_has_value_tuple(hand, 2)
            if hand_has_pair:
                matched_hands.append({"hand": hand, "pair_value": pair_value})

        if not matched_hands:
            return False, None

        best_hand = self._hand_tiebreaker_texas_holdem_pair(matched_hands)["hand"] if len(matched_hands) > 1 else matched_hands[0]["hand"]
        return True, best_hand

    def _hand_check_texas_holdem_high_card(self, player_cards, board_cards):
        """
        This private method will check if the player can make a texas holdem hand containing a hogh card.
        If the player can make multiple hands with a high card, then the best hand is returned.

        :param player_cards:List of Card objects representing the players hand
        :param board_cards: List of Card objects representing the communal cards
        :return: Tuple in format of (Bool:PLAYER_HAS_THIS_HAND, List: hand of cards used)
        """

        all_hands = self._get_hand_combinations(player_cards, board_cards, 5)

        matched_hands = []
        for hand in all_hands:
            hand = list(hand)
            matched_hands.append({"hand": hand})

        best_hand = self._hand_tiebreaker_texas_holdem_high_card(matched_hands)["hand"]
        return True, best_hand

    ######################################
    #  PRIVATE HAND TIE-BREAKER METHODS  #
    ######################################

    def _hand_tiebreaker_texas_holdem_straight_flush(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem straight flush hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of all players
        :return:
        """

        ranked_players = self._order_hands_by_highest_card(players)

        self._mark_tied_hands_on_high_card(ranked_players)

        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_quads(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem straight flush hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        quad_values_found = []
        for player_dict in players:
            _, quad_value = self._hand_has_value_tuple(player_dict["hand"], 4)
            player_dict["trump_card"] = self._filter_hand_by_value(player_dict["hand"], quad_value)
            if quad_value not in quad_values_found:
                quad_values_found.append(quad_value)

            player_dict["quad_value"] = quad_value

        tiebreaker_rank = 1
        ranked_players = []
        for quad_value in sorted(quad_values_found, reverse=True):
            quad_value_players = [player_dict for player_dict in players if player_dict["quad_value"] == quad_value]
            if len(quad_value_players) == 1:
                player_dict = quad_value_players[0]
                player_dict["tiebreaker_rank"] = tiebreaker_rank
                player_dict["hand_rank_tie"] = False
                ranked_players.append(player_dict)
                tiebreaker_rank += 1
            else:
                quad_value_players = self._order_hands_by_highest_card(quad_value_players)
                for index, player_dict in enumerate(quad_value_players):
                    if index == 0:
                        player_dict["tiebreaker_rank"] = tiebreaker_rank
                        player_dict["hand_rank_tie"] = False
                        tiebreaker_rank += 1
                    else:
                        previous_player = ranked_players[-1]
                        if previous_player["trump_card"][0].value == player_dict["trump_card"][0].value:
                            player_dict["tiebreaker_rank"] = tiebreaker_rank - 1
                            player_dict["hand_rank_tie"] = True
                            previous_player["hand_rank_tie"] = True
                        else:
                            player_dict["tiebreaker_rank"] = tiebreaker_rank
                            player_dict["hand_rank_tie"] = False
                            tiebreaker_rank += 1

                    ranked_players.append(player_dict)
        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_full_house(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem full house hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        for player_dict in players:
            _, trips_value = self._hand_has_value_tuple(player_dict["hand"], 3)
            remaining_cards = self._filter_hand_by_value(player_dict["hand"], trips_value)
            _, pair_value = self._hand_has_value_tuple(remaining_cards, 2)
            player_dict["trips_value"] = trips_value
            player_dict["pair_value"] = pair_value

        ranked_players = sorted(players,
                                key=lambda player_dict: (player_dict["trips_value"], player_dict["pair_value"]),
                                reverse=True)

        tiebreaker_rank = 1
        for index, player_dict in enumerate(ranked_players):
            if index == 0:
                player_dict["tiebreaker_rank"] = tiebreaker_rank
                player_dict["hand_rank_tie"] = False
                tiebreaker_rank += 1
            else:
                previous_player = ranked_players[index - 1]
                if previous_player["trips_value"] == player_dict["trips_value"] and previous_player["pair_value"] == player_dict["pair_value"]:
                    previous_player["hand_rank_tie"] = True
                    player_dict["tiebreaker_rank"] = tiebreaker_rank - 1
                    player_dict["hand_rank_tie"] = True
                else:
                    player_dict["tiebreaker_rank"] = tiebreaker_rank
                    player_dict["hand_rank_tie"] = False
                    tiebreaker_rank += 1

        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_flush(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem flush hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        ranked_players = self._order_hands_by_highest_card(players)
        self._mark_tied_hands_on_high_card(ranked_players)
        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_straight(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem straight hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        ranked_players = self._order_hands_by_highest_card(players)
        self._mark_tied_hands_on_high_card(ranked_players)
        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_trips(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem straight hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        trips_values_found = []
        for player_dict in players:
            _, trips_value = self._hand_has_value_tuple(player_dict["hand"], 3)
            trips_values_found.append(trips_value)
            player_dict["trips_value"] = trips_value

        trips_values_found = list(set(trips_values_found))

        tiebreaker_rank = 1
        ranked_players = []
        for trip_value in sorted(trips_values_found, reverse=True):
            trip_value_players = [player_dict for player_dict in players if player_dict["trips_value"] == trip_value]
            if len(trip_value_players) == 1:
                player_dict = trip_value_players[0]
                player_dict["tiebreaker_rank"] = tiebreaker_rank
                player_dict["hand_rank_tie"] = False
                ranked_players.append(player_dict)
                tiebreaker_rank += 1
            else:
                trip_value_players = self._order_hands_by_highest_card(trip_value_players)
                for index, player_dict in enumerate(trip_value_players):
                    if index == 0:
                        player_dict["tiebreaker_rank"] = tiebreaker_rank
                        player_dict["hand_rank_tie"] = False
                        tiebreaker_rank += 1
                    else:
                        previous_player = ranked_players[-1]
                        if self._all_card_values_the_same(previous_player["hand"], player_dict["hand"]):
                            player_dict["tiebreaker_rank"] = tiebreaker_rank - 1
                            player_dict["hand_rank_tie"] = True
                            previous_player["hand_rank_tie"] = True
                        else:
                            player_dict["tiebreaker_rank"] = tiebreaker_rank
                            player_dict["hand_rank_tie"] = False
                            tiebreaker_rank += 1

                    ranked_players.append(player_dict)
        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_two_pair(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem two pair hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        for player_dict in players:
            _, larger_pair_value = self._hand_has_value_tuple(player_dict["hand"], 2)
            remaining_cards = self._filter_hand_by_value(player_dict["hand"], larger_pair_value)
            _, smaller_pair_value = self._hand_has_value_tuple(remaining_cards, 2)
            trump_card = self._filter_hand_by_value(remaining_cards, smaller_pair_value)

            player_dict["larger_pair_value"] = larger_pair_value
            player_dict["smaller_pair_value"] = smaller_pair_value
            player_dict["trump_card_value"] = trump_card[0].value

        ranked_players = sorted(players, key=lambda player_dict: (player_dict["larger_pair_value"],
                                                                  player_dict["smaller_pair_value"],
                                                                  player_dict["trump_card_value"]), reverse=True)

        tiebreaker_rank = 1
        for index, player_dict in enumerate(ranked_players):
            if index == 0:
                player_dict["tiebreaker_rank"] = tiebreaker_rank
                player_dict["hand_rank_tie"] = False
                tiebreaker_rank += 1
            else:
                previous_player = ranked_players[index - 1]
                if self._all_card_values_the_same(previous_player["hand"], player_dict["hand"]):
                    previous_player["hand_rank_tie"] = True
                    player_dict["tiebreaker_rank"] = tiebreaker_rank - 1
                    player_dict["hand_rank_tie"] = True
                else:
                    player_dict["tiebreaker_rank"] = tiebreaker_rank
                    player_dict["hand_rank_tie"] = False
                    tiebreaker_rank += 1
        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_pair(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem single pair hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        pair_values_found = []
        for player_dict in players:
            _, pair_value = self._hand_has_value_tuple(player_dict["hand"], 2)
            pair_values_found.append(pair_value)
            player_dict["pair_value"] = pair_value

        pair_values_found = list(set(pair_values_found))

        tiebreaker_rank = 1
        ranked_players = []
        for pair_value in sorted(pair_values_found, reverse=True):
            pair_value_players = [player_dict for player_dict in players if player_dict["pair_value"] == pair_value]
            if len(pair_value_players) == 1:
                player_dict = pair_value_players[0]
                player_dict["tiebreaker_rank"] = tiebreaker_rank
                player_dict["hand_rank_tie"] = False
                ranked_players.append(player_dict)
                tiebreaker_rank += 1
            else:
                pair_value_players = self._order_hands_by_highest_card(pair_value_players)
                for index, player_dict in enumerate(pair_value_players):
                    if index == 0:
                        player_dict["tiebreaker_rank"] = tiebreaker_rank
                        player_dict["hand_rank_tie"] = False
                        tiebreaker_rank += 1
                    else:
                        previous_player = ranked_players[-1]
                        if self._all_card_values_the_same(previous_player["hand"], player_dict["hand"]):
                            player_dict["tiebreaker_rank"] = tiebreaker_rank - 1
                            player_dict["hand_rank_tie"] = True
                            previous_player["hand_rank_tie"] = True
                        else:
                            player_dict["tiebreaker_rank"] = tiebreaker_rank
                            player_dict["hand_rank_tie"] = False
                            tiebreaker_rank += 1

                    ranked_players.append(player_dict)
        return ranked_players[0] if winner_only else ranked_players

    def _hand_tiebreaker_texas_holdem_high_card(self, players, winner_only=True):
        """
        This private method will perform a tiebreaker analysis on multiple Texas Holdem high card hands.

        :param players: List of dictionaries containing the player information with the minimum keys
            {
                "hand": PLAYERS 5 CARD HAND
            }
        :param winner_only: Boolean: defines if the method should return just the winning player or an ordered list of
        all players
        :return:
        """

        ranked_players = self._order_hands_by_highest_card(players)
        self._mark_tied_hands_on_high_card(ranked_players)
        return ranked_players[0] if winner_only else ranked_players


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

    ###################################
    #  PRIVATE HAND ORDERING METHODS  #
    ###################################

    def _order_hands_by_highest_card(self, players):
        """
        This private method will order the given players hands based on the value of their cards.

        :param players: List of dictionaries containing the player information.
        :return:
        """

        for player_dict in players:
            player_dict["hand"] = sorted(player_dict["hand"], key=lambda card: card.value, reverse=True)

        players.sort(key=lambda player_dict: (
        player_dict["hand"][0].value, player_dict["hand"][1].value, player_dict["hand"][2].value,
        player_dict["hand"][3].value, player_dict["hand"][4].value), reverse=True)

        return players

    #################################
    #  PRIVATE MISC HELPER METHODS  #
    #################################

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

    def _find_hand_strength(self, hand_type):
        """
        This private method will find the appropriate hand strength value for the hand type given

        :param hand_type: String: the name of the hand type to find the strength of
        :return: Int: hand strength
        """

        return next(
            (
                hand_definition["strength"]
                for hand_definition in self.texas_holdem_hand_definitions
                if hand_definition["name"] == hand_type
            ),
            None,
        )

    def _find_tiebreaker_method(self, tiebreak_players):
        """
        This private method will return the correct tiebreaker method to use based on the hand_type of the
        tiebreaker_players.

        :param tiebreak_players: List of player dictionaries
        :return: Class Method to use for tiebreakers.
        """

        return next(
            (
                hand_definition["tiebreaker"]
                for hand_definition in self.texas_holdem_hand_definitions
                if hand_definition["name"] == tiebreak_players[0]["hand_type"]
            ),
            None,
        )

    @staticmethod
    def _rank_tiebreak_players(hand_rank, ranked_players, tiebreak_ordered):
        """
        This private method will appropriately rank and add tie-broken players to the ranked_players list.

        :param hand_rank: Int: current hand rank to assign
        :param ranked_players: List of player dictionaries that have been ranked
        :param tiebreak_ordered: List of player dictionaries that have been ordered by the appropriate tiebreak method.
        :return: updated hank_rank value
        """

        current_tiebreaker_rank = None
        for player in tiebreak_ordered:
            if player["hand_rank_tie"]:
                if (
                        current_tiebreaker_rank
                        and player["tiebreaker_rank"]
                        == current_tiebreaker_rank
                ):
                    player["hand_rank"] = hand_rank - 1
                else:
                    current_tiebreaker_rank = player["tiebreaker_rank"]
                    player["hand_rank"] = hand_rank
                    hand_rank += 1
            else:
                player["hand_rank"] = hand_rank
                hand_rank += 1
            ranked_players.append(player)
        return hand_rank

    def _mark_tied_hands_on_high_card(self, ranked_players):
        """
        This private method will search through the provided ranked players and mark players tiebreaker_rank and any
        hand ties.

        :param ranked_players: List of player dictionaries containing at least the "hand" key
        :return: None
        """

        tiebreaker_rank = 1
        for index, player_dict in enumerate(ranked_players):
            if index == 0:
                player_dict["tiebreaker_rank"] = tiebreaker_rank
                player_dict["hand_rank_tie"] = False
                tiebreaker_rank += 1
            else:
                previous_player = ranked_players[index - 1]
                if self._all_card_values_the_same(previous_player["hand"], player_dict["hand"]):
                    player_dict["tiebreaker_rank"] = tiebreaker_rank - 1
                    player_dict["hand_rank_tie"] = True
                    previous_player["hand_rank_tie"] = True
                else:
                    player_dict["tiebreaker_rank"] = tiebreaker_rank
                    player_dict["hand_rank_tie"] = False
                    tiebreaker_rank += 1

    @staticmethod
    def _all_card_values_the_same(hand_a, hand_b):
        """
        This private method checks if the card values for each hand are the same.

        :param hand_a: list of card objects
        :param hand_b: list of card objects
        :return: True if all card.values from hand_a match hand_b
        """

        hand_a.sort(key=lambda card: card.value, reverse=True)
        hand_b.sort(key=lambda card: card.value, reverse=True)

        return (
            True
            if all(
                card_a.value == card_b.value
                for (card_a, card_b) in zip(hand_a, hand_b)
            )
            else False
        )