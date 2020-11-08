from dataclasses import dataclass, field
from typing import List

from pypoker.deck import Card


@dataclass()
class Player(object):
    """
    Base Player Class for PyPoker
    """

    name: str
    chips: int
    hole_cards: List[Card] = field(init=False, default_factory=list)
    best_hand_type: str = field(init=False, default=None)
    best_hand_cards: List[Card] = field(init=False, default_factory=list)
