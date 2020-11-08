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
        ]
    }[hand_name]

    return [[get_card(descriptors) for descriptors in cards] for cards in hand_sets]
