##############
#  Fixtures  #
##############
from pytest import mark

from fixtures.cards import get_hand_sets, get_tiebreaker_dicts
from pypoker.engine.logic.functions import tiebreak_hands


@mark.parametrize("scenario", [
    "tiebreak_straight_flush_001", "tiebreak_straight_flush_002", "tiebreak_straight_flush_003"
])
def test_when_tiebreak_hands_and_texas_holdem_and_straight_flush_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Straight Flush", hands)

    assert actual == expected


@mark.parametrize("scenario", ["tiebreak_quads_001", "tiebreak_quads_002", "tiebreak_quads_003", "tiebreak_quads_004"])
def test_when_tiebreak_hands_and_texas_holdem_and_quads_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Quads", hands)

    assert actual == expected


@mark.parametrize("scenario", ["tiebreak_full_house_001", "tiebreak_full_house_002"])
def test_when_tiebreak_hands_and_texas_holdem_and_full_house_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Full House", hands)

    assert actual == expected


@mark.parametrize("scenario", ["tiebreak_flush_001", "tiebreak_flush_002"])
def test_when_tiebreak_hands_and_texas_holdem_and_flush_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Flush", hands)

    assert actual == expected


@mark.parametrize("scenario", ["tiebreak_straight_001", "tiebreak_straight_002"])
def test_when_tiebreak_hands_and_texas_holdem_and_straight_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Straight", hands)

    assert actual == expected


@mark.parametrize("scenario", ["tiebreak_trips_001", "tiebreak_trips_002", "tiebreak_trips_003", "tiebreak_trips_004"])
def test_when_tiebreak_hands_and_texas_holdem_and_trips_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Trips", hands)

    assert actual == expected


@mark.parametrize("scenario", ["tiebreak_two_pair_001", "tiebreak_two_pair_002", "tiebreak_two_pair_003"])
def test_when_tiebreak_hands_and_texas_holdem_and_two_pair_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Two Pair", hands)

    assert actual == expected


@mark.parametrize("scenario", [
    "tiebreak_pair_001", "tiebreak_pair_002", "tiebreak_pair_003", "tiebreak_pair_004", "tiebreak_pair_005"
])
def test_when_tiebreak_hands_and_texas_holdem_and_pair_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "Pair", hands)

    assert actual == expected


@mark.parametrize("scenario", [
    "tiebreak_high_card_001", "tiebreak_high_card_002", "tiebreak_high_card_003", "tiebreak_high_card_004",
    "tiebreak_high_card_005", "tiebreak_high_card_006",
])
def test_when_tiebreak_hands_and_texas_holdem_and_high_card_then_correct_dict_returned(scenario):
    hands = get_hand_sets(scenario)
    expected = get_tiebreaker_dicts(scenario)
    actual = tiebreak_hands("Texas Holdem", "High Card", hands)

    assert actual == expected