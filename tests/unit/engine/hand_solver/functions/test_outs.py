from itertools import product

from pytest import mark, fixture, raises

from fixtures.cards import get_hand
from pypoker.deck import Card, Deck
from pypoker.engine.hand_solver.functions.outs import build_out_string, claim_out_string, find_outs_scenarios


##############
#  Fixtures  #
##############
@fixture
def utilised_outs_none():
    return []


@fixture
def utilised_outs_singles_spades_001():
    return ["S7", "S8", "S9"]


@fixture
def utilised_outs_doubles_spades_001():
    return ["S7-S8", "S8-S9"]


@fixture
def utilised_outs_singles_sevens_001():
    return ["H7", "S7"]


@fixture
def utilised_outs_doubles_sevens_001():
    return ["H7-S7"]


@fixture
def drawable_cards_all():
    drawable_cards = []
    for suit in ["S", "C", "D", "H"]:
        for value in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]:
            drawable_cards.append(Card(f"{suit}{value}"))
    return drawable_cards


@fixture
def drawable_cards_spades_001():
    drawable_cards = []
    for suit in ["S", "C", "D", "H"]:
        for value in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]:
            drawable_cards.append(Card(f"{suit}{value}"))
    return [card for card in drawable_cards if card.identity not in ["S7", "S8", "S9"]]


@fixture
def drawable_cards_sevens_001():
    drawable_cards = []
    for suit in ["S", "C", "D", "H"]:
        for value in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]:
            drawable_cards.append(Card(f"{suit}{value}"))
    return [card for card in drawable_cards if card.identity not in ["S7", "H7"]]


@fixture
def expected_claim_spades():
    return sorted(["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "ST", "SJ", "SQ", "SK", "SA"])


@fixture
def expected_claim_spades_minus_spades_001():
    return sorted(["S2", "S3", "S4", "S5", "S6", "ST", "SJ", "SQ", "SK", "SA"])


@fixture
def expected_claim_spades_wildcard(drawable_cards_all):
    spades = ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "ST", "SJ", "SQ", "SK", "SA"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(spades, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def expected_claim_spades_wildcard_minus_spades_001(drawable_cards_all, utilised_outs_doubles_spades_001):
    spades = ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "ST", "SJ", "SQ", "SK", "SA"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(spades, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    combos = sorted(list(set(combos)))
    return [combo for combo in combos if combo not in utilised_outs_doubles_spades_001]


@fixture
def expected_claim_spades_wildcard_minus_spades_002(drawable_cards_all, utilised_outs_doubles_spades_001):
    spades = ["S2", "S3", "S4", "S5", "S6", "ST", "SJ", "SQ", "SK", "SA"]
    all_cards = [card.identity for card in drawable_cards_all if card.identity not in ["S7", "S8", "S9"]]
    combos = product(spades, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def expected_claim_c7_c9():
    return sorted(["C7-C9"])


@fixture
def expected_claim_c7_c9_wildcard(drawable_cards_all):
    card_one = ["C7", "C9"]
    card_two = ["C7", "C9"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(card_one, card_two, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def expected_claim_sevens():
    return sorted(["S7", "C7", "H7", "D7"])


@fixture
def expected_claim_sevens_minus_sevens_001():
    return sorted(["C7", "D7"])


@fixture
def expected_claim_sevens_wildcard(drawable_cards_all):
    sevens = ["S7", "C7", "H7", "D7"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(sevens, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def expected_claim_sevens_wildcard_minus_sevens_001(drawable_cards_all, utilised_outs_doubles_sevens_001):
    sevens = ["S7", "C7", "H7", "D7"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(sevens, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    combos = sorted(list(set(combos)))
    return [combo for combo in combos if combo not in utilised_outs_doubles_sevens_001]


@fixture
def expected_claim_sevens_wildcard_minus_sevens_002(drawable_cards_all):
    sevens = ["C7", "D7"]
    all_cards = [card.identity for card in drawable_cards_all if card.identity not in ["S7", "H7"]]
    combos = product(sevens, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def expected_claim_hearts_kings():
    card_one = ["H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "HT", "HJ", "HQ", "HK", "HA"]
    card_two = ["HK", "CK", "DK", "SK"]
    combos = product(card_one, card_two)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def expected_claim_hearts_kings_wildcard(drawable_cards_all):
    card_one = ["H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "HT", "HJ", "HQ", "HK", "HA"]
    card_two = ["HK", "CK", "DK", "SK"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(card_one, card_two, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


@fixture
def out_scenarios_none():
    return []


@fixture
def out_scenarios_straight_flush_001():
    return [{'out_string': 'SJ', 'tiebreaker': 11}, {'out_string': 'S6', 'tiebreaker': 10}]


@fixture
def out_scenarios_straight_flush_002():
    return [{'out_string': 'S8-**', 'tiebreaker': 10}, {'out_string': 'SJ-S8', 'tiebreaker': 11}]


@fixture
def out_scenarios_straight_flush_003():
    return [
        {'out_string': 'HA-H5-H3-H2-**', 'tiebreaker': 5}, {'out_string': 'H8-H7-H6-H5-**', 'tiebreaker': 8},
        {'out_string': 'H7-H6-H5-H3-**', 'tiebreaker': 7}, {'out_string': 'H6-H5-H3-H2-**', 'tiebreaker': 6},
        {'out_string': 'HA-HK-HQ-HJ-HT', 'tiebreaker': 14}, {'out_string': 'HK-HQ-HJ-HT-H9', 'tiebreaker': 13},
        {'out_string': 'HQ-HJ-HT-H9-H8', 'tiebreaker': 12}, {'out_string': 'HJ-HT-H9-H8-H7', 'tiebreaker': 11},
        {'out_string': 'HT-H9-H8-H7-H6', 'tiebreaker': 10}, {'out_string': 'H9-H8-H7-H6-H5', 'tiebreaker': 9},
        {'out_string': 'CA-CK-CQ-CJ-CT', 'tiebreaker': 14}, {'out_string': 'CA-C5-C4-C3-C2', 'tiebreaker': 5},
        {'out_string': 'CK-CQ-CJ-CT-C9', 'tiebreaker': 13}, {'out_string': 'CQ-CJ-CT-C9-C8', 'tiebreaker': 12},
        {'out_string': 'CJ-CT-C9-C8-C7', 'tiebreaker': 11}, {'out_string': 'CT-C9-C8-C7-C6', 'tiebreaker': 10},
        {'out_string': 'C9-C8-C7-C6-C5', 'tiebreaker': 9}, {'out_string': 'C8-C7-C6-C5-C4', 'tiebreaker': 8},
        {'out_string': 'C7-C6-C5-C4-C3', 'tiebreaker': 7}, {'out_string': 'C6-C5-C4-C3-C2', 'tiebreaker': 6},
        {'out_string': 'DA-DK-DQ-DJ-DT', 'tiebreaker': 14}, {'out_string': 'DA-D5-D4-D3-D2', 'tiebreaker': 5},
        {'out_string': 'DK-DQ-DJ-DT-D9', 'tiebreaker': 13}, {'out_string': 'DQ-DJ-DT-D9-D8', 'tiebreaker': 12},
        {'out_string': 'DJ-DT-D9-D8-D7', 'tiebreaker': 11}, {'out_string': 'DT-D9-D8-D7-D6', 'tiebreaker': 10},
        {'out_string': 'D9-D8-D7-D6-D5', 'tiebreaker': 9}, {'out_string': 'D8-D7-D6-D5-D4', 'tiebreaker': 8},
        {'out_string': 'D7-D6-D5-D4-D3', 'tiebreaker': 7}, {'out_string': 'D6-D5-D4-D3-D2', 'tiebreaker': 6},
        {'out_string': 'SJ-ST-S9-S8-**', 'tiebreaker': 11}, {'out_string': 'ST-S9-S8-S6-**', 'tiebreaker': 10},
        {'out_string': 'S9-S8-S6-S5-**', 'tiebreaker': 9}, {'out_string': 'S8-S6-S5-S4-**', 'tiebreaker': 8},
        {'out_string': 'S6-S5-S4-S3-**', 'tiebreaker': 7}, {'out_string': 'SA-SK-SQ-SJ-ST', 'tiebreaker': 14},
        {'out_string': 'SA-S5-S4-S3-S2', 'tiebreaker': 5}, {'out_string': 'SK-SQ-SJ-ST-S9', 'tiebreaker': 13},
        {'out_string': 'SQ-SJ-ST-S9-S8', 'tiebreaker': 12}
    ]


@fixture
def out_scenarios_straight_flush_004():
    return [{'out_string': 'H3-H2', 'tiebreaker': 5}]


@mark.parametrize("suits, values, draws, expected", [
    (["Spades"], [2], 5, "S2-**-**-**-**"),
    (["Spades", "Hearts"], [2, 14], 5, "S2-HA-**-**-**"),
    (["Spades", "Hearts", "Clubs"], [2, 14, 3], 5, "S2-HA-C3-**-**"),
    (["Spades", "Hearts", "Clubs", "Diamonds"], [2, 14, 3, 13], 5, "S2-HA-C3-DK-**"),
    (["Spades", "Hearts", "Clubs", "Diamonds", "Spades"], [2, 14, 3, 13, 4], 5, "S2-HA-C3-DK-S4"),
    (["Spades"], [5], 4, "S5-**-**-**"),
    (["Spades", "Hearts"], [5, 12], 4, "S5-HQ-**-**"),
    (["Spades", "Hearts", "Clubs"], [5, 12, 6], 4, "S5-HQ-C6-**"),
    (["Spades", "Hearts", "Clubs", "Diamonds"], [5, 12, 6, 11], 4, "S5-HQ-C6-DJ"),
    (["Spades"], [7], 3, "S7-**-**"),
    (["Spades", "Hearts"], [7, 10], 3, "S7-HT-**"),
    (["Spades", "Hearts", "Clubs"], [7, 10, 8], 3, "S7-HT-C8"),
    (["Spades"], [9], 2, "S9-**"),
    (["Spades", "Hearts"], [9, 14], 2, "S9-HA"),
    (["Spades"], [9], 1, "S9"),
    (["Hearts", "Hearts", "Hearts"], ["ANY", "ANY", "ANY"], 5, "H*-H*-H*-**-**"),
    (["ANY", "ANY", "ANY", "ANY"], [6, 6, 7, 7], 5, "*6-*6-*7-*7-**")
])
def test_when_build_out_string_then_correct_string_returned(suits, values, draws, expected):
    actual = build_out_string(suits, values, draws)
    assert actual == expected


@mark.parametrize("utilised_outs, out_string, drawable_cards, expected", [
    ("utilised_outs_none", "S*", "drawable_cards_all", "expected_claim_spades"),
    ("utilised_outs_none", "S*-**", "drawable_cards_all", "expected_claim_spades_wildcard"),
    ("utilised_outs_none", "*7", "drawable_cards_all", "expected_claim_sevens"),
    ("utilised_outs_none", "*7-**", "drawable_cards_all", "expected_claim_sevens_wildcard"),
    ("utilised_outs_none", "C7-C9", "drawable_cards_all", "expected_claim_c7_c9"),
    ("utilised_outs_none", "C7-C9-**", "drawable_cards_all", "expected_claim_c7_c9_wildcard"),
    ("utilised_outs_none", "H*-*K", "drawable_cards_all", "expected_claim_hearts_kings"),
    ("utilised_outs_none", "H*-*K-**", "drawable_cards_all", "expected_claim_hearts_kings_wildcard"),

    ("utilised_outs_singles_spades_001", "S*", "drawable_cards_all", "expected_claim_spades_minus_spades_001"),
    ("utilised_outs_doubles_spades_001", "S*-**", "drawable_cards_all", "expected_claim_spades_wildcard_minus_spades_001"),
    ("utilised_outs_singles_sevens_001", "*7", "drawable_cards_all", "expected_claim_sevens_minus_sevens_001"),
    ("utilised_outs_doubles_sevens_001", "*7-**", "drawable_cards_all", "expected_claim_sevens_wildcard_minus_sevens_001"),

    ("utilised_outs_none", "S*", "drawable_cards_spades_001", "expected_claim_spades_minus_spades_001"),
    ("utilised_outs_none", "S*-**", "drawable_cards_spades_001", "expected_claim_spades_wildcard_minus_spades_002"),
    ("utilised_outs_none", "*7", "drawable_cards_sevens_001", "expected_claim_sevens_minus_sevens_001"),
    ("utilised_outs_none", "*7-**", "drawable_cards_sevens_001", "expected_claim_sevens_wildcard_minus_sevens_002"),
])
def test_when_claim_out_strings_then_correct_values_claimed(utilised_outs, out_string, drawable_cards, expected, request):
    utilised_outs = request.getfixturevalue(utilised_outs)
    drawable_cards = request.getfixturevalue(drawable_cards)
    expected = request.getfixturevalue(expected)
    actual = claim_out_string(utilised_outs, out_string, drawable_cards)
    assert actual == expected


def test_when_find_outs_scenarios_and_bad_game_type_then_raise_error():
    with raises(ValueError, match="Game type provided 'BAD_GAME_TYPE' is not an acceptable value"):
        find_outs_scenarios("BAD_GAME_TYPE", "Straight Flush")


def test_when_find_outs_scenarios_and_bad_hand_type_then_raise_error():
    with raises(ValueError, match="Hand type provided 'WINNING_HAND_TYPE' is not an acceptable value"):
        find_outs_scenarios("Texas Holdem", "WINNING_HAND_TYPE")


@mark.parametrize("game_type, hand_type, kwargs", [
    ("Texas Holdem", "Straight Flush", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Quads", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Full House", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Flush", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Trips", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Two Pair", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Pair", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "High Card", {"DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight Flush", {}),
    ("Texas Holdem", "Quads", {}),
    ("Texas Holdem", "Full House", {}),
    ("Texas Holdem", "Flush", {}),
    ("Texas Holdem", "Straight", {}),
    ("Texas Holdem", "Trips", {}),
    ("Texas Holdem", "Two Pair", {}),
    ("Texas Holdem", "Pair", {}),
    ("Texas Holdem", "High Card", {})
])
def test_when_find_outs_scenarios_and_incorrect_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' does not contain all keys required for "
                                  f"this method"):
        find_outs_scenarios(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, kwargs", [
    ("Texas Holdem", "Straight Flush",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Quads",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Full House",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Flush",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Trips",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Two Pair",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Pair",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "High Card",
     {"hole_cards": "BLAH", "board_cards": "BLAH", "available_cards": "BLAH", "DERP": "WHOOPS"}),

])
def test_when_find_outs_scenarios_and_too_many_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' contains additional keys from what is expected"):
        find_outs_scenarios(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, hole_cards, board_cards, non_available_cards, expected", [
    # ("Texas Holdem", "Straight Flush", ["S8", "ST"], ["C2", "S9", "H4", "S7"], ["S8", "ST", "C2", "S9", "S7"], "out_scenarios_straight_flush_001"),
    # ("Texas Holdem", "Straight Flush", ["S7", "ST"], ["C2", "S9", "S6"], ["S7", "ST", "C2", "S9", "S6"], "out_scenarios_straight_flush_002"),
    # ("Texas Holdem", "Straight Flush", ["S7", "H4"], [], ["S7", "H4"], "out_scenarios_straight_flush_003"),
    ("Texas Holdem", "Straight Flush", ["S7", "H4"], ["H5", "HA", "C3"], ["S7", "H4", "H5", "HA", "C3"], "out_scenarios_straight_flush_004")
])
def test_when_find_outs_scenarios_then_correct_out_scenarios_returned(
        game_type, hand_type, hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        game_type, hand_type, hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected
