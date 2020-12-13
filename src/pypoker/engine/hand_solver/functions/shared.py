"""
Shared functionality used by all of the function modules
"""

from pypoker.engine.hand_solver.constants import (
    GAME_TYPES,
    GAME_TYPE_TEXAS_HOLDEM,
    TEXAS_HOLDEM_HAND_TYPES,
)


def _check_game_type(game_type):
    if game_type not in GAME_TYPES:
        raise ValueError(
            f"Game type provided '{game_type}' is not an acceptable value: '{GAME_TYPES}'"
        )


def _check_hand_type(game_type, hand_type):
    hand_types = {GAME_TYPE_TEXAS_HOLDEM: TEXAS_HOLDEM_HAND_TYPES}[game_type]

    if hand_type not in hand_types:
        raise ValueError(
            f"Hand type provided '{hand_type}' is not an acceptable value: '{hand_types}'"
        )


def _check_kwargs(kwargs, kwargs_required_keys):
    if not all(
        [required_key in kwargs.keys() for required_key in kwargs_required_keys]
    ):
        raise ValueError(
            f"Kwargs object '{kwargs}' does not contain all keys "
            f"required for this method '{kwargs_required_keys}'"
        )

    if len(kwargs.keys()) != len(kwargs_required_keys):
        raise ValueError(
            f"Kwargs object '{kwargs}' contains additional keys from what is "
            f"expected for this method '{kwargs_required_keys}'"
        )
