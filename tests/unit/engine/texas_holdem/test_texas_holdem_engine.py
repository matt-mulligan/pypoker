# Public Concrete Implementation of Pokerth_engine Abstract Methods
# ---------------------------------------------------------------
import re

from pypoker.constants import TexasHoldemHandType, GameTypes
from pypoker.constructs import Hand
from pypoker.exceptions import RankingError, OutsError
from pypoker.player.human import HumanPlayer
from mock import patch
from pytest import mark, raises


@mark.parametrize("hole_cards, board_cards, expected_hand_type, expected_hand_cards, expected_tiebreakers", [
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
        th_engine, get_test_cards, hole_cards, board_cards, expected_hand_type, expected_hand_cards, expected_tiebreakers
):
    player = HumanPlayer("Matt", hole_cards=get_test_cards(hole_cards))

    result = th_engine.find_player_best_hand(player, get_test_cards(board_cards))

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == Hand(
        GameTypes.TexasHoldem, expected_hand_type, get_test_cards(expected_hand_cards), expected_tiebreakers
    )
    assert result[0].cards == get_test_cards(expected_hand_cards)


def test_when_find_player_best_hand_and_multiple_hands_with_identical_tiebreakers_then_all_returned(
        th_engine, get_test_cards
):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("D9|SK"))
    board_cards = get_test_cards("S9|C9|HK|H9|C7")

    result = th_engine.find_player_best_hand(player, board_cards)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D9|S9|C9|H9|SK"),
                             [9, 13])
    assert result[0].cards == get_test_cards("D9|S9|C9|H9|SK")
    assert result[1] == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Quads, get_test_cards("D9|S9|C9|H9|HK"),
                             [9, 13])
    assert result[1].cards == get_test_cards("D9|S9|C9|H9|HK")


def test_when_rank_player_hands_and_not_all_players_are_player_objects_then_raise_error(th_engine):
    player_a = HumanPlayer("Matt")
    player_b = "Greg"
    player_c = HumanPlayer("Bill")

    with raises(RankingError, match=re.escape("All values of players list must be of BasePlayer Type")):
        th_engine.rank_player_hands([player_a, player_b, player_c])


def test_when_rank_player_hands_and_not_all_hands_set_then_raise_error(th_engine, get_test_cards):
    player_a = HumanPlayer("Matt", hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("C7|D7"),
                                             [7, None, None, None]))
    player_b = HumanPlayer("Bill")

    with raises(RankingError, match=re.escape("All players must have their player.hand attribute set to rank them.")):
        th_engine.rank_player_hands([player_a, player_b])


def test_when_rank_player_hands_and_all_different_strengths_then_return_correct_dict(th_engine, get_test_cards):
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
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C7|D4|HA|S9|S2"),
                  [14, 9, 7, 4, 2])
    )
    player_e = HumanPlayer(
        "Lucy",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("C7|D7|HA|SA|DA"), [14, 7])
    )

    ranked = th_engine.rank_player_hands([player_a, player_b, player_c, player_d, player_e])

    assert ranked == {
        1: [player_b], 2: [player_e], 3: [player_c], 4: [player_a], 5: [player_d]
    }


def test_when_rank_player_hands_and_strength_overlaps_then_return_correct_dict(th_engine, get_test_cards):
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
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C7|D4|HA|S9|S2"),
                  [14, 9, 7, 4, 2])
    )
    player_e = HumanPlayer(
        "Lucy",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("C7|D7|HA|SA|DA"), [14, 7])
    )

    ranked = th_engine.rank_player_hands([player_a, player_b, player_c, player_d, player_e])

    assert ranked == {
        1: [player_e], 2: [player_c], 3: [player_a], 4: [player_b], 5: [player_d]
    }


def test_when_rank_player_hands_and_strength_tiebreaker_overlaps_then_return_correct_dict(th_engine, get_test_cards):
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
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.HighCard, get_test_cards("C7|D4|HA|S9|S2"),
                  [14, 9, 7, 4, 2])
    )
    player_e = HumanPlayer(
        "Lucy",
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.FullHouse, get_test_cards("C7|D7|HA|SA|DA"), [14, 7])
    )

    ranked = th_engine.rank_player_hands([player_a, player_b, player_c, player_d, player_e])

    assert ranked == {
        1: [player_e], 2: [player_c], 3: [player_a, player_b], 4: [player_d]
    }


def test_when_rank_player_hands_and_incomplete_hands_then_return_correct_dict(th_engine, get_test_cards):
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

    ranked = th_engine.rank_player_hands([player_a, player_b, player_c, player_d])

    assert ranked == {
        1: [player_d], 2: [player_c], 3: [player_a], 4: [player_b]
    }


def test_when_find_player_outs_and_bad_hand_type_then_raise_error(th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|SQ"))
    hand_type = TexasHoldemHandType.HighCard
    board = get_test_cards("S7|DT|C2")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    with raises(OutsError, match="Cannot find outs for hand type HighCard, you always have this hand type made"):
        th_engine.find_player_outs(player, hand_type, board, possible_cards)


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_straight_flush")
def test_when_find_player_outs_and_straight_flush_then_correct_calls_made(find_outs_straight_flush, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|SQ"))
    hand_type = TexasHoldemHandType.StraightFlush
    board = get_test_cards("S7|ST|C2")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_straight_flush.assert_called_once_with(get_test_cards("SK|SQ|S7|ST|C2"), possible_cards, 2)
    assert result == find_outs_straight_flush()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_quads")
def test_when_find_player_outs_and_quads_then_correct_calls_made(find_outs_quads, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.Quads
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_quads.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_quads()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_full_house")
def test_when_find_player_outs_and_full_house_then_correct_calls_made(find_outs_full_house, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.FullHouse
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_full_house.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_full_house()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_flush")
def test_when_find_player_outs_and_flush_then_correct_calls_made(find_outs_flush, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.Flush
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_flush.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_flush()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_straight")
def test_when_find_player_outs_and_straight_then_correct_calls_made(find_outs_straight, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.Straight
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_straight.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_straight()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_trips")
def test_when_find_player_outs_and_trips_then_correct_calls_made(find_outs_trips, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.Trips
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_trips.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_trips()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_two_pair")
def test_when_find_player_outs_and_two_pair_then_correct_calls_made(find_outs_two_pair, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.TwoPair
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)

    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_two_pair.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_two_pair()


@patch("pypoker.engine.texas_holdem.find_outs.find_outs_pair")
def test_when_find_player_outs_and_pair_then_correct_calls_made(find_outs_pair, th_engine, get_test_cards, get_deck_minus_set):
    player = HumanPlayer("Matt", hole_cards=get_test_cards("SK|CK"))
    hand_type = TexasHoldemHandType.Pair
    board = get_test_cards("S7|ST|DK")
    possible_cards = get_deck_minus_set(player.hole_cards + board)


    result = th_engine.find_player_outs(player, hand_type, board, possible_cards)

    find_outs_pair.assert_called_once_with(get_test_cards("SK|CK|S7|ST|DK"), possible_cards, 2)
    assert result == find_outs_pair()
