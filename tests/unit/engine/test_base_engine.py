from decimal import Decimal
from typing import List, Dict

from pytest import fixture, mark

from pypoker.constants import HandType
from pypoker.constructs import Card, Deck
from pypoker.engine import BasePokerEngine
from pypoker.player import BasePlayer


@fixture
def base_engine():
    class FakePokerEngine(BasePokerEngine):
        def find_player_best_hand(
            self, player: BasePlayer, board: List[Card], **kwargs
        ):
            pass

        def rank_player_hands(self, players: List[BasePlayer]):
            pass

        def find_player_outs(self, player: BasePlayer, hand_type: HandType, board: List[Card], deck: Deck) -> List[List[Card]]:
            pass

        def find_player_odds(self, players: List[BasePlayer], board: List[Card], drawable_cards: Deck) -> Dict[str, Decimal]:
            pass

    return FakePokerEngine()


def test_when_group_cards_by_suit_then_correct_dict_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D5|H8|D6|D9|ST|SK|C2|C8|DA|S4")

    result = base_engine.group_cards_by_suit(cards)
    assert isinstance(result, dict)
    assert result["Diamonds"] == [cards[0], cards[2], cards[3], cards[8]]
    assert result["Hearts"] == [cards[1]]
    assert result["Spades"] == [cards[4], cards[5], cards[9]]
    assert result["Clubs"] == [cards[6], cards[7]]


def test_when_group_cards_by_suit_and_suit_missing_then_empty_lists_in_return_list(
    base_engine, get_test_cards
):
    cards = get_test_cards("D5|H8|D6")

    result = base_engine.group_cards_by_suit(cards)
    assert isinstance(result, dict)
    assert result["Diamonds"] == [cards[0], cards[2]]
    assert result["Hearts"] == [cards[1]]
    assert result["Clubs"] == []
    assert result["Spades"] == []


def test_when_group_cards_by_value_then_empty_list_in_returned_dict(
    base_engine, get_test_cards
):
    cards = get_test_cards("D5|H8|D6|D9|S5|SK|C5|C8|DA|S9")

    result = base_engine.group_cards_by_value(cards)
    assert isinstance(result, dict)

    assert result[2] == []
    assert result[3] == []
    assert result[4] == []
    assert result[5] == [cards[0], cards[4], cards[6]]
    assert result[6] == [cards[2]]
    assert result[7] == []
    assert result[8] == [cards[1], cards[7]]
    assert result[9] == [cards[3], cards[9]]
    assert result[10] == []
    assert result[11] == []
    assert result[12] == []
    assert result[13] == [cards[5]]
    assert result[14] == [cards[8]]


def test_when_find_consecutive_value_cards_and_no_run_size_and_single_values_then_correct_lists_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("DK|D4|D8|DQ|S6|H9|C5|SJ|HA")

    result = base_engine.find_consecutive_value_cards(cards, treat_ace_low=True)

    assert len(result) == 4
    assert result[0] == [cards[8]]
    assert result[1] == [cards[1], cards[6], cards[4]]
    assert result[2] == [cards[2], cards[5]]
    assert result[3] == [cards[7], cards[3], cards[0], cards[8]]


def test_when_find_consecutive_value_cards_and_run_size_and_single_values_then_correct_lists_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("DK|D4|D8|DQ|S6|HT|C5|SJ|HA")

    result = base_engine.find_consecutive_value_cards(
        cards, treat_ace_low=True, run_size=3
    )

    assert len(result) == 4
    assert result[0] == [cards[1], cards[6], cards[4]]
    assert result[1] == [cards[5], cards[7], cards[3]]
    assert result[2] == [cards[7], cards[3], cards[0]]
    assert result[3] == [cards[3], cards[0], cards[8]]


def test_when_find_consecutive_value_cards_and_single_values_and_ace_low_then_correct_lists_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|D8|S3|HT|C2|SJ|HA")

    result = base_engine.find_consecutive_value_cards(
        cards, treat_ace_low=True, run_size=3
    )

    assert len(result) == 2
    assert result[0] == [cards[6], cards[4], cards[2]]
    assert result[1] == [cards[4], cards[2], cards[0]]


def test_when_find_consecutive_value_cards_and_single_values_and_not_ace_low_then_correct_lists_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|D8|S3|HT|C2|SJ|HA")

    result = base_engine.find_consecutive_value_cards(
        cards, treat_ace_low=False, run_size=3
    )

    assert len(result) == 1
    assert result[0] == [cards[4], cards[2], cards[0]]


def test_when_find_consecutive_value_cards_and_multi_values_then_correct_lists_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|C6|C5|D5|H6|S6")

    result = base_engine.find_consecutive_value_cards(
        cards, treat_ace_low=True, run_size=3
    )

    assert len(result) == 6
    assert result[0] == [cards[0], cards[2], cards[1]]
    assert result[1] == [cards[0], cards[2], cards[4]]
    assert result[2] == [cards[0], cards[2], cards[5]]
    assert result[3] == [cards[0], cards[3], cards[1]]
    assert result[4] == [cards[0], cards[3], cards[4]]
    assert result[5] == [cards[0], cards[3], cards[5]]


def test_when_find_consecutive_value_cards_and_no_matches_long_enough_then_empty_list_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|C6|C5|D5|H6|S6")

    result = base_engine.find_consecutive_value_cards(
        cards, treat_ace_low=True, run_size=5
    )

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_all_unique_card_combos_then_correct_list_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|C4|H4|S4")
    result = base_engine.find_all_unique_card_combos(cards, 2)

    assert isinstance(result, list)
    assert [cards[0], cards[1]] in result
    assert [cards[0], cards[2]] in result
    assert [cards[0], cards[3]] in result
    assert [cards[1], cards[2]] in result
    assert [cards[1], cards[3]] in result
    assert [cards[2], cards[3]] in result


def test_when_check_all_card_values_unique_and_are_unique_then_true_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|C6|H7|SK")
    result = base_engine.check_all_card_values_unique(cards)

    assert result is True


def test_when_check_all_card_values_unique_and_duplicates_then_false_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("DK|C6|H7|SK")
    result = base_engine.check_all_card_values_unique(cards)

    assert result is False


@mark.parametrize("cards, expected", [
    ("C4|D4|S4|H4", True),
    ("C4|D4|S5|H4", False)
])
def test_when_check_all_card_values_match_then_correct_value_returned(base_engine, get_test_cards, cards, expected):
    cards = get_test_cards(cards)

    actual = base_engine.check_all_card_values_match(cards)

    assert actual == expected


def test_when_check_all_card_suits_unique_and_are_unique_then_true_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D4|C6|H7|SK")
    result = base_engine.check_all_card_suits_unique(cards)

    assert result is True


def test_when_check_all_card_suits_unique_and_duplicates_then_false_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("DK|C6|D7|SK")
    result = base_engine.check_all_card_suits_unique(cards)

    assert result is False


@mark.parametrize("cards, expected", [
    ("C4|C8|CK|C2", True),
    ("C4|C8|CK|H2", False)
])
def test_when_check_all_card_suits_match_then_correct_value_returned(base_engine, get_test_cards, cards, expected):
    cards = get_test_cards(cards)

    actual = base_engine.check_all_card_suits_match(cards)

    assert actual == expected


@mark.parametrize("cards, treat_ace_low, expected", [
    ("D4|C7|D5|H6|H3", True, True),
    ("D4|C7|D5|S9|H6|H3|S8", True, True),
    ("HT|HQ|DJ|SA|CK", True, True),
    ("H4|H5|D2|SA|C3", True, True),
    ("H4|H5|D2|SA|C3", False, False),
    ("H9|HQ|DJ|SA|CK", True, False),
])
def test_when_check_cards_consecutive_then_correct_values_returned(base_engine, get_test_cards, cards, treat_ace_low, expected):
    cards = get_test_cards(cards)

    actual = base_engine.check_cards_consecutive(cards, treat_ace_low)

    assert actual == expected


@mark.parametrize("raw_cards, expected_cards", [
    ("D4", "D4"),
    ("D9|H6|S2", "D9|H6|S2"),
    ("D4|H9|C7|SK", "SK|H9|C7|D4"),
    ("S9|D4|C9|CK|CA|H9", "CA|CK|S9|H9|C9|D4"),
    ("D4|H9|ANY_DIAMOND|C7|ANY_HEART|SK", "SK|H9|C7|D4|ANY_HEART|ANY_DIAMOND"),
    ("D4|H9|ANY_SEVEN|C7|ANY_CARD|SK", "SK|H9|C7|ANY_SEVEN|D4|ANY_CARD"),
])
def test_when_order_cards_then_correct_cards_returned(base_engine, get_test_cards, raw_cards, expected_cards):
    raw_cards = get_test_cards(raw_cards)
    expected_cards = get_test_cards(expected_cards)

    actual = base_engine.order_cards(raw_cards)

    assert actual == expected_cards


@mark.parametrize("raw_sets, expected_sets", [
    (["SK|S7", "C4|D9", "H2|CA"], ["CA|H2", "SK|S7", "D9|C4"]),
    (["S7|DK", "S7|SK", "SK|S7", "C2|H3", "S7|SK"], ["SK|S7", "DK|S7", "H3|C2"]),
])
def test_when_deduplicate_card_sets_then_correct_sets_returned(base_engine, get_test_cards, raw_sets, expected_sets):
    raw_sets = [get_test_cards(card_set) for card_set in raw_sets]
    expected_sets = [get_test_cards(card_set) for card_set in expected_sets]

    actual = base_engine.deduplicate_card_sets(raw_sets)

    assert actual == expected_sets
