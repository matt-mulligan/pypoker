from typing import List, Dict

from pytest import fixture, mark

from fixtures.cards import get_hand, get_hand_sets
from pypoker.deck import Card
from pypoker.poker_engine.hand_solver.base import BaseHandSolver


@fixture
def base_instance():
    class TestBaseClass(BaseHandSolver):
        def rank_hands(self, hands: Dict[str, List[Card]]):
            pass

        def find_best_hand(self, hole_cards: List[Card], board_cards: List[Card]):
            pass

        def find_odds(self, player_cards: Dict[str, List[Card]], board_cards: List[Card]):
            pass

    return TestBaseClass()


@mark.parametrize("hole_cards, board_cards, hand_size, expected_combos", [
    ("hole_cards_001", "board_cards_001", 5, "combos_001"),
    ("hole_cards_001", "board_cards_002", 5, "combos_002"),
    ("hole_cards_001", "board_cards_003", 5, "combos_003")
])
def test_when_get_all_combinations_then_correct_combinations_returned(hole_cards, board_cards, hand_size,
                                                                      expected_combos, base_instance):
    hole_cards = get_hand(hole_cards)
    board_cards = get_hand(board_cards)
    expected_combos = get_hand_sets(expected_combos)

    combos = base_instance.get_all_combinations(hole_cards, board_cards, hand_size)

    assert combos == expected_combos


@mark.parametrize("hand, expected", [
    ("hand_0001", True),
    ("hand_0002", False)
])
def test_when_hand_all_same_suit_then_correct_response_returned(hand, expected, base_instance):
    hand = get_hand(hand)
    actual = base_instance.hand_all_same_suit(hand)
    assert actual == expected


@mark.parametrize("hand, expected", [
    ("hand_0003", True),
    ("hand_0004", False)
])
def test_when_hand_values_continuous_then_correct_response_returned(hand, expected, base_instance):
    hand = get_hand(hand)
    actual = base_instance.hand_values_continuous(hand)
    assert actual == expected


@mark.parametrize("input_hands, expected_hands", [
    ("hand_set_0001", "hand_set_0002"),
])
def test_when_order_hands_highest_card_then_correct_hand_orders_returned(input_hands, expected_hands, base_instance):
    input_hands = get_hand_sets(input_hands)
    expected_hands = get_hand_sets(expected_hands)

    actual_hands = base_instance.order_hands_highest_card(input_hands)

    assert actual_hands == expected_hands


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
def test_when_hand_has_value_tuple_then_correct_response_returned(hand_name, tuple_length, expected_tuple_value,
                                                                  base_instance):
    hand = get_hand(hand_name)
    tuple_value = base_instance.hand_highest_value_tuple(hand, tuple_length)
    assert tuple_value == expected_tuple_value
