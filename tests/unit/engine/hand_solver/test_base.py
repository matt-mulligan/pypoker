from typing import List, Dict

from pytest import fixture, mark

from fixtures.cards import get_hand, get_hand_sets
from pypoker.deck import Card
from pypoker.engine.hand_solver.base import BaseHandSolver


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
