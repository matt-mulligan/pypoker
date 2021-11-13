"""
pypoker.engine package
----------------------

subpackage to handle all of the logical calculations for each type of poker game.
the following tasks will be handled by the pypoker.engine classes:
    determine players best hand
    rank players current hands
    find odds of a player making X hand type from current position
    find odds of each player winning from current position
"""
from abc import ABCMeta, abstractmethod
from itertools import groupby, product
from operator import itemgetter
from typing import List, Dict

from pypoker.deck import Card
from pypoker.player import BasePlayer


class BasePokerEngine(object, metaclass=ABCMeta):
    """
    Base class for the pypoker.engine package.
    """

    @abstractmethod
    def find_player_best_hand(self, player: BasePlayer, board: List[Card], **kwargs):
        """
        Abstract method to determine the given players best possible hand with the cards currently available
        """

    # Shared utility methods for all engine classes
    # ---------------------------------------------
    @staticmethod
    def group_cards_by_suit(cards: List[Card]) -> Dict[str, List[Card]]:
        """
        Shared utility method of BasePokerEngine class that will group the given cards by suit.

        :param cards: List of pypoker.deck.Card objects
        :return: Dictionary of lists of cards by suit "Clubs", "Diamonds", "Hearts", "Spades"
        """

        return {
            suit: list(group)
            for suit, group
            in groupby(sorted(cards, key=lambda card: card.suit), key=lambda card: card.suit)
        }

    @staticmethod
    def group_cards_by_value(cards: List[Card]) -> Dict[int, List[Card]]:
        """
        Shared utility method of BasePokerEngine class to group the given cards by value.

        :param cards: List of pypoker.deck.Card objects
        :return: Dictionary of lists of cards by card value (2-14)
        """

        return {
            value: list(group)
            for value, group
            in groupby(sorted(cards, key=lambda card: card.value), key=lambda card: card.value)
        }

    def find_consecutive_value_cards(
            self, cards: List[Card], treat_ace_low: bool = True, run_size: int = None
    ) -> List[List[Card]]:
        """
        Shared utility method of BasePokerEngine to find consecutive runs of cards based on value.

        :param cards: List of card objects.
        :param treat_ace_low: boolean indicating if the ace should also be treated as a low card.
        :param run_size: integer indicating what size of run you are looking for. If given, then all overlapping
            runs of this size are returned. If not given then only the longest, non overlapping runs are returned

        :return: List of lists of card objects for each run of cards found
        """

        # group cards into lists of values and get a list of unique card values
        cards_by_value = self.group_cards_by_value(cards)
        card_values = list(cards_by_value)
        if treat_ace_low and 14 in card_values:
            card_values.append(1)
            cards_by_value[1] = cards_by_value[14]

        runs = self._find_consecutive_numbers(card_values)
        if run_size:
            runs = self._split_consecutive_runs_to_size(runs, run_size)

        card_runs = []
        for run in runs:
            card_lists = [cards_by_value[value] for value in run]
            card_runs.extend([list(p) for p in product(*card_lists)])

        return card_runs

    # Private Method Implementations
    # ------------------------------
    @staticmethod
    def _find_consecutive_numbers(numbers: List[int]) -> List[List[int]]:
        """
        Private method to split a list of sorted numbers into lists of consecutive runs.

        :param numbers: list of integers
        :return: list of list of integers that are consecutive
        """

        numbers.sort()
        # create marker list showing breaks in consecutive values, skip first value of list as it has no comparitor
        # output list will always be one item less than original
        is_consecutive = [
            True if value == numbers[index - 1] + 1 else False
            for index, value in enumerate(numbers[1:], start=1)
        ]

        # split card_values into list of runs
        start_pos = 0
        runs = []
        for index, still_consecutive in enumerate(is_consecutive):
            if not still_consecutive:
                end_pos = index + 1
                runs.append(numbers[start_pos: end_pos])
                start_pos = end_pos
        runs.append(numbers[start_pos:])

        return runs

    @staticmethod
    def _split_consecutive_runs_to_size(runs: List[List[int]], run_size: int) -> List[List[int]]:
        """
        given a list of lists of integers, with each sublist being consecutive integers, find all
        consecutive runs of numbers that match the given run_size

        :param runs: list of list of integers that are consecutive
        :param run_size: integer specify the size of run we are seeking
        :return: List of lists of consecutive numbers that are of size run_size
        """

        # remove any runs that arent at least the run_size length
        runs = [run for run in runs if len(run) >= run_size]

        # chunk the qualified runs into overlapping runs of the correct size
        sized_runs = [
            [
                run[start: end] for start, end in enumerate(range(run_size, len(run) + 1))
            ]
            for run in runs
        ]

        # flatten lists
        return [val for sublist in sized_runs for val in sublist]