from pytest import raises, mark

from fixtures.cards import get_hand
from pypoker.engine.hand_solver.functions import hand_test


def test_when_hand_test_and_bad_game_type_then_raise_error():
    with raises(ValueError, match="Game type provided 'BAD_GAME_TYPE' is not an acceptable value"):
        hand_test("BAD_GAME_TYPE", "Straight Flush")


def test_when_hand_test_and_bad_hand_type_then_raise_error():
    with raises(ValueError, match="Hand type provided 'WINNING_HAND_TYPE' is not an acceptable value"):
        hand_test("Texas Holdem", "WINNING_HAND_TYPE")


@mark.parametrize("game_type, hand_type, kwargs", [
    ("Texas Holdem", "Straight Flush", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Quads", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Full House", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Flush", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Trips", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Two Pair", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Pair", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "High Card", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight Flush", {}),
    ("Texas Holdem", "Quads", {}),
    ("Texas Holdem", "Full House", {}),
    ("Texas Holdem", "Flush", {}),
    ("Texas Holdem", "Straight", {}),
    ("Texas Holdem", "Trips", {}),
    ("Texas Holdem", "Two Pair", {}),
    ("Texas Holdem", "Pair", {}),
    ("Texas Holdem", "High Card", {})
])
def test_when_hand_test_and_incorrect_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' does not contain all keys required for "
                                  f"this method"):
        hand_test(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, kwargs", [
    ("Texas Holdem", "Straight Flush", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Quads", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Full House", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Flush", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Trips", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Two Pair", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Pair", {"hand": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "High Card", {"hand": "HAND", "DERP": "WHOOPS"}),

])
def test_when_hand_test_and_too_many_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' contains additional keys from what is expected"):
        hand_test(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, hand_name, expected", [
    ("Texas Holdem", "Straight Flush", "hand_straight_flush_001", True),
    ("Texas Holdem", "Straight Flush", "hand_straight_flush_008", True),
    ("Texas Holdem", "Straight Flush", "hand_straight_004", False),
    ("Texas Holdem", "Straight Flush", "hand_flush_004", False),
    ("Texas Holdem", "Quads", "hand_quads_001", True),
    ("Texas Holdem", "Quads", "hand_trips_002", False),
    ("Texas Holdem", "Quads", "hand_two_pair_002", False),
    ("Texas Holdem", "Quads", "hand_full_house_003", False),
    ("Texas Holdem", "Full House", "hand_full_house_002", True),
    ("Texas Holdem", "Full House", "hand_two_pair_001", False),
    ("Texas Holdem", "Full House", "hand_trips_003", False),
    ("Texas Holdem", "Flush", "hand_straight_flush_001", True),
    ("Texas Holdem", "Flush", "hand_flush_001", True),
    ("Texas Holdem", "Flush", "hand_straight_001", False),
    ("Texas Holdem", "Straight", "hand_straight_001", True),
    ("Texas Holdem", "Straight", "hand_straight_flush_002", True),
    ("Texas Holdem", "Straight", "hand_pair_001", False),
    ("Texas Holdem", "Trips", "hand_trips_002", True),
    ("Texas Holdem", "Trips", "hand_full_house_002", True),
    ("Texas Holdem", "Trips", "hand_pair_002", False),
    ("Texas Holdem", "Trips", "hand_two_pair_001", False),
    ("Texas Holdem", "Two Pair", "hand_two_pair_001", True),
    ("Texas Holdem", "Two Pair", "hand_trips_001", False),
    ("Texas Holdem", "Two Pair", "hand_pair_001", False),
    ("Texas Holdem", "Pair", "hand_pair_001", True),
    ("Texas Holdem", "Pair", "hand_two_pair_003", True),
    ("Texas Holdem", "Pair", "hand_trips_003", True),
    ("Texas Holdem", "Pair", "hand_high_card_001", False),
    ("Texas Holdem", "High Card", "hand_high_card_001", True),
])
def test_when_hand_test_then_correct_response_returned(game_type, hand_type, hand_name, expected):
    actual = hand_test(game_type, hand_type, hand=get_hand(hand_name))
    assert actual == expected
