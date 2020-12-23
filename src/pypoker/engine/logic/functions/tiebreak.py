"""
FUNCTIONS.TIEBREAK MODULE

This module provides a public method to allow hands of the same type to be tiebroken/ranked
"""
from collections import Counter
from typing import List, Dict

from pypoker.deck import Card
from pypoker.engine.logic.constants import GAME_TYPE_TEXAS_HOLDEM, HAND_TYPE_STRAIGHT_FLUSH, HAND_TYPE_QUADS, \
    HAND_TYPE_FULL_HOUSE, HAND_TYPE_FLUSH, HAND_TYPE_STRAIGHT, HAND_TYPE_TRIPS, HAND_TYPE_TWO_PAIR, HAND_TYPE_PAIR, \
    HAND_TYPE_HIGH_CARD, OUT_STRING
from pypoker.engine.logic.functions.outs import get_all_combinations_for_out_string
from pypoker.engine.logic.functions.shared import _check_game_type, _check_hand_type, _check_kwargs


####################
#  PUBLIC METHODS  #
####################
def tiebreak_hands(game_type: str, hand_type: str, hands: List[List[Card]]) -> List[Dict]:
    """
    This public method is used to tiebreak and rank hands of the same type.

    :param game_type: the type of poker game that is being played
    :param hand_type: the type of hand that we are tiebreaking
    :param hands:  list of list of cards representing the hands
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    tb_key = f"{game_type}-{hand_type}"

    tb_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}": _tiebreak_texas_holdem_straight,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}": _tiebreak_texas_holdem_quads,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}": _tiebreak_texas_holdem_full_house,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}": _tiebreak_texas_holdem_flush,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}": _tiebreak_texas_holdem_straight,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}": _tiebreak_texas_holdem_trips,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}": _tiebreak_texas_holdem_two_pair,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}": _tiebreak_texas_holdem_pair,
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}": _tiebreak_texas_holdem_flush,
    }[tb_key]

    return tb_method(hands)


def tiebreak_out_scenarios(game_type: str, hand_type: str, **kwargs) -> List[Dict]:
    """
    This public method is used to tiebreak out scenarios for a specific hand type.

    :param game_type: the type of poker game that is being played
    :param hand_type: the type of hand that we are tiebreaking
    :param kwargs: set of kwargs required for the specific tiebreak method
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    tb_key = f"{game_type}-{hand_type}"

    kwargs_required_tb, tb_scenario_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_straight_flush,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_quads,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_full_house,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_flush,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_straight,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_trips,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_two_pair,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_pair,
        ),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}": (
            ["player_out_scenarios", "drawable_cards", "assigned_draws"],
            _tb_out_scenarios_high_flush,
        ),
    }[tb_key]

    _check_kwargs(kwargs, kwargs_required_tb)
    return tb_scenario_method(**kwargs)


#####################################################
#  PRIVATE IMPLEMENTATION METHODS - TIEBREAK HANDS  #
#####################################################
def _tiebreak_texas_holdem_straight(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem straight flush hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    hands = [sorted(hand, reverse=True, key=lambda card: card.value) for hand in hands]

    a5_straights = [hand for hand in hands if[card.value for card in hand] == [14, 5, 4, 3, 2]]
    other_straights = [hand for hand in hands if hand not in a5_straights]

    tb_primaries = [max([card.value for card in hand]) for hand in other_straights]
    tb_primaries = sorted(list(set(tb_primaries)), reverse=True)

    rank = 1
    ranked_hands = []
    for tb_primary in tb_primaries:
        ranked_hands.append({
            "rank": rank,
            "hands": [hand for hand in other_straights if max([card.value for card in hand]) == tb_primary],
            "tb_primary": tb_primary,
            "tb_secondary": None
        })
        rank += 1

    if a5_straights:
        ranked_hands.append({"rank": rank, "hands": a5_straights, "tb_primary": 5, "tb_secondary": None})

    return ranked_hands


def _tiebreak_texas_holdem_quads(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem quads hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    counters = [(sorted(hand, reverse=True), Counter([card.value for card in hand])) for hand in hands]

    tiebreakers = [
        (
            counter[0],
            [key for key, count in counter[1].items() if count == 4][0],
            [key for key, count in counter[1].items() if count == 1]
        ) for counter in counters
    ]

    sorted_tiebreakers = sorted(list(set([(tb[1], *tb[2]) for tb in tiebreakers])), reverse=True)

    rank = 1
    ranked_hands = []
    for sorted_tb in sorted_tiebreakers:
        primary_tb = sorted_tb[0]
        secondary_tb = list(sorted_tb[1:])
        ranked_hands.append({
            "rank": rank,
            "hands": [tb[0] for tb in tiebreakers if tb[1] == primary_tb and tb[2] == secondary_tb],
            "tb_primary": primary_tb,
            "tb_secondary": secondary_tb[0] if secondary_tb else None
        })
        rank += 1

    return ranked_hands


def _tiebreak_texas_holdem_full_house(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem full house hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    counters = [(sorted(hand, reverse=True), Counter([card.value for card in hand])) for hand in hands]

    tiebreakers = [
        (
            counter[0],
            [key for key, count in counter[1].items() if count == 3][0],
            [key for key, count in counter[1].items() if count == 2][0]
        ) for counter in counters
    ]

    sorted_tiebreakers = sorted(list(set([(tb[1], tb[2]) for tb in tiebreakers])), reverse=True)

    rank = 1
    ranked_hands = []
    for trip, pair in sorted_tiebreakers:
        ranked_hands.append({
            "rank": rank,
            "hands": [tb[0] for tb in tiebreakers if tb[1] == trip and tb[2] == pair],
            "tb_primary": (trip, pair),
            "tb_secondary": None
        })
        rank += 1

    return ranked_hands


def _tiebreak_texas_holdem_flush(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem flush hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    hands = [sorted(hand, reverse=True, key=lambda card: card.value) for hand in hands]
    tiebreakers = [(hand, [card.value for card in hand]) for hand in hands]

    sorted_tiebreakers = [(*tb[1], ) for tb in tiebreakers]
    sorted_tiebreakers = list(set(sorted_tiebreakers))
    sorted_tiebreakers = sorted(sorted_tiebreakers, reverse=True)

    rank = 1
    ranked_hands = []
    for tb_primary in sorted_tiebreakers:
        tb_primary = list(tb_primary)
        ranked_hands.append({
            "rank": rank,
            "hands": [tb[0] for tb in tiebreakers if tb[1] == tb_primary],
            "tb_primary": tb_primary,
            "tb_secondary": None
        })
        rank += 1

    return ranked_hands


def _tiebreak_texas_holdem_trips(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem trips hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    counters = [(sorted(hand, reverse=True), Counter([card.value for card in hand])) for hand in hands]

    tiebreakers = [
        (
            counter[0],
            [key for key, count in counter[1].items() if count == 3][0],
            sorted([key for key, count in counter[1].items() if count != 3], reverse=True)
        ) for counter in counters
    ]

    sorted_tiebreakers = sorted(list(set([(tb[1], *tb[2]) for tb in tiebreakers])), reverse=True)

    rank = 1
    ranked_hands = []
    for tiebreak_values in sorted_tiebreakers:
        trip = tiebreak_values[0]
        kickers = list(tiebreak_values[1:])
        ranked_hands.append({
            "rank": rank,
            "hands": [tb[0] for tb in tiebreakers if tb[1] == trip and tb[2] == kickers],
            "tb_primary": trip,
            "tb_secondary": kickers
        })
        rank += 1

    return ranked_hands


def _tiebreak_texas_holdem_two_pair(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem two pair hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    counters = [(sorted(hand, reverse=True), Counter([card.value for card in hand])) for hand in hands]

    tiebreakers = [
        (
            counter[0],
            sorted([key for key, count in counter[1].items() if count == 2], reverse=True),
            [key for key, count in counter[1].items() if count != 2]
        ) for counter in counters
    ]

    sorted_tiebreakers = sorted(list(set([(*tb[1], *tb[2]) for tb in tiebreakers])), reverse=True)

    rank = 1
    ranked_hands = []
    for tiebreak_values in sorted_tiebreakers:
        pairs = list(tiebreak_values[:2])
        kickers = list(tiebreak_values[2:])
        ranked_hands.append({
            "rank": rank,
            "hands": [tb[0] for tb in tiebreakers if tb[1] == pairs and tb[2] == kickers],
            "tb_primary": pairs,
            "tb_secondary": None if not kickers else kickers[0]
        })
        rank += 1

    return ranked_hands


def _tiebreak_texas_holdem_pair(hands: List[List[Card]]) -> List[Dict]:
    """
    private method to tiebreak texas holdem pair hands

    :param hands: List of List of Card types representing the hands to be tiebroken
    :return: List of dictionaries representing each ranking found. dictionaries will be in the format of:
        {"rank": rank_num, "hands": list_of_hands, "tb_primary": primary_tb_info, "tb"secondary": secondary_tb_info}
    """

    counters = [(sorted(hand, reverse=True), Counter([card.value for card in hand])) for hand in hands]

    tiebreakers = [
        (
            counter[0],
            [key for key, count in counter[1].items() if count == 2][0],
            sorted([key for key, count in counter[1].items() if count != 2], reverse=True)
        ) for counter in counters
    ]

    sorted_tiebreakers = sorted(list(set([(tb[1], *tb[2]) for tb in tiebreakers])), reverse=True)

    rank = 1
    ranked_hands = []
    for tiebreak_values in sorted_tiebreakers:
        pair = tiebreak_values[0]
        kickers = list(tiebreak_values[1:])
        ranked_hands.append({
            "rank": rank,
            "hands": [tb[0] for tb in tiebreakers if tb[1] == pair and tb[2] == kickers],
            "tb_primary": pair,
            "tb_secondary": kickers
        })
        rank += 1

    return ranked_hands


#####################################################
#  PRIVATE IMPLEMENTATION METHODS - TIEBREAK HANDS  #
#####################################################
def _tb_out_scenarios_straight_flush(player_out_scenarios, drawable_cards, assigned_draws):
    """
    private method to tiebreak straight flush out scenarios and award draws to players

    :param player_out_scenarios: Dict of each players out scenarios in the structure
        {
            "PLAYER_A": [
                {"out_string": ...}, {"out_string": ...}
            ],
            "PLAYER_B": [
                {"out_string": ...}, {"out_string": ...}
            ],
        }
    :param drawable_cards: List of card objects still available
    :param assigned_draws: List of draw strings that have already been assigned
    :return: Dict of players and their assigned wins for these outs
    """

    # dictionary for all new outs for each player
    player_assigned_draws = {player: [] for player in player_out_scenarios.keys()}

    for tb_high_card in [14, 13, 12, 11, 10, 9, 8, 7, 6, 5]:
        players_out_strings = {
            player: [
                scenario[OUT_STRING] for scenario in out_scenarios
                if scenario["TB_STRAIGHT_HIGH_CARD"] == tb_high_card
            ] for player, out_scenarios in player_out_scenarios.items()
        }

        players_with_outs = [player for player, out_strings in players_out_strings.items() if out_strings]

        if not players_with_outs:
            continue

        if len(players_with_outs) == 1:
            player = players_with_outs[0]
            out_draws = [
                get_all_combinations_for_out_string(assigned_draws, out_string, drawable_cards)
                for out_string in players_out_strings[player]
            ]
            out_draws = [item for sublist in out_draws for item in sublist]
            out_draws = list(set(out_draws))

            player_assigned_draws[player].extend(out_draws)
            assigned_draws.extend(out_draws)
        else:
            player_out_draws = dict()
            for player in players_with_outs:
                out_draws = [
                    get_all_combinations_for_out_string(assigned_draws, out_string, drawable_cards)
                    for out_string in players_out_strings[player]
                ]
                out_draws = [item for sublist in out_draws for item in sublist]
                out_draws = list(set(out_draws))
                player_out_draws[player] = out_draws

            for player, out_draws in player_out_draws.items():
                my_draws = [draw for draw in out_draws if draw not in assigned_draws]
                their_draws = [out_draw for other_player, out_draw in player_out_draws.items() if other_player != player]
                their_draws = [item for sublist in their_draws for item in sublist]

                unique_draws = [draw for draw in my_draws if draw not in their_draws]
                shared_draws = [draw for draw in my_draws if draw not in unique_draws]

                player_assigned_draws[player].extend(unique_draws)
                assigned_draws.extend(out_draws)

                for draw in shared_draws:
                    shared_draw_players = [player for player, draws in player_out_draws.items() if draw in draws]
                    name = f"TIE({','.join(shared_draw_players)})"
                    if name in player_assigned_draws.keys():
                        player_assigned_draws[name].append(draw)
                    else:
                        player_assigned_draws[name] = [draw]
                    assigned_draws.append(draw)

    return player_assigned_draws
