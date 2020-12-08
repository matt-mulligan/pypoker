from pytest import raises, mark

from fixtures.cards import get_hand
from pypoker.engine.hand_solver.functions import describe_hand


def test_when_describe_hand_and_bad_game_type_then_raise_error():
    with raises(ValueError, match="Game type provided 'BAD_GAME_TYPE' is not an acceptable value"):
        describe_hand("BAD_GAME_TYPE", "Straight Flush")


def test_when_describe_hand_and_bad_hand_type_then_raise_error():
    with raises(ValueError, match="Hand type provided 'WINNING_HAND_TYPE' is not an acceptable value"):
        describe_hand("Texas Holdem", "WINNING_HAND_TYPE")


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
def test_when_describe_hand_and_incorrect_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' does not contain all keys required for "
                                  f"this method"):
        describe_hand(game_type, hand_type, **kwargs)


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
def test_when_describe_hand_and_too_many_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' contains additional keys from what is expected"):
        describe_hand(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, hand, expected", [
    ("Texas Holdem", "Straight Flush", "hand_straight_flush_002", "Straight Flush (Ten to Six)"),
    ("Texas Holdem", "Straight Flush", "hand_straight_flush_005", "Straight Flush (Ace to Ten)"),
    ("Texas Holdem", "Straight Flush", "hand_straight_flush_008", "Straight Flush (Five to Ace)"),
    ("Texas Holdem", "Quads", "hand_quads_002", "Quads (Queens with Jack kicker)"),
    ("Texas Holdem", "Quads", "hand_quads_short_001", "Quads (Queens)"),
    ("Texas Holdem", "Full House", "hand_full_house_001", "Full House (Nines full of Kings)"),
    ("Texas Holdem", "Full House", "hand_full_house_003", "Full House (Queens full of Jacks)"),
    ("Texas Holdem", "Flush", "hand_flush_005", "Flush (King, Nine, Eight, Seven, Four)"),
    ("Texas Holdem", "Straight", "hand_straight_flush_002", "Straight (Ten to Six)"),
    ("Texas Holdem", "Straight", "hand_straight_flush_005", "Straight (Ace to Ten)"),
    ("Texas Holdem", "Straight", "hand_straight_flush_008", "Straight (Five to Ace)"),
    ("Texas Holdem", "Trips", "hand_trips_001", "Trips (Kings with kickers Nine, Eight)"),
    ("Texas Holdem", "Trips", "hand_trips_short_001", "Trips (Kings with kickers Nine)"),
    ("Texas Holdem", "Trips", "hand_trips_short_002", "Trips (Kings)"),
    ("Texas Holdem", "Two Pair", "hand_two_pair_001", "Two Pair (Nines and Sevens with kicker Ten)"),
    ("Texas Holdem", "Two Pair", "hand_two_pair_004", "Two Pair (Nines and Sevens with kicker Six)"),
    ("Texas Holdem", "Two Pair", "hand_two_pair_short_001", "Two Pair (Nines and Sevens)"),
    ("Texas Holdem", "Pair", "hand_pair_001", "Pair (Sevens with kickers Ace, Ten, Eight)"),
    ("Texas Holdem", "Pair", "hand_pair_short_001", "Pair (Sevens with kickers Ace, Ten)"),
    ("Texas Holdem", "Pair", "hand_pair_short_002", "Pair (Sevens with kickers Ace)"),
    ("Texas Holdem", "Pair", "hand_pair_short_003", "Pair (Sevens)"),
    ("Texas Holdem", "High Card", "hand_high_card_001", "High Card (Jack, Nine, Eight, Six, Four)"),
    ("Texas Holdem", "High Card", "hand_high_card_short_001", "High Card (Jack, Nine, Eight, Six)"),
    ("Texas Holdem", "High Card", "hand_high_card_short_002", "High Card (Jack, Nine, Eight)"),
    ("Texas Holdem", "High Card", "hand_high_card_short_003", "High Card (Jack, Nine)"),
    ("Texas Holdem", "High Card", "hand_high_card_short_004", "High Card (Jack)"),
])
def test_when_describe_hand_then_correct_description_returned(game_type, hand_type, hand, expected):
    hand = get_hand(hand)
    actual = describe_hand(game_type, hand_type, hand=hand)
    assert actual == expected
