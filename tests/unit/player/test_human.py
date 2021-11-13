from pypoker.deck import Card
from pypoker.player.human import HumanPlayer


def test_when_human_player_created_then_values_set_correctly():
    player = HumanPlayer(
        "Matt", chips=10000, hole_cards=[Card("S4"), Card("S9")], table_pos=7
    )

    assert player.name == "Matt"
    assert player.chips == 10000
    assert player.hole_cards == [Card("S4"), Card("S9")]
    assert player.table_pos == 7
