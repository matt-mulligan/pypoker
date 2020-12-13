from itertools import product

from pytest import mark, fixture, raises

from fixtures.cards import get_hand, get_player_hands_dict, get_tiebreaker_dict
from pypoker.deck import Card, Deck
from pypoker.engine.hand_logic.constants import GAME_TYPE_TEXAS_HOLDEM
from pypoker.engine.hand_logic.functions.outs import build_out_string, claim_out_string, find_outs_scenarios, \
    tiebreak_outs_draw


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


@fixture
def out_scenarios_straight_flush_005():
    return [{'out_string': 'H9-**', 'tiebreaker': 9}, {'out_string': 'HT-H9', 'tiebreaker': 10}]


@fixture
def out_scenarios_quads_001():
    return [{"out_string": "*4-*4", "tiebreaker": 4}]


@fixture
def out_scenarios_quads_002():
    return [{"out_string": "*4-*4", "tiebreaker": 4}, {"out_string": "*5-*5", "tiebreaker": 5}]


@fixture
def out_scenarios_quads_003():
    return [{"out_string": "*4-**", "tiebreaker": 4}]


@fixture
def out_scenarios_quads_004():
    return sorted([
        {"out_string": "*A-*A-*A-**-**", "tiebreaker": 14}, {"out_string": "*K-*K-*K-**-**", "tiebreaker": 13},
        {"out_string": "*Q-*Q-*Q-*Q-**", "tiebreaker": 12}, {"out_string": "*J-*J-*J-*J-**", "tiebreaker": 11},
        {"out_string": "*T-*T-*T-*T-**", "tiebreaker": 10}, {"out_string": "*9-*9-*9-*9-**", "tiebreaker": 9},
        {"out_string": "*8-*8-*8-*8-**", "tiebreaker": 8}, {"out_string": "*7-*7-*7-*7-**", "tiebreaker": 7},
        {"out_string": "*6-*6-*6-*6-**", "tiebreaker": 6}, {"out_string": "*5-*5-*5-*5-**", "tiebreaker": 5},
        {"out_string": "*4-*4-*4-*4-**", "tiebreaker": 4}, {"out_string": "*3-*3-*3-*3-**", "tiebreaker": 3},
        {"out_string": "*2-*2-*2-*2-**", "tiebreaker": 2}
    ], key=lambda scenario: scenario["tiebreaker"])


@fixture
def out_scenarios_quads_005():
    return [{"out_string": "*7", "tiebreaker": 7}]


@fixture
def out_scenarios_full_house_001():
    return [{"out_string": "*K", "tiebreaker": (13, 14)}, {"out_string": "*A", "tiebreaker": (14, 13)}]


@fixture
def out_scenarios_full_house_002():
    return [
        {"out_string": "*4", "tiebreaker": (13, 4)}, {"out_string": "*7", "tiebreaker": (13, 7)},
        {"out_string": "*A", "tiebreaker": (13, 14)}
    ]


@fixture
def out_scenarios_full_house_003():
    return [
        {"out_string": "*7", "tiebreaker": (7, 13)}, {"out_string": "*9", "tiebreaker": (9, 13)},
        {"out_string": "*K", "tiebreaker": (13, 9)}
    ]


@fixture
def out_scenarios_full_house_004():
    return [{"out_string": "*9", "tiebreaker": (13, 9)}]


@fixture
def out_scenarios_full_house_005():
    return sorted([
        {"out_string": "*5-**", "tiebreaker": (7, 5)}, {"out_string": "*Q-**", "tiebreaker": (7, 12)},
        {"out_string": "*3-*3", "tiebreaker": (7, 3)}, {"out_string": "*4-*4", "tiebreaker": (7, 4)},
        {"out_string": "*2-*2", "tiebreaker": (7, 2)}, {"out_string": "*6-*6", "tiebreaker": (7, 6)},
        {"out_string": "*8-*8", "tiebreaker": (7, 8)}, {"out_string": "*9-*9", "tiebreaker": (7, 9)},
        {"out_string": "*T-*T", "tiebreaker": (7, 10)}, {"out_string": "*J-*J", "tiebreaker": (7, 11)},
        {"out_string": "*Q-*Q", "tiebreaker": (12, 7)}, {"out_string": "*K-*K", "tiebreaker": (7, 13)},
        {"out_string": "*A-*A", "tiebreaker": (7, 14)}
    ], key=lambda scenario: scenario["tiebreaker"])


@fixture
def out_scenarios_full_house_006():
    return [
        {'out_string': '*2-*2-*2-**-**', 'tiebreaker': (2, 12)}, {'out_string': '*2-*2-*2-*K-*K', 'tiebreaker': (2, 13)},
        {'out_string': '*2-*2-*2-*A-*A', 'tiebreaker': (2, 14)}, {'out_string': '*3-*3-*3-**-**', 'tiebreaker': (3, 12)},
        {'out_string': '*3-*3-*3-*K-*K', 'tiebreaker': (3, 13)}, {'out_string': '*3-*3-*3-*A-*A', 'tiebreaker': (3, 14)},
        {'out_string': '*4-*4-*4-**-**', 'tiebreaker': (4, 12)}, {'out_string': '*4-*4-*4-*K-*K', 'tiebreaker': (4, 13)},
        {'out_string': '*4-*4-*4-*A-*A', 'tiebreaker': (4, 14)}, {'out_string': '*5-*5-*5-**-**', 'tiebreaker': (5, 12)},
        {'out_string': '*5-*5-*5-*K-*K', 'tiebreaker': (5, 13)}, {'out_string': '*5-*5-*5-*A-*A', 'tiebreaker': (5, 14)},
        {'out_string': '*6-*6-*6-**-**', 'tiebreaker': (6, 12)}, {'out_string': '*6-*6-*6-*K-*K', 'tiebreaker': (6, 13)},
        {'out_string': '*6-*6-*6-*A-*A', 'tiebreaker': (6, 14)}, {'out_string': '*7-*7-*7-**-**', 'tiebreaker': (7, 12)},
        {'out_string': '*7-*7-*7-*K-*K', 'tiebreaker': (7, 13)}, {'out_string': '*7-*7-*7-*A-*A', 'tiebreaker': (7, 14)},
        {'out_string': '*8-*8-*8-**-**', 'tiebreaker': (8, 12)}, {'out_string': '*8-*8-*8-*K-*K', 'tiebreaker': (8, 13)},
        {'out_string': '*8-*8-*8-*A-*A', 'tiebreaker': (8, 14)}, {'out_string': '*9-*9-*9-**-**', 'tiebreaker': (9, 12)},
        {'out_string': '*9-*9-*9-*K-*K', 'tiebreaker': (9, 13)}, {'out_string': '*9-*9-*9-*A-*A', 'tiebreaker': (9, 14)},
        {'out_string': '*T-*T-*T-**-**', 'tiebreaker': (10, 12)}, {'out_string': '*T-*T-*T-*K-*K', 'tiebreaker': (10, 13)},
        {'out_string': '*T-*T-*T-*A-*A', 'tiebreaker': (10, 14)}, {'out_string': '*J-*J-*J-**-**', 'tiebreaker': (11, 12)},
        {'out_string': '*J-*J-*J-*K-*K', 'tiebreaker': (11, 13)}, {'out_string': '*J-*J-*J-*A-*A', 'tiebreaker': (11, 14)},
        {'out_string': '*Q-*2-*2-**-**', 'tiebreaker': (12, 2)}, {'out_string': '*Q-*3-*3-**-**', 'tiebreaker': (12, 3)},
        {'out_string': '*Q-*4-*4-**-**', 'tiebreaker': (12, 4)}, {'out_string': '*Q-*5-*5-**-**', 'tiebreaker': (12, 5)},
        {'out_string': '*Q-*6-*6-**-**', 'tiebreaker': (12, 6)}, {'out_string': '*Q-*7-*7-**-**', 'tiebreaker': (12, 7)},
        {'out_string': '*Q-*8-*8-**-**', 'tiebreaker': (12, 8)}, {'out_string': '*Q-*9-*9-**-**', 'tiebreaker': (12, 9)},
        {'out_string': '*Q-*T-*T-**-**', 'tiebreaker': (12, 10)}, {'out_string': '*Q-*J-*J-**-**', 'tiebreaker': (12, 11)},
        {'out_string': '*Q-*K-*K-**-**', 'tiebreaker': (12, 13)}, {'out_string': '*Q-*A-*A-**-**', 'tiebreaker': (12, 14)},
        {'out_string': '*K-*K-*K-**-**', 'tiebreaker': (13, 12)}, {'out_string': '*K-*K-*K-*A-*A', 'tiebreaker': (13, 14)},
        {'out_string': '*A-*A-*A-**-**', 'tiebreaker': (14, 12)}, {'out_string': '*A-*A-*A-*K-*K', 'tiebreaker': (14, 13)}
    ]


@fixture
def out_scenarios_full_house_007():
    return [
        {'out_string': '*2-*2', 'tiebreaker': (2, 12)}, {'out_string': '*8-*8', 'tiebreaker': (8, 12)},
        {"out_string": "*Q-*2", "tiebreaker": (12, 2)}, {"out_string": "*Q-*8", "tiebreaker": (12, 8)},
        {"out_string": "*Q-*K", "tiebreaker": (12, 13)}, {'out_string': '*K-*K', 'tiebreaker': (13, 12)}
    ]


@fixture
def out_scenarios_flush_001():
    return [{'out_string': 'H*-H*', 'tiebreaker': "Hearts"}]


@fixture
def out_scenarios_flush_002():
    return [{'out_string': 'H*-**', 'tiebreaker': "Hearts"}]


@fixture
def out_scenarios_flush_003():
    return [{'out_string': 'H*', 'tiebreaker': "Hearts"}]


@fixture
def out_scenarios_flush_004():
    return [
        {'out_string': 'H*-H*-H*-**-**', 'tiebreaker': 'Hearts'},
        {'out_string': 'C*-C*-C*-C*-C*', 'tiebreaker': 'Clubs'},
        {'out_string': 'D*-D*-D*-D*-D*', 'tiebreaker': 'Diamonds'},
        {'out_string': 'S*-S*-S*-S*-S*', 'tiebreaker': 'Spades'}
    ]


@fixture
def out_scenarios_flush_005():
    return [
        {'out_string': 'HQ-**', 'tiebreaker': 'Hearts'},
        {'out_string': 'HK-**', 'tiebreaker': 'Hearts'},
        {'out_string': 'HA-**', 'tiebreaker': 'Hearts'}
    ]


@fixture
def out_scenarios_straight_001():
    return [{'out_string': '*J', 'tiebreaker': 11}, {'out_string': '*6', 'tiebreaker': 10}]


@fixture
def out_scenarios_straight_002():
    return [{'out_string': '*8-**', 'tiebreaker': 10}, {'out_string': '*J-*8', 'tiebreaker': 11}]


@fixture
def out_scenarios_straight_003():
    return [
        {'out_string': '*8-*6-*5-**-**', 'tiebreaker': 8}, {'out_string': '*6-*5-*3-**-**', 'tiebreaker': 7},
        {'out_string': '*A-*5-*3-*2-**', 'tiebreaker': 5}, {'out_string': '*J-*T-*9-*8-**', 'tiebreaker': 11},
        {'out_string': '*T-*9-*8-*6-**', 'tiebreaker': 10}, {'out_string': '*9-*8-*6-*5-**', 'tiebreaker': 9},
        {'out_string': '*A-*K-*Q-*J-*T', 'tiebreaker': 14}, {'out_string': '*K-*Q-*J-*T-*9', 'tiebreaker': 13},
        {'out_string': '*Q-*J-*T-*9-*8', 'tiebreaker': 12}
    ]


@fixture
def out_scenarios_straight_004():
    return [
        {'out_string': '*6-**', 'tiebreaker': 7}, {'out_string': '*2-**', 'tiebreaker': 5},
        {'out_string': '*8-*6', 'tiebreaker': 8},
    ]


@fixture
def out_scenarios_straight_005():
    return [{'out_string': '*9-**', 'tiebreaker': 9}, {'out_string': '*T-*9', 'tiebreaker': 10}]


@fixture
def out_scenarios_trips_001():
    return [
        {"out_string": "*2-**", "tiebreaker": 2}, {"out_string": "*3-**", "tiebreaker": 3},
        {"out_string": "*9-*9", "tiebreaker": 9}
    ]


@fixture
def out_scenarios_trips_002():
    return [
        {'out_string': '*2-*2', 'tiebreaker': 2}, {'out_string': '*3-*3', 'tiebreaker': 3},
        {'out_string': '*7-*7', 'tiebreaker': 7}, {'out_string': '*9-*9', 'tiebreaker': 9},
        {'out_string': '*K-*K', 'tiebreaker': 13}
    ]


@fixture
def out_scenarios_trips_003():
    return [{'out_string': '*K-*K', 'tiebreaker': 13}]


@fixture
def out_scenarios_trips_004():
    return [
        {'out_string': '*2-*2-*2-**-**', 'tiebreaker': 2}, {'out_string': '*3-*3-*3-**-**', 'tiebreaker': 3},
        {'out_string': '*4-*4-*4-**-**', 'tiebreaker': 4}, {'out_string': '*5-*5-*5-**-**', 'tiebreaker': 5},
        {'out_string': '*6-*6-*6-**-**', 'tiebreaker': 6}, {'out_string': '*7-*7-**-**-**', 'tiebreaker': 7},
        {'out_string': '*8-*8-*8-**-**', 'tiebreaker': 8}, {'out_string': '*9-*9-*9-**-**', 'tiebreaker': 9},
        {'out_string': '*T-*T-*T-**-**', 'tiebreaker': 10}, {'out_string': '*J-*J-*J-**-**', 'tiebreaker': 11},
        {'out_string': '*Q-*Q-*Q-**-**', 'tiebreaker': 12}, {'out_string': '*K-*K-*K-**-**', 'tiebreaker': 13},
        {'out_string': '*A-*A-**-**-**', 'tiebreaker': 14}
    ]


@fixture
def out_scenarios_two_pair_001():
    return [
        {'out_string': '*6-*2', 'tiebreaker': (6, 2)}, {'out_string': '*9-*2', 'tiebreaker': (9, 2)},
        {'out_string': '*J-*2', 'tiebreaker': (11, 2)}, {'out_string': '*K-*2', 'tiebreaker': (13, 2)},
        {'out_string': '*9-*6', 'tiebreaker': (9, 6)}, {'out_string': '*J-*6', 'tiebreaker': (11, 6)},
        {'out_string': '*K-*6', 'tiebreaker': (13, 6)}, {'out_string': '*J-*9', 'tiebreaker': (11, 9)},
        {'out_string': '*K-*9', 'tiebreaker': (13, 9)}, {'out_string': '*K-*J', 'tiebreaker': (13, 11)}
    ]


@fixture
def out_scenarios_two_pair_002():
    return [
        {'out_string': '*2', 'tiebreaker': (9, 2)}, {'out_string': '*6', 'tiebreaker': (9, 6)},
        {'out_string': '*8', 'tiebreaker': (9, 8)}, {'out_string': '*K', 'tiebreaker': (13, 9)}
    ]


@fixture
def out_scenarios_two_pair_003():
    return [
        {'out_string': '*2-**', 'tiebreaker': (6, 2)}, {'out_string': '*3-*3', 'tiebreaker': (6, 3)},
        {'out_string': '*4-*4', 'tiebreaker': (6, 4)}, {'out_string': '*5-*5', 'tiebreaker': (6, 5)},
        {'out_string': '*7-*7', 'tiebreaker': (7, 6)}, {'out_string': '*8-**', 'tiebreaker': (8, 6)},
        {'out_string': '*9-*9', 'tiebreaker': (9, 6)}, {'out_string': '*T-*T', 'tiebreaker': (10, 6)},
        {'out_string': '*J-*J', 'tiebreaker': (11, 6)}, {'out_string': '*Q-*Q', 'tiebreaker': (12, 6)},
        {'out_string': '*K-**', 'tiebreaker': (13, 6)}, {'out_string': '*A-*A', 'tiebreaker': (14, 6)},
        {'out_string': '*K-*8', 'tiebreaker': (13, 8)}
    ]


@fixture
def out_scenarios_two_pair_004():
    return [{'out_string': '*K', 'tiebreaker': (13, 9)}]


@fixture
def out_scenarios_two_pair_005():
    return [
        {'out_string': '*T-*T', 'tiebreaker': (10, 9)}, {'out_string': '*J-*J', 'tiebreaker': (11, 9)},
        {'out_string': '*Q-*Q', 'tiebreaker': (12, 9)}, {'out_string': '*K-**', 'tiebreaker': (13, 9)},
        {'out_string': '*A-*A', 'tiebreaker': (14, 9)}
    ]


@fixture
def out_scenarios_two_pair_006():
    return [
        {'out_string': '*3-*3-*2-*2-**', 'tiebreaker': (3, 2)}, {'out_string': '*4-*4-*2-*2-**', 'tiebreaker': (4, 2)},
        {'out_string': '*5-*5-*2-*2-**', 'tiebreaker': (5, 2)}, {'out_string': '*6-*6-*2-*2-**', 'tiebreaker': (6, 2)},
        {'out_string': '*7-*2-*2-**-**', 'tiebreaker': (7, 2)}, {'out_string': '*8-*8-*2-*2-**', 'tiebreaker': (8, 2)},
        {'out_string': '*9-*2-*2-**-**', 'tiebreaker': (9, 2)}, {'out_string': '*T-*T-*2-*2-**', 'tiebreaker': (10, 2)},
        {'out_string': '*J-*J-*2-*2-**', 'tiebreaker': (11, 2)}, {'out_string': '*Q-*Q-*2-*2-**', 'tiebreaker': (12, 2)},
        {'out_string': '*K-*K-*2-*2-**', 'tiebreaker': (13, 2)}, {'out_string': '*A-*A-*2-*2-**', 'tiebreaker': (14, 2)},
        {'out_string': '*4-*4-*3-*3-**', 'tiebreaker': (4, 3)}, {'out_string': '*5-*5-*3-*3-**', 'tiebreaker': (5, 3)},
        {'out_string': '*6-*6-*3-*3-**', 'tiebreaker': (6, 3)}, {'out_string': '*7-*3-*3-**-**', 'tiebreaker': (7, 3)},
        {'out_string': '*8-*8-*3-*3-**', 'tiebreaker': (8, 3)}, {'out_string': '*9-*3-*3-**-**', 'tiebreaker': (9, 3)},
        {'out_string': '*T-*T-*3-*3-**', 'tiebreaker': (10, 3)}, {'out_string': '*J-*J-*3-*3-**', 'tiebreaker': (11, 3)},
        {'out_string': '*Q-*Q-*3-*3-**', 'tiebreaker': (12, 3)}, {'out_string': '*K-*K-*3-*3-**', 'tiebreaker': (13, 3)},
        {'out_string': '*A-*A-*3-*3-**', 'tiebreaker': (14, 3)}, {'out_string': '*5-*5-*4-*4-**', 'tiebreaker': (5, 4)},
        {'out_string': '*6-*6-*4-*4-**', 'tiebreaker': (6, 4)}, {'out_string': '*7-*4-*4-**-**', 'tiebreaker': (7, 4)},
        {'out_string': '*8-*8-*4-*4-**', 'tiebreaker': (8, 4)}, {'out_string': '*9-*4-*4-**-**', 'tiebreaker': (9, 4)},
        {'out_string': '*T-*T-*4-*4-**', 'tiebreaker': (10, 4)}, {'out_string': '*J-*J-*4-*4-**', 'tiebreaker': (11, 4)},
        {'out_string': '*Q-*Q-*4-*4-**', 'tiebreaker': (12, 4)}, {'out_string': '*K-*K-*4-*4-**', 'tiebreaker': (13, 4)},
        {'out_string': '*A-*A-*4-*4-**', 'tiebreaker': (14, 4)}, {'out_string': '*6-*6-*5-*5-**', 'tiebreaker': (6, 5)},
        {'out_string': '*7-*5-*5-**-**', 'tiebreaker': (7, 5)}, {'out_string': '*8-*8-*5-*5-**', 'tiebreaker': (8, 5)},
        {'out_string': '*9-*5-*5-**-**', 'tiebreaker': (9, 5)}, {'out_string': '*T-*T-*5-*5-**', 'tiebreaker': (10, 5)},
        {'out_string': '*J-*J-*5-*5-**', 'tiebreaker': (11, 5)}, {'out_string': '*Q-*Q-*5-*5-**', 'tiebreaker': (12, 5)},
        {'out_string': '*K-*K-*5-*5-**', 'tiebreaker': (13, 5)}, {'out_string': '*A-*A-*5-*5-**', 'tiebreaker': (14, 5)},
        {'out_string': '*7-*6-*6-**-**', 'tiebreaker': (7, 6)}, {'out_string': '*8-*8-*6-*6-**', 'tiebreaker': (8, 6)},
        {'out_string': '*9-*6-*6-**-**', 'tiebreaker': (9, 6)}, {'out_string': '*T-*T-*6-*6-**', 'tiebreaker': (10, 6)},
        {'out_string': '*J-*J-*6-*6-**', 'tiebreaker': (11, 6)}, {'out_string': '*Q-*Q-*6-*6-**', 'tiebreaker': (12, 6)},
        {'out_string': '*K-*K-*6-*6-**', 'tiebreaker': (13, 6)}, {'out_string': '*A-*A-*6-*6-**', 'tiebreaker': (14, 6)},
        {'out_string': '*8-*8-*7-**-**', 'tiebreaker': (8, 7)}, {'out_string': '*9-*7-**-**-**', 'tiebreaker': (9, 7)},
        {'out_string': '*T-*T-*7-**-**', 'tiebreaker': (10, 7)}, {'out_string': '*J-*J-*7-**-**', 'tiebreaker': (11, 7)},
        {'out_string': '*Q-*Q-*7-**-**', 'tiebreaker': (12, 7)}, {'out_string': '*K-*K-*7-**-**', 'tiebreaker': (13, 7)},
        {'out_string': '*A-*A-*7-**-**', 'tiebreaker': (14, 7)}, {'out_string': '*9-*8-*8-**-**', 'tiebreaker': (9, 8)},
        {'out_string': '*T-*T-*8-*8-**', 'tiebreaker': (10, 8)}, {'out_string': '*J-*J-*8-*8-**', 'tiebreaker': (11, 8)},
        {'out_string': '*Q-*Q-*8-*8-**', 'tiebreaker': (12, 8)}, {'out_string': '*K-*K-*8-*8-**', 'tiebreaker': (13, 8)},
        {'out_string': '*A-*A-*8-*8-**', 'tiebreaker': (14, 8)}, {'out_string': '*T-*T-*9-**-**', 'tiebreaker': (10, 9)},
        {'out_string': '*J-*J-*9-**-**', 'tiebreaker': (11, 9)}, {'out_string': '*Q-*Q-*9-**-**', 'tiebreaker': (12, 9)},
        {'out_string': '*K-*K-*9-**-**', 'tiebreaker': (13, 9)}, {'out_string': '*A-*A-*9-**-**', 'tiebreaker': (14, 9)},
        {'out_string': '*J-*J-*T-*T-**', 'tiebreaker': (11, 10)}, {'out_string': '*Q-*Q-*T-*T-**', 'tiebreaker': (12, 10)},
        {'out_string': '*K-*K-*T-*T-**', 'tiebreaker': (13, 10)}, {'out_string': '*A-*A-*T-*T-**', 'tiebreaker': (14, 10)},
        {'out_string': '*Q-*Q-*J-*J-**', 'tiebreaker': (12, 11)}, {'out_string': '*K-*K-*J-*J-**', 'tiebreaker': (13, 11)},
        {'out_string': '*A-*A-*J-*J-**', 'tiebreaker': (14, 11)}, {'out_string': '*K-*K-*Q-*Q-**', 'tiebreaker': (13, 12)},
        {'out_string': '*A-*A-*Q-*Q-**', 'tiebreaker': (14, 12)}, {'out_string': '*A-*A-*K-*K-**', 'tiebreaker': (14, 13)}
    ]


@fixture
def out_scenarios_two_pair_007():
    return [{'out_string': '*3', 'tiebreaker': (9, 3)}, {'out_string': '*K', 'tiebreaker': (13, 9)}]


@fixture
def out_scenarios_pair_001():
    return [
        {'out_string': '*2', 'tiebreaker': 2}, {'out_string': '*3', 'tiebreaker': 3},
        {'out_string': '*4', 'tiebreaker': 4}, {'out_string': '*8', 'tiebreaker': 8},
        {'out_string': '*K', 'tiebreaker': 13}, {'out_string': '*A', 'tiebreaker': 14}
    ]


@fixture
def out_scenarios_pair_002():
    return [
        {'out_string': '*2-*2-**-**-**', 'tiebreaker': 2}, {'out_string': '*3-**-**-**-**', 'tiebreaker': 3},
        {'out_string': '*4-*4-**-**-**', 'tiebreaker': 4}, {'out_string': '*5-**-**-**-**', 'tiebreaker': 5},
        {'out_string': '*6-*6-**-**-**', 'tiebreaker': 6}, {'out_string': '*7-*7-**-**-**', 'tiebreaker': 7},
        {'out_string': '*8-*8-**-**-**', 'tiebreaker': 8}, {'out_string': '*9-*9-**-**-**', 'tiebreaker': 9},
        {'out_string': '*T-*T-**-**-**', 'tiebreaker': 10}, {'out_string': '*J-*J-**-**-**', 'tiebreaker': 11},
        {'out_string': '*Q-*Q-**-**-**', 'tiebreaker': 12}, {'out_string': '*K-*K-**-**-**', 'tiebreaker': 13},
        {'out_string': '*A-*A-**-**-**', 'tiebreaker': 14}
    ]


@fixture
def out_scenarios_pair_003():
    return [
        {'out_string': '*8-**', 'tiebreaker': 8}, {'out_string': '*9-*9', 'tiebreaker': 9},
        {'out_string': '*T-**', 'tiebreaker': 10}, {'out_string': '*J-*J', 'tiebreaker': 11},
        {'out_string': '*Q-*Q', 'tiebreaker': 12}, {'out_string': '*K-*K', 'tiebreaker': 13},
        {'out_string': '*A-*A', 'tiebreaker': 14}
    ]


@fixture
def out_scenarios_pair_004():
    return [
        {'out_string': '*T', 'tiebreaker': 10}
    ]


@fixture
def out_scenarios_high_card_001():
    return [{'out_string': '*K', 'tiebreaker': 13}, {'out_string': '*A', 'tiebreaker': 14}]


@fixture
def out_scenarios_high_card_002():
    return [
        {'out_string': '*Q-**-**-**-**', 'tiebreaker': 12}, {'out_string': '*K-**-**-**-**', 'tiebreaker': 13},
        {'out_string': '*A-**-**-**-**', 'tiebreaker': 14}
    ]


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


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["S8", "ST"], ["C2", "S9", "H4", "S7"], ["S8", "ST", "C2", "S9", "S7"], "out_scenarios_straight_flush_001"),
    (["S7", "ST"], ["C2", "S9", "S6"], ["S7", "ST", "C2", "S9", "S6"], "out_scenarios_straight_flush_002"),
    (["S7", "H4"], [], ["S7", "H4"], "out_scenarios_straight_flush_003"),
    (["S7", "H4"], ["H5", "HA", "C3"], ["S7", "H4", "H5", "HA", "C3"], "out_scenarios_straight_flush_004"),
    (["H7", "H4"], ["H5", "H6", "H8"], ["H7", "H4", "H5", "H6", "H8"], "out_scenarios_straight_flush_005"),
    (["S7", "H4"], ["H5", "SA", "C3"], ["S7", "H4", "H5", "SA", "C3"], "out_scenarios_none"),
    (["CK", "DT"], ["D9", "D7", "D6"], ["CK", "DT", "D9", "D7", "D6", "D8"], "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_straight_flush_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Straight Flush", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["H4", "C4"], ["S5", "C2", "DK"], ["H4", "C4", "S5", "C2", "DK"], "out_scenarios_quads_001"),
    (["H4", "C4"], ["S5", "D5", "DK"], ["H4", "C4", "S5", "D5", "DK"], "out_scenarios_quads_002"),
    (["H4", "C4"], ["S4", "D5", "DK"], ["H4", "C4", "S4", "D5", "DK"], "out_scenarios_quads_003"),
    (["HK", "CA"], [], ["HK", "CA"], "out_scenarios_quads_004"),
    (["H7", "C7"], ["S7", "D5", "DK", "SK"], ["H7", "C7", "S7", "D5", "DK", "SK"], "out_scenarios_quads_005"),
    (["HK", "CA"], ["CK", "DA", "D8", "C7"], ["HK", "CA", "CK", "DA", "D8", "C7"], "out_scenarios_none"),
    (["HK", "CA"], ["CK", "DA", "D8"], ["HK", "CK", "DK", "CA", "DA", "SA", "D8"], "out_scenarios_none"),
    (["HK", "CK"], ["DK", "SK", "D8"], ["HK", "CK", "DK", "SK", "D8"], "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_quads_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Quads", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["HK", "DA"], ["CK", "SA", "C7", "D9"], ["HK", "DA", "CK", "SA", "C7", "D9"], "out_scenarios_full_house_001"),
    (["HK", "DK"], ["CK", "SA", "C7", "D4"], ["HK", "DK", "CK", "SA", "C7", "D4"], "out_scenarios_full_house_002"),
    (["HK", "DK"], ["C9", "S9", "C7", "D7"], ["HK", "DK", "C9", "S9", "C7", "D7"], "out_scenarios_full_house_003"),
    (["HK", "DK"], ["CK", "S7", "C7", "C9"], ["HK", "DK", "CK", "S7", "C7", "C9"], "out_scenarios_full_house_004"),
    (["H7", "D7"], ["C7", "SQ", "C5"], ["H7", "D7", "C7", "SQ", "C5"], "out_scenarios_full_house_005"),
    (["HQ", "DQ"], [], ["HQ", "DQ"], "out_scenarios_full_house_006"),
    (["HQ", "DQ"], ["SK", "D2", "H8"], ["HQ", "DQ", "SK", "D2", "H8"], "out_scenarios_full_house_007"),
    (["HQ", "DT"], ["SK", "D2", "H8"], ["HQ", "DT", "SK", "D2", "H8"], "out_scenarios_none"),
    (["HQ", "DT"], ["SK", "D2", "H8", "HK"], ["HQ", "DT", "SK", "D2", "H8", "HK"], "out_scenarios_none"),
    (["HQ", "DT"], ["SQ", "CT", "H8"], ["HQ", "DT", "SQ", "CT", "H8", "CQ", "DQ", "HT", "ST", "C8", "S8", "D8"],
     "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_full_house_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Full House", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["HQ", "DT"], ["HK", "D2", "H8"], ["HQ", "DT", "HK", "D2", "H8"], "out_scenarios_flush_001"),
    (["HQ", "HT"], ["HK", "D2", "H8"], ["HQ", "HT", "HK", "D2", "H8"], "out_scenarios_flush_002"),
    (["HQ", "DT"], ["HK", "D2", "H8", "H2"], ["HQ", "DT", "HK", "D2", "H8", "H2"], "out_scenarios_flush_003"),
    (["HQ", "HT"], [], ["HQ", "HT"], "out_scenarios_flush_004"),
    (["HJ", "H9"], ["H5", "H2", "H6"], ["HJ", "H9", "H5", "H2", "H6"], "out_scenarios_flush_005"),
    (["HJ", "C9"], ["S5", "D2", "C6"], ["HJ", "C9", "S5", "D2", "C6"], "out_scenarios_none"),
    (["HJ", "C9"], ["S5", "D2", "C6", "C2"], ["HJ", "C9", "S5", "D2", "C6", "C2"], "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_flush_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Flush", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["S8", "HT"], ["C2", "C9", "H4", "S7"], ["S8", "HT", "C2", "C9", "H4", "S7"], "out_scenarios_straight_001"),
    (["S7", "HT"], ["C2", "S9", "D6"], ["S7", "HT", "C2", "S9", "D6"], "out_scenarios_straight_002"),
    (["S7", "H4"], [], ["S7", "H4"], "out_scenarios_straight_003"),
    (["S7", "H4"], ["C5", "HA", "C3"], ["S7", "H4", "C5", "HA", "C3"], "out_scenarios_straight_004"),
    (["H7", "C4"], ["H5", "S6", "D8"], ["H7", "C4", "H5", "S6", "D8"], "out_scenarios_straight_005"),
    (["H7", "C4"], ["HK", "SJ", "DJ"], ["H7", "C4", "HK", "SJ", "DJ"], "out_scenarios_none"),
    (["H7", "C4"], ["H6", "S3", "DJ"], ["H7", "C4", "H6", "S3", "DJ", "S5", "C5", "H5", "D5"], "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_straight_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Straight", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["H3", "D3"], ["C2", "D2", "S9"], ["H3", "D3", "C2", "D2", "S9"], "out_scenarios_trips_001"),
    (["H3", "D7"], ["C2", "D9", "SK"], ["H3", "D7", "C2", "D9", "SK"], "out_scenarios_trips_002"),
    (["H7", "D7"], ["C7", "D6", "SK"], ["H7", "D7", "C7", "D6", "SK"], "out_scenarios_trips_003"),
    (["H7", "DA"], [], ["H7", "DA"], "out_scenarios_trips_004"),
    (["H7", "DA"], ["C2", "D5", "CQ", "ST"], ["H7", "DA", "C2", "D5", "CQ", "ST"], "out_scenarios_none"),
    (["H7", "D7"], ["C2", "D5", "CQ", "ST"], ["H7", "D7", "C2", "D5", "CQ", "ST", "C7", "S7"], "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_trips_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Trips", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["H9", "CJ"], ["D2", "S6", "HK"], ["H9", "CJ", "D2", "S6", "HK"], "out_scenarios_two_pair_001"),
    (["H9", "C9"], ["D2", "S6", "HK", "D8"], ["H9", "C9", "D2", "S6", "HK", "D8"], "out_scenarios_two_pair_002"),
    (["H6", "C6"], ["D2", "S8", "HK"], ["H6", "C6", "D2", "S8", "HK"], "out_scenarios_two_pair_003"),
    (["H9", "C9"], ["D6", "S6", "HK", "S4"], ["H9", "C9", "D6", "S6", "HK", "S4"], "out_scenarios_two_pair_004"),
    (["H9", "C9"], ["D8", "S8", "HK"], ["H9", "C9", "D8", "S8", "HK"], "out_scenarios_two_pair_005"),
    (["H9", "C7"], [], ["H9", "C7"], "out_scenarios_two_pair_006"),
    (["H9", "C9"], ["D9", "S9", "HK", "S3"], ["H9", "C9", "D9", "S9", "HK", "S3"], "out_scenarios_two_pair_007"),
    (["H9", "C7"], ["D6", "S2", "HK", "SJ"], ["H9", "C7", "D6", "S2", "HK", "SJ"], "out_scenarios_none"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_two_pair_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Two Pair", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["C2", "D4"], ["H8", "CK", "CA", "D3"], ["C2", "D4", "H8", "CK", "CA", "D3"], "out_scenarios_pair_001"),
    (["D5", "H3"], [], ["D5", "H3"], "out_scenarios_pair_002"),
    (["D7", "H7"], ["C4", "S8", "DT"], ["D7", "H7" "C4", "S8", "DT"], "out_scenarios_pair_003"),
    (["D7", "H7"], ["C8", "S8", "DT", "C6"], ["D7", "H7", "C8", "S8", "DT", "C6"], "out_scenarios_pair_004"),
])
def test_when_find_outs_scenarios_and_texas_holdem_and_pair_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "Pair", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


@mark.parametrize("hole_cards, board_cards, non_available_cards, expected", [
    (["D7", "HQ"], ["C8", "S2", "DT", "C6"], ["D7", "HQ", "C8", "S2", "DT", "C6"], "out_scenarios_high_card_001"),
    (["D7", "HJ"], [], ["D7", "HJ"], "out_scenarios_high_card_002")
])
def test_when_find_outs_scenarios_and_texas_holdem_and_high_card_then_correct_out_scenarios_returned(
        hole_cards, board_cards, non_available_cards, expected, request
):
    hole_cards = [Card(card) for card in hole_cards]
    board_cards = [Card(card) for card in board_cards]
    available_cards = [card for card in Deck().cards_all if card.identity not in non_available_cards]
    expected = request.getfixturevalue(expected)
    actual = find_outs_scenarios(
        "Texas Holdem", "High Card", hole_cards=hole_cards, board_cards=board_cards, available_cards=available_cards
    )

    assert actual == expected


def test_when_tiebreak_outs_draw_and_bad_game_type_then_raise_error():
    with raises(ValueError, match="Game type provided 'BAD_GAME_TYPE' is not an acceptable value"):
        tiebreak_outs_draw("BAD_GAME_TYPE", "Straight Flush")


def test_when_tiebreak_outs_draw_and_bad_hand_type_then_raise_error():
    with raises(ValueError, match="Hand type provided 'WINNING_HAND_TYPE' is not an acceptable value"):
        tiebreak_outs_draw("Texas Holdem", "WINNING_HAND_TYPE")


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
def test_when_tiebreak_outs_draw_and_incorrect_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' does not contain all keys required for "
                                  f"this method"):
        tiebreak_outs_draw(game_type, hand_type, **kwargs)


@mark.parametrize("game_type, hand_type, kwargs", [
    ("Texas Holdem", "Straight Flush",
     {"tiebreakers": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Quads",
     {"tiebreakers": "BLAH", "hole_cards": "BLAH", "board_cards": "BLAH", "drawn_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Full House",
     {"tiebreakers": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Flush",
     {"tiebreakers": "BLAH", "hole_cards": "BLAH", "board_cards": "BLAH", "drawn_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Straight",
     {"tiebreakers": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Trips",
     {"tiebreakers": "BLAH", "hole_cards": "BLAH", "board_cards": "BLAH", "drawn_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Two Pair",
     {"tiebreakers": "BLAH", "hole_cards": "BLAH", "board_cards": "BLAH", "drawn_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "Pair",
     {"tiebreakers": "BLAH", "hole_cards": "BLAH", "board_cards": "BLAH", "drawn_cards": "BLAH", "DERP": "WHOOPS"}),
    ("Texas Holdem", "High Card",
     {"tiebreakers": "BLAH", "hole_cards": "BLAH", "board_cards": "BLAH", "drawn_cards": "BLAH", "DERP": "WHOOPS"}),
])
def test_when_tiebreak_outs_draw_and_too_many_kwargs_passed_then_raise_error(game_type, hand_type, kwargs):
    with raises(ValueError, match=f"Kwargs object '{kwargs}' contains additional keys from what is expected"):
        tiebreak_outs_draw(game_type, hand_type, **kwargs)


@mark.parametrize("tiebreakers, expected", [
    ("tb_dict_straight_flush_001", "player_b"),
    ("tb_dict_straight_flush_002", "TIE(player_a,player_c)"),
    ("tb_dict_straight_flush_003", "TIE(player_a,player_b,player_d)"),
    ("tb_dict_straight_flush_004", "TIE(player_a,player_b,player_c,player_d)")
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_straight_flush_then_correct_winner_returned(tiebreakers, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    actual = tiebreak_outs_draw("Texas Holdem", "Straight Flush", tiebreakers=tiebreakers)
    assert actual == expected


@mark.parametrize("tiebreakers, hole_cards, board_cards, drawn_cards, expected", [
    ("tb_dict_quads_001", "hole_tb_quads_001", "board_tb_quads_001", "draws_tb_quads_001", "player_a"),
    ("tb_dict_quads_002", "hole_tb_quads_002", "board_tb_quads_002", "draws_tb_quads_002", "player_c"),
    ("tb_dict_quads_002", "hole_tb_quads_003", "board_tb_quads_002", "draws_tb_quads_002", "TIE(player_a,player_c)"),
    ("tb_dict_quads_002", "hole_tb_quads_004", "board_tb_quads_002", "draws_tb_quads_002", "TIE(player_a,player_b,player_c)"),
    ("tb_dict_quads_002", "hole_tb_quads_002", "board_tb_quads_002", "draws_tb_quads_003", "TIE(player_a,player_b,player_c)"),
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_quads_then_correct_winner_returned(
        tiebreakers, hole_cards, board_cards, drawn_cards, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_hand(board_cards)
    drawn_cards = get_hand(drawn_cards)
    actual = tiebreak_outs_draw(
        "Texas Holdem", "Quads",
        tiebreakers=tiebreakers, hole_cards=hole_cards, board_cards=board_cards, drawn_cards=drawn_cards
    )
    assert actual == expected


@mark.parametrize("tiebreakers, expected", [
    ("tb_dict_full_house_001", "player_b"),
    ("tb_dict_full_house_002", "player_c"),
    ("tb_dict_full_house_003", "TIE(player_a,player_b)")
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_full_house_then_correct_winner_returned(tiebreakers, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    actual = tiebreak_outs_draw("Texas Holdem", "Full House", tiebreakers=tiebreakers)
    assert actual == expected


@mark.parametrize("tiebreakers, hole_cards, board_cards, drawn_cards, expected", [
    ("tb_dict_flush_001", "hole_tb_flush_001", "board_tb_flush_001", "draws_tb_flush_001", "player_a"),
    ("tb_dict_flush_001", "hole_tb_flush_002", "board_tb_flush_002", "draws_tb_flush_002", "player_b"),
    ("tb_dict_flush_001", "hole_tb_flush_003", "board_tb_flush_003", "draws_tb_flush_003", "player_c"),
    ("tb_dict_flush_001", "hole_tb_flush_004", "board_tb_flush_004", "draws_tb_flush_004", "player_a"),
    ("tb_dict_flush_001", "hole_tb_flush_005", "board_tb_flush_005", "draws_tb_flush_005", "player_b"),
    ("tb_dict_flush_001", "hole_tb_flush_006", "board_tb_flush_006", "draws_tb_flush_006", "player_c"),
    ("tb_dict_flush_001", "hole_tb_flush_007", "board_tb_flush_007", "draws_tb_flush_007", "player_a"),
    ("tb_dict_flush_001", "hole_tb_flush_008", "board_tb_flush_008", "draws_tb_flush_008", "player_b"),
    ("tb_dict_flush_001", "hole_tb_flush_009", "board_tb_flush_009", "draws_tb_flush_009", "TIE(player_a,player_b,player_c)"),
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_flush_then_correct_winner_returned(
        tiebreakers, hole_cards, board_cards, drawn_cards, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_hand(board_cards)
    drawn_cards = get_hand(drawn_cards)
    actual = tiebreak_outs_draw(
        "Texas Holdem", "Flush",
        tiebreakers=tiebreakers, hole_cards=hole_cards, board_cards=board_cards, drawn_cards=drawn_cards
    )
    assert actual == expected


@mark.parametrize("tiebreakers, expected", [
    ("tb_dict_straight_001", "player_a"),
    ("tb_dict_straight_002", "TIE(player_a,player_c)"),
    ("tb_dict_straight_003", "TIE(player_a,player_b,player_c)")
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_straight_then_correct_winner_returned(tiebreakers, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    actual = tiebreak_outs_draw("Texas Holdem", "Straight", tiebreakers=tiebreakers)
    assert actual == expected


@mark.parametrize("tiebreakers, hole_cards, board_cards, drawn_cards, expected", [
    ("tb_dict_trips_001", "hole_tb_trips_001", "board_tb_trips_001", "draws_tb_trips_001", "player_a"),  # win on tiebreaker alone
    ("tb_dict_trips_002", "hole_tb_trips_002", "board_tb_trips_002", "draws_tb_trips_002", "player_b"),  # all past tiebreaker, win on first kicker
    ("tb_dict_trips_002", "hole_tb_trips_003", "board_tb_trips_003", "draws_tb_trips_003", "player_c"),  # all past tiebreaker, win on second kicker
    ("tb_dict_trips_003", "hole_tb_trips_004", "board_tb_trips_004", "draws_tb_trips_004", "player_a"),  # subset past tiebreaker, player failing tiebreaker has bigger kicker
    ("tb_dict_trips_003", "hole_tb_trips_005", "board_tb_trips_005", "draws_tb_trips_005", "TIE(player_a,player_c)"),  # tie
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_trips_then_correct_winner_returned(
        tiebreakers, hole_cards, board_cards, drawn_cards, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_hand(board_cards)
    drawn_cards = get_hand(drawn_cards)
    actual = tiebreak_outs_draw(
        "Texas Holdem", "Trips",
        tiebreakers=tiebreakers, hole_cards=hole_cards, board_cards=board_cards, drawn_cards=drawn_cards
    )
    assert actual == expected


@mark.parametrize("tiebreakers, hole_cards, board_cards, drawn_cards, expected", [
    ("tb_dict_two_pair_001", "hole_tb_two_pair_001", "board_tb_two_pair_001", "draws_tb_two_pair_001", "player_a"),  # win on first tiebreaker
    ("tb_dict_two_pair_002", "hole_tb_two_pair_001", "board_tb_two_pair_001", "draws_tb_two_pair_001", "player_b"),
    # win on second tiebreaker tiebreaker
    ("tb_dict_two_pair_003", "hole_tb_two_pair_001", "board_tb_two_pair_001", "draws_tb_two_pair_001", "player_c"),
    # win on kicker.
    ("tb_dict_two_pair_003", "hole_tb_two_pair_002", "board_tb_two_pair_002", "draws_tb_two_pair_002", "TIE(player_b,player_c)"),
    # tie
    ("tb_dict_two_pair_003", "hole_tb_two_pair_002", "board_tb_two_pair_003", "draws_tb_two_pair_003", "TIE(player_a,player_b,player_c)"),
    # tie
    ("tb_dict_two_pair_004", "hole_tb_two_pair_003", "board_tb_two_pair_002", "draws_tb_two_pair_002", "player_b"),
    # two plays throuhg to kickers, player missing tiebreaker would have better kicker
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_two_pair_then_correct_winner_returned(
        tiebreakers, hole_cards, board_cards, drawn_cards, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_hand(board_cards)
    drawn_cards = get_hand(drawn_cards)
    actual = tiebreak_outs_draw(
        "Texas Holdem", "Two Pair",
        tiebreakers=tiebreakers, hole_cards=hole_cards, board_cards=board_cards, drawn_cards=drawn_cards
    )
    assert actual == expected


@mark.parametrize("tiebreakers, hole_cards, board_cards, drawn_cards, expected", [
    ("tb_dict_pair_001", "hole_tb_pair_001", "board_tb_pair_001", "draws_tb_pair_001", "player_a"),  # win on tiebreaker
    ("tb_dict_pair_002", "hole_tb_pair_001", "board_tb_pair_001", "draws_tb_pair_001", "player_b"),  # win on first kicker
    ("tb_dict_pair_002", "hole_tb_pair_001", "board_tb_pair_002", "draws_tb_pair_001", "player_b"),  # win on second kicker
    ("tb_dict_pair_002", "hole_tb_pair_001", "board_tb_pair_003", "draws_tb_pair_001", "player_b"),  # win on third kicker
    ("tb_dict_pair_002", "hole_tb_pair_001", "board_tb_pair_004", "draws_tb_pair_001", "TIE(player_a,player_b,player_c)"),  # tie
    ("tb_dict_pair_003", "hole_tb_pair_001", "board_tb_pair_002", "draws_tb_pair_001", "player_c"),  # player_b lost on tiebreaker but had better kicker
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_pair_then_correct_winner_returned(
        tiebreakers, hole_cards, board_cards, drawn_cards, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_hand(board_cards)
    drawn_cards = get_hand(drawn_cards)
    actual = tiebreak_outs_draw(
        "Texas Holdem", "Pair",
        tiebreakers=tiebreakers, hole_cards=hole_cards, board_cards=board_cards, drawn_cards=drawn_cards
    )
    assert actual == expected


@mark.parametrize("tiebreakers, hole_cards, board_cards, drawn_cards, expected", [
    ("tb_dict_high_card_001", "hole_tb_high_card_001", "board_tb_high_card_001", "draws_tb_high_card_001", "player_a"),  # win on second kicker
    ("tb_dict_high_card_001", "hole_tb_high_card_001", "board_tb_high_card_002", "draws_tb_high_card_001", "player_a"),  # win on third kicker
    ("tb_dict_high_card_001", "hole_tb_high_card_001", "board_tb_high_card_003", "draws_tb_high_card_001", "player_a"),  # win on fourth kicker
    ("tb_dict_high_card_001", "hole_tb_high_card_001", "board_tb_high_card_004", "draws_tb_high_card_001", "player_a"),  # win on fifth kicker
    ("tb_dict_high_card_001", "hole_tb_high_card_001", "board_tb_high_card_005", "draws_tb_high_card_001", "TIE(player_a,player_b)")  # tie
])
def test_when_tiebreak_outs_draw_and_texas_holdem_and_high_card_then_correct_winner_returned(
        tiebreakers, hole_cards, board_cards, drawn_cards, expected):
    tiebreakers = get_tiebreaker_dict(tiebreakers)
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_hand(board_cards)
    drawn_cards = get_hand(drawn_cards)
    actual = tiebreak_outs_draw(
        "Texas Holdem", "High Card",
        tiebreakers=tiebreakers, hole_cards=hole_cards, board_cards=board_cards, drawn_cards=drawn_cards
    )
    assert actual == expected
