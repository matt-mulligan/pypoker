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
