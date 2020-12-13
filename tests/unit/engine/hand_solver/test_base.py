from typing import List, Dict

from pytest import fixture, mark

from fixtures.cards import get_hand, get_hand_sets
from pypoker.deck import Card
from pypoker.engine.hand_logic.base import BaseHandSolver


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
