from itertools import combinations, product, groupby
from typing import List

from pypoker.constants import CardSuit
from pypoker.constructs import Card, AnyCard
from pypoker.engine import group_cards_by_suit, find_all_unique_card_combos, find_consecutive_value_cards, \
    deduplicate_card_sets, group_cards_by_value, order_cards


def find_outs_straight_flush(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for the a straight flush hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of drawd remaining.

    :return List of draw combinations that would give a straight flush. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_suits_grouped = group_cards_by_suit(current_cards)
    drawable_suits_grouped = group_cards_by_suit(available_cards)

    eligible_suits = {
        suit: (curr_cards, drawable_suits_grouped[suit])
        for suit, curr_cards in current_suits_grouped.items()
        if len(curr_cards) + len(drawable_suits_grouped[suit]) >= 5
    }

    if not eligible_suits:
        return []

    outs = []
    for curr_suit_cards, drawable_suit_cards in eligible_suits.values():
        for draw_size in range(1, remaining_draws + 1):
            straight_flushes = []
            draw_combos = find_all_unique_card_combos(
                drawable_suit_cards, draw_size
            )

            for draw_combo in draw_combos:
                straight_flushes.extend(
                    find_consecutive_value_cards(
                        curr_suit_cards + draw_combo, run_size=5
                    )
                )

            straight_flushes = deduplicate_card_sets(straight_flushes)

            for cards in straight_flushes:
                out_cards = [card for card in cards if card in drawable_suit_cards]
                out_cards = out_cards + [AnyCard("")] * (
                        remaining_draws - len(out_cards)
                )
                outs.append(out_cards)

    return deduplicate_card_sets(outs)


def find_outs_quads(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a quad hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of drawd remaining.

    :return List of draw combinations that would give a quad hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_value = group_cards_by_value(current_cards)
    available_cards_by_value = group_cards_by_value(available_cards)

    possible_values = [
        value
        for value in range(2, 15)
        if len(current_cards_by_value[value]) + remaining_draws >= 4
           and len(current_cards_by_value[value])
           + len(available_cards_by_value[value])
           >= 4
    ]

    outs = []
    for quad_value in possible_values:
        required_quad_draws = 4 - len(current_cards_by_value[quad_value])
        surplus_draws = [AnyCard("")] * (remaining_draws - required_quad_draws)

        if not required_quad_draws:
            outs.append(surplus_draws)
            continue

        for draw_combo in find_all_unique_card_combos(
                available_cards_by_value[quad_value], required_quad_draws
        ):
            outs.append(order_cards(draw_combo + surplus_draws))

    return outs


def find_outs_full_house(current_cards: List[Card], available_cards: List[Card], remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a full house hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of draws remaining.

    :return List of draw combinations that would give a full house hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_value = group_cards_by_value(current_cards)
    available_cards_by_value = group_cards_by_value(available_cards)

    # find all values that could make a triple with the remaining number of draws
    trip_possible_values = [
        value
        for value in range(2, 15)
        if len(current_cards_by_value[value]) + remaining_draws >= 3
           and len(current_cards_by_value[value])
           + len(available_cards_by_value[value])
           >= 3
    ]

    # find all values that could make a pair with the remaining number of draws
    pair_possible_values = [
        value
        for value in range(2, 15)
        if len(current_cards_by_value[value]) + remaining_draws >= 2
           and len(current_cards_by_value[value])
           + len(available_cards_by_value[value])
           >= 2
    ]

    full_house_values = [
        (trip_value, pair_value)
        for trip_value in trip_possible_values
        for pair_value in pair_possible_values
        if trip_value != pair_value
           and max(3 - len(current_cards_by_value[trip_value]), 0)
           + max(2 - len(current_cards_by_value[pair_value]), 0)
           <= remaining_draws
    ]

    outs = []
    for trip_value, pair_value in full_house_values:
        trip_req_draws = max(3 - len(current_cards_by_value[trip_value]), 0)
        pair_req_draws = max(2 - len(current_cards_by_value[pair_value]), 0)

        trip_draw_combos = (
            find_all_unique_card_combos(
                available_cards_by_value[trip_value], trip_req_draws
            )
            if trip_req_draws
            else []
        )

        pair_draw_combos = (
            find_all_unique_card_combos(
                available_cards_by_value[pair_value], pair_req_draws
            )
            if pair_req_draws
            else []
        )

        if not trip_draw_combos and not pair_draw_combos:
            outs.append([AnyCard("")] * remaining_draws)

        elif not trip_draw_combos:
            outs.extend(
                [
                    pair_draw + [AnyCard("")] * (remaining_draws - len(pair_draw))
                    for pair_draw in pair_draw_combos
                ]
            )

        elif not pair_draw_combos:
            outs.extend(
                [
                    trip_draw + [AnyCard("")] * (remaining_draws - len(trip_draw))
                    for trip_draw in trip_draw_combos
                ]
            )

        else:
            outs.extend(
                [
                    trip_draw
                    + pair_draw
                    + [AnyCard("")]
                    * (remaining_draws - len(trip_draw) - len(pair_draw))
                    for trip_draw in trip_draw_combos
                    for pair_draw in pair_draw_combos
                ]
            )

    return deduplicate_card_sets(outs)


def find_outs_flush(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a flush hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of draws remaining.

    :return List of draw combinations that would give a flush hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_suit = group_cards_by_suit(current_cards)
    available_cards_by_suit = group_cards_by_suit(available_cards)

    flush_suits = [
        suit.name
        for suit in CardSuit
        if suit != suit.Any
           and len(current_cards_by_suit[suit.name])
           + len(available_cards_by_suit[suit.name])
           >= 5
           and len(current_cards_by_suit[suit.name]) + remaining_draws >= 5
    ]

    outs = []
    for suit in flush_suits:
        required_draws = max(5 - len(current_cards_by_suit[suit]), 0)
        surplus_draws = [AnyCard("")] * (remaining_draws - required_draws)

        if not required_draws:
            outs.append(surplus_draws)
            continue

        draw_combos = find_all_unique_card_combos(
            available_cards_by_suit[suit], required_draws
        )
        for draw_combo in draw_combos:
            outs.append(draw_combo + surplus_draws)

    return deduplicate_card_sets(outs)


def find_outs_straight(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a straight hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of draws remaining.

    :return List of draw combinations that would give a straight hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_value = group_cards_by_value(current_cards)
    available_cards_by_value = group_cards_by_value(available_cards)

    current_values = [
        key for key, value in current_cards_by_value.items() if len(value) > 0
    ]
    available_values = [
        key for key, value in available_cards_by_value.items() if len(value) > 0
    ]

    # loop through drawing 1 to remaining draws number of cards, test straights, create outs
    outs = []
    for draw_amount in range(1, remaining_draws + 1):
        draw_value_combos = [
            list(value) for value in combinations(available_values, draw_amount)
        ]

        for draw_value_combo in draw_value_combos:
            test_draw_cards = [
                available_cards_by_value[value][0] for value in draw_value_combo
            ]
            straights = find_consecutive_value_cards(
                current_cards + test_draw_cards, run_size=5
            )

            for straight in straights:
                straight_draw_values = [
                    card.value
                    for card in straight
                    if card.value in draw_value_combo
                       and card.value not in current_values
                ]

                possible_draw_cards = [
                    available_cards_by_value[value]
                    for value in straight_draw_values
                ]
                draw_card_combos = list(product(*possible_draw_cards))
                surplus_draws = [AnyCard("")] * (
                        remaining_draws - len(straight_draw_values)
                )

                outs.extend(
                    [
                        list(draw_card_combo) + surplus_draws
                        for draw_card_combo in draw_card_combos
                    ]
                )

    return deduplicate_card_sets(outs)


def find_outs_trips(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a trips hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of draws remaining.

    :return List of draw combinations that would give a trips hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_value = group_cards_by_value(current_cards)
    available_cards_by_value = group_cards_by_value(available_cards)

    trip_values = [
        value
        for value, cards in current_cards_by_value.items()
        if len(cards) + remaining_draws >= 3
           and len(cards) + len(available_cards_by_value[value]) >= 3
    ]

    outs = []
    for trip_value in trip_values:
        draws_required = max(3 - len(current_cards_by_value[trip_value]), 0)
        surplus_draws = [AnyCard("")] * (remaining_draws - draws_required)

        if not draws_required:
            outs.append(surplus_draws)
            continue

        draw_combos = find_all_unique_card_combos(
            available_cards_by_value[trip_value], draws_required
        )
        outs.extend([draw_combo + surplus_draws for draw_combo in draw_combos])

    return deduplicate_card_sets(outs)


def find_outs_two_pair(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a two pair hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of draws remaining.

    :return List of draw combinations that would give a two pair hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_value = group_cards_by_value(current_cards)
    available_cards_by_value = group_cards_by_value(available_cards)

    pair_values = [
        value
        for value, cards in current_cards_by_value.items()
        if len(cards) + remaining_draws >= 2
           and len(cards) + len(available_cards_by_value[value]) >= 2
    ]

    pair_combos = [
        sorted([pair_a, pair_b])
        for pair_a in pair_values
        for pair_b in pair_values
        if pair_a != pair_b
           and max(2 - len(current_cards_by_value[pair_a]), 0)
           + max(2 - len(current_cards_by_value[pair_b]), 0)
           <= remaining_draws
    ]

    # de-duplicates any pair combos that are repeated
    pair_combos.sort(key=lambda pairs: (pairs[0], pairs[1]))
    pair_combos = list(k for k, _ in groupby(pair_combos))

    outs = []
    for pair_a, pair_b in pair_combos:
        pair_a_draws_required = max(2 - len(current_cards_by_value[pair_a]), 0)
        pair_b_draws_required = max(2 - len(current_cards_by_value[pair_b]), 0)
        surplus_cards = [AnyCard("")] * (
                remaining_draws - pair_a_draws_required - pair_b_draws_required
        )

        if not pair_a_draws_required and not pair_b_draws_required:
            outs.append(surplus_cards)
            continue

        pair_a_combos = find_all_unique_card_combos(
            available_cards_by_value[pair_a], pair_a_draws_required
        )
        pair_b_combos = find_all_unique_card_combos(
            available_cards_by_value[pair_b], pair_b_draws_required
        )

        if not pair_a_combos:
            outs.extend(
                [pair_b_combo + surplus_cards for pair_b_combo in pair_b_combos]
            )
            continue

        if not pair_b_combos:
            outs.extend(
                [pair_a_combo + surplus_cards for pair_a_combo in pair_a_combos]
            )
            continue

        draw_sets = product(pair_a_combos, pair_b_combos)
        draw_sets = [set_a + set_b for set_a, set_b in draw_sets]
        outs.extend([draw_set + surplus_cards for draw_set in draw_sets])

    return deduplicate_card_sets(outs)


def find_outs_pair(
        current_cards: List[Card],
        available_cards: List[Card],
        remaining_draws: int,
) -> List[List[Card]]:
    """
    Texas Holdem Poker Engine Find Outs Method
    Method to find all possible outs for a pair hand with the given current_cards and available_cards

    :param current_cards: List of the players hole cards and the current board cards.
    :param available_cards: List of cards remaining in the deck that could be drawn
    :param remaining_draws: the number of draws remaining.

    :return List of draw combinations that would give a pair hand. with required draws being explict cards
    (D7, SK, etc) and surplus draws represented by AnyCard special cards
    """

    current_cards_by_value = group_cards_by_value(current_cards)
    available_cards_by_value = group_cards_by_value(available_cards)

    pair_values = [
        value
        for value, cards in current_cards_by_value.items()
        if len(cards) + remaining_draws >= 2
           and len(cards) + len(available_cards_by_value[value]) >= 2
    ]

    outs = []
    for pair_value in pair_values:
        draws_required = max(2 - len(current_cards_by_value[pair_value]), 0)
        surplus_draws = [AnyCard("")] * (remaining_draws - draws_required)

        if not draws_required:
            outs.append(surplus_draws)
            continue

        draw_combos = find_all_unique_card_combos(
            available_cards_by_value[pair_value], draws_required
        )
        outs.extend([draw_combo + surplus_draws for draw_combo in draw_combos])

    return deduplicate_card_sets(outs)
