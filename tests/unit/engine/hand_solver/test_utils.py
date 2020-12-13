from pytest import mark

from fixtures.cards import get_hand, get_hand_sets
from pypoker.engine.hand_logic.utils import hand_all_same_suit, hand_values_continuous, hand_highest_value_tuple, \
    hand_is_ace_low_straight, order_hands_highest_card, hands_have_same_card_values, get_all_combinations


@mark.parametrize("hand, expected", [
    ("hand_0001", True),
    ("hand_0002", False)
])
def test_when_hand_all_same_suit_then_correct_response_returned(hand, expected):
    hand = get_hand(hand)
    actual = hand_all_same_suit(hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_0003", True),
    ("hand_0004", False)
])
def test_when_hand_values_continuous_then_correct_response_returned(hand, expected):
    hand = get_hand(hand)
    actual = hand_values_continuous(hand)
    assert actual == expected


@mark.parametrize("hand_name, tuple_length, expected_tuple_value", [
    ("hand_high_card_001", 1, 11),
    ("hand_pair_001", 1, 14),
    ("hand_two_pair_001", 1, 10),
    ("hand_trips_001", 1, 13),
    ("hand_full_house_001", 1, 13),
    ("hand_quads_001", 1, 12),
    ("hand_high_card_001", 2, None),
    ("hand_pair_001", 2, 7),
    ("hand_two_pair_001", 2, 9),
    ("hand_trips_001", 2, 13),
    ("hand_full_house_001", 2, 13),
    ("hand_quads_001", 2, 4),
    ("hand_high_card_001", 3, None),
    ("hand_pair_001", 3, None),
    ("hand_two_pair_001", 3, None),
    ("hand_trips_001", 3, 13),
    ("hand_full_house_001", 3, 9),
    ("hand_quads_001", 3, 4),
    ("hand_high_card_001", 4, None),
    ("hand_pair_001", 4, None),
    ("hand_two_pair_001", 4, None),
    ("hand_trips_001", 4, None),
    ("hand_full_house_001", 4, None),
    ("hand_quads_001", 4, 4)
])
def test_when_hand_has_value_tuple_then_correct_response_returned(hand_name, tuple_length, expected_tuple_value):
    hand = get_hand(hand_name)
    tuple_value = hand_highest_value_tuple(hand, tuple_length)
    assert tuple_value == expected_tuple_value


@mark.parametrize("hand_name, expected", [
    ("hand_0005", True),
    ("hand_0006", False),
    ("hand_0007", False)
])
def test_when_hand_is_ace_low_straight_then_correct_response_returned(hand_name, expected):
    hand = get_hand(hand_name)
    actual = hand_is_ace_low_straight(hand)
    assert actual == expected


@mark.parametrize("input_hands, expected_hands", [
    ("hand_set_0001", "hand_set_0002"),
])
def test_when_order_hands_highest_card_then_correct_hand_orders_returned(input_hands, expected_hands):
    input_hands = get_hand_sets(input_hands)
    expected_hands = get_hand_sets(expected_hands)

    actual_hands = order_hands_highest_card(input_hands)

    assert actual_hands == expected_hands


@mark.parametrize("hand_a, hand_b, expected", [
    ("hand_straight_flush_001", "hand_straight_flush_005", True),
    ("hand_straight_flush_001", "hand_straight_flush_004", False)
])
def test_when_hands_have_same_card_values_then_correct_response_returned(hand_a, hand_b, expected):
    hand_a = get_hand(hand_a)
    hand_b = get_hand(hand_b)
    actual = hands_have_same_card_values(hand_a, hand_b)

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, hand_size, expected_combos", [
    ("hole_cards_001", "board_cards_001", 5, "combos_001"),
    ("hole_cards_001", "board_cards_002", 5, "combos_002"),
    ("hole_cards_001", "board_cards_003", 5, "combos_003")
])
def test_when_get_all_combinations_then_correct_combinations_returned(hole_cards, board_cards, hand_size,
                                                                      expected_combos):
    hole_cards = get_hand(hole_cards)
    board_cards = get_hand(board_cards)
    expected_combos = get_hand_sets(expected_combos)

    combos = get_all_combinations(hole_cards, board_cards, hand_size)

    assert combos == expected_combos
