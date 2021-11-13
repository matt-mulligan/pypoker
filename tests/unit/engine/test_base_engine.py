from typing import List

from pytest import fixture

from pypoker.deck import Card
from pypoker.engine2 import BasePokerEngine
from pypoker.player import BasePlayer


@fixture
def base_engine():
    class FakePokerEngine(BasePokerEngine):
        def find_player_best_hand(
            self, player: BasePlayer, board: List[Card], **kwargs
        ):
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


def test_when_group_cards_by_suit_and_suit_missing_then_not_in_return_list(
    base_engine, get_test_cards
):
    cards = get_test_cards("D5|H8|D6")

    result = base_engine.group_cards_by_suit(cards)
    assert isinstance(result, dict)
    assert result["Diamonds"] == [cards[0], cards[2]]
    assert result["Hearts"] == [cards[1]]

    assert "Clubs" not in list(result)
    assert "Spades" not in list(result)


def test_when_group_cards_by_value_then_correct_dict_returned(
    base_engine, get_test_cards
):
    cards = get_test_cards("D5|H8|D6|D9|S5|SK|C5|C8|DA|S9")

    result = base_engine.group_cards_by_value(cards)
    assert isinstance(result, dict)

    assert 2 not in list(result)
    assert 3 not in list(result)
    assert 4 not in list(result)
    assert result[5] == [cards[0], cards[4], cards[6]]
    assert result[6] == [cards[2]]
    assert 7 not in list(result)
    assert result[8] == [cards[1], cards[7]]
    assert result[9] == [cards[3], cards[9]]
    assert 10 not in list(result)
    assert 11 not in list(result)
    assert 12 not in list(result)
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
