from pytest import fixture

from pypoker.constants import GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, TH_HAND_QUADS, TH_HAND_FULL_HOUSE, \
    TH_HAND_FLUSH, TH_HAND_STRAIGHT, TH_HAND_TRIPS, TH_HAND_TWO_PAIR, TH_HAND_PAIR, TH_HAND_HIGH_CARD
from pypoker.constructs import Hand
from pypoker.engine.texas_holdem import TexasHoldemPokerEngine


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
    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, get_test_cards("D2|D3|D4|D5|D6"), [6])
    assert result[0].cards == get_test_cards("D2|D3|D4|D5|D6")


def test_when_make_straight_flush_hands_and_multiple_sets_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("H8|D4|D6|HT|D2|HJ|D5|D3|HQ|H9")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, get_test_cards("H8|H9|HT|HJ|HQ"), [12])
    assert result[0].cards == get_test_cards("H8|H9|HT|HJ|HQ")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, get_test_cards("D2|D3|D4|D5|D6"), [6])
    assert result[1].cards == get_test_cards("D2|D3|D4|D5|D6")


def test_when_make_straight_flush_hands_and_overlapping_set_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|D6|D2|D5|D3|HQ|D7|D8")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, get_test_cards("D4|D5|D6|D7|D8"), [8])
    assert result[0].cards == get_test_cards("D4|D5|D6|D7|D8")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, get_test_cards("D3|D4|D5|D6|D7"), [7])
    assert result[1].cards == get_test_cards("D3|D4|D5|D6|D7")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, get_test_cards("D2|D3|D4|D5|D6"), [6])
    assert result[2].cards == get_test_cards("D2|D3|D4|D5|D6")


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

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4"), [4, None])
    assert result[0].cards == get_test_cards("D4|C4|S4|H4")


def test_when_make_quads_hands_and_only_five_cards_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|C4|DA|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|DA"), [4, 14])
    assert result[0].cards == get_test_cards("D4|C4|S4|H4|DA")


def test_when_make_quads_hands_and_many_kickers_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|S3|C4|DA|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|CA"), [4, 14])
    assert result[0].cards == get_test_cards("D4|C4|S4|H4|CA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|DA"), [4, 14])
    assert result[1].cards == get_test_cards("D4|C4|S4|H4|DA")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|S3"), [4, 3])
    assert result[2].cards == get_test_cards("D4|C4|S4|H4|S3")


def test_when_make_quads_hands_and_multiple_quads_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|SA|C4|DA|S4|H4|HA|S7")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 10

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("CA|SA|DA|HA|S7"), [14, 7])
    assert result[0].cards == get_test_cards("CA|SA|DA|HA|S7")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("CA|SA|DA|HA|D4"), [14, 4])
    assert result[1].cards == get_test_cards("CA|SA|DA|HA|D4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("CA|SA|DA|HA|C4"), [14, 4])
    assert result[2].cards == get_test_cards("CA|SA|DA|HA|C4")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("CA|SA|DA|HA|S4"), [14, 4])
    assert result[3].cards == get_test_cards("CA|SA|DA|HA|S4")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("CA|SA|DA|HA|H4"), [14, 4])
    assert result[4].cards == get_test_cards("CA|SA|DA|HA|H4")

    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|CA"), [4, 14])
    assert result[5].cards == get_test_cards("D4|C4|S4|H4|CA")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|SA"), [4, 14])
    assert result[6].cards == get_test_cards("D4|C4|S4|H4|SA")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|DA"), [4, 14])
    assert result[7].cards == get_test_cards("D4|C4|S4|H4|DA")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|HA"), [4, 14])
    assert result[8].cards == get_test_cards("D4|C4|S4|H4|HA")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4|S7"), [4, 7])
    assert result[9].cards == get_test_cards("D4|C4|S4|H4|S7")


def test_when_make_quads_hands_and_not_include_kickers_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|SA|C4|DA|S4|H4|HA|S7")
    result = engine.make_quads_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("CA|SA|DA|HA"), [14, None])
    assert result[0].cards == get_test_cards("CA|SA|DA|HA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_QUADS, get_test_cards("D4|C4|S4|H4"), [4, None])
    assert result[1].cards == get_test_cards("D4|C4|S4|H4")


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

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|DA|HA|S4|C4"), [14, 4])
    assert result[0].cards == get_test_cards("CA|DA|HA|S4|C4")


def test_when_make_full_house_hands_and_many_options_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D7|S2|H7|C2|SA|D2|S7|HA")
    result = engine.make_full_house_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 18

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|SA|HA|D7|H7"), [14, 7])
    assert result[0].cards == get_test_cards("CA|SA|HA|D7|H7")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|SA|HA|D7|S7"), [14, 7])
    assert result[1].cards == get_test_cards("CA|SA|HA|D7|S7")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|SA|HA|H7|S7"), [14, 7])
    assert result[2].cards == get_test_cards("CA|SA|HA|H7|S7")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|SA|HA|S2|C2"), [14, 2])
    assert result[3].cards == get_test_cards("CA|SA|HA|S2|C2")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|SA|HA|S2|D2"), [14, 2])
    assert result[4].cards == get_test_cards("CA|SA|HA|S2|D2")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("CA|SA|HA|C2|D2"), [14, 2])
    assert result[5].cards == get_test_cards("CA|SA|HA|C2|D2")

    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("D7|H7|S7|CA|SA"), [7, 14])
    assert result[6].cards == get_test_cards("D7|H7|S7|CA|SA")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("D7|H7|S7|CA|HA"), [7, 14])
    assert result[7].cards == get_test_cards("D7|H7|S7|CA|HA")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("D7|H7|S7|SA|HA"), [7, 14])
    assert result[8].cards == get_test_cards("D7|H7|S7|SA|HA")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("D7|H7|S7|S2|C2"), [7, 2])
    assert result[9].cards == get_test_cards("D7|H7|S7|S2|C2")
    assert result[10] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("D7|H7|S7|S2|D2"), [7, 2])
    assert result[10].cards == get_test_cards("D7|H7|S7|S2|D2")
    assert result[11] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("D7|H7|S7|C2|D2"), [7, 2])
    assert result[11].cards == get_test_cards("D7|H7|S7|C2|D2")

    assert result[12] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("S2|C2|D2|CA|SA"), [2, 14])
    assert result[12].cards == get_test_cards("S2|C2|D2|CA|SA")
    assert result[13] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("S2|C2|D2|CA|HA"), [2, 14])
    assert result[13].cards == get_test_cards("S2|C2|D2|CA|HA")
    assert result[14] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("S2|C2|D2|SA|HA"), [2, 14])
    assert result[14].cards == get_test_cards("S2|C2|D2|SA|HA")
    assert result[15] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("S2|C2|D2|D7|H7"), [2, 7])
    assert result[15].cards == get_test_cards("S2|C2|D2|D7|H7")
    assert result[16] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("S2|C2|D2|D7|S7"), [2, 7])
    assert result[16].cards == get_test_cards("S2|C2|D2|D7|S7")
    assert result[17] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, get_test_cards("S2|C2|D2|H7|S7"), [2, 7])
    assert result[17].cards == get_test_cards("S2|C2|D2|H7|S7")


def test_when_make_flush_hands_and_less_than_five_cards_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|C7|C2|C9")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_flush_hands_and_no_suit_with_five_cards_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D8|C7|DK|C2|DJ|C9|ST|S6|S4")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_flush_hands_and_only_five_cards_of_flush_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|C7|C2|C9|CT|S4")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|C9|CT"), [14, 10, 9, 7, 2])
    assert result[0].cards == get_test_cards("CA|C7|C2|C9|CT")


def test_when_make_flush_hands_and_many_cards_of_flush_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|C7|C2|C9|CT|S4|C4|D9|SJ|DQ")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 6

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C9|CT|C4"), [14, 10, 9, 7, 4])
    assert result[0].cards == get_test_cards("CA|C7|C9|CT|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|C9|CT"), [14, 10, 9, 7, 2])
    assert result[1].cards == get_test_cards("CA|C7|C2|C9|CT")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C2|C9|CT|C4"), [14, 10, 9, 4, 2])
    assert result[2].cards == get_test_cards("CA|C2|C9|CT|C4")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|CT|C4"), [14, 10, 7, 4, 2])
    assert result[3].cards == get_test_cards("CA|C7|C2|CT|C4")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|C9|C4"), [14, 9, 7, 4, 2])
    assert result[4].cards == get_test_cards("CA|C7|C2|C9|C4")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("C7|C2|C9|CT|C4"), [10, 9, 7, 4, 2])
    assert result[5].cards == get_test_cards("C7|C2|C9|CT|C4")


def test_when_make_flush_hands_and_multiple_flush_suits_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|C7|C2|C9|CT|S4|C4|D9|SJ|DQ|D4|D8|DT")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 7

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C9|CT|C4"), [14, 10, 9, 7, 4])
    assert result[0].cards == get_test_cards("CA|C7|C9|CT|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|C9|CT"), [14, 10, 9, 7, 2])
    assert result[1].cards == get_test_cards("CA|C7|C2|C9|CT")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C2|C9|CT|C4"), [14, 10, 9, 4, 2])
    assert result[2].cards == get_test_cards("CA|C2|C9|CT|C4")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|CT|C4"), [14, 10, 7, 4, 2])
    assert result[3].cards == get_test_cards("CA|C7|C2|CT|C4")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("CA|C7|C2|C9|C4"), [14, 9, 7, 4, 2])
    assert result[4].cards == get_test_cards("CA|C7|C2|C9|C4")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("D9|DQ|D4|D8|DT"), [12, 10, 9, 8, 4])
    assert result[5].cards == get_test_cards("D9|DQ|D4|D8|DT")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, get_test_cards("C7|C2|C9|CT|C4"), [10, 9, 7, 4, 2])
    assert result[6].cards == get_test_cards("C7|C2|C9|CT|C4")


def test_when_make_straight_hands_and_less_than_five_cards_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|DK|ST|CQ")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_straight_hands_and_single_straight_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|SJ|C7|DK|ST|CQ")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("CA|SJ|DK|ST|CQ"), [14])
    assert result[0].cards == get_test_cards("ST|SJ|CQ|DK|CA")


def test_when_make_straight_hands_and_running_straights_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("D8|CA|SJ|DK|ST|D9|CQ")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("ST|SJ|CQ|DK|CA"), [14])
    assert result[0].cards == get_test_cards("ST|SJ|CQ|DK|CA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("D9|ST|SJ|CQ|DK"), [13])
    assert result[1].cards == get_test_cards("D9|ST|SJ|CQ|DK")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("D8|D9|ST|SJ|CQ"), [12])
    assert result[2].cards == get_test_cards("D8|D9|ST|SJ|CQ")


def test_when_make_straight_hands_and_ace_low_straight_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("D5|CA|S3|D2|S6|D4")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("D2|S3|D4|D5|S6"), [6])
    assert result[0].cards == get_test_cards("D2|S3|D4|D5|S6")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("CA|D2|S3|D4|D5"), [5])
    assert result[1].cards == get_test_cards("CA|D2|S3|D4|D5")


def test_when_make_straight_hands_and_disconnected_straights_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("D3|CA|SJ|DK|ST|D2|CQ|S4|S5")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("ST|SJ|CQ|DK|CA"), [14])
    assert result[0].cards == get_test_cards("ST|SJ|CQ|DK|CA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, get_test_cards("CA|D2|D3|S4|S5"), [5])
    assert result[1].cards == get_test_cards("CA|D2|D3|S4|S5")


def test_when_make_trips_hands_and_less_then_3_cards_then_return_empty_list(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ")
    result = engine.make_trips_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_trips_hands_and_no_trips_then_return_empty_list(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|ST|C3|S5")
    result = engine.make_trips_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_trips_hands_and_multiple_trips_not_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|C9|CJ|DQ|C7|CQ")
    result = engine.make_trips_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ"), [12, None, None])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|CQ"), [12, None, None])
    assert result[1].cards == get_test_cards("SQ|HQ|CQ")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|DQ|CQ"), [12, None, None])
    assert result[2].cards == get_test_cards("SQ|DQ|CQ")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("HQ|DQ|CQ"), [12, None, None])
    assert result[3].cards == get_test_cards("HQ|DQ|CQ")


def test_when_make_trips_hands_and_multiple_trips_and_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|C9|CJ|DQ|C7|CQ")
    result = engine.make_trips_hands(cards, include_kickers=True)

    assert isinstance(result, list)
    assert len(result) == 12

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|CJ|C9"), [12, 11, 9])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ|CJ|C9")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|CQ|CJ|C9"), [12, 11, 9])
    assert result[1].cards == get_test_cards("SQ|HQ|CQ|CJ|C9")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|DQ|CQ|CJ|C9"), [12, 11, 9])
    assert result[2].cards == get_test_cards("SQ|DQ|CQ|CJ|C9")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("HQ|DQ|CQ|CJ|C9"), [12, 11, 9])
    assert result[3].cards == get_test_cards("HQ|DQ|CQ|CJ|C9")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|CJ|C7"), [12, 11, 7])
    assert result[4].cards == get_test_cards("SQ|HQ|DQ|CJ|C7")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|CQ|CJ|C7"), [12, 11, 7])
    assert result[5].cards == get_test_cards("SQ|HQ|CQ|CJ|C7")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|DQ|CQ|CJ|C7"), [12, 11, 7])
    assert result[6].cards == get_test_cards("SQ|DQ|CQ|CJ|C7")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("HQ|DQ|CQ|CJ|C7"), [12, 11, 7])
    assert result[7].cards == get_test_cards("HQ|DQ|CQ|CJ|C7")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|C9|C7"), [12, 9, 7])
    assert result[8].cards == get_test_cards("SQ|HQ|DQ|C9|C7")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|CQ|C9|C7"), [12, 9, 7])
    assert result[9].cards == get_test_cards("SQ|HQ|CQ|C9|C7")
    assert result[10] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|DQ|CQ|C9|C7"), [12, 9, 7])
    assert result[10].cards == get_test_cards("SQ|DQ|CQ|C9|C7")
    assert result[11] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("HQ|DQ|CQ|C9|C7"), [12, 9, 7])
    assert result[11].cards == get_test_cards("HQ|DQ|CQ|C9|C7")


def test_when_make_trips_hands_and_multiple_trip_values_and_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|S9|CJ|DQ|D9|C9")
    result = engine.make_trips_hands(cards, include_kickers=True)

    assert isinstance(result, list)
    assert len(result) == 6

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|CJ|S9"), [12, 11, 9])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ|CJ|S9")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|CJ|D9"), [12, 11, 9])
    assert result[1].cards == get_test_cards("SQ|HQ|DQ|CJ|D9")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|CJ|C9"), [12, 11, 9])
    assert result[2].cards == get_test_cards("SQ|HQ|DQ|CJ|C9")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("S9|D9|C9|SQ|CJ"), [9, 12, 11])
    assert result[3].cards == get_test_cards("S9|D9|C9|SQ|CJ")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("S9|D9|C9|HQ|CJ"), [9, 12, 11])
    assert result[4].cards == get_test_cards("S9|D9|C9|HQ|CJ")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("S9|D9|C9|DQ|CJ"), [9, 12, 11])
    assert result[5].cards == get_test_cards("S9|D9|C9|DQ|CJ")


def test_when_make_trips_hands_and_multiple_trip_values_and_not_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|S9|CJ|DQ|D9|C9")
    result = engine.make_trips_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ"), [12, None, None])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("S9|D9|C9"), [9, None, None])
    assert result[1].cards == get_test_cards("S9|D9|C9")


def test_when_make_trips_hands_and_only_one_kicker_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|S9|DQ|D9")
    result = engine.make_trips_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|S9"), [12, 9, None])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ|S9")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ|D9"), [12, 9, None])
    assert result[1].cards == get_test_cards("SQ|HQ|DQ|D9")


def test_when_make_trips_hands_and_no_kicker_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|CQ|DQ")
    result = engine.make_trips_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|CQ"), [12, None, None])
    assert result[0].cards == get_test_cards("SQ|HQ|CQ")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|HQ|DQ"), [12, None, None])
    assert result[1].cards == get_test_cards("SQ|HQ|DQ")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("SQ|CQ|DQ"), [12, None, None])
    assert result[2].cards == get_test_cards("SQ|CQ|DQ")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, get_test_cards("HQ|CQ|DQ"), [12, None, None])
    assert result[3].cards == get_test_cards("HQ|CQ|DQ")


def test_when_make_two_pair_hands_and_less_than_four_cards_then_return_empty_list(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_two_pair_hands_and_not_two_values_with_pairs_then_return_empty_list(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H9|HK|SJ|S4")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_two_pair_hands_and_single_set_of_values_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HK|SJ|SA")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|SA"), [7, 4, 14])
    assert result[0].cards == get_test_cards("C4|D4|S7|H7|SA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|HK"), [7, 4, 13])
    assert result[1].cards == get_test_cards("C4|D4|S7|H7|HK")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|SJ"), [7, 4, 11])
    assert result[2].cards == get_test_cards("C4|D4|S7|H7|SJ")


def test_when_make_two_pair_hands_and_single_set_of_values_over_two_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HK|SJ|SA|S4|C7")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 27

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|SA"), [7, 4, 14])
    assert result[0].cards == get_test_cards("C4|D4|S7|H7|SA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|C7|SA"), [7, 4, 14])
    assert result[1].cards == get_test_cards("C4|D4|S7|C7|SA")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|H7|C7|SA"), [7, 4, 14])
    assert result[2].cards == get_test_cards("C4|D4|H7|C7|SA")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|H7|SA"), [7, 4, 14])
    assert result[3].cards == get_test_cards("C4|S4|S7|H7|SA")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|C7|SA"), [7, 4, 14])
    assert result[4].cards == get_test_cards("C4|S4|S7|C7|SA")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|H7|C7|SA"), [7, 4, 14])
    assert result[5].cards == get_test_cards("C4|S4|H7|C7|SA")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|H7|SA"), [7, 4, 14])
    assert result[6].cards == get_test_cards("D4|S4|S7|H7|SA")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|C7|SA"), [7, 4, 14])
    assert result[7].cards == get_test_cards("D4|S4|S7|C7|SA")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|H7|C7|SA"), [7, 4, 14])
    assert result[8].cards == get_test_cards("D4|S4|H7|C7|SA")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|HK"), [7, 4, 13])
    assert result[9].cards == get_test_cards("C4|D4|S7|H7|HK")
    assert result[10] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|C7|HK"), [7, 4, 13])
    assert result[10].cards == get_test_cards("C4|D4|S7|C7|HK")
    assert result[11] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|H7|C7|HK"), [7, 4, 13])
    assert result[11].cards == get_test_cards("C4|D4|H7|C7|HK")
    assert result[12] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|H7|HK"), [7, 4, 13])
    assert result[12].cards == get_test_cards("C4|S4|S7|H7|HK")
    assert result[13] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|C7|HK"), [7, 4, 13])
    assert result[13].cards == get_test_cards("C4|S4|S7|C7|HK")
    assert result[14] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|H7|C7|HK"), [7, 4, 13])
    assert result[14].cards == get_test_cards("C4|S4|H7|C7|HK")
    assert result[15] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|H7|HK"), [7, 4, 13])
    assert result[15].cards == get_test_cards("D4|S4|S7|H7|HK")
    assert result[16] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|C7|HK"), [7, 4, 13])
    assert result[16].cards == get_test_cards("D4|S4|S7|C7|HK")
    assert result[17] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|H7|C7|HK"), [7, 4, 13])
    assert result[17].cards == get_test_cards("D4|S4|H7|C7|HK")
    assert result[18] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|SJ"), [7, 4, 11])
    assert result[18].cards == get_test_cards("C4|D4|S7|H7|SJ")
    assert result[19] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|C7|SJ"), [7, 4, 11])
    assert result[19].cards == get_test_cards("C4|D4|S7|C7|SJ")
    assert result[20] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|H7|C7|SJ"), [7, 4, 11])
    assert result[20].cards == get_test_cards("C4|D4|H7|C7|SJ")
    assert result[21] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|H7|SJ"), [7, 4, 11])
    assert result[21].cards == get_test_cards("C4|S4|S7|H7|SJ")
    assert result[22] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|C7|SJ"), [7, 4, 11])
    assert result[22].cards == get_test_cards("C4|S4|S7|C7|SJ")
    assert result[23] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|H7|C7|SJ"), [7, 4, 11])
    assert result[23].cards == get_test_cards("C4|S4|H7|C7|SJ")
    assert result[24] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|H7|SJ"), [7, 4, 11])
    assert result[24].cards == get_test_cards("D4|S4|S7|H7|SJ")
    assert result[25] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|C7|SJ"), [7, 4, 11])
    assert result[25].cards == get_test_cards("D4|S4|S7|C7|SJ")
    assert result[26] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|H7|C7|SJ"), [7, 4, 11])
    assert result[26].cards == get_test_cards("D4|S4|H7|C7|SJ")


def test_when_make_two_pair_hands_and_multiple_sets_of_values_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HA|SJ|SA|CA")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 22

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|SA|SJ"), [14, 7, 11])
    assert result[0].cards == get_test_cards("S7|H7|HA|SA|SJ")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|CA|SJ"), [14, 7, 11])
    assert result[1].cards == get_test_cards("S7|H7|HA|CA|SJ")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|SA|CA|SJ"), [14, 7, 11])
    assert result[2].cards == get_test_cards("S7|H7|SA|CA|SJ")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|SA|C4"), [14, 7, 4])
    assert result[3].cards == get_test_cards("S7|H7|HA|SA|C4")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|SA|D4"), [14, 7, 4])
    assert result[4].cards == get_test_cards("S7|H7|HA|SA|D4")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|CA|C4"), [14, 7, 4])
    assert result[5].cards == get_test_cards("S7|H7|HA|CA|C4")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|CA|D4"), [14, 7, 4])
    assert result[6].cards == get_test_cards("S7|H7|HA|CA|D4")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|SA|CA|C4"), [14, 7, 4])
    assert result[7].cards == get_test_cards("S7|H7|SA|CA|C4")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|SA|CA|D4"), [14, 7, 4])
    assert result[8].cards == get_test_cards("S7|H7|SA|CA|D4")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|SA|SJ"), [14, 4, 11])
    assert result[9].cards == get_test_cards("C4|D4|HA|SA|SJ")
    assert result[10] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|CA|SJ"), [14, 4, 11])
    assert result[10].cards == get_test_cards("C4|D4|HA|CA|SJ")
    assert result[11] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|SA|CA|SJ"), [14, 4, 11])
    assert result[11].cards == get_test_cards("C4|D4|SA|CA|SJ")
    assert result[12] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|SA|S7"), [14, 4, 7])
    assert result[12].cards == get_test_cards("C4|D4|HA|SA|S7")
    assert result[13] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|SA|H7"), [14, 4, 7])
    assert result[13].cards == get_test_cards("C4|D4|HA|SA|H7")
    assert result[14] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|CA|S7"), [14, 4, 7])
    assert result[14].cards == get_test_cards("C4|D4|HA|CA|S7")
    assert result[15] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|CA|H7"), [14, 4, 7])
    assert result[15].cards == get_test_cards("C4|D4|HA|CA|H7")
    assert result[16] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|SA|CA|S7"), [14, 4, 7])
    assert result[16].cards == get_test_cards("C4|D4|SA|CA|S7")
    assert result[17] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|SA|CA|H7"), [14, 4, 7])
    assert result[17].cards == get_test_cards("C4|D4|SA|CA|H7")
    assert result[18] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|HA"), [7, 4, 14])
    assert result[18].cards == get_test_cards("C4|D4|S7|H7|HA")
    assert result[19] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|SA"), [7, 4, 14])
    assert result[19].cards == get_test_cards("C4|D4|S7|H7|SA")
    assert result[20] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|CA"), [7, 4, 14])
    assert result[20].cards == get_test_cards("C4|D4|S7|H7|CA")
    assert result[21] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7|SJ"), [7, 4, 11])
    assert result[21].cards == get_test_cards("C4|D4|S7|H7|SJ")


def test_when_make_two_pair_hands_and_not_kickers_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HA|SJ|SA|CA")

    result = engine.make_two_pair_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 7

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|SA"), [14, 7, None])
    assert result[0].cards == get_test_cards("S7|H7|HA|SA")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|HA|CA"), [14, 7, None])
    assert result[1].cards == get_test_cards("S7|H7|HA|CA")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("S7|H7|SA|CA"), [14, 7, None])
    assert result[2].cards == get_test_cards("S7|H7|SA|CA")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|SA"), [14, 4, None])
    assert result[3].cards == get_test_cards("C4|D4|HA|SA")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|HA|CA"), [14, 4, None])
    assert result[4].cards == get_test_cards("C4|D4|HA|CA")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|SA|CA"), [14, 4, None])
    assert result[5].cards == get_test_cards("C4|D4|SA|CA")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7"), [7, 4, None])
    assert result[6].cards == get_test_cards("C4|D4|S7|H7")


def test_when_make_two_pair_hands_and_no_kickers_available_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|S4")

    result = engine.make_two_pair_hands(cards, include_kickers=True)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|D4|S7|H7"), [7, 4, None])
    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("C4|S4|S7|H7"), [7, 4, None])
    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D4|S4|S7|H7"), [7, 4, None])


def test_when_make_pair_hands_and_less_than_two_cards_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4")
    
    result = engine.make_pair_hands(cards)
    
    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_pair_hands_and_no_pairs_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|HA|S2")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_make_pair_hands_and_single_pair_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|HA|S2|H8|CQ|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 10

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|CQ|H8"), [4, 14, 12, 8])
    assert result[0].cards == get_test_cards("C4|D4|HA|CQ|H8")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|CQ|D7"), [4, 14, 12, 7])
    assert result[1].cards == get_test_cards("C4|D4|HA|CQ|D7")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|CQ|S2"), [4, 14, 12, 2])
    assert result[2].cards == get_test_cards("C4|D4|HA|CQ|S2")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|H8|D7"), [4, 14, 8, 7])
    assert result[3].cards == get_test_cards("C4|D4|HA|H8|D7")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[4].cards == get_test_cards("C4|D4|HA|H8|S2")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|D7|S2"), [4, 14, 7, 2])
    assert result[5].cards == get_test_cards("C4|D4|HA|D7|S2")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|CQ|H8|D7"), [4, 12, 8, 7])
    assert result[6].cards == get_test_cards("C4|D4|CQ|H8|D7")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|CQ|H8|S2"), [4, 12, 8, 2])
    assert result[7].cards == get_test_cards("C4|D4|CQ|H8|S2")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|CQ|D7|S2"), [4, 12, 7, 2])
    assert result[8].cards == get_test_cards("C4|D4|CQ|D7|S2")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[9].cards == get_test_cards("C4|D4|H8|D7|S2")


def test_when_make_pair_hands_and_single_overloaded_pair_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|H7|HA|S2|H8|S4|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 12

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|HA|H8|H7"), [4, 14, 8, 7])
    assert result[0].cards == get_test_cards("C4|S4|HA|H8|H7")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|H8|H7"), [4, 14, 8, 7])
    assert result[1].cards == get_test_cards("C4|D4|HA|H8|H7")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4|HA|H8|H7"), [4, 14, 8, 7])
    assert result[2].cards == get_test_cards("S4|D4|HA|H8|H7")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[3].cards == get_test_cards("C4|S4|HA|H8|S2")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[4].cards == get_test_cards("C4|D4|HA|H8|S2")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[5].cards == get_test_cards("S4|D4|HA|H8|S2")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|HA|H7|S2"), [4, 14, 7, 2])
    assert result[6].cards == get_test_cards("C4|S4|HA|H7|S2")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|HA|H7|S2"), [4, 14, 7, 2])
    assert result[7].cards == get_test_cards("C4|D4|HA|H7|S2")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4|HA|H7|S2"), [4, 14, 7, 2])
    assert result[8].cards == get_test_cards("S4|D4|HA|H7|S2")
    assert result[9] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[9].cards == get_test_cards("C4|S4|H8|H7|S2")
    assert result[10] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[10].cards == get_test_cards("C4|D4|H8|H7|S2")
    assert result[11] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[11].cards == get_test_cards("S4|D4|H8|H7|S2")


def test_when_make_pair_hands_and_multiple_pairs_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S2|H8|S4|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 9

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|H8|C4|S2"), [7, 8, 4, 2])
    assert result[0].cards == get_test_cards("D7|H7|H8|C4|S2")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|H8|S4|S2"), [7, 8, 4, 2])
    assert result[1].cards == get_test_cards("D7|H7|H8|S4|S2")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|H8|D4|S2"), [7, 8, 4, 2])
    assert result[2].cards == get_test_cards("D7|H7|H8|D4|S2")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[3].cards == get_test_cards("C4|S4|H8|D7|S2")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[4].cards == get_test_cards("C4|S4|H8|H7|S2")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[5].cards == get_test_cards("C4|D4|H8|D7|S2")
    assert result[6] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[6].cards == get_test_cards("C4|D4|H8|H7|S2")
    assert result[7] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[7].cards == get_test_cards("S4|D4|H8|D7|S2")
    assert result[8] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[8].cards == get_test_cards("S4|D4|H8|H7|S2")


def test_when_make_pair_hands_and_no_kickers_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S2|H8|S4|D4")

    result = engine.make_pair_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7"), [7, None, None, None])
    assert result[0].cards == get_test_cards("D7|H7")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4"), [4, None, None, None])
    assert result[1].cards == get_test_cards("C4|S4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4"), [4, None, None, None])
    assert result[2].cards == get_test_cards("C4|D4")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4"), [4, None, None, None])
    assert result[3].cards == get_test_cards("S4|D4")


def test_when_make_pair_hands_and_only_two_kickers_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S2|S4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|C4|S2"), [7, 4, 2, None])
    assert result[0].cards == get_test_cards("D7|H7|C4|S2")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|S4|S2"), [7, 4, 2, None])
    assert result[1].cards == get_test_cards("D7|H7|S4|S2")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|D7|S2"), [4, 7, 2, None])
    assert result[2].cards == get_test_cards("C4|S4|D7|S2")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|H7|S2"), [4, 7, 2, None])
    assert result[3].cards == get_test_cards("C4|S4|H7|S2")


def test_when_make_pair_hands_and_only_one_kicker_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|C4"), [7, 4, None, None])
    assert result[0].cards == get_test_cards("D7|H7|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D7|H7|S4"), [7, 4, None, None])
    assert result[1].cards == get_test_cards("D7|H7|S4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|D7"), [4, 7, None, None])
    assert result[2].cards == get_test_cards("C4|S4|D7")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4|H7"), [4, 7, None, None])
    assert result[3].cards == get_test_cards("C4|S4|H7")


def test_when_make_pair_hands_and_only_no_kicker_available_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S4|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|S4"), [4, None, None, None])
    assert result[0].cards == get_test_cards("C4|S4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("C4|D4"), [4, None, None, None])
    assert result[1].cards == get_test_cards("C4|D4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("S4|D4"), [4, None, None, None])
    assert result[2].cards == get_test_cards("S4|D4")


def test_when_make_high_card_hands_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|D8|SK|C5|DT|S2")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 6

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|DT|D8|C5|C4"), [13, 10, 8, 5, 4])
    assert result[0].cards == get_test_cards("SK|DT|D8|C5|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|DT|D8|C5|S2"), [13, 10, 8, 5, 2])
    assert result[1].cards == get_test_cards("SK|DT|D8|C5|S2")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|DT|D8|C4|S2"), [13, 10, 8, 4, 2])
    assert result[2].cards == get_test_cards("SK|DT|D8|C4|S2")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|DT|C5|C4|S2"), [13, 10, 5, 4, 2])
    assert result[3].cards == get_test_cards("SK|DT|C5|C4|S2")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|D8|C5|C4|S2"), [13, 8, 5, 4, 2])
    assert result[4].cards == get_test_cards("SK|D8|C5|C4|S2")
    assert result[5] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("DT|D8|C5|C4|S2"), [10, 8, 5, 4, 2])
    assert result[5].cards == get_test_cards("DT|D8|C5|C4|S2")


def test_when_make_high_card_hands_and_pairs_excluded_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|D8|SK|C8|DT|S2")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|DT|D8|C4|S2"), [13, 10, 8, 4, 2])
    assert result[0].cards == get_test_cards("SK|DT|D8|C4|S2")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|DT|C8|C4|S2"), [13, 10, 8, 4, 2])
    assert result[1].cards == get_test_cards("SK|DT|C8|C4|S2")


def test_when_make_high_card_hands_and_flush_excluded_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|C8|SK|C7|CT|C2")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 5

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|CT|C8|C7|C4"), [13, 10, 8, 7, 4])
    assert result[0].cards == get_test_cards("SK|CT|C8|C7|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|CT|C8|C7|C2"), [13, 10, 8, 7, 2])
    assert result[1].cards == get_test_cards("SK|CT|C8|C7|C2")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|CT|C8|C4|C2"), [13, 10, 8, 4, 2])
    assert result[2].cards == get_test_cards("SK|CT|C8|C4|C2")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|CT|C7|C4|C2"), [13, 10, 7, 4, 2])
    assert result[3].cards == get_test_cards("SK|CT|C7|C4|C2")
    assert result[4] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("SK|C8|C7|C4|C2"), [13, 8, 7, 4, 2])
    assert result[4].cards == get_test_cards("SK|C8|C7|C4|C2")


def test_when_make_high_card_hands_and_straight_excluded_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S8|S9|H7|D5|C6")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|S8|H7|C6|C4"), [9, 8, 7, 6, 4])
    assert result[0].cards == get_test_cards("S9|S8|H7|C6|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|S8|H7|D5|C4"), [9, 8, 7, 5, 4])
    assert result[1].cards == get_test_cards("S9|S8|H7|D5|C4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|S8|C6|D5|C4"), [9, 8, 6, 5, 4])
    assert result[2].cards == get_test_cards("S9|S8|C6|D5|C4")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|H7|C6|D5|C4"), [9, 7, 6, 5, 4])
    assert result[3].cards == get_test_cards("S9|H7|C6|D5|C4")


def test_when_make_high_card_hands_and_only_four_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|S9|H7|D5")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|H7|D5|C4"), [9, 7, 5, 4, None])
    assert result[0].cards == get_test_cards("S9|H7|D5|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|H7|D5|S4"), [9, 7, 5, 4, None])
    assert result[1].cards == get_test_cards("S9|H7|D5|S4")


def test_when_make_high_card_hands_and_only_three_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|S9|H7|D7")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|H7|C4"), [9, 7, 4, None, None])
    assert result[0].cards == get_test_cards("S9|H7|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|D7|C4"), [9, 7, 4, None, None])
    assert result[1].cards == get_test_cards("S9|D7|C4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|H7|S4"), [9, 7, 4, None, None])
    assert result[2].cards == get_test_cards("S9|H7|S4")
    assert result[3] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|D7|S4"), [9, 7, 4, None, None])
    assert result[3].cards == get_test_cards("S9|D7|S4")


def test_when_make_high_card_hands_and_only_two_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|S9|H4")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|C4"), [9, 4, None, None, None])
    assert result[0].cards == get_test_cards("S9|C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|S4"), [9, 4, None, None, None])
    assert result[1].cards == get_test_cards("S9|S4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S9|H4"), [9, 4, None, None, None])
    assert result[2].cards == get_test_cards("S9|H4")


def test_when_make_high_card_hands_and_only_single_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|H4")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("C4"), [4, None, None, None, None])
    assert result[0].cards == get_test_cards("C4")
    assert result[1] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("S4"), [4, None, None, None, None])
    assert result[1].cards == get_test_cards("S4")
    assert result[2] == Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, get_test_cards("H4"), [4, None, None, None, None])
    assert result[2].cards == get_test_cards("H4")
