import random
from decimal import Decimal
from typing import List, Dict, Any

from pypoker.constructs import Card
from pypoker.engine import find_all_unique_card_combos
from pypoker.player import BasePlayer


def find_player_odds_enumerate(cls: Any, players: List[BasePlayer], board: List[Card], drawable_cards: List[Card]) -> Dict[str, Decimal]:
    """
    find the win percentages for each player by enumerating over each possible draw combination and calculating
    the winner of each.
    """

    draws_remaining = 5 - len(board)
    draw_combos = find_all_unique_card_combos(drawable_cards, draws_remaining)
    return _enumerate_draw_combos(cls, draw_combos, players, board)


def find_player_odds_simulate(cls: Any, players: List[BasePlayer], board: List[Card], drawable_cards: List[Card], sample_size: int) -> Dict[str, Decimal]:
    """
    find the win percentages for each player by processing a random "sample" of games.
    Obviously this method is imprecise and flawed but for pre-flop its an easier cheat method that will do for now.
    """

    draws_remaining = 5 - len(board)
    draw_combos = find_all_unique_card_combos(drawable_cards, draws_remaining)

    sample_size = sample_size if sample_size <= len(draw_combos) else len(draw_combos)
    sampled_draw_combos = random.sample(draw_combos, sample_size)

    return _enumerate_draw_combos(cls, sampled_draw_combos, players, board)


# Private Method Implementations
# -------------------------------
def _enumerate_draw_combos(cls: Any, draw_combos: List[List[Card]], players: List[BasePlayer], board):
    """
    enumerate over the draw combinations and determine win percentages for each player.
    """

    wins = {}
    for draw_combo in draw_combos:
        drawn_out_board = board + draw_combo

        for player in players:
            player.hand = cls.find_player_best_hand(player, drawn_out_board)[0]

        draw_winners = cls.rank_player_hands(players)[1]
        wins = _add_winners_to_win_counter(wins, draw_winners)

    odds = {key: win_count / len(draw_combos) * 100 for key, win_count in wins.items()}

    # add any missing players to odds dict
    for player in players:
        if player.name not in odds.keys():
            odds[player.name] = 0

    return {key: Decimal(f"{odd_pct:.2f}") for key, odd_pct in odds.items()}


def _add_winners_to_win_counter(wins, draw_winners):
    """
    helper method to update the wins dictionary used as part of the calculation of odds.
    """

    winner_id = draw_winners[0].name \
        if len(draw_winners) == 1 \
        else f"TIE({','.join([player.name for player in sorted(draw_winners, key=lambda player: player.name)])})"

    if winner_id in wins.keys():
        wins[winner_id] += 1
    else:
        wins[winner_id] = 1

    return wins