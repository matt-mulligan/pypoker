import sys
from pathlib import Path
from typing import List

from pytest import fixture

from pypoker.constructs import Card, AnyCard, AnyValueCard, AnySuitCard, Deck

here = Path(__file__).absolute()
tests_path = here.parent.parent
src_path = here.parent.parent.parent / "src"
fixtures_path = tests_path / "fixtures"

sys.path.insert(0, str(src_path))


@fixture
def get_deck_minus_set():
    """
    test helper to return a full deck of cards minus the cards provided
    """

    def _get_deck_minus_set(exclude_cards: List[Card]):
        deck_cards = Deck().cards_all
        return [card for card in deck_cards if card not in exclude_cards]

    return _get_deck_minus_set


@fixture
def get_test_cards():
    """
    test helper method to get card objects
    """

    def _get_test_cards(card_ids: str):
        card_ids = card_ids.split("|")

        return [Card(card_id) if len(card_id) == 2 else _get_special_card(card_id) for card_id in card_ids]

    return _get_test_cards


def _get_special_card(card_id):
    """build SpecialCard construct for test sets"""

    return {
        "ANY_CARD": AnyCard(""),
        "ANY_HEART": AnyValueCard("H"),
        "ANY_DIAMOND": AnyValueCard("D"),
        "ANY_SPADE": AnyValueCard("S"),
        "ANY_CLUB": AnyValueCard("C"),
        "ANY_TWO": AnySuitCard("2"),
        "ANY_THREE": AnySuitCard("3"),
        "ANY_FOUR": AnySuitCard("4"),
        "ANY_FIVE": AnySuitCard("5"),
        "ANY_SIX": AnySuitCard("6"),
        "ANY_SEVEN": AnySuitCard("7"),
        "ANY_EIGHT": AnySuitCard("8"),
        "ANY_NINE": AnySuitCard("9"),
        "ANY_TEN": AnySuitCard("T"),
        "ANY_JACK": AnySuitCard("J"),
        "ANY_QUEEN": AnySuitCard("Q"),
        "ANY_KING": AnySuitCard("K"),
        "ANY_ACE": AnySuitCard("A"),
    }[card_id]
