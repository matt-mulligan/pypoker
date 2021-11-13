from pytest import fixture

from pypoker.engine2.texas_holdem import TexasHoldemPokerEngine


@fixture
def engine():
    return TexasHoldemPokerEngine()


# Public "Hand Maker" method tests
# --------------------------------
def test_when_make_straight_flush_hands_and_too_few_cards_then_empty_list_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|D2|D5|D3")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_straight_flush_hands_and_too_few_cards_of_any_suit_then_empty_list_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|HT|D2|HK|D5|HJ|D3|HQ")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_straight_flush_hands_and_single_set_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|D6|D2|D5|D3|HQ")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == [cards[2], cards[4], cards[0], cards[3], cards[1]]


def test_when_make_straight_flush_hands_and_multiple_sets_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("H8|D4|D6|HT|D2|HJ|D5|D3|HQ|H9")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2
    assert [cards[0], cards[9], cards[3], cards[5], cards[8]] in result
    assert [cards[4], cards[7], cards[1], cards[6], cards[2]] in result


def test_when_make_straight_flush_hands_and_overlapping_set_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|D6|D2|D5|D3|HQ|D7|D8")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == [cards[2], cards[4], cards[0], cards[3], cards[1]]
    assert result[1] == [cards[4], cards[0], cards[3], cards[1], cards[6]]
    assert result[2] == [cards[0], cards[3], cards[1], cards[6], cards[7]]


def test_when_make_quads_hands_and_not_enough_cards_then_return_empty_list(
    engine, get_test_cards
):
    cards = get_test_cards("D4|H4|C4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_quads_hands_and_not_enough_cards_of_any_value_then_return_empty_list(
    engine, get_test_cards
):
    cards = get_test_cards("D4|D7|DK|H4|HK|H7|C4|S7|CK")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_quads_hands_and_only_four_cards_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|C4|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == [cards[0], cards[1], cards[2], cards[3]]


def test_when_make_quads_hands_and_only_five_cards_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|C4|DA|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == [cards[0], cards[1], cards[3], cards[4], cards[2]]


def test_when_make_quads_hands_and_many_kickers_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|S3|C4|DA|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == [cards[1], cards[3], cards[5], cards[6], cards[0]]
    assert result[1] == [cards[1], cards[3], cards[5], cards[6], cards[2]]
    assert result[2] == [cards[1], cards[3], cards[5], cards[6], cards[4]]


def test_when_make_quads_hands_and_multiple_quads_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|SA|C4|DA|S4|H4|HA|S7")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 10

    assert [cards[0], cards[2], cards[4], cards[7], cards[1]] in result
    assert [cards[0], cards[2], cards[4], cards[7], cards[3]] in result
    assert [cards[0], cards[2], cards[4], cards[7], cards[5]] in result
    assert [cards[0], cards[2], cards[4], cards[7], cards[6]] in result
    assert [cards[0], cards[2], cards[4], cards[7], cards[8]] in result

    assert [cards[1], cards[3], cards[5], cards[6], cards[0]] in result
    assert [cards[1], cards[3], cards[5], cards[6], cards[2]] in result
    assert [cards[1], cards[3], cards[5], cards[6], cards[4]] in result
    assert [cards[1], cards[3], cards[5], cards[6], cards[7]] in result
    assert [cards[1], cards[3], cards[5], cards[6], cards[8]] in result


def test_when_make_full_house_hands_and_not_enough_cards_then_return_empty_list(
    engine, get_test_cards
):
    cards = get_test_cards("CA|DA|S4|C4")
    result = engine.make_full_house_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_full_house_hands_and_single_option_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|DA|S4|HA|C4")
    result = engine.make_full_house_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1

    assert result[0] == [cards[0], cards[1], cards[3], cards[2], cards[4]]


def test_when_make_full_house_hands_and_many_options_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D7|S2|H7|C2|SA|D2|S7|HA")
    result = engine.make_full_house_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 18

    assert [cards[2], cards[4], cards[6], cards[1], cards[3]] in result
    assert [cards[2], cards[4], cards[6], cards[1], cards[7]] in result
    assert [cards[2], cards[4], cards[6], cards[3], cards[7]] in result
    assert [cards[2], cards[4], cards[6], cards[0], cards[5]] in result
    assert [cards[2], cards[4], cards[6], cards[0], cards[8]] in result
    assert [cards[2], cards[4], cards[6], cards[5], cards[8]] in result

    assert [cards[1], cards[3], cards[7], cards[2], cards[4]] in result
    assert [cards[1], cards[3], cards[7], cards[2], cards[6]] in result
    assert [cards[1], cards[3], cards[7], cards[4], cards[6]] in result
    assert [cards[1], cards[3], cards[7], cards[0], cards[5]] in result
    assert [cards[1], cards[3], cards[7], cards[0], cards[8]] in result
    assert [cards[1], cards[3], cards[7], cards[5], cards[8]] in result

    assert [cards[0], cards[5], cards[8], cards[2], cards[4]] in result
    assert [cards[0], cards[5], cards[8], cards[2], cards[6]] in result
    assert [cards[0], cards[5], cards[8], cards[4], cards[6]] in result
    assert [cards[0], cards[5], cards[8], cards[1], cards[3]] in result
    assert [cards[0], cards[5], cards[8], cards[1], cards[7]] in result
    assert [cards[0], cards[5], cards[8], cards[3], cards[7]] in result
