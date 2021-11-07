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
from itertools import groupby
from operator import itemgetter
from typing import List

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
    def find_consecutive_cards(self, cards: List[Card], treat_ace_low: bool = True, run_size: int = None):
        """
        utility method to find consecutive runs of cards based on value.

        :param cards: List of card objects.
        :param treat_ace_low: boolean indicating if the ace should also be treated as a low card.
        :param run_size: integer indicating what size of run you are looking for. If given, then all overlapping
            runs of this size are returned. If not given then only the longest, non overlapping runs are returned

        :return: List of lists of card objects for each run of cards found
        """

        # Add a value of one to the available list if we are to treat ace as low and an ace is present
        card_values = [card.value for card in cards]
        if treat_ace_low and 14 in card_values:
            card_values.append(1)
        card_values.sort()

        # find all consecutive runs (of any size)
        runs = []
        for k, g in groupby(enumerate(card_values), lambda ix: ix[0] - ix[1]):
            runs.append((list(map(itemgetter(1), g))))

        # If run_size is set, get all groups of that size (including splitting larger groups with overlapping values)
        if run_size:
            sized_runs = []
            runs = [run for run in runs if len(run) >= run_size]

            for run in runs:
                start = 0
                end = run_size - 1
                while not end > len(run):
                    sized_runs.append(run[start:end])
                    start += 1
                    end += 1

            runs = sized_runs

        # remove any one values from list and replace with 14's before adding back cards
        runs = [[14 if value == 1 else value for value in run] for run in runs]

        # assign back cards based on values
        return [
            [
                [card for card in cards if card.value == value][0] for value in run
            ] for run in runs
        ]




