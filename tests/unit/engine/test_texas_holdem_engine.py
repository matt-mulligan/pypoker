from pytest import fixture

from pypoker.engine2.texas_holdem import TexasHoldemPokerEngine


@fixture
def engine():
    return TexasHoldemPokerEngine()


# Public "Hand Maker" method tests
# --------------------------------
def test_when_make_straight_flush_hands_and_too_few_cards_then_empty_list_returned(engine, get_test_cards):
    cards = get_test_cards("D4|D2|D5|D3")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_straight_flush_hands_and_too_few_cards_of_any_suit_then_empty_list_returned(engine, get_test_cards):
    cards = get_test_cards("D4|HT|D2|HK|D5|HJ|D3|HQ")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_straight_flush_hands_and_single_set_then_correct_values_returned(engine, get_test_cards):
    cards = get_test_cards("D4|D6|D2|D5|D3|HQ")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == [cards[2], cards[4], cards[0], cards[3], cards[1]]


def test_when_make_straight_flush_hands_and_multiple_sets_then_correct_values_returned(engine, get_test_cards):
    cards = get_test_cards("H8|D4|D6|HT|D2|HJ|D5|D3|HQ|H9")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2
    assert [cards[0], cards[9], cards[3], cards[5], cards[8]] in result
    assert [cards[4], cards[7], cards[1], cards[6], cards[2]] in result


def test_when_make_straight_flush_hands_and_overlapping_set_then_correct_values_returned(engine, get_test_cards):
    cards = get_test_cards("D4|D6|D2|D5|D3|HQ|D7|D8")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == [cards[2], cards[4], cards[0], cards[3], cards[1]]
    assert result[1] == [cards[4], cards[0], cards[3], cards[1], cards[6]]
    assert result[2] == [cards[0], cards[3], cards[1], cards[6], cards[7]]
