from pytest import raises, mark

from fixtures.cards import get_rank_dictionary, get_hand_sets
from pypoker.engine.hand_solver.functions import rank_hand_type


def test_when_rank_hand_type_and_bad_game_type_then_raise_error():
    with raises(ValueError, match="Game type provided 'BAD_GAME_TYPE' is not an acceptable value"):
        rank_hand_type("BAD_GAME_TYPE", "Straight Flush")


def test_when_rank_hand_type_and_bad_hand_type_then_raise_error():
    with raises(ValueError, match="Hand type provided 'WINNING_HAND_TYPE' is not an acceptable value"):
        rank_hand_type("Texas Holdem", "WINNING_HAND_TYPE")


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
def test_when_rank_hand_type_and_incorrect_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' does not contain all keys required for "
                                  f"this method"):
        rank_hand_type(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, kwargs", [
    ("Texas Holdem", "Straight Flush", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Quads", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Full House", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Flush", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Trips", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Two Pair", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Pair", {"hands": "HAND", "DERP": "WHOOPS"}),
    ("Texas Holdem", "High Card", {"hands": "HAND", "DERP": "WHOOPS"}),

])
def test_when_rank_hand_type_and_too_many_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' contains additional keys from what is expected"):
        rank_hand_type(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, hands, expected", [
    ("Texas Holdem", "Straight Flush", "hand_set_straight_flush_001", "rank_dict_straight_flush_001"),
    ("Texas Holdem", "Quads", "hand_set_quads_001", "rank_dict_quads_001"),
    ("Texas Holdem", "Full House", "hand_set_full_house_001", "rank_dict_full_house_001"),
    ("Texas Holdem", "Flush", "hand_set_flush_001", "rank_dict_flush_001"),
    ("Texas Holdem", "Straight", "hand_set_straight_001", "rank_dict_straight_001"),
    ("Texas Holdem", "Trips", "hand_set_trips_001", "rank_dict_trips_001"),
    ("Texas Holdem", "Two Pair", "hand_set_two_pair_001", "rank_dict_two_pair_001"),
    ("Texas Holdem", "Pair", "hand_set_pair_001", "rank_dict_pair_001"),
    ("Texas Holdem", "High Card", "hand_set_high_card_001", "rank_dict_high_card_001")
])
def test_when_rank_hand_type_then_correct_ranking_returned(game_type, hand_type, hands, expected):
    expected = get_rank_dictionary(expected, build_cards=True)
    hands = get_hand_sets(hands)
    actual = rank_hand_type(game_type, hand_type, hands=hands)
    actual_sorted = {rank: [sorted(hand, reverse=True) for hand in hands] for rank, hands in actual.items()}

    assert actual_sorted == expected
