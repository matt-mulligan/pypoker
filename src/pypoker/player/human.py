from typing import List

from pypoker.constructs import Card, Hand
from pypoker.player import BasePlayer


class HumanPlayer(BasePlayer):
    """Real human implementation of the player base class"""

    def __init__(
        self,
        name: str,
        chips: int = None,
        hole_cards: List[Card] = None,
        table_pos: int = None,
        hand: Hand = None,
    ):
        super().__init__(
            name, chips=chips, hole_cards=hole_cards, table_pos=table_pos, hand=hand
        )
