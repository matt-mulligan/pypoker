"""
FUNCTIONS.OUTS MODULE

this module contains the implementation of all outs scenario evaluation and outs tiebreaker logic
This module also contains some public methods to assist in building out-strings and claiming the card combinations that
are represented by an out-string
"""
from collections import Counter
from itertools import product, groupby, combinations
from typing import List, Dict

from pypoker.deck import Card
from pypoker.engine.hand_solver.constants import GAME_TYPE_TEXAS_HOLDEM, HAND_TYPE_STRAIGHT_FLUSH, \
    HAND_TYPE_QUADS, HAND_TYPE_FULL_HOUSE, HAND_TYPE_FLUSH, HAND_TYPE_STRAIGHT, HAND_TYPE_TRIPS, HAND_TYPE_TWO_PAIR, \
    HAND_TYPE_PAIR, HAND_TYPE_HIGH_CARD, SUIT_HEARTS, SUIT_CLUBS, SUIT_DIAMONDS, SUIT_SPADES, OUT_STRING, TIEBREAKER, \
    CARD_VALUES
from pypoker.engine.hand_solver.functions.shared import _check_game_type, _check_hand_type, _check_kwargs
from pypoker.engine.hand_solver.utils import get_all_combinations


####################
#  PUBLIC METHODS  #
####################
def find_outs_scenarios(game_type: str, hand_type: str, **kwargs: Dict) -> str:
    """
    Public method to find any outs sceanrios that are possible for the given hand and the given hand type

    :param game_type: indicates what type of poker game you are playing. Tested against constants.GAME_TYPES
    :param hand_type: indicates the hand type you are testing for. Tested against constants.<GAME_TYPE>_HAND_TYPES
    :param kwargs: Unbounded keyword arguments list required for the implementation of the rank_hand_type method you
                   are using. Arguments passed to this command are be validated before calling underlying implementation
    :return: List of possible draw scenarios that would give the player this hand type.
             Dictionary in the following format:
                OUT_STRING: string value representing the cards required to be drawn for this scenario
                TIEBREAKER: data to be utilised by the outs_tiebreaker methods to determine which draw is stronger

    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    outs_key = f"{game_type}-{hand_type}"

    kwargs_required_keys, describe_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}":
            (["hole_cards", "board_cards", "available_cards"], _outs_straight_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}":
            (["hole_cards", "board_cards", "available_cards"], _outs_quads),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}":
            (["hole_cards", "board_cards", "available_cards"], _outs_full_house),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}":
            (["hole_cards", "board_cards", "available_cards"], _outs_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}":
            (["hole_cards", "board_cards", "available_cards"], _outs_straight),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}":
            (["hole_cards", "board_cards", "available_cards"], _outs_trips),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}":
            (["hole_cards", "board_cards", "available_cards"], _outs_two_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}":
            (["hole_cards", "board_cards", "available_cards"], _outs_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}":
            (["hole_cards", "board_cards", "available_cards"], _outs_high_card),
    }[outs_key]

    _check_kwargs(kwargs, kwargs_required_keys)
    return describe_method(**kwargs)


def build_out_string(suits: List[str], values: List[int], draws: int) -> str:
    """
    THis public shared method will produce a list of out strings, that represent what cards can be drawn to give
    the player an out.

    THe composition of these strings are very important and follow the below rules:
         - Out strings will contain an entry for each card that is yet to be drawn
         - Out strings will seperate card entries with a dash (-)
         - Out string card entries will have the first character represent the suit (S,C,D,H)
         - Out string card entries will have the second characters represent the value of the card (2,3,4,5,6,7,8,9,T,J,Q,K,A)
         - if a value is unimportant then it can use a wildcard (*) to represent ANY value.
         - a card that isnt required (e.g. the second card in a one card out) will be represented by **

     :param suits: List of suits for each draw card required e.g. ["Hearts", "Hearts"
     :param values: List of values for each card required (ANY used for wildcard e.g. [4, 14]
     :param draws: Int representing total cards yet to be drawn
    """

    out_string_parts = []

    for index in range(draws):
        suit = "*"
        value = "*"

        if index < len(suits):
            suit = {
                "Hearts": "H",
                "Diamonds": "D",
                "Clubs": "C",
                "Spades": "S",
                "ANY": "*",
            }[suits[index]]

            value = {
                2: "2",
                3: "3",
                4: "4",
                5: "5",
                6: "6",
                7: "7",
                8: "8",
                9: "9",
                10: "T",
                11: "J",
                12: "Q",
                13: "K",
                14: "A",
                "ANY": "*",
            }[values[index]]

        out_string_parts.append(f"{suit}{value}")

    return "-".join(out_string_parts)


def claim_out_strings(utilised_outs: List[str], out_strings: List[str], drawable_cards: List[Card]) -> List[str]:
    """
    Public method to claim all possible out combinations for the cards given

    :param utilised_outs: List of out strings that have already been claimed
    :param out_strings: List of out strings that we want to assess for claiming
    :param drawable_cards: List of card objects representing all of the cards yet to be drawn
    """

    test_outs = utilised_outs.copy()
    claimed_outs = []

    for out in out_strings:
        combos = _create_combos_for_out_string(out, drawable_cards)
        combos = [combo for combo in combos if combo not in test_outs]
        test_outs.extend(combos)
        claimed_outs.extend(combos)

    return claimed_outs


###################################################
#  PRIVATE IMPLEMENTATION METHODS - TEXAS HOLDEM  #
###################################################
def _outs_straight_flush(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    :return: List of possible draw scenarios that would give the player this hand type.
             Dictionary in the following format:
                OUT_STRING: string value representing the cards required to be drawn for this scenario
                TIEBREAKER: data to be utilised by the outs_tiebreaker methods to determine which draw is stronger
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards
    suit_drawn = {
        SUIT_HEARTS: sum([1 for card in drawn_cards if card.suit == SUIT_HEARTS]),
        SUIT_CLUBS: sum([1 for card in drawn_cards if card.suit == SUIT_CLUBS]),
        SUIT_DIAMONDS: sum([1 for card in drawn_cards if card.suit == SUIT_DIAMONDS]),
        SUIT_SPADES: sum([1 for card in drawn_cards if card.suit == SUIT_SPADES]),
    }
    suit_remaining = {
        SUIT_HEARTS: sum(
            [1 for card in available_cards if card.suit == SUIT_HEARTS]
        ),
        SUIT_CLUBS: sum([1 for card in available_cards if card.suit == SUIT_CLUBS]),
        SUIT_DIAMONDS: sum(
            [1 for card in available_cards if card.suit == SUIT_DIAMONDS]
        ),
        SUIT_SPADES: sum(
            [1 for card in available_cards if card.suit == SUIT_SPADES]
        ),
    }

    suit_eligable = [
        suit
        for suit, count in suit_drawn.items()
        if count + draws >= 5 and suit_remaining[suit] >= (5 - count)
    ]

    for suit in suit_eligable:
        drawn_suit_cards = [card for card in drawn_cards if card.suit == suit]
        available_suit_cards = [
            card for card in available_cards if card.suit == suit
        ]

        drawn_suit_cards = sorted(
            drawn_suit_cards, key=lambda card: card.value, reverse=True
        )
        available_suit_cards = sorted(
            available_suit_cards, key=lambda card: card.value, reverse=True
        )

        for draws_used in range(1, draws + 1):
            for hypothetical_draw_cards in get_all_combinations(
                available_suit_cards, [], draws_used
            ):
                usable_cards = drawn_suit_cards + hypothetical_draw_cards
                usable_card_vals = [card.value for card in usable_cards]
                usable_card_vals.sort()

                gaps = [
                    [s, e]
                    for s, e in zip(usable_card_vals, usable_card_vals[1:])
                    if s + 1 < e
                ]
                edges = iter(
                    usable_card_vals[:1] + sum(gaps, []) + usable_card_vals[-1:]
                )
                runs = list(zip(edges, edges))

                qualifying_straights = [
                    run
                    for run in runs
                    if run[1] - run[0] >= 4
                    and all(
                        (run[1] - 4) <= card.value <= run[1]
                        for card in hypothetical_draw_cards
                    )
                ]

                for straight_vals in qualifying_straights:
                    suits = []
                    values = []
                    for card in hypothetical_draw_cards:
                        suits.append(card.suit)
                        values.append(card.value)
                    draw_scenarios.append(
                        {
                            OUT_STRING: build_out_string(suits, values, draws),
                            TIEBREAKER: straight_vals[1],
                        }
                    )

    return draw_scenarios


def _outs_quads(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards

    drawn_value_counter = Counter([card.value for card in drawn_cards])
    available_values_counter = Counter([card.value for card in available_cards])
    value_eligable = [
        value
        for value, count in drawn_value_counter.items()
        if count + draws >= 4 and available_values_counter[value] + value >= 4
    ]

    for value in value_eligable:
        cards_needed = 4 - drawn_value_counter[value]
        suits = ["ANY" for _ in range(cards_needed)]
        values = [value for _ in range(cards_needed)]

        draw_scenarios.append(
            {
                OUT_STRING: build_out_string(suits, values, draws),
                TIEBREAKER: value,
            }
        )

    return draw_scenarios


def _outs_full_house(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards

    drawn_value_counter = Counter([card.value for card in drawn_cards])
    available_values_counter = Counter([card.value for card in available_cards])

    trips_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 3
        and available_values_counter[value] + drawn_value_counter[value] >= 3
    ]

    pair_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 2
        and available_values_counter[value] + drawn_value_counter[value] >= 2
    ]

    for trip_info, pair_info in product(trips_eligable, pair_eligable):
        # check we havent selected the same value for both trips and pairs
        if trip_info[0] == pair_info[0]:
            continue

        trip_draws_required = max([3 - trip_info[1], 0])
        pair_draws_required = max([2 - pair_info[1], 0])

        if trip_draws_required + pair_draws_required > draws:
            continue

        suits = ["ANY" for _ in range(trip_draws_required + pair_draws_required)]
        values = [trip_info[0] for _ in range(trip_draws_required)]
        values.extend([pair_info[0] for _ in range(pair_draws_required)])

        draw_scenarios.append(
            {
                OUT_STRING: build_out_string(suits, values, draws),
                TIEBREAKER: (trip_info[0], pair_info[0]),
            }
        )
    return draw_scenarios


def _outs_flush(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards
    suit_drawn = {
        SUIT_HEARTS: sum([1 for card in drawn_cards if card.suit == SUIT_HEARTS]),
        SUIT_CLUBS: sum([1 for card in drawn_cards if card.suit == SUIT_CLUBS]),
        SUIT_DIAMONDS: sum(
            [1 for card in drawn_cards if card.suit == SUIT_DIAMONDS]
        ),
        SUIT_SPADES: sum([1 for card in drawn_cards if card.suit == SUIT_SPADES]),
    }
    suit_remaining = {
        SUIT_HEARTS: sum(
            [1 for card in available_cards if card.suit == SUIT_HEARTS]
        ),
        SUIT_CLUBS: sum([1 for card in available_cards if card.suit == SUIT_CLUBS]),
        SUIT_DIAMONDS: sum(
            [1 for card in available_cards if card.suit == SUIT_DIAMONDS]
        ),
        SUIT_SPADES: sum(
            [1 for card in available_cards if card.suit == SUIT_SPADES]
        ),
    }

    suit_eligable = [
        suit
        for suit, count in suit_drawn.items()
        if count + draws >= 5 and suit_remaining[suit] >= (5 - count)
    ]

    for suit in suit_eligable:
        draws_required = max([5 - suit_drawn[suit], 0])
        suits = [suit for _ in range(draws_required)]
        values = ["ANY" for _ in range(draws_required)]

        draw_scenarios.append(
            {
                OUT_STRING: build_out_string(suits, values, draws),
                TIEBREAKER: suit,
            }
        )

    return draw_scenarios


def _outs_straight(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards

    drawn_values = sorted(
        list(set([card.value for card in drawn_cards])), reverse=True
    )
    available_values = sorted(
        list(set([card.value for card in available_cards])), reverse=True
    )
    not_drawn_values = [
        value for value in available_values if value not in drawn_values
    ]

    for draws_used in range(1, draws + 1):
        for possible_draw in combinations(not_drawn_values, draws_used):
            combined_values = sorted(drawn_values + list(possible_draw))

            gaps = [
                [s, e]
                for s, e in zip(combined_values, combined_values[1:])
                if s + 1 < e
            ]
            edges = iter(combined_values[:1] + sum(gaps, []) + combined_values[-1:])
            runs = list(zip(edges, edges))

            qualifying_straights = [
                run
                for run in runs
                if run[1] - run[0] >= 4
                and all((run[1] - 4) <= value <= run[1] for value in possible_draw)
            ]

            for straight_vals in qualifying_straights:
                suits = ["ANY" for _ in possible_draw]
                values = [value for value in possible_draw]
                draw_scenarios.append(
                    {
                        OUT_STRING: build_out_string(suits, values, draws),
                        TIEBREAKER: straight_vals[1],
                    }
                )
    return draw_scenarios


def _outs_trips(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards

    drawn_value_counter = Counter([card.value for card in drawn_cards])
    available_values_counter = Counter([card.value for card in available_cards])

    trips_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 3
        and available_values_counter[value] + drawn_value_counter[value] >= 3
    ]

    for value, count in trips_eligable:
        draws_required = max([3 - count, 0])
        suits = ["ANY" for _ in range(draws_required)]
        values = [value for _ in range(draws_required)]

        draw_scenarios.append(
            {
                OUT_STRING: build_out_string(suits, values, draws),
                TIEBREAKER: value,
            }
        )

    return draw_scenarios


def _outs_two_pair(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards

    drawn_value_counter = Counter([card.value for card in drawn_cards])
    available_values_counter = Counter([card.value for card in available_cards])

    pair_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 2
        and available_values_counter[value] + drawn_value_counter[value] >= 2
    ]

    for pair_a, pair_b in combinations(pair_eligable, 2):
        high_pair = pair_a if pair_a[0] > pair_b[0] else pair_b
        low_pair = pair_a if pair_a[0] < pair_b[0] else pair_b

        high_pair_draws_req = max([2 - high_pair[1], 0])
        low_pair_draws_req = max([2 - low_pair[1], 0])
        if high_pair_draws_req + low_pair_draws_req <= draws:
            suits = ["ANY" for _ in range(high_pair_draws_req + low_pair_draws_req)]
            values = [high_pair[0] for _ in range(high_pair_draws_req)]
            values.extend([low_pair[0] for _ in range(low_pair_draws_req)])
            draw_scenarios.append(
                {
                    OUT_STRING: build_out_string(suits, values, draws),
                    TIEBREAKER: (high_pair[0], low_pair[0]),
                }
            )

    return draw_scenarios


def _outs_pair(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    draw_scenarios = []
    draws = 5 - len(board_cards)
    drawn_cards = hole_cards + board_cards

    drawn_value_counter = Counter([card.value for card in drawn_cards])
    available_values_counter = Counter([card.value for card in available_cards])

    pair_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 2
        and available_values_counter[value] + drawn_value_counter[value] >= 2
    ]

    for pair in pair_eligable:
        draws_req = max([2 - pair[1], 0])
        suits = ["ANY" for _ in range(draws_req)]
        values = [pair[0] for _ in range(draws_req)]
        draw_scenarios.append(
            {
                OUT_STRING: build_out_string(suits, values, draws),
                TIEBREAKER: pair[0],
            }
        )

    return draw_scenarios


def _outs_high_card(hole_cards: List[Card], board_cards: List[Card], available_cards: List[Card]) -> List[Dict]:
    """
    Private method to find all of the possible draw scenarios to get the player this specific draw type.
    :param hole_cards: List of card objects representing the players hole cards
    :param board_cards: List of card objects representing the cards that have been dealt to the board.
    :param available_cards: List of card objects representing the cards that can be drawn.
    """

    return []


############################
#  Private helper methods  #
############################
def _create_combos_for_out_string(out_string: str, drawable_cards: List[Card]) -> List[str]:
    """
    Method to create all possible draw combinations with the drawable cards based on the out string provided.

    :param out_string: string describing the out conditions
    :param drawable_card: list opf card objects representing all possible draw cards.
    """

    card_candidates = []

    for card_str in out_string.split("-"):
        suit = card_str[0]
        value = card_str[1]

        if suit == "*" and value == "*":
            card_candidates.append([card.identity for card in drawable_cards])
        elif suit == "*":
            card_candidates.append(
                [
                    card.identity
                    for card in drawable_cards
                    if card.identity[1] == value
                ]
            )
        elif value == "*":
            card_candidates.append(
                [
                    card.identity
                    for card in drawable_cards
                    if card.identity[0] == suit
                ]
            )
        else:
            card_candidates.append([card_str])

    combos = product(*card_candidates)
    combos = [sorted(list(combo)) for combo in combos]
    combos = [combo for combo in combos if len(combo) == len(set(combo))]
    combos.sort()
    combos = list(combo for combo, _ in groupby(combos))
    return combos
