from pypoker.deck import Card


def get_card(descriptor: str):
    """
    test helper method to return a single card object

    :param descriptor: Str describing which card you want.
        First character of the descriptor represents the suit of the card (H, S, D, C)
        Remaining characters describe the value (A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2)

    :return: Card object
    """

    suit = descriptor[0]
    value = descriptor[1:]
    if value.isdigit():
        value = int(value)

    return Card(value, suit)


def get_hand(hand_name):
    """
    test helper method to return a set of cards.

    :param hand_name: Str representing the hand to return
    :return: List[Card] representing a players hand
    """

    cards = {
        "hole_cards_001": ["H10", "D7"],
        "hole_cards_straight_flush_001": ["DA", "DJ"],
        "hole_cards_straight_flush_002": ["SA", "H7"],
        "hole_cards_straight_flush_003": ["SK", "H9"],
        "hole_cards_straight_flush_004": ["DQ", "D7"],
        "hole_cards_straight_flush_005": ["HJ", "DA"],
        "hole_cards_straight_flush_006": ["D8", "D4"],
        "hole_cards_straight_flush_007": ["CJ", "C2"],
        "hole_cards_straight_flush_008": ["SA", "S5"],
        "hole_cards_quads_001": ["S4", "D4"],
        "hole_cards_quads_002": ["CQ", "D4"],
        "hole_cards_quads_003": ["S9", "S8"],
        "hole_cards_quads_004": ["CQ", "D4"],
        "hole_cards_full_house_001": ["SK", "D9"],
        "hole_cards_full_house_002": ["D10", "C4"],
        "hole_cards_full_house_003": ["D10", "C4"],
        "hole_cards_full_house_004": ["C10", "S4"],
        "hole_cards_full_house_005": ["D10", "D9"],
        "hole_cards_flush_001": ["H4", "HK"],
        "hole_cards_flush_002": ["H4", "S3"],
        "hole_cards_flush_003": ["D10", "S3"],
        "hole_cards_flush_004": ["D7", "S7"],
        "hole_cards_flush_005": ["D7", "S9"],
        "hole_cards_flush_006": ["D7", "S10"],
        "hole_cards_flush_007": ["D6", "S10"],
        "hole_cards_straight_001": ["D8", "SJ"],
        "hole_cards_straight_002": ["HA", "SJ"],
        "hole_cards_straight_003": ["HA", "S2"],
        "hole_cards_straight_004": ["H10", "S10"],
        "hole_cards_straight_005": ["HJ", "S10"],
        "hole_cards_straight_006": ["H2", "S10"],
        "hole_cards_straight_007": ["HA", "S5"],
        "hole_cards_trips_001": ["S9", "DK"],
        "hole_cards_trips_002": ["H3", "DK"],
        "hole_cards_trips_003": ["H3", "H4"],
        "hole_cards_two_pair_001": ["H7", "D9"],
        "hole_cards_two_pair_002": ["H2", "D9"],
        "hole_cards_two_pair_003": ["H2", "D4"],
        "hole_cards_two_pair_004": ["C6", "D4"],
        "hole_cards_pair_001": ["H7", "D7"],
        "hole_cards_pair_002": ["H2", "D7"],
        "hole_cards_pair_003": ["H2", "H4"],
        "hole_cards_high_card_001": ["H9", "CJ"],
        "hole_cards_high_card_002": ["H9", "C2"],
        "hole_cards_high_card_003": ["H3", "C2"],

        "board_cards_001": ["S2", "S3", "DK", "CQ", "S8"],
        "board_cards_002": ["S2", "S3", "DK", "CQ"],
        "board_cards_003": ["S2", "S3", "DK"],
        "board_cards_straight_flush_001": ["DK", "S7", "D10", "C2", "DQ"],
        "board_cards_straight_flush_002": ["DK", "H8", "H10", "H6", "H9"],
        "board_cards_straight_flush_003": ["C4", "C6", "C3", "C7", "C5"],
        "board_cards_straight_flush_004": ["D8", "DK", "D9", "DJ", "D10"],
        "board_cards_straight_flush_005": ["H10", "SA", "HA", "HK", "HQ"],
        "board_cards_straight_flush_006": ["H4", "D6", "D7", "S8", "D5"],
        "board_cards_straight_flush_007": ["D2", "C8", "C9", "C10", "C7"],
        "board_cards_straight_flush_008": ["S4", "DA", "D5", "S2", "S3"],
        "board_cards_quads_001": ["C4", "H4", "D9", "D8", "HQ"],
        "board_cards_quads_002": ["HQ", "DQ", "D8", "SQ", "HJ"],
        "board_cards_quads_003": ["DQ", "HJ", "SQ", "CQ", "HQ"],
        "board_cards_quads_004": ["DQ", "HJ", "S4", "SQ", "HQ"],
        "board_cards_full_house_001": ["HK", "HJ", "D4", "C9", "S9"],
        "board_cards_full_house_002": ["S4", "HJ", "DJ", "D4", "SA"],
        "board_cards_full_house_003": ["DQ", "CQ", "CJ", "SQ", "HJ"],
        "board_cards_full_house_004": ["D10", "DK", "S10", "H4", "D4"],
        "board_cards_full_house_005": ["C10", "S10", "H4", "S4", "H9"],
        "board_cards_flush_001": ["D2", "H9", "H7", "H8", "SA"],
        "board_cards_flush_002": ["HK", "H9", "H7", "H8", "SA"],
        "board_cards_flush_003": ["HK", "H9", "H7", "H8", "H4"],
        "board_cards_flush_004": ["HK", "H9", "H7", "H8", "H4"],
        "board_cards_flush_005": ["HK", "H9", "H7", "H8", "H4"],
        "board_cards_flush_006": ["HK", "H9", "H7", "H8", "H4"],
        "board_cards_flush_007": ["HK", "H9", "H7", "H8", "H4"],
        "board_cards_straight_001": ["C10", "D9", "SK", "H4", "C7"],
        "board_cards_straight_002": ["C10", "D9", "D8", "H4", "C7"],
        "board_cards_straight_003": ["C10", "D9", "SJ", "D8", "C7"],
        "board_cards_straight_004": ["C10", "D9", "SJ", "D8", "C7"],
        "board_cards_straight_005": ["C10", "D9", "SJ", "D8", "C7"],
        "board_cards_straight_006": ["C10", "D9", "SJ", "D8", "C7"],
        "board_cards_straight_007": ["C2", "D4", "D9", "C9", "C3"],
        "board_cards_trips_001": ["D4", "H8", "H2", "CK", "SK"],
        "board_cards_trips_002": ["D4", "H8", "S9", "CK", "SK"],
        "board_cards_trips_003": ["DK", "H8", "S9", "CK", "SK"],
        "board_cards_two_pair_001": ["S10", "H4", "S2", "C9", "S7"],
        "board_cards_two_pair_002": ["S10", "H4", "S7", "C9", "H7"],
        "board_cards_two_pair_003": ["S10", "H7", "D9", "C9", "S7"],
        "board_cards_two_pair_004": ["H6", "H7", "D9", "C9", "S7"],
        "board_cards_pair_001": ["S10", "H4", "D2", "D8", "CA"],
        "board_cards_pair_002": ["H7", "H4", "S10", "D8", "CA"],
        "board_cards_pair_003": ["H7", "D7", "S10", "D8", "CA"],
        "board_cards_high_card_001": ["S6", "D4", "H8", "H3", "C2"],
        "board_cards_high_card_002": ["S6", "D4", "H8", "H3", "CJ"],
        "board_cards_high_card_003": ["S6", "D4", "H8", "H9", "CJ"],

        "hand_0001": ["S10", "S5", "S4", "SK", "S2"],
        "hand_0002": ["S10", "H5", "S4", "SK", "S2"],
        "hand_0003": ["S10", "S7", "H8", "DJ", "S9"],
        "hand_0004": ["S10", "S7", "H8", "DQ", "S9"],
        "hand_straight_flush_001": ["DA", "DK", "DQ", "DJ", "D10"],
        "hand_straight_flush_002": ["H10", "H9", "H8", "H7", "H6"],
        "hand_straight_flush_003": ["C7", "C6", "C5", "C4", "C3"],
        "hand_straight_flush_004": ["DK", "DQ", "DJ", "D10", "D9"],
        "hand_straight_flush_005": ["HA", "HK", "HQ", "HJ", "H10"],
        "hand_straight_flush_006": ["D8", "D7", "D6", "D5", "D4"],
        "hand_straight_flush_007": ["CJ", "C10", "C9", "C8", "C7"],
        "hand_straight_flush_008": ["SA", "S5", "S4", "S3", "S2"],
        "hand_quads_001": ["HQ", "S4", "D4", "C4", "H4"],
        "hand_quads_002": ["HQ", "DQ", "SQ", "CQ", "HJ"],
        "hand_quads_003": ["HQ", "DQ", "SQ", "CQ", "HJ"],
        "hand_quads_004": ["HQ", "DQ", "SQ", "CQ", "HJ"],
        "hand_full_house_001": ["HK", "SK", "D9", "C9", "S9"],
        "hand_full_house_002": ["HJ", "DJ", "D4", "S4", "C4"],
        "hand_full_house_003": ["DQ", "CQ", "SQ", "HJ", "CJ"],
        "hand_full_house_004": ["D10", "C10", "S10", "H4", "S4"],
        "hand_full_house_005": ["D10", "C10", "S10", "H9", "D9"],
        "hand_flush_001": ["H4", "HK", "H9", "H7", "H8"],
        "hand_flush_002": ["H4", "HK", "H9", "H7", "H8"],
        "hand_flush_003": ["H4", "HK", "H9", "H7", "H8"],
        "hand_flush_004": ["H4", "HK", "H9", "H7", "H8"],
        "hand_flush_005": ["H4", "HK", "H9", "H7", "H8"],
        "hand_flush_006": ["H4", "HK", "H9", "H7", "H8"],
        "hand_flush_007": ["H4", "HK", "H9", "H7", "H8"],
        "hand_straight_001": ["D8", "SJ", "C10", "D9", "C7"],
        "hand_straight_002": ["D8", "SJ", "C10", "D9", "C7"],
        "hand_straight_003": ["D8", "SJ", "C10", "D9", "C7"],
        "hand_straight_004": ["D8", "SJ", "H10", "D9", "C7"],
        "hand_straight_005": ["D8", "HJ", "S10", "D9", "C7"],
        "hand_straight_006": ["D8", "SJ", "S10", "D9", "C7"],
        "hand_straight_007": ["HA", "S5", "D4", "C3", "C2"],
        "hand_trips_001": ["S9", "H8", "DK", "CK", "SK"],
        "hand_trips_002": ["S9", "H8", "DK", "CK", "SK"],
        "hand_trips_003": ["S9", "H8", "DK", "CK", "SK"],
        "hand_two_pair_001": ["S10", "H7", "D9", "C9", "S7"],
        "hand_two_pair_002": ["S10", "H7", "D9", "C9", "S7"],
        "hand_two_pair_003": ["S10", "H7", "D9", "C9", "S7"],
        "hand_two_pair_004": ["H7", "D9", "C9", "S7", "C6"],
        "hand_pair_001": ["S10", "H7", "D8", "D7", "CA"],
        "hand_pair_002": ["S10", "H7", "D8", "D7", "CA"],
        "hand_pair_003": ["S10", "H7", "D8", "D7", "CA"],
        "hand_high_card_001": ["S6", "D4", "H8", "H9", "CJ"],
        "hand_high_card_002": ["S6", "D4", "H8", "H9", "CJ"],
        "hand_high_card_003": ["S6", "D4", "H8", "H9", "CJ"],
    }[hand_name]

    return [get_card(descriptors) for descriptors in cards]


def get_hand_sets(hand_name):
    """
    test helper method to return a set of hands, each containing a set of cards.

    :param hand_name: Str representing the hand to return
    :return: List[Card] representing a players hand
    """

    hand_sets = {
        "combos_001": [
            ['H10', 'D7', 'S2', 'S3', 'DK'], ['H10', 'D7', 'S2', 'S3', 'CQ'], ['H10', 'D7', 'S2', 'S3', 'S8'],
            ['H10', 'D7', 'S2', 'DK', 'CQ'], ['H10', 'D7', 'S2', 'DK', 'S8'], ['H10', 'D7', 'S2', 'CQ', 'S8'],
            ['H10', 'D7', 'S3', 'DK', 'CQ'], ['H10', 'D7', 'S3', 'DK', 'S8'], ['H10', 'D7', 'S3', 'CQ', 'S8'],
            ['H10', 'D7', 'DK', 'CQ', 'S8'], ['H10', 'S2', 'S3', 'DK', 'CQ'], ['H10', 'S2', 'S3', 'DK', 'S8'],
            ['H10', 'S2', 'S3', 'CQ', 'S8'], ['H10', 'S2', 'DK', 'CQ', 'S8'], ['H10', 'S3', 'DK', 'CQ', 'S8'],
            ['D7', 'S2', 'S3', 'DK', 'CQ'], ['D7', 'S2', 'S3', 'DK', 'S8'], ['D7', 'S2', 'S3', 'CQ', 'S8'],
            ['D7', 'S2', 'DK', 'CQ', 'S8'], ['D7', 'S3', 'DK', 'CQ', 'S8'], ['S2', 'S3', 'DK', 'CQ', 'S8']
        ],
        "combos_002": [
            ['H10', 'D7', 'S2', 'S3', 'DK'], ['H10', 'D7', 'S2', 'S3', 'CQ'], ['H10', 'D7', 'S2', 'DK', 'CQ'],
            ['H10', 'D7', 'S3', 'DK', 'CQ'], ['H10', 'S2', 'S3', 'DK', 'CQ'], ['D7', 'S2', 'S3', 'DK', 'CQ']
        ],
        "combos_003": [['H10', 'D7', 'S2', 'S3', 'DK']],
        "hand_set_0001": [
            ['H10', 'D7', 'S2', 'DK', 'CQ'], ['D7', 'S2', 'S3', 'DK', 'S8'], ['D7', 'S3', 'DK', 'H10', 'CQ'],
            ['DK', 'H10', 'S3', 'CQ', 'S8']
        ],
        "hand_set_0002": [
            ['DK', 'CQ', 'H10', 'S8', 'S3'], ['DK', 'CQ', 'H10', 'D7', 'S3'], ['DK', 'CQ', 'H10', 'D7', 'S2'],
            ['DK', 'S8', 'D7', 'S3', 'S2']
        ],

        "straight_flush_multi": [
            ["DK", "D10", "DJ", "D9", "DQ"], ["S4", "S6", "S8", "S5", "S7"], ["C9", "C10", "C6", "C8", "C7"],
            ["HA", "HJ", "HQ", "H10", "HK"], ["SA", "S3", "S4", "S2", "S5"]
        ],
        "straight_flush_multi_A": [["HA", "HJ", "HQ", "H10", "HK"]],
        "straight_flush_multi_B": [["DK", "D10", "DJ", "D9", "DQ"]],
        "straight_flush_multi_C": [["C9", "C10", "C6", "C8", "C7"]],
        "straight_flush_multi_D": [["S4", "S6", "S8", "S5", "S7"]],
        "straight_flush_multi_E": [["SA", "S3", "S4", "S2", "S5"]],

        "straight_flush_multi_tie": [
            ["DK", "D10", "DJ", "D9", "DQ"], ["CJ", "C9", "C7", "C10", "C8"], ["H9", "HJ", "H7", "H8", "H10"],
            ["SQ", "S10", "S9", "SK", "SJ"], ["D7", "D10", "DJ", "D9", "D8"]
        ],
        "straight_flush_multi_tie_A": [["DK", "D10", "DJ", "D9", "DQ"], ["SQ", "S10", "S9", "SK", "SJ"]],
        "straight_flush_multi_tie_B": [
            ["CJ", "C9", "C7", "C10", "C8"], ["H9", "HJ", "H7", "H8", "H10"], ["D7", "D10", "DJ", "D9", "D8"]
        ],

        "straight_flush_multi_tie_exact": [
            ["CJ", "C9", "C7", "C10", "C8"], ["C9", "C8", "C10", "CJ", "C7"], ["H9", "HJ", "HQ", "H8", "H10"]
        ],
        "straight_flush_multi_tie_exact_A": [["H9", "HJ", "HQ", "H8", "H10"]],
        "straight_flush_multi_tie_exact_B": [["CJ", "C9", "C7", "C10", "C8"], ["C9", "C8", "C10", "CJ", "C7"]],

        "straight_flush_multi_ace_low_straights": [
            ["DK", "D10", "DJ", "D9", "DQ"], ["SA", "S3", "S4", "S2", "S5"], ["CA", "C3", "C4", "C2", "C5"],
            ["HA", "H3", "H4", "H2", "H5"]
        ],
        "straight_flush_multi_ace_low_straights_A": [["DK", "D10", "DJ", "D9", "DQ"]],
        "straight_flush_multi_ace_low_straights_B": [
            ["HA", "H3", "H4", "H2", "H5"], ["CA", "C3", "C4", "C2", "C5"], ["SA", "S3", "S4", "S2", "S5"]
        ],

        "straight_flush_all_ace_low_straights": [
            ["SA", "S3", "S4", "S2", "S5"], ["CA", "C3", "C4", "C2", "C5"], ["HA", "H3", "H4", "H2", "H5"]
        ],
        "straight_flush_all_ace_low_straights_A": [
            ["HA", "H3", "H4", "H2", "H5"], ["CA", "C3", "C4", "C2", "C5"], ["SA", "S3", "S4", "S2", "S5"]
        ],

        "quads_multi": [
            ["H7", "S7", "C2", "D7", "C7"], ["S5", "H5", "D7", "C5", "D5"], ["H9", "C7", "H7", "S7", "D7"],
            ["DK", "SA", "SK", "CK", "HK"], ["D7", "S7", "H7", "DK", "C7"]
        ],
        "quads_multi_A": [["DK", "SA", "SK", "CK", "HK"]],
        "quads_multi_B": [["D7", "S7", "H7", "DK", "C7"]],
        "quads_multi_C": [["H9", "C7", "H7", "S7", "D7"]],
        "quads_multi_D": [["H7", "S7", "C2", "D7", "C7"]],
        "quads_multi_E": [["S5", "H5", "D7", "C5", "D5"]],

        "quads_multi_tie": [
            ["D7", "S7", "H7", "D4", "C7"], ["D7", "S7", "H7", "C4", "C7"], ["D7", "S7", "H7", "S9", "C7"],
            ["D7", "S7", "H7", "H9", "C7"]
        ],
        "quads_multi_tie_A": [["D7", "S7", "H7", "S9", "C7"], ["D7", "S7", "H7", "H9", "C7"]],
        "quads_multi_tie_B": [["D7", "S7", "H7", "D4", "C7"], ["D7", "S7", "H7", "C4", "C7"]],

        "quads_multi_tie_exact": [["D7", "S7", "H7", "D4", "C7"], ["D7", "D4", "C7", "S7", "H7"]],

        "full_house_multi": [
            ["S2", "C3", "H3", "D2", "H2"], ["DK", "S9", "C9", "HK", "SK"], ["DK", "C7", "SK", "S7", "CK"],
            ["DA", "S2", "C2", "HA", "SA"], ["DQ", "SA", "CA", "HQ", "SQ"],
        ],
        "full_house_multi_A": [["DA", "S2", "C2", "HA", "SA"]],
        "full_house_multi_B": [["DK", "S9", "C9", "HK", "SK"]],
        "full_house_multi_C": [["DK", "C7", "SK", "S7", "CK"]],
        "full_house_multi_D": [["DQ", "SA", "CA", "HQ", "SQ"]],
        "full_house_multi_E": [["S2", "C3", "H3", "D2", "H2"]],

        "full_house_multi_tie": [
            ["HK", "SQ", "DQ", "CQ", "CK"], ["CQ", "CK", "SK", "HQ", "DQ"], ["CQ", "DK", "SK", "HQ", "SQ"],
            ["DA", "SA", "CA", "H4", "D4"], ["DA", "HA", "CA", "C4", "S4"]
        ],
        "full_house_multi_tie_A": [["DA", "SA", "CA", "H4", "D4"], ["DA", "HA", "CA", "C4", "S4"]],
        "full_house_multi_tie_B": [
            ["HK", "SQ", "DQ", "CQ", "CK"], ["CQ", "CK", "SK", "HQ", "DQ"], ["CQ", "DK", "SK", "HQ", "SQ"]
        ],

        "full_house_multi_tie_exact": [["DA", "SA", "CA", "H4", "D4"], ["CA", "SA", "D4", "H4", "DA"]],

        "flush_multi": [
            ["H6", "HA", "H5", "H7", "H9"], ["HA", "H9", "H7", "H4", "H3"], ["C9", "C6", "C7", "C4", "CA"],
            ["SJ", "SQ", "S6", "S7", "S10"], ["CA", "C7", "C2", "C4", "C3"]
        ],
        "flush_multi_A": [["H6", "HA", "H5", "H7", "H9"]],
        "flush_multi_B": [["C9", "C6", "C7", "C4", "CA"]],
        "flush_multi_C": [["HA", "H9", "H7", "H4", "H3"]],
        "flush_multi_D": [["CA", "C7", "C2", "C4", "C3"]],
        "flush_multi_E": [["SJ", "SQ", "S6", "S7", "S10"]],

        "flush_multi_tie": [
            ["H4", "H10", "H9", "HQ", "H7"], ["S4", "SQ", "S7", "S10", "S9"], ["D7", "D4", "DA", "DK", "D10"],
            ["CK", "C10", "C7", "C4", "CA"]
        ],
        "flush_multi_tie_A": [["D7", "D4", "DA", "DK", "D10"], ["CK", "C10", "C7", "C4", "CA"]],
        "flush_multi_tie_B": [["H4", "H10", "H9", "HQ", "H7"], ["S4", "SQ", "S7", "S10", "S9"]],

        "flush_multi_tie_exact": [
            ["D7", "D4", "DA", "DK", "D10"], ["DQ", "D10", "D8", "D2", "D4"], ["DA", "DK", "D7", "D4", "D10"],
            ["DK", "D10", "D7", "D4", "DA"], ["DQ", "D10", "D8", "D2", "D4"]
        ],
        "flush_multi_tie_exact_A": [
            ["D7", "D4", "DA", "DK", "D10"], ["DA", "DK", "D7", "D4", "D10"], ["DK", "D10", "D7", "D4", "DA"]
        ],
        "flush_multi_tie_exact_B": [["DQ", "D10", "D8", "D2", "D4"], ["DQ", "D10", "D8", "D2", "D4"]],

        "straight_multi": [
            ["S7", "C10", "SJ", "H8", "C9"], ["DK", "D10", "SQ", "HJ", "S9"], ["SA", "H3", "C4", "D2", "S5"],
            ["S6", "H2", "H4", "S5", "S3"]
        ],
        "straight_multi_A": [["DK", "D10", "SQ", "HJ", "S9"]],
        "straight_multi_B": [["S7", "C10", "SJ", "H8", "C9"]],
        "straight_multi_C": [["S6", "H2", "H4", "S5", "S3"]],
        "straight_multi_D": [["SA", "H3", "C4", "D2", "S5"]],

        "straight_multi_tie": [
            ["H10", "HQ", "CJ", "C9", "D8"], ["C10", "CQ", "SJ", "S9", "H8"], ["S10", "SQ", "HJ", "H9", "S8"],
            ["H8", "C6", "S4", "D5", "D7"], ["C8", "S6", "H4", "D5", "S7"]
        ],
        "straight_multi_tie_A": [
            ["H10", "HQ", "CJ", "C9", "D8"], ["C10", "CQ", "SJ", "S9", "H8"], ["S10", "SQ", "HJ", "H9", "S8"]
        ],
        "straight_multi_tie_B": [["H8", "C6", "S4", "D5", "D7"], ["C8", "S6", "H4", "D5", "S7"]],

        "straight_multi_tie_exact": [["H10", "HQ", "CJ", "C9", "D8"], ["H10", "HQ", "CJ", "C9", "D8"]],

        "straight_multi_ace_low_straights": [
            ["SK", "D9", "D10", "SQ", "CJ"], ["SA", "H3", "C4", "D5", "H2"], ["HA", "C3", "S4", "S5", "S2"],
            ["DA", "S3", "H4", "H5", "D2"]
        ],
        "straight_multi_ace_low_straights_A": [["SK", "D9", "D10", "SQ", "CJ"]],
        "straight_multi_ace_low_straights_B": [
            ["DA", "S3", "H4", "H5", "D2"], ["HA", "C3", "S4", "S5", "S2"], ["SA", "H3", "C4", "D5", "H2"]
        ],

        "straight_all_ace_low_straights": [
            ["SA", "H3", "C4", "D5", "H2"], ["HA", "C3", "S4", "S5", "S2"], ["DA", "S3", "H4", "H5", "D2"]
        ],
        "straight_all_ace_low_straights_A": [
            ["DA", "S3", "H4", "H5", "D2"], ["HA", "C3", "S4", "S5", "S2"], ["SA", "H3", "C4", "D5", "H2"]
        ],

        "trips_multi": [
            ["S7", "C9", "D7", "H2", "H7"], ["H9", "S6", "C7", "D7", "H7"], ["D10", "D2", "D7", "C7", "H7"],
            ["D10", "S10", "SA", "S2", "H10"], ["C4", "S4", "C2", "H3", "D4"]
        ],
        "trips_multi_A": [["D10", "S10", "SA", "S2", "H10"]],
        "trips_multi_B": [["D10", "D2", "D7", "C7", "H7"]],
        "trips_multi_C": [["H9", "S6", "C7", "D7", "H7"]],
        "trips_multi_D": [["S7", "C9", "D7", "H2", "H7"]],
        "trips_multi_E": [["C4", "S4", "C2", "H3", "D4"]],

        "trips_multi_tie": [
            ["S7", "C9", "D7", "H2", "H7"], ["H7", "D9", "C7", "H2", "S7"], ["C7", "H9", "S7", "C2", "D7"]
        ],

        "trips_multi_tie_exact": [
            ["S7", "C9", "D7", "H2", "H7"], ["S7", "C9", "D7", "H2", "H7"], ["S7", "C9", "D7", "H2", "H7"]
        ],

        "two_pair_multi": [
            ["S9", "C4", "H4", "C9", "D7"], ["H9", "C4", "D4", "D9", "DJ"], ["H9", "C6", "D6", "D9", "DJ"],
            ["H9", "C2", "D2", "D9", "DJ"], ["HJ", "H2", "CJ", "D2", "S7"]
        ],
        "two_pair_multi_A": [["HJ", "H2", "CJ", "D2", "S7"]],
        "two_pair_multi_B": [["H9", "C6", "D6", "D9", "DJ"]],
        "two_pair_multi_C": [["H9", "C4", "D4", "D9", "DJ"]],
        "two_pair_multi_D": [["S9", "C4", "H4", "C9", "D7"]],
        "two_pair_multi_E": [["H9", "C2", "D2", "D9", "DJ"]],

        "two_pair_multi_tie": [
            ["S9", "C4", "H4", "C9", "D7"], ["C9", "D4", "S4", "H9", "H7"], ["H9", "C4", "D4", "D9", "DJ"],
            ["D9", "S4", "H4", "H9", "CJ"]
        ],
        "two_pair_multi_tie_A": [["H9", "C4", "D4", "D9", "DJ"], ["D9", "S4", "H4", "H9", "CJ"]],
        "two_pair_multi_tie_B": [["S9", "C4", "H4", "C9", "D7"], ["C9", "D4", "S4", "H9", "H7"]],

        "two_pair_multi_tie_exact": [["S9", "C4", "H4", "C9", "D7"], ["S9", "C4", "H4", "C9", "D7"]],

        "pair_multi": [
            ["H7", "D7", "SK", "S10", "S9"], ["C7", "S7", "HK", "S10", "S8"], ["S7", "C7", "CK", "H8", "H5"],
            ["D7", "C7", "SJ", "S8", "C3"], ["D10", "C10", "CJ", "H3", "D7"], ["H4", "D4", "HJ", "C9", "S2"]
        ],
        "pair_multi_A": [["D10", "C10", "CJ", "H3", "D7"]],
        "pair_multi_B": [["H7", "D7", "SK", "S10", "S9"]],
        "pair_multi_C": [["C7", "S7", "HK", "S10", "S8"]],
        "pair_multi_D": [["S7", "C7", "CK", "H8", "H5"]],
        "pair_multi_E": [["D7", "C7", "SJ", "S8", "C3"]],
        "pair_multi_F": [["H4", "D4", "HJ", "C9", "S2"]],

        "pair_multi_tie": [["H7", "D7", "SK", "S10", "S9"], ["C7", "S7", "HK", "H10", "C9"]],

        "pair_multi_tie_exact": [["H7", "D7", "SK", "S10", "S9"], ["H7", "D7", "SK", "S10", "S9"]],

        "high_card_multi": [
            ["HK", "SQ", "C4", "C7", "H9"], ["HK", "SQ", "C2", "C7", "H9"], ["HK", "SQ", "C4", "C6", "H9"]
        ],
        "high_card_multi_A": [["HK", "SQ", "C4", "C7", "H9"]],
        "high_card_multi_B": [["HK", "SQ", "C2", "C7", "H9"]],
        "high_card_multi_C": [["HK", "SQ", "C4", "C6", "H9"]],

        "high_card_multi_tie": [["HK", "SQ", "C4", "C7", "H9"], ["DK", "DQ", "H4", "S7", "C9"]],

        "high_card_multi_tie_exact": [["HK", "SQ", "C4", "C7", "H9"], ["HK", "SQ", "C4", "C7", "H9"]],

        "one_hand_mixed": [["CJ", "C9", "C7", "C10", "C8"]],

        "two_hands_mixed": [["DK", "SA", "SK", "CK", "HK"], ["CJ", "C9", "C7", "C10", "C8"]],
        "two_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "two_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],

        "three_hands_mixed": [
            ["DK", "SA", "SK", "CK", "HK"], ["S2", "C3", "H3", "D2", "H2"], ["CJ", "C9", "C7", "C10", "C8"]
        ],
        "three_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "three_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "three_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],

        "four_hands_mixed": [
            ["H6", "HA", "H5", "H7", "H9"], ["DK", "SA", "SK", "CK", "HK"], ["S2", "C3", "H3", "D2", "H2"],
            ["CJ", "C9", "C7", "C10", "C8"]
        ],
        "four_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "four_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "four_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],
        "four_hands_mixed_D": [["H6", "HA", "H5", "H7", "H9"]],

        "five_hands_mixed": [
            ["H6", "HA", "H5", "H7", "H9"], ["S7", "C10", "SJ", "H8", "C9"], ["DK", "SA", "SK", "CK", "HK"],
            ["S2", "C3", "H3", "D2", "H2"], ["CJ", "C9", "C7", "C10", "C8"]
        ],
        "five_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "five_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "five_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],
        "five_hands_mixed_D": [["H6", "HA", "H5", "H7", "H9"]],
        "five_hands_mixed_E": [["S7", "C10", "SJ", "H8", "C9"]],

        "six_hands_mixed": [
            ["H6", "HA", "H5", "H7", "H9"], ["S7", "C10", "SJ", "H8", "C9"], ["DK", "SA", "SK", "CK", "HK"],
            ["S2", "C3", "H3", "D2", "H2"], ["D10", "S10", "SA", "S2", "H10"], ["CJ", "C9", "C7", "C10", "C8"]
        ],
        "six_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "six_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "six_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],
        "six_hands_mixed_D": [["H6", "HA", "H5", "H7", "H9"]],
        "six_hands_mixed_E": [["S7", "C10", "SJ", "H8", "C9"]],
        "six_hands_mixed_F": [["D10", "S10", "SA", "S2", "H10"]],

        "seven_hands_mixed": [
            ["H9", "C2", "D2", "D9", "DJ"], ["H6", "HA", "H5", "H7", "H9"], ["S7", "C10", "SJ", "H8", "C9"],
            ["DK", "SA", "SK", "CK", "HK"], ["S2", "C3", "H3", "D2", "H2"], ["D10", "S10", "SA", "S2", "H10"],
            ["CJ", "C9", "C7", "C10", "C8"]
        ],
        "seven_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "seven_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "seven_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],
        "seven_hands_mixed_D": [["H6", "HA", "H5", "H7", "H9"]],
        "seven_hands_mixed_E": [["S7", "C10", "SJ", "H8", "C9"]],
        "seven_hands_mixed_F": [["D10", "S10", "SA", "S2", "H10"]],
        "seven_hands_mixed_G": [["H9", "C2", "D2", "D9", "DJ"]],

        "eight_hands_mixed": [
            ["H9", "C2", "D2", "D9", "DJ"], ["H6", "HA", "H5", "H7", "H9"], ["S7", "C10", "SJ", "H8", "C9"],
            ["DK", "SA", "SK", "CK", "HK"], ["D10", "C10", "CJ", "H3", "D7"], ["S2", "C3", "H3", "D2", "H2"],
            ["D10", "S10", "SA", "S2", "H10"], ["CJ", "C9", "C7", "C10", "C8"]
        ],
        "eight_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "eight_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "eight_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],
        "eight_hands_mixed_D": [["H6", "HA", "H5", "H7", "H9"]],
        "eight_hands_mixed_E": [["S7", "C10", "SJ", "H8", "C9"]],
        "eight_hands_mixed_F": [["D10", "S10", "SA", "S2", "H10"]],
        "eight_hands_mixed_G": [["H9", "C2", "D2", "D9", "DJ"]],
        "eight_hands_mixed_H": [["D10", "C10", "CJ", "H3", "D7"]],

        "nine_hands_mixed": [
            ["H9", "C2", "D2", "D9", "DJ"], ["H6", "HA", "H5", "H7", "H9"], ["S7", "C10", "SJ", "H8", "C9"],
            ["DK", "SA", "SK", "CK", "HK"], ["D10", "C10", "CJ", "H3", "D7"], ["S2", "C3", "H3", "D2", "H2"],
            ["D10", "S10", "SA", "S2", "H10"], ["CJ", "C9", "C7", "C10", "C8"], ["HK", "SQ", "C4", "C6", "H9"]
        ],
        "nine_hands_mixed_A": [["CJ", "C9", "C7", "C10", "C8"]],
        "nine_hands_mixed_B": [["DK", "SA", "SK", "CK", "HK"]],
        "nine_hands_mixed_C": [["S2", "C3", "H3", "D2", "H2"]],
        "nine_hands_mixed_D": [["H6", "HA", "H5", "H7", "H9"]],
        "nine_hands_mixed_E": [["S7", "C10", "SJ", "H8", "C9"]],
        "nine_hands_mixed_F": [["D10", "S10", "SA", "S2", "H10"]],
        "nine_hands_mixed_G": [["H9", "C2", "D2", "D9", "DJ"]],
        "nine_hands_mixed_H": [["D10", "C10", "CJ", "H3", "D7"]],
        "nine_hands_mixed_I": [["HK", "SQ", "C4", "C6", "H9"]]
    }[hand_name]

    return [[get_card(descriptors) for descriptors in cards] for cards in hand_sets]


def get_rank_dictionary(rank_dict_name):
    return {
        "straight_flush_multi": {
            1: get_hand_sets("straight_flush_multi_A"), 2: get_hand_sets("straight_flush_multi_B"),
            3: get_hand_sets("straight_flush_multi_C"), 4: get_hand_sets("straight_flush_multi_D"),
            5: get_hand_sets("straight_flush_multi_E")
        },
        "straight_flush_multi_tie": {
            1: get_hand_sets("straight_flush_multi_tie_A"), 2: get_hand_sets("straight_flush_multi_tie_B")
        },
        "straight_flush_multi_tie_exact": {
            1: get_hand_sets("straight_flush_multi_tie_exact_A"), 2: get_hand_sets("straight_flush_multi_tie_exact_B")
        },
        "straight_flush_multi_ace_low_straights": {
            1: get_hand_sets("straight_flush_multi_ace_low_straights_A"),
            2: get_hand_sets("straight_flush_multi_ace_low_straights_B"),
        },
        "straight_flush_all_ace_low_straights": {1: get_hand_sets("straight_flush_all_ace_low_straights_A")},
        "quads_multi": {
            1: get_hand_sets("quads_multi_A"), 2: get_hand_sets("quads_multi_B"), 3: get_hand_sets("quads_multi_C"),
            4: get_hand_sets("quads_multi_D"), 5: get_hand_sets("quads_multi_E")
        },
        "quads_multi_tie": {1: get_hand_sets("quads_multi_tie_A"), 2: get_hand_sets("quads_multi_tie_B")},
        "quads_multi_tie_exact": {1: get_hand_sets("quads_multi_tie_exact")},
        "full_house_multi": {
            1: get_hand_sets("full_house_multi_A"), 2: get_hand_sets("full_house_multi_B"),
            3: get_hand_sets("full_house_multi_C"), 4: get_hand_sets("full_house_multi_D"),
            5: get_hand_sets("full_house_multi_E")
        },
        "full_house_multi_tie": {
            1: get_hand_sets("full_house_multi_tie_A"), 2: get_hand_sets("full_house_multi_tie_B")
        },
        "full_house_multi_tie_exact": {1: get_hand_sets("full_house_multi_tie_exact")},
        "flush_multi": {
            1: get_hand_sets("flush_multi_A"), 2: get_hand_sets("flush_multi_B"), 3: get_hand_sets("flush_multi_C"),
            4: get_hand_sets("flush_multi_D"), 5: get_hand_sets("flush_multi_E")
        },
        "flush_multi_tie": {1: get_hand_sets("flush_multi_tie_A"), 2: get_hand_sets("flush_multi_tie_B")},
        "flush_multi_tie_exact": {
            1: get_hand_sets("flush_multi_tie_exact_A"), 2: get_hand_sets("flush_multi_tie_exact_B")
        },
        "straight_multi": {
            1: get_hand_sets("straight_multi_A"), 2: get_hand_sets("straight_multi_B"),
            3: get_hand_sets("straight_multi_C"), 4: get_hand_sets("straight_multi_D"),
        },
        "straight_multi_tie": {1: get_hand_sets("straight_multi_tie_A"), 2: get_hand_sets("straight_multi_tie_B")},
        "straight_multi_tie_exact": {1: get_hand_sets("straight_multi_tie_exact")},
        "straight_multi_ace_low_straights": {
            1: get_hand_sets("straight_multi_ace_low_straights_A"),
            2: get_hand_sets("straight_multi_ace_low_straights_B")
        },
        "straight_all_ace_low_straights": {1: get_hand_sets("straight_all_ace_low_straights_A")},
        "trips_multi": {
            1: get_hand_sets("trips_multi_A"), 2: get_hand_sets("trips_multi_B"), 3: get_hand_sets("trips_multi_C"),
            4: get_hand_sets("trips_multi_D"), 5: get_hand_sets("trips_multi_E")
        },
        "trips_multi_tie": {1: get_hand_sets("trips_multi_tie")},
        "trips_multi_tie_exact": {1: get_hand_sets("trips_multi_tie_exact")},
        "two_pair_multi": {
            1: get_hand_sets("two_pair_multi_A"), 2: get_hand_sets("two_pair_multi_B"),
            3: get_hand_sets("two_pair_multi_C"), 4: get_hand_sets("two_pair_multi_D"),
            5: get_hand_sets("two_pair_multi_E")
        },
        "two_pair_multi_tie": {1: get_hand_sets("two_pair_multi_tie_A"), 2: get_hand_sets("two_pair_multi_tie_B")},
        "two_pair_multi_tie_exact": {1: get_hand_sets("two_pair_multi_tie_exact")},
        "pair_multi": {
            1: get_hand_sets("pair_multi_A"), 2: get_hand_sets("pair_multi_B"), 3: get_hand_sets("pair_multi_C"),
            4: get_hand_sets("pair_multi_D"), 5: get_hand_sets("pair_multi_E"), 6: get_hand_sets("pair_multi_F")
        },
        "pair_multi_tie": {1: get_hand_sets("pair_multi_tie")},
        "pair_multi_tie_exact": {1: get_hand_sets("pair_multi_tie_exact")},
        "high_card_multi": {
            1: get_hand_sets("high_card_multi_A"), 2: get_hand_sets("high_card_multi_B"),
            3: get_hand_sets("high_card_multi_C")
        },
        "high_card_multi_tie": {1: get_hand_sets("high_card_multi_tie")},
        "high_card_multi_tie_exact": {1: get_hand_sets("high_card_multi_tie_exact")},
        "one_hand_mixed": {1: get_hand_sets("one_hand_mixed")},
        "two_hands_mixed": {1: get_hand_sets("two_hands_mixed_A"), 2: get_hand_sets("two_hands_mixed_B")},
        "three_hands_mixed": {
            1: get_hand_sets("three_hands_mixed_A"), 2: get_hand_sets("three_hands_mixed_B"),
            3: get_hand_sets("three_hands_mixed_C")
        },
        "four_hands_mixed": {
            1: get_hand_sets("four_hands_mixed_A"), 2: get_hand_sets("four_hands_mixed_B"),
            3: get_hand_sets("four_hands_mixed_C"), 4: get_hand_sets("four_hands_mixed_D")
        },
        "five_hands_mixed": {
            1: get_hand_sets("five_hands_mixed_A"), 2: get_hand_sets("five_hands_mixed_B"),
            3: get_hand_sets("five_hands_mixed_C"), 4: get_hand_sets("five_hands_mixed_D"),
            5: get_hand_sets("five_hands_mixed_E")
        },
        "six_hands_mixed": {
            1: get_hand_sets("six_hands_mixed_A"), 2: get_hand_sets("six_hands_mixed_B"),
            3: get_hand_sets("six_hands_mixed_C"), 4: get_hand_sets("six_hands_mixed_D"),
            5: get_hand_sets("six_hands_mixed_E"), 6: get_hand_sets("six_hands_mixed_F")
        },
        "seven_hands_mixed": {
            1: get_hand_sets("seven_hands_mixed_A"), 2: get_hand_sets("seven_hands_mixed_B"),
            3: get_hand_sets("seven_hands_mixed_C"), 4: get_hand_sets("seven_hands_mixed_D"),
            5: get_hand_sets("seven_hands_mixed_E"), 6: get_hand_sets("seven_hands_mixed_F"),
            7: get_hand_sets("seven_hands_mixed_G")
        },
        "eight_hands_mixed": {
            1: get_hand_sets("eight_hands_mixed_A"), 2: get_hand_sets("eight_hands_mixed_B"),
            3: get_hand_sets("eight_hands_mixed_C"), 4: get_hand_sets("eight_hands_mixed_D"),
            5: get_hand_sets("eight_hands_mixed_E"), 6: get_hand_sets("eight_hands_mixed_F"),
            7: get_hand_sets("eight_hands_mixed_G"), 8: get_hand_sets("eight_hands_mixed_H")
        },
        "nine_hands_mixed": {
            1: get_hand_sets("nine_hands_mixed_A"), 2: get_hand_sets("nine_hands_mixed_B"),
            3: get_hand_sets("nine_hands_mixed_C"), 4: get_hand_sets("nine_hands_mixed_D"),
            5: get_hand_sets("nine_hands_mixed_E"), 6: get_hand_sets("nine_hands_mixed_F"),
            7: get_hand_sets("nine_hands_mixed_G"), 8: get_hand_sets("nine_hands_mixed_H"),
            9: get_hand_sets("nine_hands_mixed_I")
        }
    }[rank_dict_name]
