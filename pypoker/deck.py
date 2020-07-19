"""
Deck of cards class.
produces a deck of cards object to be used by the game class
"""

import random


class Deck (object):

    def __init__(self):
        self.cards_all = self._build_all_cards()
        self.cards_avaliable = self.cards_all
        self.cards_used = []

    @staticmethod
    def _build_all_cards():
        """
        Method to populate the self.cards_all attribute

        :return: list of all 52 playing card objects
        """

        cards = []

        for suit in range(4):
            for value in range(2, 15):
                cards.append(Card(value, suit))

        return cards

    def shuffle(self):
        """
        shuffles the avaliable cards in the deck, reordering self.avaliable_cards object

        :return: None
        """

        random.shuffle(self.cards_avaliable)

    def draw(self, num=1):
        """
        draws the number of cards from the deck as specified.

        :param num: the number of cards to draw
        :return: the number of card objecs specified
        """

        if num > len(self.cards_avaliable):
            raise ValueError("Not enough cards left in the deck!")

        # Select the cards to return
        cards = self.cards_avaliable[:num]

        # Add the cards to the used list
        self.cards_used.extend(cards)

        # remove the cards from the availiable list
        self.cards_avaliable = self.cards_avaliable[num:]

        return cards

    def reset(self):
        """
        resets the cards in the deck. removes all cards from the self.cards_used list and adds all cards to the
        self.cards_avaliable list

        :return: None
        """

        self.cards_used = []
        self.cards_avaliable = self.cards_all

    def get_card_from_img_path(self, img_path):
        """
        helper method that will return the correct card object based on the image path provided.
        :param img_path:
        :return:
        """
        for card in self.cards_all:
            if card.img == img_path:
                return card

    @staticmethod
    def order_cards(cards, descending=False):
        """
        helper method that will order a list of card objects
        :param cards:
        :param descending: boolean, should the ordering be descending
        :return:
        """

        ordered_cards = []
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]

        for suit in suits:
            suited_cards = [card for card in cards if card.suit == suit]
            suited_cards.sort(key=lambda x: x.value, reverse=descending)
            ordered_cards.extend(suited_cards)

        return ordered_cards


class Card (object):
    """
    Class representing a single playing card
    """

    SUIT_MAPPING = {0: "Clubs", 1: "Diamonds", 2: "Hearts", 3: "Spades"}
    VALUE_MAPPING = {
        2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
        9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"
    }

    def __init__(self, card_value, suit_value):
        """
        the Init method of the card class.

        :param card_value: integer representing the value of the card between 2 and 14
        (where 2 represents a 2 and 14 represents and ace)
        :param suit_value: Integer representing the suit of the card between 0 and 3 mapping to the suit of the card
        (0=Clubs, 1=Diamonds, 2=Hearts, 3=Spades)
        """

        self.value = card_value
        self.suit = self._determine_suit(suit_value)
        self.rank = self._determine_rank(card_value)
        self.name = self._determine_name(self.rank, self.suit)

    def _determine_suit(self, suit_value):
        """
        determines the suite of the card based on the given value
        (0=Clubs, 1=Diamonds, 2=Hearts, 3=Spades)

        :param suit_value: value of the cards suit
        :return:
        """

        if suit_value not in self.SUIT_MAPPING.keys():
            raise ValueError(f"Suit value '{suit_value}'  is not in list of valid values '{self.SUIT_MAPPING}")

        return self.SUIT_MAPPING[suit_value]

    def _determine_rank(self, value):
        """
        returns the english rank of the card based on the value.

        :param value: integer representing the value of the card between 2 and 14
        (where 2 represents a 2 and 14 represents and ace)
        :return: English rank of the card
        """

        if value not in self.VALUE_MAPPING.keys():
            raise ValueError(f"Specified card value {value} is not in value mapping dictionary '{self.VALUE_MAPPING}'.")

        return self.VALUE_MAPPING[value]

    @staticmethod
    def _determine_name(rank, suit):
        """
        Simple method to return the full english name of a card

        :param rank: the english rank of the card.
        :param suit: the english suit of the card.
        :return: Full english name of the card
        """

        return f"{rank} of {suit}"
