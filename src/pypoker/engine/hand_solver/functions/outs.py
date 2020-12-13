"""
FUNCTIONS.OUTS MODULE

this module contains the implementation of all outs scenario evaluation and outs tiebreaker logic
This module also contains some public methods to assist in building out-strings and claiming the card combinations that
are represented by an out-string
"""
from collections import Counter
from itertools import product, groupby, combinations
from typing import List, Dict, Union

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
def find_outs_scenarios(game_type: str, hand_type: str, **kwargs) -> str:
    """
    Public method to find any all out scenarios for a given set of hole and board cards for the specified hand and game type.
    Note that this method will attempt to find all scenarios to produce hands of this type that are BETTER than any current hand of this type the player can make
    for example:
        Game Type: Texas Holdem
        Hand Type: Full House
        hole_cards: ["H7", "C7"]
        board_cards: ["D7", "SQ", "D2",]

        This method would return out strings for 7/2->A and Q/7
        It will not however return outs for 2/7 as the outs for this would ultimate also give you 7/2 and that is a strong hand

    A similar example:
        Game Type: Texas Holdem
        Hand Type: Full House
        hole_cards: ["HT", "CT"]
        board_cards: ["DT", "SJ", "DJ"]

        the player already has a full house (T/J) so the method will only return out scenarios that improve this position
        the method would return scenarios for T/Q | T/K | T/A | J/T
        it will not return outs for T/2->9 as the current full house is better than this.


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

    kwargs_required_keys, outs_scenario_method = {
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
    return outs_scenario_method(**kwargs)


def tiebreak_outs_draw(game_type: str, hand_type: str, **kwargs) -> str:
    """
    Public method used to determine the winner of a possible draw if more than one player is claiming it for a
    specific hand type.
    This method utilises the tiebreaker information built by the "find_outs_scenarios" method as well as the
    players own hole cards and board/draw cards if required.
    """

    _check_game_type(game_type)
    _check_hand_type(game_type, hand_type)
    tb_key = f"{game_type}-{hand_type}"

    kwargs_required_keys, draw_tb_method = {
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT_FLUSH}":
            (["tiebreakers"], _outs_tb_straight_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_QUADS}":
            (["tiebreakers", "hole_cards", "board_cards", "drawn_cards"], _outs_tb_quads),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FULL_HOUSE}":
            (["tiebreakers"], _outs_tb_full_house),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_FLUSH}":
            (["tiebreakers", "hole_cards", "board_cards", "drawn_cards"], _outs_tb_flush),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_STRAIGHT}":
            (["tiebreakers"], _outs_tb_straight),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TRIPS}":
            (["tiebreakers", "hole_cards", "board_cards", "drawn_cards"], _outs_tb_trips),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_TWO_PAIR}":
            (["tiebreakers", "hole_cards", "board_cards", "drawn_cards"], _outs_tb_two_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_PAIR}":
            (["tiebreakers", "hole_cards", "board_cards", "drawn_cards"], _outs_tb_pair),
        f"{GAME_TYPE_TEXAS_HOLDEM}-{HAND_TYPE_HIGH_CARD}":
            (["tiebreakers", "hole_cards", "board_cards", "drawn_cards"], _outs_tb_high_card),
    }[tb_key]

    _check_kwargs(kwargs, kwargs_required_keys)
    return draw_tb_method(**kwargs)


def build_out_string(suits: List[str], values: List[Union[int, str]], draws: int) -> str:
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


def claim_out_string(utilised_outs: List[str], out_string: str, drawable_cards: List[Card]) -> List[str]:
    """
    Public method to claim all possible out combinations for the cards given

    :param utilised_outs: List of out strings that have already been claimed
    :param out_string: out string that we want to assess for claiming
    :param drawable_cards: List of card objects representing all of the cards yet to be drawn
    """

    combos = _create_card_combinations_for_out_string(out_string, drawable_cards)
    combos = [combo for combo in combos if combo not in utilised_outs]

    return combos


##########################################################
#  PRIVATE IMPLEMENTATION METHODS - OUTS - TEXAS HOLDEM  #
##########################################################
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

                # Account for the possibility of an 5->A straight
                if 14 in usable_card_vals:
                    usable_card_vals.append(1)
                    usable_card_vals.sort()

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

                # check possible straights to ensure they have at least 5 positions and all drawn cards are required
                # checks to ensure that the
                qualifying_straights = []
                for run in runs:
                    if run[1] - run[0] < 4:
                        continue

                    drawn_suit_cards_values = [card.value for card in drawn_suit_cards]
                    hypothetical_draw_cards_values = [card.value for card in hypothetical_draw_cards]
                    straight_values = list(range(run[1] - 4, run[1] + 1))
                    required_straight_values = [value for value in straight_values if value not in drawn_suit_cards_values]

                    if run[0] == 1:
                        hypothetical_draw_cards_values.append(1)
                        hypothetical_draw_cards_values = [value for value in hypothetical_draw_cards_values if value != 14]

                    hypothetical_draw_cards_values.sort()
                    required_straight_values.sort()

                    if required_straight_values == hypothetical_draw_cards_values:
                        qualifying_straights.append(run)

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
    current_quads = [value for value, count in drawn_value_counter.items() if count >= 4]
    value_eligable = [
        value
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 4 and available_values_counter[value] + drawn_value_counter[value] >= 4 and value not in current_quads
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

    # OLD APPROACH - does not account for situations with multiple full houses available (three pairs problem)
    for trip_info, pair_info in product(trips_eligable, pair_eligable):
        # check we havent selected the same value for both trips and pairs
        if trip_info[0] == pair_info[0]:
            continue

        trip_draws_required = max([3 - trip_info[1], 0])
        pair_draws_required = max([2 - pair_info[1], 0])

        if trip_draws_required + pair_draws_required > draws:
            continue

        current_trips = [value for value, counter in drawn_value_counter.items() if counter >= 3]
        if current_trips and trip_info[0] < max(current_trips):
            continue

        current_pairs = [value for value, counter in drawn_value_counter.items() if counter >= 2]
        current_pairs = [value for value in current_pairs if value != trip_info[0]]
        if current_pairs and pair_info[0] < max(current_pairs):
            continue

        if trip_info[0] in current_trips and pair_info[0] in current_pairs:
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
        if draws_required == 0:  # Player already has a flush, look to improve it with specific outs
            current_flush_values = sorted([card.value for card in drawn_cards if card.suit == suit], reverse=True)
            better_flush_values = [card.value for card in available_cards if card.suit == suit and card.value > max(current_flush_values)]
            for flush_value in better_flush_values:
                suits = [suit]
                suits.extend(["ANY" for _ in range(draws - 1)])
                values = [flush_value]
                values.extend(["ANY" for _ in range(draws - 1)])

                draw_scenarios.append(
                    {
                        OUT_STRING: build_out_string(suits, values, draws),
                        TIEBREAKER: suit
                    }
                )

        else:  # Player doesn't have a flush already, give generic outs
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

            # Account for the possibility of an 5->A straight
            if 14 in combined_values:
                combined_values.append(1)
                combined_values.sort()

            gaps = [
                [s, e]
                for s, e in zip(combined_values, combined_values[1:])
                if s + 1 < e
            ]
            edges = iter(combined_values[:1] + sum(gaps, []) + combined_values[-1:])
            runs = list(zip(edges, edges))

            # check possible straights to ensure they have at least 5 positions and all drawn cards are required
            # checks to ensure that the
            qualifying_straights = []
            for run in runs:
                if run[1] - run[0] < 4:
                    continue

                drawn_cards_values = [card.value for card in drawn_cards]
                possible_draw_values = [value for value in possible_draw]
                straight_values = list(range(run[1] - 4, run[1] + 1))
                required_straight_values = [value for value in straight_values if value not in drawn_cards_values]

                if run[0] == 1:
                    possible_draw_values.append(1)
                    possible_draw_values = [value for value in possible_draw_values if value != 14]

                possible_draw_values.sort()
                required_straight_values.sort()

                if required_straight_values == possible_draw_values:
                    qualifying_straights.append(run)

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
    current_trips = [value for value, count in drawn_value_counter.items() if count >= 3]
    current_trips = 0 if not current_trips else max(current_trips)

    trips_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 3
        and available_values_counter[value] + drawn_value_counter[value] >= 3
        and value > current_trips
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
    current_pairs = [value for value, count in drawn_value_counter.items() if count >= 2]

    pair_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 2
        and available_values_counter[value] + drawn_value_counter[value] >= 2
    ]

    for pair_a, pair_b in combinations(pair_eligable, 2):
        high_pair = pair_a if pair_a[0] > pair_b[0] else pair_b
        low_pair = pair_a if pair_a[0] < pair_b[0] else pair_b
        all_pairs = sorted(list({high_pair[0], low_pair[0], *current_pairs}), reverse=True)

        if all_pairs[0] != high_pair[0] or all_pairs[1] != low_pair[0]:
            continue

        if high_pair[0] in current_pairs and low_pair[0] in current_pairs:
            continue

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
    current_pairs = [value for value, count in drawn_value_counter.items() if count >= 2]

    pair_eligable = [
        (value, drawn_value_counter[value])
        for value in CARD_VALUES
        if drawn_value_counter[value] + draws >= 2
        and available_values_counter[value] + drawn_value_counter[value] >= 2
    ]

    for pair in pair_eligable:
        if current_pairs and pair[0] <= max(current_pairs):
            continue
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

    draw_scenarios = []
    draws = 5 - len(board_cards)
    if draws <= 0:
        return draw_scenarios

    drawn_cards = hole_cards + board_cards

    current_high_card = max([card.value for card in drawn_cards])
    available_values = list(set([card.value for card in available_cards]))
    viable_values = [value for value in available_values if value > current_high_card]

    for value in viable_values:
        suits = ["ANY"]
        suits.extend(["ANY" for _ in range(draws - 1)])
        values = [value]
        values.extend(["ANY" for _ in range(draws - 1)])

        draw_scenarios.append(
            {
                OUT_STRING: build_out_string(suits, values, draws),
                TIEBREAKER: value,
            }
        )

    return draw_scenarios


#######################################################################
#  PRIVATE IMPLEMENTATION METHODS - OUTS TIEBRERAKERS - TEXAS HOLDEM  #
#######################################################################
def _outs_tb_straight_flush(tiebreakers: Dict) -> str:
    """
    Private method to determine which player would have the stronger straight flush hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
    winners = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker == max_tiebreaker
    ]
    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_quads(
    tiebreakers: Dict,
    hole_cards: Dict[str, List[Card]],
    board_cards: List[Card],
    drawn_cards: List[Card],
) -> str:
    """
    Private method to determine which player would have the stronger quads hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
    possible_winners = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker == max_tiebreaker
    ]

    if len(possible_winners) == 1:
        return possible_winners[0]

    player_kickers = {}
    for player in possible_winners:
        player_values = [card.value for card in hole_cards[player]]
        player_values.extend([card.value for card in board_cards])
        player_values.extend([card.value for card in drawn_cards])
        player_values = [
            value for value in player_values if value != max_tiebreaker
        ]

        player_kickers[player] = max(player_values)

    max_kicker = max([kicker for kicker in player_kickers.values()])
    winners = [
        player for player, kicker in player_kickers.items() if kicker == max_kicker
    ]
    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_full_house(tiebreakers: Dict) -> str:
    """
    Private method to determine which player would have the stronger full house hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_trips = max([tiebreaker[0] for tiebreaker in tiebreakers.values()])
    max_trips_players = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker[0] == max_trips
    ]

    if len(max_trips_players) == 1:
        return max_trips_players[0]

    max_pair = max(
        [
            tiebreaker[1]
            for player, tiebreaker in tiebreakers.items()
            if player in max_trips_players
        ]
    )
    max_pair_players = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker[1] == max_pair and player in max_trips_players
    ]

    return (
        max_pair_players[0]
        if len(max_pair_players) == 1
        else f"TIE({','.join(max_pair_players)})"
    )


def _outs_tb_flush(
    tiebreakers: Dict,
    hole_cards: Dict[str, List[Card]],
    board_cards: List[Card],
    drawn_cards: List[Card],
) -> str:
    """
    Private method to determine which player would have the stronger flush hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    player_flush_values = {}
    for player, cards in hole_cards.items():
        flush_values = [
            card.value for card in cards if card.suit == tiebreakers[player]
        ]
        flush_values.extend(
            [card.value for card in board_cards if card.suit == tiebreakers[player]]
        )
        flush_values.extend(
            [card.value for card in drawn_cards if card.suit == tiebreakers[player]]
        )

        player_flush_values[player] = sorted(flush_values, reverse=True)

    winners = [player for player in hole_cards.keys()]

    for index in range(5):
        max_index_value = max(
            [
                values[index]
                for player, values in player_flush_values.items()
                if player in winners
            ]
        )

        winners = [
            player
            for player in winners
            if player_flush_values[player][index] == max_index_value
        ]

    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_straight(tiebreakers: Dict) -> str:
    """
    Private method to determine which player would have the stronger straight hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
    winners = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker == max_tiebreaker
    ]
    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_trips(
    tiebreakers: Dict,
    hole_cards: Dict[str, List[Card]],
    board_cards: List[Card],
    drawn_cards: List[Card],
) -> str:
    """
    Private method to determine which player would have the stronger trips hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
    possible_winners = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker == max_tiebreaker
    ]

    if len(possible_winners) == 1:
        return possible_winners[0]

    player_kickers = {}
    for player in possible_winners:
        player_values = [card.value for card in hole_cards[player]]
        player_values.extend([card.value for card in board_cards])
        player_values.extend([card.value for card in drawn_cards])
        player_values = [
            value for value in player_values if value != max_tiebreaker
        ]

        player_kickers[player] = sorted(player_values, reverse=True)

    winners = [player for player in possible_winners]
    for index in range(2):
        max_index_value = max(
            [
                values[index]
                for player, values in player_kickers.items()
                if player in winners
            ]
        )

        winners = [
            player
            for player in winners
            if player_kickers[player][index] == max_index_value
        ]

    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_two_pair(
    tiebreakers: Dict,
    hole_cards: Dict[str, List[Card]],
    board_cards: List[Card],
    drawn_cards: List[Card],
) -> str:
    """
    Private method to determine which player would have the stronger two pair hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_high_pair = max([tiebreaker[0] for tiebreaker in tiebreakers.values()])
    max_high_pair_players = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker[0] == max_high_pair
    ]

    if len(max_high_pair_players) == 1:
        return max_high_pair_players[0]

    max_low_pair = max(
        [
            tiebreaker[1]
            for player, tiebreaker in tiebreakers.items()
            if player in max_high_pair_players
        ]
    )
    max_low_pair_players = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker[1] == max_low_pair and player in max_high_pair_players
    ]

    if len(max_low_pair_players) == 1:
        return max_low_pair_players[0]

    player_kickers = {}
    for player in max_low_pair_players:
        player_values = [card.value for card in hole_cards[player]]
        player_values.extend([card.value for card in board_cards])
        player_values.extend([card.value for card in drawn_cards])
        player_values = [
            value
            for value in player_values
            if value not in [max_high_pair, max_low_pair]
        ]

        player_kickers[player] = max(player_values)

    max_kicker = max([kicker for kicker in player_kickers.values()])
    winners = [
        player for player, kicker in player_kickers.items() if kicker == max_kicker
    ]
    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_pair(
    tiebreakers: Dict,
    hole_cards: Dict[str, List[Card]],
    board_cards: List[Card],
    drawn_cards: List[Card],
) -> str:
    """
    Private method to determine which player would have the stronger pair hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
    possible_winners = [
        player
        for player, tiebreaker in tiebreakers.items()
        if tiebreaker == max_tiebreaker
    ]

    if len(possible_winners) == 1:
        return possible_winners[0]

    player_kickers = {}
    for player in possible_winners:
        player_values = [card.value for card in hole_cards[player]]
        player_values.extend([card.value for card in board_cards])
        player_values.extend([card.value for card in drawn_cards])
        player_values = [
            value for value in player_values if value != max_tiebreaker
        ]

        player_kickers[player] = sorted(player_values, reverse=True)

    winners = [player for player in possible_winners]
    for index in range(3):
        max_index_value = max(
            [
                values[index]
                for player, values in player_kickers.items()
                if player in winners
            ]
        )

        winners = [
            player
            for player in winners
            if player_kickers[player][index] == max_index_value
        ]

    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


def _outs_tb_high_card(
    tiebreakers: Dict,
    hole_cards: Dict[str, List[Card]],
    board_cards: List[Card],
    drawn_cards: List[Card],
) -> str:
    """
    Private method to determine which player would have the stronger high card hand. given the drawn cards.

    :param tiebreakers: dictionary of each players tiebreak information for this draw.
    :param hole_cards: dictionary of each players hole cards
    :param board_cards: List of the board cards that have been dealt
    :param drawn_cards: List of cards that would be drawn in this scenario

    :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
             a comma-separated list of the players who have tied
    """

    player_kickers = {}
    for player in hole_cards.keys():
        player_values = [card.value for card in hole_cards[player]]
        player_values.extend([card.value for card in board_cards])
        player_values.extend([card.value for card in drawn_cards])

        player_kickers[player] = sorted(player_values, reverse=True)

    winners = [player for player in tiebreakers.keys()]
    for index in range(5):
        max_index_value = max(
            [
                values[index]
                for player, values in player_kickers.items()
                if player in winners
            ]
        )

        winners = [
            player
            for player in winners
            if player_kickers[player][index] == max_index_value
        ]

    return winners[0] if len(winners) == 1 else f"TIE({','.join(sorted(winners))})"


############################
#  Private helper methods  #
############################
def _create_card_combinations_for_out_string(out_string: str, drawable_cards: List[Card]) -> List[str]:
    """
    Method to create all possible draw combinations with the drawable cards based on the out string provided.
    each combination is represented by a string of the card ID's broken apart by dashes (-)

    :param out_string: string describing the out conditions
    :param drawable_card: list opf card objects representing all possible draw cards.
    :return: List of strings representing the card outs
    """

    card_candidates = []

    for out_component in out_string.split("-"):
        suit = out_component[0]
        value = out_component[1]

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
            card_candidates.append([out_component])

    combos = product(*card_candidates)
    combos = [sorted(list(combo)) for combo in combos]
    combos = [combo for combo in combos if len(combo) == len(set(combo))]
    combos = ["-".join(combo) for combo in combos]
    combos = sorted(list(set(combos)))
    return combos
