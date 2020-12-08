"""
Hand Solver - Base Class

Abstract Base Class of the hand_solver package.
"""
import collections
from abc import ABCMeta, abstractmethod
from itertools import combinations, product, groupby

from typing import List, Dict, Any

from pypoker.deck import Card


class BaseHandSolver(metaclass=ABCMeta):
    @abstractmethod
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
            "hand_description": String - full description of the hand
        }
        child classes implementing this abstract method can choose to expand the dictionary where
        appropriate but must at minimum have the above keys
        """

    @abstractmethod
    def rank_hands(self, player_hands: Dict[str, List[Card]]):
        """
        Abstract method to implement to rank players hands against each other

        :param player_hands: Dict in format of
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

    @abstractmethod
    def find_odds(self, player_cards: Dict[str, List[Card]], board_cards: List[Card]):
        """
        Abstract method to implement to find the odds of all players winning from the current situation.

        :param player_cards: Dictionary, of player names and their hole cards
        :param board_cards: List of cards representing the current board cards
        :return: Dictionary of player names and their likelyhood of winning from this situation.
        """

    ####################################
    #  SHARED HAND GENERATION METHODS  #
    ####################################
    @staticmethod
    def get_all_combinations(
        hole_cards: List[Card],
        board_cards: List[Card],
        hand_size: int,
        always_use_hole_cards=False,
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

        if always_use_hole_cards:
            return [
                combo
                for combo in all_combinations
                if all([True for card in hole_cards if card in combo])
            ]
        else:
            return all_combinations

    #####################################
    #  SHARED OUTS CALCULATION METHODS  #
    #####################################

    def build_out_string(self, suits, values, draws):
        """
        THis public shared method will produce a list of out strings, that represent what cards can be drawn to give
        the player an out.

        THe composition of these strings are very important and follow the below rules:
             - Out strings will contain an entry for each card that is yet to be drawn
             - Out strings will seperate card entries with a dash (-)
             - Out string card entries will have the first character represent the suit (S,C,D,H)
             - Out string card entries will have the second characters represent the value of the card (2,3,4,5,6,7,8,9,T,J,Q,K,A)
             - if a value is unimportant then it can use a wildcard (*) to represent ANY value.
             - a card that isnt required (e.g. the second card in a one card out) will be represented by **

         :param suits: List of suits for each draw card required e.g. ["Hearts", "Hearts"
         :param values: List of values for each card required (ANY used for wildcard e.g. [4, 14]
         :param draws: Int representing total cards yet to be drawn
        """

        out_string_parts = []

        for index in range(draws):
            suit = "*"
            value = "*"

            if index < len(suits):
                suit = {
                    "Hearts": "H",
                    "Diamonds": "D",
                    "Clubs": "C",
                    "Spades": "S",
                    "ANY": "*",
                }[suits[index]]

                value = {
                    2: "2",
                    3: "3",
                    4: "4",
                    5: "5",
                    6: "6",
                    7: "7",
                    8: "8",
                    9: "9",
                    10: "T",
                    11: "J",
                    12: "Q",
                    13: "K",
                    14: "A",
                    "ANY": "*",
                }[values[index]]

            out_string_parts.append(f"{suit}{value}")

        return "-".join(out_string_parts)

    def claim_out_strings(self, utilised_outs, potential_outs, drawable_cards):
        """
        Public method to claim all possible out combinations for the cards given

        :param utilised_outs: List of out strings that have already been claimed
        :param potential_outs: List of out strings that we want to assess for claiming
        :param drawable_cards: List of card objects representing all of the cards yet to be drawn
        """

        test_outs = utilised_outs.copy()
        claimed_outs = []

        for out in potential_outs:
            combos = self._create_combos_for_out_string(out, drawable_cards)
            combos = [combo for combo in combos if combo not in test_outs]
            test_outs.extend(combos)
            claimed_outs.extend(combos)

        return claimed_outs

    def _create_combos_for_out_string(self, out_string, drawable_cards):
        """
        Method to create all possible draw combinations with the drawable cards based on the out string provided.

        :param out_string: string describing the out conditions
        :param drawable_card: list opf card objects representing all possible draw cards.
        """

        card_candidates = []

        for card_str in out_string.split("-"):
            suit = card_str[0]
            value = card_str[1]

            if suit == "*" and value == "*":
                card_candidates.append([card.identity for card in drawable_cards])
            elif suit == "*":
                card_candidates.append(
                    [
                        card.identity
                        for card in drawable_cards
                        if card.identity[1] == value
                    ]
                )
            elif value == "*":
                card_candidates.append(
                    [
                        card.identity
                        for card in drawable_cards
                        if card.identity[0] == suit
                    ]
                )
            else:
                card_candidates.append([card_str])

        combos = product(*card_candidates)
        combos = [sorted(list(combo)) for combo in combos]
        combos = [combo for combo in combos if len(combo) == len(set(combo))]
        combos.sort()
        combos = list(combo for combo, _ in groupby(combos))
        return combos
