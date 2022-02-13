"""
PyPoker.Player Package
----------------------

Holds all logic and structures to represent the player classes in pypoker.
"""

from abc import ABCMeta
from typing import List

from pypoker.constructs import Card, Hand


class BasePlayer(object, metaclass=ABCMeta):
    """
    Base Player Class for PyPoker
    """

    def __init__(
        self,
        name: str,
        chips: int = None,
        hole_cards: List[Card] = None,
        table_pos: int = None,
        hand: Hand = None,
    ):
        self.name = name
        self._chips = None if not chips else self._valid_chips_check(chips)
        self._hole_cards = (
            None if not hole_cards else self._valid_hole_cards_check(hole_cards)
        )
        self._table_pos = (
            None if table_pos is None else self._valid_table_pos_check(table_pos)
        )
        self._hand = None if not hand else self._valid_hand_check(hand)
        self._current_bet = None

    # Property getters
    @property
    def chips(self):
        return self._chips

    @property
    def hole_cards(self):
        return self._hole_cards

    @property
    def table_pos(self):
        return self._table_pos

    @property
    def current_bet(self):
        return self._current_bet

    @property
    def hand(self):
        return self._hand

    # Property setters
    @chips.setter
    def chips(self, chips: int):
        self._chips = self._valid_chips_check(chips)

    @hole_cards.setter
    def hole_cards(self, cards: List[Card]):
        self._hole_cards = self._valid_hole_cards_check(cards)

    @table_pos.setter
    def table_pos(self, pos: int):
        self._table_pos = self._valid_table_pos_check(pos)

    @current_bet.setter
    def current_bet(self, bet: int):
        self._current_bet = self._valid_bet_check(bet)

    @hand.setter
    def hand(self, bet: int):
        self._hand = self._valid_hand_check(bet)

    # validity checker methods
    @staticmethod
    def _valid_chips_check(chips):
        """
        checks that the chips value passed to player is an integer and is greater than or equal to zero
        """
        if not isinstance(chips, int) or chips < 0:
            raise ValueError("Player chips must be set to a positive integer")
        return chips

    @staticmethod
    def _valid_hole_cards_check(cards):
        """
        checks that the hole card value passed to player is a list and all objects of lists are of type Card
        """
        if not isinstance(cards, list):
            raise ValueError("hole cards must be a list object")
        if any([not isinstance(card, Card) for card in cards]):
            raise ValueError("hole card objects must all be card objects")
        return cards

    @staticmethod
    def _valid_table_pos_check(pos):
        """
        checks that the table position value passed to player is an integer and between 1 and 9
        """
        if not isinstance(pos, int) or not 1 <= pos <= 9:
            raise ValueError("table position must be set to between 1 and 9")
        return pos

    @staticmethod
    def _valid_bet_check(bet):
        """
        checks the value passed to current bet is an integer is greater than or equal to zero
        """
        if not isinstance(bet, int) or bet < 0:
            raise ValueError("bet must be set to a positive integer or zero")
        return bet

    @staticmethod
    def _valid_hand_check(hand):
        """
        checks that the hand value passed is of type Hand
        """

        if not isinstance(hand, Hand):
            raise ValueError("player.hand values must be of type Hand")
        return hand
