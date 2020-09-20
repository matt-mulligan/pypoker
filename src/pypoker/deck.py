"""
Deck of cards class.
produces a deck of cards object to be used by the game class
"""

import random
from dataclasses import dataclass, InitVar, field
from typing import Union, List


@dataclass()
class Card(object):
    """
    Class representing a single playing card
    """

    rank_value: InitVar[Union[str, int]]
    suit_value: InitVar[str]
    rank: str = field(init=False, compare=False, repr=False)
    suit: str = field(init=False, compare=False, repr=False)
    value: int = field(init=False, compare=False, repr=False)
    name: str = field(init=False)

    def __post_init__(self, rank_value, suit_value):
        self.rank = self._determine_rank(rank_value)
        self.suit = self._determine_suit(suit_value)
        self.value = self._determine_value(self.rank)
        self.name = self._determine_name(self.rank, self.suit)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    @staticmethod
    def _determine_suit(suit_value: str) -> str:
        """
        determines the suite of the card based on the given value

        :param suit_value: value of the cards suit
        :return:
        """

        suit_mapping = {"C": "Clubs", "D": "Diamonds", "H": "Hearts", "S": "Spades"}

        if suit_value not in suit_mapping.keys():
            raise ValueError(
                f"Suit value '{suit_value}' is not in list of valid values '{suit_mapping.keys()}"
            )

        return suit_mapping[suit_value]

    @staticmethod
    def _determine_rank(rank_value: Union[str, int]) -> str:
        """
        returns the english rank of the card based on the value.

        :param rank_value: integer/str representing the value of the card between 2 and A
        (where 2 represents a 2 and A represents an ace)
        :return: English rank of the card
        """

        rank_mapping = {
            "2": "Two",
            "3": "Three",
            "4": "Four",
            "5": "Five",
            "6": "Six",
            "7": "Seven",
            "8": "Eight",
            "9": "Nine",
            "10": "Ten",
            "J": "Jack",
            "Q": "Queen",
            "K": "King",
            "A": "Ace",
        }

        if str(rank_value) not in rank_mapping.keys():
            raise ValueError(
                f"Specified card rank {rank_value} is not in value mapping dictionary '{rank_mapping}'."
            )

        return rank_mapping[str(rank_value)]

    @staticmethod
    def _determine_value(rank: str) -> int:
        """
        returns the numeric value of a rank, used for greater_than and less_than comparisons

        :param rank: str representing the rank of a card between "Two" and "Ace"
        :return: comparison value of a card
        """

        return {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": 11,
            "Queen": 12,
            "King": 13,
            "Ace": 14,
        }[rank]

    @staticmethod
    def _determine_name(rank: str, suit: str) -> str:
        """
        Simple method to return the full english name of a card

        :param rank: the english rank of the card.
        :param suit: the english suit of the card.
        :return: Full english name of the card
        """

        return f"{rank} of {suit}"


class Deck(object):
    def __init__(self):
        self.cards_all: List[Card] = self._build_all_cards()
        self.cards_available: List[Card] = self.cards_all.copy()
        self.cards_used: List[Card] = []

    @staticmethod
    def _build_all_cards() -> List[Card]:
        """
        Method to populate the self.cards_all attribute

        :return: list of all 52 playing card objects
        """

        cards = []

        for suit in ["H", "D", "C", "S"]:
            for value in [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]:
                cards.append(Card(value, suit))

        return cards

    def shuffle(self) -> None:
        """
        shuffles the avaliable cards in the deck, reordering self.avaliable_cards object

        :return: None
        """

        random.shuffle(self.cards_available)

    def draw(self, num: int = 1) -> List[Card]:
        """
        draws the number of cards from the deck as specified.

        :param num: the number of cards to draw
        :return: the number of card objecs specified
        """

        if num > len(self.cards_available):
            raise ValueError("Not enough cards left in the deck!")

        # Select the cards to return
        cards = self.cards_available[:num]

        # Add the cards to the used list
        self.cards_used.extend(cards)

        # remove the cards from the availiable list
        self.cards_available = self.cards_available[num:]

        return cards

    def reset(self):
        """
        resets the cards in the deck. removes all cards from the self.cards_used list and adds all cards to the
        self.cards_avaliable list

        :return: None
        """

        self.cards_used = []
        self.cards_available = self.cards_all.copy()

    @staticmethod
    def order_cards(cards: List[Card], descending: bool = False) -> List[Card]:
        """
        helper method that will order a list of card objects
        :param cards: List of card objects
        :param descending: boolean, should the ordering be descending
        :return:
        """

        if not all(isinstance(card, Card) for card in cards):
            raise ValueError(
                "All objects within cards value must be an instance of the Cards Class"
            )

        ordered_cards = []
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]

        for suit in suits:
            suited_cards = [card for card in cards if card.suit == suit]
            suited_cards.sort(key=lambda x: x.value, reverse=descending)
            ordered_cards.extend(suited_cards)

        return ordered_cards
