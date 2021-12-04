"""
pypoker.deck module
---------------------

Basic Dataclasses containing logic to represent a deck of cards as well as individual card objects
"""

import random
from dataclasses import dataclass, InitVar, field
from typing import List

from pypoker.constants import (
    GAME_TYPES,
    GAME_HAND_TYPES,
    GAME_HAND_STRENGTHS,
    GAME_HAND_TIEBREAKERS_ARGS,
    GAME_HAND_NUM_CARDS,
    CARD_ANY_VALUE,
    CARD_ANY_SUIT,
)
from pypoker.exceptions import InvalidGameError, InvalidHandTypeError, GameMismatchError

CARD_SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
CARD_RANKS = [
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
]

CARD_ID_SUITS = {"C": "Clubs", "D": "Diamonds", "H": "Hearts", "S": "Spades"}
CARD_ID_RANKS = {
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
    "T": "Ten",
    "J": "Jack",
    "Q": "Queen",
    "K": "King",
    "A": "Ace",
}


@dataclass()
class Card(object):
    """
    Construct class used to represent a card within pypoker
    """

    card_id: InitVar[str]
    rank: str = field(init=False, compare=False, repr=False)
    suit: str = field(init=False, compare=False, repr=False)
    value: int = field(init=False, compare=False, repr=False)
    name: str = field(init=False)

    def __post_init__(self, card_id):
        self.identity = self._check_card_id(card_id)
        self.rank = self._determine_rank(self.identity)
        self.suit = self._determine_suit(self.identity)
        self.value = self._determine_value(self.rank)
        self.name = self._determine_name(self.rank, self.suit)

    def __gt__(self, other):
        if any(isinstance(obj, SpecialCard) for obj in [self, other]):
            raise ValueError("Cannot compare any cards of type SpecialCard")

        return self.value > other.value

    def __lt__(self, other):
        if any(isinstance(obj, SpecialCard) for obj in [self, other]):
            raise ValueError("Cannot compare any cards of type SpecialCard")

        return self.value < other.value

    @staticmethod
    def _check_card_id(card_id: str) -> str:
        """
        Private method used to check the ID passed for the card creation is valid and then assign it to the card object
        """

        if len(card_id) != 2:
            raise ValueError("Card ID provided must be exactly 2 characters long.")

        if card_id[0] not in CARD_ID_SUITS.keys():
            raise ValueError(
                f"Card ID first character '{card_id[0]}' is not within valid list of "
                f"suit identifiers '{CARD_ID_SUITS.keys()}'"
            )

        if card_id[1] not in CARD_ID_RANKS.keys():
            raise ValueError(
                f"Card ID second character '{card_id[1]}' is not within valid list of "
                f"rank identifiers '{CARD_ID_RANKS.keys()}'"
            )

        return card_id

    @staticmethod
    def _determine_suit(card_id: str) -> str:
        """
        determines the suite of the card based on the card id value

        :param card_id: 2 character string representation of the card. First character representing Suit,
        Second character representing the rank
        :return: Suit value of the card
        """

        return CARD_ID_SUITS[card_id[0]]

    @staticmethod
    def _determine_rank(card_id: str) -> str:
        """
        returns the english rank of the card based on the card id value

        :param card_id: 2 character string representation of the card. First character representing Suit,
        Second character representing the rank
        :return: English rank of the card
        """

        return CARD_ID_RANKS[card_id[1]]

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
            CARD_ANY_VALUE: None,
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


@dataclass()
class SpecialCard(Card):
    """
    data class to identify "special" cards
    special cards are ones that are not used within games but represent abstract card sets
    e.g. any 7 card, any heart card, any card at all
    """


@dataclass()
class AnyValueCard(SpecialCard):

    rank: str = field(init=False, compare=False, repr=False)
    suit: str = field(init=False, compare=False, repr=False)
    value: int = field(init=False, compare=False, repr=False)
    name: str = field(init=False)

    def __post_init__(self, card_id):
        self.identity = self._check_card_any_value_id(card_id)
        self.rank = CARD_ANY_VALUE
        self.suit = self._determine_suit(self.identity)
        self.value = self._determine_value(self.rank)
        self.name = self._determine_name(self.rank, self.suit)

    @staticmethod
    def _check_card_any_value_id(card_id):
        """
        checks the ID value passed to AnyValueCard class.
        Value should be just the suit component
        """

        if len(card_id) != 1:
            raise ValueError(
                "Card ID provided for AnyValueCard must be exactly 1 character."
            )

        if card_id not in CARD_ID_SUITS.keys():
            raise ValueError(
                f"Card ID '{card_id}' is not within valid list of suit identifiers '{CARD_ID_SUITS.keys()}'"
            )

        return f"{card_id}{CARD_ANY_VALUE}"


@dataclass()
class AnySuitCard(SpecialCard):

    rank: str = field(init=False, compare=False, repr=False)
    suit: str = field(init=False, compare=False, repr=False)
    value: int = field(init=False, compare=False, repr=False)
    name: str = field(init=False)

    def __post_init__(self, card_id):
        self.identity = self._check_card_any_suit_id(card_id)
        self.rank = CARD_ID_RANKS[card_id]
        self.suit = CARD_ANY_SUIT
        self.value = self._determine_value(self.rank)
        self.name = self._determine_name(self.rank, self.suit)

    @staticmethod
    def _check_card_any_suit_id(card_id):
        """
        checks the ID value passed to AnySuitCard class.
        Value should be just the suit component
        """

        if len(card_id) != 1:
            raise ValueError(
                "Card ID provided for AnySuitCard must be exactly 1 character."
            )

        if card_id not in CARD_ID_RANKS.keys():
            raise ValueError(
                f"Card ID '{card_id}' is not within valid list of rank identifiers '{CARD_ID_RANKS.keys()}'"
            )

        return f"{CARD_ANY_SUIT}{card_id}"


@dataclass()
class AnyCard(SpecialCard):

    rank: str = field(init=False, compare=False, repr=False)
    suit: str = field(init=False, compare=False, repr=False)
    value: int = field(init=False, compare=False, repr=False)
    name: str = field(init=False)

    def __post_init__(self, card_id):
        self.identity = f"{CARD_ANY_SUIT}{CARD_ANY_VALUE}"
        self.rank = CARD_ANY_VALUE
        self.suit = CARD_ANY_SUIT
        self.value = self._determine_value(self.rank)
        self.name = self._determine_name(self.rank, self.suit)


class Deck(object):
    """
    Construct class used to represent a deck of cards within pypoker
    """

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
            for value in [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "T",
                "J",
                "Q",
                "K",
                "A",
            ]:
                card_id = f"{suit}{value}"
                cards.append(Card(card_id))

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


class Hand(object):
    """
    Construct class used to represent a hand within pypoker.
    """

    def __init__(
        self, game: str, hand_type: str, cards: List[Card], tiebreakers: List[int]
    ):
        self.game = self._validate_game(game)
        self.type = self._validate_type(game, hand_type)
        self.cards = self._validate_cards(game, hand_type, cards)
        self.tiebreakers = self._validate_tiebreakers(game, hand_type, tiebreakers)
        self.strength = self._get_hand_strength(game, hand_type)

    def __eq__(self, other):
        """
        Tests equality of hands in terms of hand type, strength and tiebreakers.
        equality check does not check that hand.cards are the same.
        """
        if self.game != other.game:
            raise GameMismatchError(
                "Hand comparisons can only occur for hands of the same game type."
            )

        return self.strength == other.strength and self.tiebreakers == other.tiebreakers

    def __gt__(self, other):
        """
        Tests equality of hands in terms of hand type, strength and tiebreakers.
        equality check does not check that hand.cards are the same.
        """
        if self.game != other.game:
            raise GameMismatchError(
                "Hand comparisons can only occur for hands of the same game type."
            )

        if self.strength > other.strength:
            return True
        if self.strength < other.strength:
            return False

        for self_value, other_value in zip(self.tiebreakers, other.tiebreakers):
            if self_value is None and other_value is None:
                continue
            if self_value is None and other_value is not None:
                return False
            if other_value is None and self_value is not None:
                return True
            if self_value > other_value:
                return True
            if self_value < other_value:
                return False

        return False

    def __lt__(self, other):
        """
        Tests equality of hands in terms of hand type, strength and tiebreakers.
        equality check does not check that hand.cards are the same.
        """
        if self.game != other.game:
            raise GameMismatchError(
                "Hand comparisons can only occur for hands of the same game type."
            )

        if self.strength > other.strength:
            return False
        if self.strength < other.strength:
            return True

        for self_value, other_value in zip(self.tiebreakers, other.tiebreakers):
            if self_value is None and other_value is None:
                continue
            if self_value is None and other_value is not None:
                return True
            if other_value is None and self_value is not None:
                return False
            if self_value > other_value:
                return False
            if self_value < other_value:
                return True

        return False

    def __ge__(self, other):
        """
        Tests equality of hands in terms of hand type, strength and tiebreakers.
        equality check does not check that hand.cards are the same.
        """
        if self.__eq__(other) or self.__gt__(other):
            return True

        return False

    def __le__(self, other):
        """
        Tests equality of hands in terms of hand type, strength and tiebreakers.
        equality check does not check that hand.cards are the same.
        """
        if self.__eq__(other) or self.__lt__(other):
            return True

        return False

    @staticmethod
    def _validate_game(game: str) -> str:
        """
        private method to validate the game value.

        :param game: value to validate

        :return: validated game type
        """

        if game not in GAME_TYPES:
            raise InvalidGameError(f"Game type '{game}' is invalid")

        return game

    @staticmethod
    def _validate_type(game: str, hand_type: str) -> str:
        """
        private method to validate the hand type giv

        :param game: type of game the hand is from
        :param hand_type: the hand type to validate

        :return: validated hand type
        """

        hand_types = GAME_HAND_TYPES[game]
        if hand_type not in hand_types:
            raise InvalidHandTypeError(f"Hand type '{hand_type}' is invalid")

        return hand_type

    @staticmethod
    def _validate_cards(game: str, hand_type: str, cards: List[Card]) -> List[Card]:
        """
        private method to validate card objects.

        :param cards: value to validate

        :return: validated cards object
        """

        if not all(isinstance(card, Card) for card in cards):
            raise ValueError(
                "Cards object passed to hand must be a list of Card objects"
            )

        min_cards, max_cards = GAME_HAND_NUM_CARDS[game][hand_type]
        if not min_cards <= len(cards) <= max_cards:
            raise ValueError(
                f"{game} {hand_type} hand required between {min_cards} and {max_cards} cards"
            )

        return cards

    @staticmethod
    def _get_hand_strength(game: str, hand_type: str) -> int:
        """
        private method to get the strength of the hand type for a specific game

        :param game: the type of poker game
        :param hand_type: the type of poker hand

        :return: strength of the hand type for the specific game type
        """

        hand_strengths = GAME_HAND_STRENGTHS[game]
        return hand_strengths[hand_type]

    @staticmethod
    def _validate_tiebreakers(
        game: str, hand_type: str, tiebreakers: List[int]
    ) -> List[int]:
        """
        private method to check that the tiebreaker lists has the correct datatypes and number of args
        based on the game and hand types

        :param game: the type of poker game
        :param hand_type: the type of hand
        :param tiebreakers: value to validate

        :return: validated list of tiebreakers
        """

        if not all(isinstance(arg, int) or arg is None for arg in tiebreakers):
            raise ValueError(
                "all arguments in tiebreakers must be integers or Nonetype"
            )

        arg_num = GAME_HAND_TIEBREAKERS_ARGS[game][hand_type]
        if not len(tiebreakers) == arg_num:
            raise ValueError(f"{game} {hand_type} hand requires {arg_num} tiebreakers")

        return tiebreakers
