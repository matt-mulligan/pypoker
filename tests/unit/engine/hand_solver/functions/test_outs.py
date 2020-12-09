from itertools import product

from pytest import mark, fixture

from pypoker.deck import Card
from pypoker.engine.hand_solver.functions.outs import build_out_string, claim_out_strings


##############
#  Fixtures  #
##############
@fixture
def utilised_outs_none():
    return []


@fixture
def drawable_cards_all():
    drawable_cards = []
    for suit in ["S", "C", "D", "H"]:
        for value in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]:
            drawable_cards.append(Card(f"{suit}{value}"))
    return drawable_cards


@fixture
def expected_claim_all_spades_singles():
    return sorted(["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "ST", "SJ", "SQ", "SK", "SA"])


@fixture
def expected_claim_all_spades_single_wildcard(drawable_cards_all):
    spades = ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "ST", "SJ", "SQ", "SK", "SA"]
    all_cards = [card.identity for card in drawable_cards_all]
    combos = product(spades, all_cards)
    combos = [sorted(list(combo)) for combo in combos if len(set(combo)) == len(combo)]
    combos = ["-".join(combo) for combo in combos]
    return sorted(list(set(combos)))


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


@mark.parametrize("utilised_outs, out_strings, drawable_cards, expected", [
    ("utilised_outs_none", ["S*"], "drawable_cards_all", "expected_claim_all_spades_singles"),
    ("utilised_outs_none", ["S*-**"], "drawable_cards_all", "expected_claim_all_spades_single_wildcard")
])
def test_when_claim_out_strings_then_correct_values_claimed(utilised_outs, out_strings, drawable_cards, expected, request):
    utilised_outs = request.getfixturevalue(utilised_outs)
    drawable_cards = request.getfixturevalue(drawable_cards)
    expected = request.getfixturevalue(expected)
    actual = claim_out_strings(utilised_outs, out_strings, drawable_cards)
    assert actual == expected
