from typing import List

from pytest import fixture

from pypoker.deck import Card
from pypoker.engine2 import BasePokerEngine
from pypoker.player import BasePlayer


@fixture
def base_engine():
    class FakePokerEngine(BasePokerEngine):

        def find_player_best_hand(self, player: BasePlayer, board: List[Card], **kwargs):
            pass

    return FakePokerEngine()


def test_when_find_consecutive_cards_then_derp(base_engine, get_test_cards):
    cards = get_test_cards("D5|H8|C6|S9|ST")

    result = base_engine.find_consecutive_cards(cards)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == [cards[0], cards[2]]
    assert result[1] == [cards[1], cards[3], cards[4]]
