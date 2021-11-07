"""
PyPoker.Player Package
----------------------

Holds all logic and structures to represent the player classes in pypoker.
"""

from abc import ABCMeta
from typing import List

from pypoker.deck import Card


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
    ):
        self.name = name
        self._chips = None if not chips else self._valid_chips_check(chips)
        self._hole_cards = (
            None if not hole_cards else self._valid_hole_cards_check(hole_cards)
        )
        self._table_pos = (
            None if table_pos is None else self._valid_table_pos_check(table_pos)
        )
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

    # validity checker methods
    @staticmethod
    def _valid_chips_check(chips):
        if not isinstance(chips, int) or chips < 0:
            raise ValueError("Player chips must be set to a positive integer")
        return chips

    @staticmethod
    def _valid_hole_cards_check(cards):
        if not isinstance(cards, list):
            raise ValueError("hole cards must be a list object")
        if any([not isinstance(card, Card) for card in cards]):
            raise ValueError("hole card objects must all be card objects")
        return cards

    @staticmethod
    def _valid_table_pos_check(pos):
        if not isinstance(pos, int) or not 1 <= pos <= 9:
            raise ValueError("table position must be set to between 1 and 9")
        return pos

    @staticmethod
    def _valid_bet_check(bet):
        if not isinstance(bet, int) or bet < 0:
            raise ValueError("bet must be set to a positive integer or zero")
        return bet
