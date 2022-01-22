import re

from pytest import fixture, mark, raises

from pypoker.constants import GameTypes, TexasHoldemHandType, OutsCalculationMethod
from pypoker.constructs import Hand, Deck, Card
from pypoker.engine.texas_holdem import TexasHoldemPokerEngine
from pypoker.exceptions import RankingError
from pypoker.player.human import HumanPlayer


@fixture
def engine():
    return TexasHoldemPokerEngine()


@fixture
def full_deck():
    """full deck of card objects"""
    return Deck().cards_all


# Public Concrete Implementation of PokerEngine Abstract Methods
# ---------------------------------------------------------------
@mark.parametrize("hole_cards, board_cards, expected_hand_type, expected_hand_cards, expected_tiebreakers",[
    ("D4|D5", "D7|H6|D6|C3|D3", TexasHoldemHandType.StraightFlush, "D3|D4|D5|D6|D7", [7]),
    ("D4|D5", "C5|H6|DA|H5|S5", TexasHoldemHandType.Quads, "D5|C5|H5|S5|DA", [5, 14]),
    ("D4|D5", "C5|H6|DA|H5|S6", TexasHoldemHandType.FullHouse, "D5|C5|H5|H6|S6", [5, 6]),
    ("D4|H5", "D7|H6|DK|D3|DQ", TexasHoldemHandType.Flush, "D4|D7|DK|D3|DQ", [13, 12, 7, 4, 3]),
    ("D4|H5", "S7|H6|C3|SK", TexasHoldemHandType.Straight, "C3|D4|H5|H6|S7", [7]),
    ("D4|H5", "S4|H4|C3|SK", TexasHoldemHandType.Trips, "D4|S4|H4|SK|H5", [4, 13, 5]),
    ("D4|H5", "S4|H3|C3|SK", TexasHoldemHandType.TwoPair, "H3|C3|D4|S4|SK", [4, 3, 13]),
    ("D4|H5", "S4|H3|C9|SK", TexasHoldemHandType.Pair, "D4|S4|SK|C9|H5", [4, 13, 9, 5]),
    ("D4|H5", "SJ|H3|C9|SK", TexasHoldemHandType.HighCard, "SK|SJ|C9|H5|D4", [13, 11, 9, 5, 4]),
])
def test_when_find_player_best_hand_then_correct_hand_returned(
        engine, get_test_cards, hole_cards, board_cards, expected_hand_type, expected_hand_cards, expected_tiebreakers
):
    player = HumanPlayer("Matt", hole_cards=get_test_cards(hole_cards))

    result = engine.find_player_best_hand(player, get_test_cards(board_cards))

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == Hand(
        GameTypes.TexasHoldem, expected_hand_type, get_test_cards(expected_hand_cards), expected_tiebreakers
    )
    assert result[0].cards == get_test_cards(expected_hand_cards)


def test_when_find_player_best_hand_and_multiple_hands_with_identical_tiebreakers_then_all_returned(
        engine, get_test_cards
):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("D9|SK"))
    board_cards = get_test_cards("S9|C9|HK|H9|C7")

    result = engine.find_player_best_hand(player, board_cards)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D9|S9|C9|H9|SK"), [9, 13])
    assert result[0].cards == get_test_cards("D9|S9|C9|H9|SK")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D9|S9|C9|H9|HK"), [9, 13])
    assert result[1].cards == get_test_cards("D9|S9|C9|H9|HK")


def test_when_rank_player_hands_and_not_all_players_are_player_objects_then_raise_error(engine):
    player_a = HumanPlayer("Matt")
    player_b = "Greg"
    player_c = HumanPlayer("Bill")

    with raises(RankingError, match=re.escape("All values of players list must be of BasePlayer Type")):
        engine.rank_player_hands([player_a, player_b, player_c])


def test_when_rank_player_hands_and_not_all_hands_set_then_raise_error(engine, get_test_cards):
    player_a = HumanPlayer("Matt", hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7"), [7, None, None, None]))
    player_b = HumanPlayer("Bill")

    with raises(RankingError, match=re.escape("All players must have their player.hand attribute set to rank them.")):
        engine.rank_player_hands([player_a, player_b])


def test_when_rank_player_hands_and_all_different_strengths_then_return_correct_dict(engine, get_test_cards):
    player_a = HumanPlayer(
        "Matt",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|HA|HT|HJ"), [7, 14, 11, 10])
    )
    player_b = HumanPlayer(
        "Greg",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("C7|D7|H7|HK|S7"), [7, 13])
    )
    player_c = HumanPlayer(
        "Sarah",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("C7|D9|HT|H6|S8"), [10])
    )
    player_d = HumanPlayer(
        "Jane",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C7|D4|HA|S9|S2"), [14, 9, 7, 4, 2])
    )
    player_e = HumanPlayer(
        "Lucy",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("C7|D7|HA|SA|DA"), [14, 7])
    )

    ranked = engine.rank_player_hands([player_a, player_b, player_c, player_d, player_e])

    assert ranked == {
        1: [player_b], 2: [player_e], 3: [player_c], 4: [player_a], 5: [player_d]
    }


def test_when_rank_player_hands_and_strength_overlaps_then_return_correct_dict(engine, get_test_cards):
    player_a = HumanPlayer(
        "Matt",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|H2|HK|S7"), [7, 13, 7, 2])
    )
    player_b = HumanPlayer(
        "Greg",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|HQ|HT|HJ"), [7, 12, 11, 10])
    )
    player_c = HumanPlayer(
        "Sarah",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C9|D9|H2|H4|S6"), [9, 6, 4, 2])
    )
    player_d = HumanPlayer(
        "Jane",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C7|D4|HA|S9|S2"), [14, 9, 7, 4, 2])
    )
    player_e = HumanPlayer(
        "Lucy",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("C7|D7|HA|SA|DA"), [14, 7])
    )

    ranked = engine.rank_player_hands([player_a, player_b, player_c, player_d, player_e])

    assert ranked == {
        1: [player_e], 2: [player_c], 3: [player_a], 4: [player_b], 5: [player_d]
    }


def test_when_rank_player_hands_and_strength_tiebreaker_overlaps_then_return_correct_dict(engine, get_test_cards):
    player_a = HumanPlayer(
        "Matt",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|H2|HK|S7"), [7, 13, 7, 2])
    )
    player_b = HumanPlayer(
        "Greg",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|SK|H2|S7"), [7, 13, 7, 2])
    )
    player_c = HumanPlayer(
        "Sarah",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C9|D9|H2|H4|S6"), [9, 6, 4, 2])
    )
    player_d = HumanPlayer(
        "Jane",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C7|D4|HA|S9|S2"), [14, 9, 7, 4, 2])
    )
    player_e = HumanPlayer(
        "Lucy",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("C7|D7|HA|SA|DA"), [14, 7])
    )

    ranked = engine.rank_player_hands([player_a, player_b, player_c, player_d, player_e])

    assert ranked == {
        1: [player_e], 2: [player_c], 3: [player_a, player_b], 4: [player_d]
    }


def test_when_rank_player_hands_and_incomplete_hands_then_return_correct_dict(engine, get_test_cards):
    player_a = HumanPlayer(
        "Matt",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|SK|S7"), [7, 13, 7, None])
    )
    player_b = HumanPlayer(
        "Greg",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7|H2|HK"), [7, 13, 2, None])
    )
    player_c = HumanPlayer(
        "Sarah",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C9|D9|H2|H4"), [9, 4, 2, None])
    )
    player_d = HumanPlayer(
        "Ted",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("C9|D9|H9|H4"), [9, 4, None])
    )

    ranked = engine.rank_player_hands([player_a, player_b, player_c, player_d])

    assert ranked == {
        1: [player_d], 2: [player_c], 3: [player_a], 4: [player_b]
    }


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
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("D2|D3|D4|D5|D6"), [6])
    assert result[0].cards == get_test_cards("D2|D3|D4|D5|D6")


def test_when_make_straight_flush_hands_and_multiple_sets_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("H8|D4|D6|HT|D2|HJ|D5|D3|HQ|H9")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("H8|H9|HT|HJ|HQ"), [12])
    assert result[0].cards == get_test_cards("H8|H9|HT|HJ|HQ")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("D2|D3|D4|D5|D6"), [6])
    assert result[1].cards == get_test_cards("D2|D3|D4|D5|D6")


def test_when_make_straight_flush_hands_and_overlapping_set_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|D6|D2|D5|D3|HQ|D7|D8")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("D4|D5|D6|D7|D8"), [8])
    assert result[0].cards == get_test_cards("D4|D5|D6|D7|D8")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("D3|D4|D5|D6|D7"), [7])
    assert result[1].cards == get_test_cards("D3|D4|D5|D6|D7")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("D2|D3|D4|D5|D6"), [6])
    assert result[2].cards == get_test_cards("D2|D3|D4|D5|D6")


def test_when_make_straight_flush_hands_and_ace_low_hand_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|DA|D2|D5|D3|HQ|D7|D8")
    result = engine.make_straight_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, get_test_cards("DA|D2|D3|D4|D5"), [5])
    assert result[0].cards == get_test_cards("DA|D2|D3|D4|D5")


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

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4"), [4, None])
    assert result[0].cards == get_test_cards("D4|C4|S4|H4")


def test_when_make_quads_hands_and_only_five_cards_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("D4|C4|DA|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|DA"), [4, 14])
    assert result[0].cards == get_test_cards("D4|C4|S4|H4|DA")


def test_when_make_quads_hands_and_many_kickers_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|S3|C4|DA|S4|H4")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|CA"), [4, 14])
    assert result[0].cards == get_test_cards("D4|C4|S4|H4|CA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|DA"), [4, 14])
    assert result[1].cards == get_test_cards("D4|C4|S4|H4|DA")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|S3"), [4, 3])
    assert result[2].cards == get_test_cards("D4|C4|S4|H4|S3")


def test_when_make_quads_hands_and_multiple_quads_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|SA|C4|DA|S4|H4|HA|S7")
    result = engine.make_quads_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 10

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("CA|SA|DA|HA|S7"), [14, 7])
    assert result[0].cards == get_test_cards("CA|SA|DA|HA|S7")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("CA|SA|DA|HA|D4"), [14, 4])
    assert result[1].cards == get_test_cards("CA|SA|DA|HA|D4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("CA|SA|DA|HA|C4"), [14, 4])
    assert result[2].cards == get_test_cards("CA|SA|DA|HA|C4")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("CA|SA|DA|HA|S4"), [14, 4])
    assert result[3].cards == get_test_cards("CA|SA|DA|HA|S4")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("CA|SA|DA|HA|H4"), [14, 4])
    assert result[4].cards == get_test_cards("CA|SA|DA|HA|H4")

    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|CA"), [4, 14])
    assert result[5].cards == get_test_cards("D4|C4|S4|H4|CA")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|SA"), [4, 14])
    assert result[6].cards == get_test_cards("D4|C4|S4|H4|SA")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|DA"), [4, 14])
    assert result[7].cards == get_test_cards("D4|C4|S4|H4|DA")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|HA"), [4, 14])
    assert result[8].cards == get_test_cards("D4|C4|S4|H4|HA")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4|S7"), [4, 7])
    assert result[9].cards == get_test_cards("D4|C4|S4|H4|S7")


def test_when_make_quads_hands_and_not_include_kickers_then_correct_values_returned(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D4|SA|C4|DA|S4|H4|HA|S7")
    result = engine.make_quads_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("CA|SA|DA|HA"), [14, None])
    assert result[0].cards == get_test_cards("CA|SA|DA|HA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D4|C4|S4|H4"), [4, None])
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

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|DA|HA|S4|C4"), [14, 4])
    assert result[0].cards == get_test_cards("CA|DA|HA|S4|C4")


def test_when_make_full_house_hands_and_many_options_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|D7|S2|H7|C2|SA|D2|S7|HA")
    result = engine.make_full_house_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 18

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|SA|HA|D7|H7"), [14, 7])
    assert result[0].cards == get_test_cards("CA|SA|HA|D7|H7")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|SA|HA|D7|S7"), [14, 7])
    assert result[1].cards == get_test_cards("CA|SA|HA|D7|S7")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|SA|HA|H7|S7"), [14, 7])
    assert result[2].cards == get_test_cards("CA|SA|HA|H7|S7")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|SA|HA|S2|C2"), [14, 2])
    assert result[3].cards == get_test_cards("CA|SA|HA|S2|C2")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|SA|HA|S2|D2"), [14, 2])
    assert result[4].cards == get_test_cards("CA|SA|HA|S2|D2")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("CA|SA|HA|C2|D2"), [14, 2])
    assert result[5].cards == get_test_cards("CA|SA|HA|C2|D2")

    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("D7|H7|S7|CA|SA"), [7, 14])
    assert result[6].cards == get_test_cards("D7|H7|S7|CA|SA")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("D7|H7|S7|CA|HA"), [7, 14])
    assert result[7].cards == get_test_cards("D7|H7|S7|CA|HA")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("D7|H7|S7|SA|HA"), [7, 14])
    assert result[8].cards == get_test_cards("D7|H7|S7|SA|HA")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("D7|H7|S7|S2|C2"), [7, 2])
    assert result[9].cards == get_test_cards("D7|H7|S7|S2|C2")
    assert result[10] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("D7|H7|S7|S2|D2"), [7, 2])
    assert result[10].cards == get_test_cards("D7|H7|S7|S2|D2")
    assert result[11] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("D7|H7|S7|C2|D2"), [7, 2])
    assert result[11].cards == get_test_cards("D7|H7|S7|C2|D2")

    assert result[12] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("S2|C2|D2|CA|SA"), [2, 14])
    assert result[12].cards == get_test_cards("S2|C2|D2|CA|SA")
    assert result[13] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("S2|C2|D2|CA|HA"), [2, 14])
    assert result[13].cards == get_test_cards("S2|C2|D2|CA|HA")
    assert result[14] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("S2|C2|D2|SA|HA"), [2, 14])
    assert result[14].cards == get_test_cards("S2|C2|D2|SA|HA")
    assert result[15] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("S2|C2|D2|D7|H7"), [2, 7])
    assert result[15].cards == get_test_cards("S2|C2|D2|D7|H7")
    assert result[16] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("S2|C2|D2|D7|S7"), [2, 7])
    assert result[16].cards == get_test_cards("S2|C2|D2|D7|S7")
    assert result[17] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("S2|C2|D2|H7|S7"), [2, 7])
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

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|C9|CT"), [14, 10, 9, 7, 2])
    assert result[0].cards == get_test_cards("CA|C7|C2|C9|CT")


def test_when_make_flush_hands_and_many_cards_of_flush_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|C7|C2|C9|CT|S4|C4|D9|SJ|DQ")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 6

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C9|CT|C4"), [14, 10, 9, 7, 4])
    assert result[0].cards == get_test_cards("CA|C7|C9|CT|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|C9|CT"), [14, 10, 9, 7, 2])
    assert result[1].cards == get_test_cards("CA|C7|C2|C9|CT")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C2|C9|CT|C4"), [14, 10, 9, 4, 2])
    assert result[2].cards == get_test_cards("CA|C2|C9|CT|C4")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|CT|C4"), [14, 10, 7, 4, 2])
    assert result[3].cards == get_test_cards("CA|C7|C2|CT|C4")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|C9|C4"), [14, 9, 7, 4, 2])
    assert result[4].cards == get_test_cards("CA|C7|C2|C9|C4")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("C7|C2|C9|CT|C4"), [10, 9, 7, 4, 2])
    assert result[5].cards == get_test_cards("C7|C2|C9|CT|C4")


def test_when_make_flush_hands_and_multiple_flush_suits_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("CA|C7|C2|C9|CT|S4|C4|D9|SJ|DQ|D4|D8|DT")
    result = engine.make_flush_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 7

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C9|CT|C4"), [14, 10, 9, 7, 4])
    assert result[0].cards == get_test_cards("CA|C7|C9|CT|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|C9|CT"), [14, 10, 9, 7, 2])
    assert result[1].cards == get_test_cards("CA|C7|C2|C9|CT")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C2|C9|CT|C4"), [14, 10, 9, 4, 2])
    assert result[2].cards == get_test_cards("CA|C2|C9|CT|C4")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|CT|C4"), [14, 10, 7, 4, 2])
    assert result[3].cards == get_test_cards("CA|C7|C2|CT|C4")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("CA|C7|C2|C9|C4"), [14, 9, 7, 4, 2])
    assert result[4].cards == get_test_cards("CA|C7|C2|C9|C4")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("D9|DQ|D4|D8|DT"), [12, 10, 9, 8, 4])
    assert result[5].cards == get_test_cards("D9|DQ|D4|D8|DT")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Flush, get_test_cards("C7|C2|C9|CT|C4"), [10, 9, 7, 4, 2])
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
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("CA|SJ|DK|ST|CQ"), [14])
    assert result[0].cards == get_test_cards("ST|SJ|CQ|DK|CA")


def test_when_make_straight_hands_and_running_straights_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("D8|CA|SJ|DK|ST|D9|CQ")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("ST|SJ|CQ|DK|CA"), [14])
    assert result[0].cards == get_test_cards("ST|SJ|CQ|DK|CA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("D9|ST|SJ|CQ|DK"), [13])
    assert result[1].cards == get_test_cards("D9|ST|SJ|CQ|DK")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("D8|D9|ST|SJ|CQ"), [12])
    assert result[2].cards == get_test_cards("D8|D9|ST|SJ|CQ")


def test_when_make_straight_hands_and_ace_low_straight_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("D5|CA|S3|D2|S6|D4")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("D2|S3|D4|D5|S6"), [6])
    assert result[0].cards == get_test_cards("D2|S3|D4|D5|S6")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("CA|D2|S3|D4|D5"), [5])
    assert result[1].cards == get_test_cards("CA|D2|S3|D4|D5")


def test_when_make_straight_hands_and_disconnected_straights_then_return_correct_values(
    engine, get_test_cards
):
    cards = get_test_cards("D3|CA|SJ|DK|ST|D2|CQ|S4|S5")
    result = engine.make_straight_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("ST|SJ|CQ|DK|CA"), [14])
    assert result[0].cards == get_test_cards("ST|SJ|CQ|DK|CA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, get_test_cards("CA|D2|D3|S4|S5"), [5])
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

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ"), [12, None, None])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|CQ"), [12, None, None])
    assert result[1].cards == get_test_cards("SQ|HQ|CQ")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|DQ|CQ"), [12, None, None])
    assert result[2].cards == get_test_cards("SQ|DQ|CQ")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("HQ|DQ|CQ"), [12, None, None])
    assert result[3].cards == get_test_cards("HQ|DQ|CQ")


def test_when_make_trips_hands_and_multiple_trips_and_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|C9|CJ|DQ|C7|CQ")
    result = engine.make_trips_hands(cards, include_kickers=True)

    assert isinstance(result, list)
    assert len(result) == 12

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|CJ|C9"), [12, 11, 9])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ|CJ|C9")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|CQ|CJ|C9"), [12, 11, 9])
    assert result[1].cards == get_test_cards("SQ|HQ|CQ|CJ|C9")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|DQ|CQ|CJ|C9"), [12, 11, 9])
    assert result[2].cards == get_test_cards("SQ|DQ|CQ|CJ|C9")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("HQ|DQ|CQ|CJ|C9"), [12, 11, 9])
    assert result[3].cards == get_test_cards("HQ|DQ|CQ|CJ|C9")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|CJ|C7"), [12, 11, 7])
    assert result[4].cards == get_test_cards("SQ|HQ|DQ|CJ|C7")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|CQ|CJ|C7"), [12, 11, 7])
    assert result[5].cards == get_test_cards("SQ|HQ|CQ|CJ|C7")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|DQ|CQ|CJ|C7"), [12, 11, 7])
    assert result[6].cards == get_test_cards("SQ|DQ|CQ|CJ|C7")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("HQ|DQ|CQ|CJ|C7"), [12, 11, 7])
    assert result[7].cards == get_test_cards("HQ|DQ|CQ|CJ|C7")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|C9|C7"), [12, 9, 7])
    assert result[8].cards == get_test_cards("SQ|HQ|DQ|C9|C7")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|CQ|C9|C7"), [12, 9, 7])
    assert result[9].cards == get_test_cards("SQ|HQ|CQ|C9|C7")
    assert result[10] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|DQ|CQ|C9|C7"), [12, 9, 7])
    assert result[10].cards == get_test_cards("SQ|DQ|CQ|C9|C7")
    assert result[11] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("HQ|DQ|CQ|C9|C7"), [12, 9, 7])
    assert result[11].cards == get_test_cards("HQ|DQ|CQ|C9|C7")


def test_when_make_trips_hands_and_multiple_trip_values_and_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|S9|CJ|DQ|D9|C9")
    result = engine.make_trips_hands(cards, include_kickers=True)

    assert isinstance(result, list)
    assert len(result) == 6

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|CJ|S9"), [12, 11, 9])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ|CJ|S9")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|CJ|D9"), [12, 11, 9])
    assert result[1].cards == get_test_cards("SQ|HQ|DQ|CJ|D9")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|CJ|C9"), [12, 11, 9])
    assert result[2].cards == get_test_cards("SQ|HQ|DQ|CJ|C9")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("S9|D9|C9|SQ|CJ"), [9, 12, 11])
    assert result[3].cards == get_test_cards("S9|D9|C9|SQ|CJ")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("S9|D9|C9|HQ|CJ"), [9, 12, 11])
    assert result[4].cards == get_test_cards("S9|D9|C9|HQ|CJ")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("S9|D9|C9|DQ|CJ"), [9, 12, 11])
    assert result[5].cards == get_test_cards("S9|D9|C9|DQ|CJ")


def test_when_make_trips_hands_and_multiple_trip_values_and_not_kickers_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|S9|CJ|DQ|D9|C9")
    result = engine.make_trips_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ"), [12, None, None])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("S9|D9|C9"), [9, None, None])
    assert result[1].cards == get_test_cards("S9|D9|C9")


def test_when_make_trips_hands_and_only_one_kicker_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|S9|DQ|D9")
    result = engine.make_trips_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|S9"), [12, 9, None])
    assert result[0].cards == get_test_cards("SQ|HQ|DQ|S9")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ|D9"), [12, 9, None])
    assert result[1].cards == get_test_cards("SQ|HQ|DQ|D9")


def test_when_make_trips_hands_and_no_kicker_then_return_hands(engine, get_test_cards):
    cards = get_test_cards("SQ|HQ|CQ|DQ")
    result = engine.make_trips_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|CQ"), [12, None, None])
    assert result[0].cards == get_test_cards("SQ|HQ|CQ")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|HQ|DQ"), [12, None, None])
    assert result[1].cards == get_test_cards("SQ|HQ|DQ")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("SQ|CQ|DQ"), [12, None, None])
    assert result[2].cards == get_test_cards("SQ|CQ|DQ")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Trips, get_test_cards("HQ|CQ|DQ"), [12, None, None])
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

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|SA"), [7, 4, 14])
    assert result[0].cards == get_test_cards("C4|D4|S7|H7|SA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|HK"), [7, 4, 13])
    assert result[1].cards == get_test_cards("C4|D4|S7|H7|HK")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|SJ"), [7, 4, 11])
    assert result[2].cards == get_test_cards("C4|D4|S7|H7|SJ")


def test_when_make_two_pair_hands_and_single_set_of_values_over_two_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HK|SJ|SA|S4|C7")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 27

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|SA"), [7, 4, 14])
    assert result[0].cards == get_test_cards("C4|D4|S7|H7|SA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|C7|SA"), [7, 4, 14])
    assert result[1].cards == get_test_cards("C4|D4|S7|C7|SA")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|H7|C7|SA"), [7, 4, 14])
    assert result[2].cards == get_test_cards("C4|D4|H7|C7|SA")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|H7|SA"), [7, 4, 14])
    assert result[3].cards == get_test_cards("C4|S4|S7|H7|SA")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|C7|SA"), [7, 4, 14])
    assert result[4].cards == get_test_cards("C4|S4|S7|C7|SA")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|H7|C7|SA"), [7, 4, 14])
    assert result[5].cards == get_test_cards("C4|S4|H7|C7|SA")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|H7|SA"), [7, 4, 14])
    assert result[6].cards == get_test_cards("D4|S4|S7|H7|SA")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|C7|SA"), [7, 4, 14])
    assert result[7].cards == get_test_cards("D4|S4|S7|C7|SA")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|H7|C7|SA"), [7, 4, 14])
    assert result[8].cards == get_test_cards("D4|S4|H7|C7|SA")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|HK"), [7, 4, 13])
    assert result[9].cards == get_test_cards("C4|D4|S7|H7|HK")
    assert result[10] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|C7|HK"), [7, 4, 13])
    assert result[10].cards == get_test_cards("C4|D4|S7|C7|HK")
    assert result[11] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|H7|C7|HK"), [7, 4, 13])
    assert result[11].cards == get_test_cards("C4|D4|H7|C7|HK")
    assert result[12] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|H7|HK"), [7, 4, 13])
    assert result[12].cards == get_test_cards("C4|S4|S7|H7|HK")
    assert result[13] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|C7|HK"), [7, 4, 13])
    assert result[13].cards == get_test_cards("C4|S4|S7|C7|HK")
    assert result[14] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|H7|C7|HK"), [7, 4, 13])
    assert result[14].cards == get_test_cards("C4|S4|H7|C7|HK")
    assert result[15] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|H7|HK"), [7, 4, 13])
    assert result[15].cards == get_test_cards("D4|S4|S7|H7|HK")
    assert result[16] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|C7|HK"), [7, 4, 13])
    assert result[16].cards == get_test_cards("D4|S4|S7|C7|HK")
    assert result[17] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|H7|C7|HK"), [7, 4, 13])
    assert result[17].cards == get_test_cards("D4|S4|H7|C7|HK")
    assert result[18] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|SJ"), [7, 4, 11])
    assert result[18].cards == get_test_cards("C4|D4|S7|H7|SJ")
    assert result[19] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|C7|SJ"), [7, 4, 11])
    assert result[19].cards == get_test_cards("C4|D4|S7|C7|SJ")
    assert result[20] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|H7|C7|SJ"), [7, 4, 11])
    assert result[20].cards == get_test_cards("C4|D4|H7|C7|SJ")
    assert result[21] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|H7|SJ"), [7, 4, 11])
    assert result[21].cards == get_test_cards("C4|S4|S7|H7|SJ")
    assert result[22] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|C7|SJ"), [7, 4, 11])
    assert result[22].cards == get_test_cards("C4|S4|S7|C7|SJ")
    assert result[23] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|H7|C7|SJ"), [7, 4, 11])
    assert result[23].cards == get_test_cards("C4|S4|H7|C7|SJ")
    assert result[24] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|H7|SJ"), [7, 4, 11])
    assert result[24].cards == get_test_cards("D4|S4|S7|H7|SJ")
    assert result[25] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|C7|SJ"), [7, 4, 11])
    assert result[25].cards == get_test_cards("D4|S4|S7|C7|SJ")
    assert result[26] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|H7|C7|SJ"), [7, 4, 11])
    assert result[26].cards == get_test_cards("D4|S4|H7|C7|SJ")


def test_when_make_two_pair_hands_and_multiple_sets_of_values_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HA|SJ|SA|CA")

    result = engine.make_two_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 22

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|SA|SJ"), [14, 7, 11])
    assert result[0].cards == get_test_cards("S7|H7|HA|SA|SJ")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|CA|SJ"), [14, 7, 11])
    assert result[1].cards == get_test_cards("S7|H7|HA|CA|SJ")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|SA|CA|SJ"), [14, 7, 11])
    assert result[2].cards == get_test_cards("S7|H7|SA|CA|SJ")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|SA|C4"), [14, 7, 4])
    assert result[3].cards == get_test_cards("S7|H7|HA|SA|C4")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|SA|D4"), [14, 7, 4])
    assert result[4].cards == get_test_cards("S7|H7|HA|SA|D4")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|CA|C4"), [14, 7, 4])
    assert result[5].cards == get_test_cards("S7|H7|HA|CA|C4")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|CA|D4"), [14, 7, 4])
    assert result[6].cards == get_test_cards("S7|H7|HA|CA|D4")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|SA|CA|C4"), [14, 7, 4])
    assert result[7].cards == get_test_cards("S7|H7|SA|CA|C4")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|SA|CA|D4"), [14, 7, 4])
    assert result[8].cards == get_test_cards("S7|H7|SA|CA|D4")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|SA|SJ"), [14, 4, 11])
    assert result[9].cards == get_test_cards("C4|D4|HA|SA|SJ")
    assert result[10] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|CA|SJ"), [14, 4, 11])
    assert result[10].cards == get_test_cards("C4|D4|HA|CA|SJ")
    assert result[11] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|SA|CA|SJ"), [14, 4, 11])
    assert result[11].cards == get_test_cards("C4|D4|SA|CA|SJ")
    assert result[12] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|SA|S7"), [14, 4, 7])
    assert result[12].cards == get_test_cards("C4|D4|HA|SA|S7")
    assert result[13] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|SA|H7"), [14, 4, 7])
    assert result[13].cards == get_test_cards("C4|D4|HA|SA|H7")
    assert result[14] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|CA|S7"), [14, 4, 7])
    assert result[14].cards == get_test_cards("C4|D4|HA|CA|S7")
    assert result[15] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|CA|H7"), [14, 4, 7])
    assert result[15].cards == get_test_cards("C4|D4|HA|CA|H7")
    assert result[16] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|SA|CA|S7"), [14, 4, 7])
    assert result[16].cards == get_test_cards("C4|D4|SA|CA|S7")
    assert result[17] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|SA|CA|H7"), [14, 4, 7])
    assert result[17].cards == get_test_cards("C4|D4|SA|CA|H7")
    assert result[18] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|HA"), [7, 4, 14])
    assert result[18].cards == get_test_cards("C4|D4|S7|H7|HA")
    assert result[19] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|SA"), [7, 4, 14])
    assert result[19].cards == get_test_cards("C4|D4|S7|H7|SA")
    assert result[20] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|CA"), [7, 4, 14])
    assert result[20].cards == get_test_cards("C4|D4|S7|H7|CA")
    assert result[21] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7|SJ"), [7, 4, 11])
    assert result[21].cards == get_test_cards("C4|D4|S7|H7|SJ")


def test_when_make_two_pair_hands_and_not_kickers_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|HA|SJ|SA|CA")

    result = engine.make_two_pair_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 7

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|SA"), [14, 7, None])
    assert result[0].cards == get_test_cards("S7|H7|HA|SA")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|HA|CA"), [14, 7, None])
    assert result[1].cards == get_test_cards("S7|H7|HA|CA")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("S7|H7|SA|CA"), [14, 7, None])
    assert result[2].cards == get_test_cards("S7|H7|SA|CA")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|SA"), [14, 4, None])
    assert result[3].cards == get_test_cards("C4|D4|HA|SA")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|HA|CA"), [14, 4, None])
    assert result[4].cards == get_test_cards("C4|D4|HA|CA")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|SA|CA"), [14, 4, None])
    assert result[5].cards == get_test_cards("C4|D4|SA|CA")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7"), [7, 4, None])
    assert result[6].cards == get_test_cards("C4|D4|S7|H7")


def test_when_make_two_pair_hands_and_no_kickers_available_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S7|D4|H7|S4")

    result = engine.make_two_pair_hands(cards, include_kickers=True)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|D4|S7|H7"), [7, 4, None])
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("C4|S4|S7|H7"), [7, 4, None])
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.TwoPair, get_test_cards("D4|S4|S7|H7"), [7, 4, None])


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

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|CQ|H8"), [4, 14, 12, 8])
    assert result[0].cards == get_test_cards("C4|D4|HA|CQ|H8")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|CQ|D7"), [4, 14, 12, 7])
    assert result[1].cards == get_test_cards("C4|D4|HA|CQ|D7")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|CQ|S2"), [4, 14, 12, 2])
    assert result[2].cards == get_test_cards("C4|D4|HA|CQ|S2")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|H8|D7"), [4, 14, 8, 7])
    assert result[3].cards == get_test_cards("C4|D4|HA|H8|D7")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[4].cards == get_test_cards("C4|D4|HA|H8|S2")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|D7|S2"), [4, 14, 7, 2])
    assert result[5].cards == get_test_cards("C4|D4|HA|D7|S2")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|CQ|H8|D7"), [4, 12, 8, 7])
    assert result[6].cards == get_test_cards("C4|D4|CQ|H8|D7")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|CQ|H8|S2"), [4, 12, 8, 2])
    assert result[7].cards == get_test_cards("C4|D4|CQ|H8|S2")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|CQ|D7|S2"), [4, 12, 7, 2])
    assert result[8].cards == get_test_cards("C4|D4|CQ|D7|S2")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[9].cards == get_test_cards("C4|D4|H8|D7|S2")


def test_when_make_pair_hands_and_single_overloaded_pair_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|H7|HA|S2|H8|S4|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 12

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|HA|H8|H7"), [4, 14, 8, 7])
    assert result[0].cards == get_test_cards("C4|S4|HA|H8|H7")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|H8|H7"), [4, 14, 8, 7])
    assert result[1].cards == get_test_cards("C4|D4|HA|H8|H7")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4|HA|H8|H7"), [4, 14, 8, 7])
    assert result[2].cards == get_test_cards("S4|D4|HA|H8|H7")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[3].cards == get_test_cards("C4|S4|HA|H8|S2")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[4].cards == get_test_cards("C4|D4|HA|H8|S2")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4|HA|H8|S2"), [4, 14, 8, 2])
    assert result[5].cards == get_test_cards("S4|D4|HA|H8|S2")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|HA|H7|S2"), [4, 14, 7, 2])
    assert result[6].cards == get_test_cards("C4|S4|HA|H7|S2")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|HA|H7|S2"), [4, 14, 7, 2])
    assert result[7].cards == get_test_cards("C4|D4|HA|H7|S2")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4|HA|H7|S2"), [4, 14, 7, 2])
    assert result[8].cards == get_test_cards("S4|D4|HA|H7|S2")
    assert result[9] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[9].cards == get_test_cards("C4|S4|H8|H7|S2")
    assert result[10] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[10].cards == get_test_cards("C4|D4|H8|H7|S2")
    assert result[11] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[11].cards == get_test_cards("S4|D4|H8|H7|S2")


def test_when_make_pair_hands_and_multiple_pairs_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S2|H8|S4|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 9

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|H8|C4|S2"), [7, 8, 4, 2])
    assert result[0].cards == get_test_cards("D7|H7|H8|C4|S2")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|H8|S4|S2"), [7, 8, 4, 2])
    assert result[1].cards == get_test_cards("D7|H7|H8|S4|S2")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|H8|D4|S2"), [7, 8, 4, 2])
    assert result[2].cards == get_test_cards("D7|H7|H8|D4|S2")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[3].cards == get_test_cards("C4|S4|H8|D7|S2")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[4].cards == get_test_cards("C4|S4|H8|H7|S2")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[5].cards == get_test_cards("C4|D4|H8|D7|S2")
    assert result[6] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[6].cards == get_test_cards("C4|D4|H8|H7|S2")
    assert result[7] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4|H8|D7|S2"), [4, 8, 7, 2])
    assert result[7].cards == get_test_cards("S4|D4|H8|D7|S2")
    assert result[8] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4|H8|H7|S2"), [4, 8, 7, 2])
    assert result[8].cards == get_test_cards("S4|D4|H8|H7|S2")


def test_when_make_pair_hands_and_no_kickers_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S2|H8|S4|D4")

    result = engine.make_pair_hands(cards, include_kickers=False)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7"), [7, None, None, None])
    assert result[0].cards == get_test_cards("D7|H7")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4"), [4, None, None, None])
    assert result[1].cards == get_test_cards("C4|S4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4"), [4, None, None, None])
    assert result[2].cards == get_test_cards("C4|D4")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4"), [4, None, None, None])
    assert result[3].cards == get_test_cards("S4|D4")


def test_when_make_pair_hands_and_only_two_kickers_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S2|S4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|C4|S2"), [7, 4, 2, None])
    assert result[0].cards == get_test_cards("D7|H7|C4|S2")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|S4|S2"), [7, 4, 2, None])
    assert result[1].cards == get_test_cards("D7|H7|S4|S2")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|D7|S2"), [4, 7, 2, None])
    assert result[2].cards == get_test_cards("C4|S4|D7|S2")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|H7|S2"), [4, 7, 2, None])
    assert result[3].cards == get_test_cards("C4|S4|H7|S2")


def test_when_make_pair_hands_and_only_one_kicker_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|D7|H7|S4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|C4"), [7, 4, None, None])
    assert result[0].cards == get_test_cards("D7|H7|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|S4"), [7, 4, None, None])
    assert result[1].cards == get_test_cards("D7|H7|S4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|D7"), [4, 7, None, None])
    assert result[2].cards == get_test_cards("C4|S4|D7")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4|H7"), [4, 7, None, None])
    assert result[3].cards == get_test_cards("C4|S4|H7")


def test_when_make_pair_hands_and_only_no_kicker_available_then_correct_list_returned(engine, get_test_cards):
    cards = get_test_cards("C4|S4|D4")

    result = engine.make_pair_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|S4"), [4, None, None, None])
    assert result[0].cards == get_test_cards("C4|S4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C4|D4"), [4, None, None, None])
    assert result[1].cards == get_test_cards("C4|D4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("S4|D4"), [4, None, None, None])
    assert result[2].cards == get_test_cards("S4|D4")


def test_when_make_high_card_hands_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|D8|SK|C5|DT|S2")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 6

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|DT|D8|C5|C4"), [13, 10, 8, 5, 4])
    assert result[0].cards == get_test_cards("SK|DT|D8|C5|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|DT|D8|C5|S2"), [13, 10, 8, 5, 2])
    assert result[1].cards == get_test_cards("SK|DT|D8|C5|S2")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|DT|D8|C4|S2"), [13, 10, 8, 4, 2])
    assert result[2].cards == get_test_cards("SK|DT|D8|C4|S2")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|DT|C5|C4|S2"), [13, 10, 5, 4, 2])
    assert result[3].cards == get_test_cards("SK|DT|C5|C4|S2")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|D8|C5|C4|S2"), [13, 8, 5, 4, 2])
    assert result[4].cards == get_test_cards("SK|D8|C5|C4|S2")
    assert result[5] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("DT|D8|C5|C4|S2"), [10, 8, 5, 4, 2])
    assert result[5].cards == get_test_cards("DT|D8|C5|C4|S2")


def test_when_make_high_card_hands_and_pairs_excluded_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|D8|SK|C8|DT|S2")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|DT|D8|C4|S2"), [13, 10, 8, 4, 2])
    assert result[0].cards == get_test_cards("SK|DT|D8|C4|S2")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|DT|C8|C4|S2"), [13, 10, 8, 4, 2])
    assert result[1].cards == get_test_cards("SK|DT|C8|C4|S2")


def test_when_make_high_card_hands_and_flush_excluded_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|C8|SK|C7|CT|C2")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 5

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|CT|C8|C7|C4"), [13, 10, 8, 7, 4])
    assert result[0].cards == get_test_cards("SK|CT|C8|C7|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|CT|C8|C7|C2"), [13, 10, 8, 7, 2])
    assert result[1].cards == get_test_cards("SK|CT|C8|C7|C2")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|CT|C8|C4|C2"), [13, 10, 8, 4, 2])
    assert result[2].cards == get_test_cards("SK|CT|C8|C4|C2")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|CT|C7|C4|C2"), [13, 10, 7, 4, 2])
    assert result[3].cards == get_test_cards("SK|CT|C7|C4|C2")
    assert result[4] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("SK|C8|C7|C4|C2"), [13, 8, 7, 4, 2])
    assert result[4].cards == get_test_cards("SK|C8|C7|C4|C2")


def test_when_make_high_card_hands_and_straight_excluded_then_return_five_card_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S8|S9|H7|D5|C6")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|S8|H7|C6|C4"), [9, 8, 7, 6, 4])
    assert result[0].cards == get_test_cards("S9|S8|H7|C6|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|S8|H7|D5|C4"), [9, 8, 7, 5, 4])
    assert result[1].cards == get_test_cards("S9|S8|H7|D5|C4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|S8|C6|D5|C4"), [9, 8, 6, 5, 4])
    assert result[2].cards == get_test_cards("S9|S8|C6|D5|C4")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|H7|C6|D5|C4"), [9, 7, 6, 5, 4])
    assert result[3].cards == get_test_cards("S9|H7|C6|D5|C4")


def test_when_make_high_card_hands_and_only_four_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|S9|H7|D5")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|H7|D5|C4"), [9, 7, 5, 4, None])
    assert result[0].cards == get_test_cards("S9|H7|D5|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|H7|D5|S4"), [9, 7, 5, 4, None])
    assert result[1].cards == get_test_cards("S9|H7|D5|S4")


def test_when_make_high_card_hands_and_only_three_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|S9|H7|D7")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 4

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|H7|C4"), [9, 7, 4, None, None])
    assert result[0].cards == get_test_cards("S9|H7|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|D7|C4"), [9, 7, 4, None, None])
    assert result[1].cards == get_test_cards("S9|D7|C4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|H7|S4"), [9, 7, 4, None, None])
    assert result[2].cards == get_test_cards("S9|H7|S4")
    assert result[3] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|D7|S4"), [9, 7, 4, None, None])
    assert result[3].cards == get_test_cards("S9|D7|S4")


def test_when_make_high_card_hands_and_only_two_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|S9|H4")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|C4"), [9, 4, None, None, None])
    assert result[0].cards == get_test_cards("S9|C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|S4"), [9, 4, None, None, None])
    assert result[1].cards == get_test_cards("S9|S4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S9|H4"), [9, 4, None, None, None])
    assert result[2].cards == get_test_cards("S9|H4")


def test_when_make_high_card_hands_and_only_single_card_combos_available_then_return_correct_hands(engine, get_test_cards):
    cards = get_test_cards("C4|S4|H4")

    result = engine.make_high_card_hands(cards)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C4"), [4, None, None, None, None])
    assert result[0].cards == get_test_cards("C4")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("S4"), [4, None, None, None, None])
    assert result[1].cards == get_test_cards("S4")
    assert result[2] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("H4"), [4, None, None, None, None])
    assert result[2].cards == get_test_cards("H4")


# Public "Find Outs" method tests
# --------------------------------
def test_when_find_outs_straight_flush_and_one_draw_and_no_suits_with_enough_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|S7|D8|H5|H6|C3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_straight_flush_and_one_draw_inside_straight_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|C7|C8|C5|H6|C3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 1
    assert get_test_cards("C6") in outs


def test_when_find_outs_straight_flush_and_one_draw_open_straight_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|C7|C8|C5|H6|SA")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 2
    assert get_test_cards("C4") in outs
    assert get_test_cards("C9") in outs


def test_when_find_outs_straight_flush_and_already_have_one_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|C7|C8|C5|C4|SA")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 3
    assert get_test_cards("ANY_CARD") in outs
    assert get_test_cards("C9") in outs
    assert get_test_cards("C3") in outs


def test_when_find_outs_straight_flush_and_two_draws_and_no_suits_with_enough_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|S7|D8|H5|H6")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_straight_flush_and_two_draws_inside_straight_need_all_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|C8|C5|H6|S3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 1
    assert get_test_cards("C7|C6") in outs


def test_when_find_outs_straight_flush_and_two_draws_inside_straight_need_partial_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|C8|C5|C6|S3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 4
    assert get_test_cards("C7|ANY_CARD") in outs
    assert get_test_cards("C9|C7") in outs
    assert get_test_cards("C7|C3") in outs
    assert get_test_cards("C3|C2") in outs


def test_when_find_outs_straight_flush_and_two_draws_open_straight_need_all_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|C7|C8|H7|H6|SA")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 3
    assert get_test_cards("C9|C5") in outs
    assert get_test_cards("C5|C4") in outs
    assert get_test_cards("CT|C9") in outs


def test_when_find_outs_straight_flush_and_two_draws_open_straight_need_partial_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|C7|C8|C5|SA")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 4

    assert get_test_cards("C4|ANY_CARD") in outs
    assert get_test_cards("C9|ANY_CARD") in outs
    assert get_test_cards("C4|C3") in outs
    assert get_test_cards("CT|C9") in outs


def test_when_find_outs_straight_flush_and_three_draws_and_no_suits_with_enough_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|S7|D8|H5")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_straight_flush_and_three_draws_inside_straight_need_all_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|D8|H6|S3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 1
    assert get_test_cards("D7|D6|D5") in outs


def test_when_find_outs_straight_flush_and_three_draws_inside_straight_need_partial_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("H8|H5|H9|C3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 5

    assert get_test_cards("H7|H6|ANY_CARD") in outs
    assert get_test_cards("H7|H6|H4") in outs
    assert get_test_cards("HT|H7|H6") in outs
    assert get_test_cards("HJ|HT|H7") in outs
    assert get_test_cards("HQ|HJ|HT") in outs


def test_when_find_outs_straight_flush_and_three_draws_open_straight_need_all_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|C7|H6|SA")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 4

    assert get_test_cards("C5|C4|C3") in outs
    assert get_test_cards("C8|C5|C4") in outs
    assert get_test_cards("C9|C8|C5") in outs
    assert get_test_cards("CT|C9|C8") in outs


def test_when_find_outs_straight_flush_and_three_draws_open_straight_need_partial_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|C7|C8|C5")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 6

    assert get_test_cards("C4|ANY_CARD|ANY_CARD") in outs
    assert get_test_cards("C9|ANY_CARD|ANY_CARD") in outs
    assert get_test_cards("C4|C3|ANY_CARD") in outs
    assert get_test_cards("CT|C9|ANY_CARD") in outs
    assert get_test_cards("C4|C3|C2") in outs
    assert get_test_cards("CJ|CT|C9") in outs


def test_when_find_outs_straight_flush_and_three_draws_multiple_suits_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C6|S7|S8|C5")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 8

    assert get_test_cards("C4|C3|C2") in outs
    assert get_test_cards("C7|C4|C3") in outs
    assert get_test_cards("C8|C7|C4") in outs
    assert get_test_cards("C9|C8|C7") in outs

    assert get_test_cards("S6|S5|S4") in outs
    assert get_test_cards("S9|S6|S5") in outs
    assert get_test_cards("ST|S9|S6") in outs
    assert get_test_cards("SJ|ST|S9") in outs


def test_when_find_outs_straight_flush_and_four_draws_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|D6")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 4

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 8

    assert get_test_cards("DA|D5|D3|D2") in outs
    assert get_test_cards("D5|D3|D2|ANY_CARD") in outs
    assert get_test_cards("D7|D5|D3|ANY_CARD") in outs
    assert get_test_cards("D8|D7|D5|ANY_CARD") in outs
    assert get_test_cards("D9|D8|D7|D5") in outs
    assert get_test_cards("DT|D9|D8|D7") in outs
    assert get_test_cards("DA|DQ|DJ|DT") in outs
    assert get_test_cards("DQ|DJ|DT|D9") in outs


def test_when_find_outs_straight_flush_and_five_draws_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 5

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 40

    assert get_test_cards("DA|D5|D3|D2|ANY_CARD") in outs
    assert get_test_cards("D6|D5|D3|D2|ANY_CARD") in outs
    assert get_test_cards("D7|D6|D5|D3|ANY_CARD") in outs
    assert get_test_cards("D8|D7|D6|D5|ANY_CARD") in outs
    assert get_test_cards("D9|D8|D7|D6|D5") in outs
    assert get_test_cards("DT|D9|D8|D7|D6") in outs
    assert get_test_cards("DJ|DT|D9|D8|D7") in outs
    assert get_test_cards("DQ|DJ|DT|D9|D8") in outs
    assert get_test_cards("DQ|DJ|DT|D9|ANY_CARD") in outs
    assert get_test_cards("DA|DQ|DJ|DT|ANY_CARD") in outs

    assert get_test_cards("CA|C5|C4|C3|C2") in outs
    assert get_test_cards("C6|C5|C4|C3|C2") in outs
    assert get_test_cards("C7|C6|C5|C4|C3") in outs
    assert get_test_cards("C8|C7|C6|C5|C4") in outs
    assert get_test_cards("C9|C8|C7|C6|C5") in outs
    assert get_test_cards("CT|C9|C8|C7|C6") in outs
    assert get_test_cards("CJ|CT|C9|C8|C7") in outs
    assert get_test_cards("CQ|CJ|CT|C9|C8") in outs
    assert get_test_cards("CK|CQ|CJ|CT|C9") in outs
    assert get_test_cards("CA|CK|CQ|CJ|CT") in outs

    assert get_test_cards("HA|H5|H4|H3|H2") in outs
    assert get_test_cards("H6|H5|H4|H3|H2") in outs
    assert get_test_cards("H7|H6|H5|H4|H3") in outs
    assert get_test_cards("H8|H7|H6|H5|H4") in outs
    assert get_test_cards("H9|H8|H7|H6|H5") in outs
    assert get_test_cards("HT|H9|H8|H7|H6") in outs
    assert get_test_cards("HJ|HT|H9|H8|H7") in outs
    assert get_test_cards("HQ|HJ|HT|H9|H8") in outs
    assert get_test_cards("HK|HQ|HJ|HT|H9") in outs
    assert get_test_cards("HA|HK|HQ|HJ|HT") in outs

    assert get_test_cards("SA|S5|S4|S3|S2") in outs
    assert get_test_cards("S6|S5|S4|S3|S2") in outs
    assert get_test_cards("S7|S6|S5|S4|S3") in outs
    assert get_test_cards("S8|S7|S6|S5|S4") in outs
    assert get_test_cards("S9|S8|S7|S6|S5") in outs
    assert get_test_cards("ST|S9|S8|S7|S6") in outs
    assert get_test_cards("SJ|ST|S9|S8|S7") in outs
    assert get_test_cards("SQ|SJ|ST|S9|S8") in outs
    assert get_test_cards("SK|SQ|SJ|ST|S9") in outs
    assert get_test_cards("SA|SK|SQ|SJ|ST") in outs


def test_when_find_outs_straight_flush_implicit_outs_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|C8|C5|C6|S3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.Implicit)

    assert isinstance(outs, list)
    assert len(outs) == 4
    assert get_test_cards("C7|ANY_CARD") in outs
    assert get_test_cards("C9|C7") in outs
    assert get_test_cards("C7|C3") in outs
    assert get_test_cards("C3|C2") in outs


def test_when_find_outs_straight_flush_explict_partial_outs_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|C8|C5|C6|S3")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitPartial)

    assert isinstance(outs, list)
    assert len(outs) == 4
    assert get_test_cards("C7|ANY_CARD") in outs
    assert get_test_cards("C9|C7") in outs
    assert get_test_cards("C7|C3") in outs
    assert get_test_cards("C3|C2") in outs


def test_when_find_outs_straight_flush_explicit_full_outs_then_return_outs(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("C4|C8|C5|C6|S3")
    possible_draws = get_test_cards("C7|C9|C3|C2|S6|D9|HK|DA")
    remaining_draws = 2

    outs = engine.find_outs_straight_flush(current_cards, possible_draws, remaining_draws, OutsCalculationMethod.ExplicitFull)

    assert isinstance(outs, list)
    assert len(outs) == 8

    # C7 and any other card
    assert get_test_cards("C9|C7") in outs
    assert get_test_cards("C7|C3") in outs
    assert get_test_cards("C7|C2") in outs
    assert get_test_cards("C7|S6") in outs
    assert get_test_cards("D9|C7") in outs
    assert get_test_cards("HK|C7") in outs
    assert get_test_cards("DA|C7") in outs

    # Other Outs
    assert get_test_cards("C3|C2") in outs


def test_when_find_outs_quads_and_one_draw_no_quads_possible_then_empty_list_returned(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|S4|C9")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_quads_and_one_draw_one_quads_possible_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|S4|C4")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 1

    assert get_test_cards("H4") in outs


def test_when_find_outs_quads_and_one_draw_multiple_quads_possible_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|S4|C4|HK|SK")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 2

    assert get_test_cards("H4") in outs
    assert get_test_cards("CK") in outs


def test_when_find_outs_quads_and_one_draw_already_haev_quads_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CK|DK|S4|C4|HK|SK")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 1

    assert get_test_cards("ANY_CARD") in outs


def test_when_find_outs_quads_and_and_missing_card_not_in_possible_draws_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CK|D7|S4|C4|HK|SK")
    possible_draws = [card for card in full_deck if card not in current_cards and card not in get_test_cards("DK")]
    remaining_draws = 1

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0








def test_when_find_outs_quads_and_multiple_draws_no_quads_possible_then_empty_list_returned(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|SA|C9")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_quads_and_multiple_draw_one_quads_possible_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|S4|C3|D9")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 1

    assert get_test_cards("H4|C4") in outs


def test_when_find_outs_quads_and_multiple_draw_multiple_quads_possible_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("D4|DK|S7|C9")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 3

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 4

    assert get_test_cards("H4|C4|S4") in outs
    assert get_test_cards("HK|CK|SK") in outs
    assert get_test_cards("H7|D7|C7") in outs
    assert get_test_cards("H9|D9|S9") in outs


def test_when_find_outs_quads_and_multiple_draw_already_have_quads_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CK|DK|S4|C7|HK|SK")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 1

    assert get_test_cards("ANY_CARD|ANY_CARD") in outs


def test_when_find_outs_quads_and_multiple_draw_and_only_need_one_then_any_cards_fill_in_blanks(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CK|DK|S4|C7|HK")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_quads(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 1

    assert get_test_cards("SK|ANY_CARD") in outs


def test_when_find_outs_full_house_and_single_draw_and_no_full_house_possible_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CK|DK|S4|C7|H8")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_full_house_and_single_draw_and_hand_possible_on_pair_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CK|DK|S4|HK|H8")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 6

    assert get_test_cards("H4") in outs
    assert get_test_cards("C4") in outs
    assert get_test_cards("D4") in outs

    assert get_test_cards("S8") in outs
    assert get_test_cards("C8") in outs
    assert get_test_cards("D8") in outs


def test_when_find_outs_full_house_and_single_draw_and_hand_possible_on_trips_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CA|D2|SA|H2|H8")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 4

    assert get_test_cards("DA") in outs
    assert get_test_cards("HA") in outs

    assert get_test_cards("C2") in outs
    assert get_test_cards("S2") in outs


def test_when_find_outs_full_house_and_single_draw_and_deck_exhausted_of_req_value_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CA|D2|SA|H2|H8")
    possible_draws = [card for card in full_deck if card not in current_cards and card not in get_test_cards("DA|HA|C2|S2")]
    remaining_draws = 1

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_full_house_and_single_draw_and_already_have_full_house_then_return_correct_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CA|D2|SA|H2|HA")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 1

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 3

    assert get_test_cards("ANY_CARD") in outs
    assert get_test_cards("C2") in outs
    assert get_test_cards("S2") in outs


def test_when_find_outs_full_house_and_multiple_draw_and_no_full_house_possible_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CA|D2|SK|H7|H8")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0


def test_when_find_outs_full_house_and_multiple_draw_and_full_house_possible_then_return_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CA|D2|S2|H7|H8")
    possible_draws = [card for card in full_deck if card not in current_cards]
    remaining_draws = 2

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 27

    assert get_test_cards("H2|DA") in outs
    assert get_test_cards("H2|SA") in outs
    assert get_test_cards("H2|HA") in outs
    assert get_test_cards("H2|C7") in outs
    assert get_test_cards("H2|D7") in outs
    assert get_test_cards("H2|S7") in outs
    assert get_test_cards("H2|C8") in outs
    assert get_test_cards("H2|D8") in outs
    assert get_test_cards("H2|S8") in outs

    assert get_test_cards("C2|DA") in outs
    assert get_test_cards("C2|SA") in outs
    assert get_test_cards("C2|HA") in outs
    assert get_test_cards("C2|C7") in outs
    assert get_test_cards("C2|D7") in outs
    assert get_test_cards("C2|S7") in outs
    assert get_test_cards("C2|C8") in outs
    assert get_test_cards("C2|D8") in outs
    assert get_test_cards("C2|S8") in outs

    assert get_test_cards("HA|DA") in outs
    assert get_test_cards("DA|SA") in outs
    assert get_test_cards("HA|SA") in outs

    assert get_test_cards("D7|C7") in outs
    assert get_test_cards("D7|S7") in outs
    assert get_test_cards("C7|S7") in outs

    assert get_test_cards("D8|C8") in outs
    assert get_test_cards("D8|S8") in outs
    assert get_test_cards("C8|S8") in outs


def test_when_find_outs_full_house_and_deck_missing_required_outs_then_return_empty_list(engine, get_test_cards, full_deck):
    current_cards = get_test_cards("CA|DA|S2|H2|H8")
    possible_draws = [card for card in full_deck if card not in current_cards and card not in get_test_cards("SA|HA|C2|D2")]
    remaining_draws = 1

    outs = engine.find_outs_full_house(current_cards, possible_draws, remaining_draws)

    assert isinstance(outs, list)
    assert len(outs) == 0