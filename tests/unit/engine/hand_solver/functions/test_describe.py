from pytest import raises, mark

from fixtures.cards import get_hand
from pypoker.engine.hand_logic.functions import describe_hand


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


@mark.parametrize("hand, expected", [
    ("hand_straight_flush_002", "Straight Flush (Ten to Six)"),
    ("hand_straight_flush_005", "Straight Flush (Ace to Ten)"),
    ("hand_straight_flush_008", "Straight Flush (Five to Ace)"),
])
def test_when_describe_hand_and_texas_holdem_and_straight_flush_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Straight Flush", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_quads_002", "Quads (Queens with Jack kicker)"),
    ("hand_quads_short_001", "Quads (Queens)"),
])
def test_when_describe_hand_and_texas_holdem_and_quads_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Quads", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_full_house_001", "Full House (Nines full of Kings)"),
    ("hand_full_house_003", "Full House (Queens full of Jacks)"),
])
def test_when_describe_hand_and_texas_holdem_and_full_house_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Full House", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_flush_005", "Flush (King, Nine, Eight, Seven, Four)"),
])
def test_when_describe_hand_and_texas_holdem_and_flush_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Flush", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_straight_flush_002", "Straight (Ten to Six)"),
    ("hand_straight_flush_005", "Straight (Ace to Ten)"),
    ("hand_straight_flush_008", "Straight (Five to Ace)"),
])
def test_when_describe_hand_and_texas_holdem_and_straight_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Straight", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_trips_001", "Trips (Kings with kickers Nine, Eight)"),
    ("hand_trips_short_001", "Trips (Kings with kickers Nine)"),
    ("hand_trips_short_002", "Trips (Kings)"),
])
def test_when_describe_hand_and_texas_holdem_and_trips_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Trips", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_two_pair_001", "Two Pair (Nines and Sevens with kicker Ten)"),
    ("hand_two_pair_004", "Two Pair (Nines and Sevens with kicker Six)"),
    ("hand_two_pair_short_001", "Two Pair (Nines and Sevens)"),
])
def test_when_describe_hand_and_texas_holdem_and_two_pair_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Two Pair", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_pair_001", "Pair (Sevens with kickers Ace, Ten, Eight)"),
    ("hand_pair_short_001", "Pair (Sevens with kickers Ace, Ten)"),
    ("hand_pair_short_002", "Pair (Sevens with kickers Ace)"),
    ("hand_pair_short_003", "Pair (Sevens)"),
])
def test_when_describe_hand_and_texas_holdem_and_pair_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "Pair", hand=hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_high_card_001", "High Card (Jack, Nine, Eight, Six, Four)"),
    ("hand_high_card_short_001", "High Card (Jack, Nine, Eight, Six)"),
    ("hand_high_card_short_002", "High Card (Jack, Nine, Eight)"),
    ("hand_high_card_short_003", "High Card (Jack, Nine)"),
    ("hand_high_card_short_004", "High Card (Jack)"),
])
def test_when_describe_hand_and_texas_holdem_and_high_card_then_correct_description_returned(hand, expected):
    hand = get_hand(hand)
    actual = describe_hand("Texas Holdem", "High Card", hand=hand)
    assert actual == expected
