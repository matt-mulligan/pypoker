from pypoker.deck import Card

PLAYERS = "players"
HAND_DESC = "hand_description"


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
        "straight_flush_multi_A": ["HA", "HJ", "HQ", "H10", "HK"],
        "straight_flush_multi_B": ["DK", "D10", "DJ", "D9", "DQ"],
        "straight_flush_multi_C": ["C9", "C10", "C6", "C8", "C7"],
        "straight_flush_multi_D": ["S4", "S6", "S8", "S5", "S7"],
        "straight_flush_multi_E": ["SA", "S3", "S4", "S2", "S5"],
        "straight_flush_multi_tie_A": ["DK", "D10", "DJ", "D9", "DQ"],
        "straight_flush_multi_tie_B": ["SQ", "S10", "S9", "SK", "SJ"],
        "straight_flush_multi_tie_C": ["CJ", "C9", "C7", "C10", "C8"],
        "straight_flush_multi_tie_D": ["H9", "HJ", "H7", "H8", "H10"],
        "straight_flush_multi_tie_E": ["D7", "D10", "DJ", "D9", "D8"],
        "straight_flush_multi_tie_exact_A": ["H9", "HJ", "HQ", "H8", "H10"],
        "straight_flush_multi_tie_exact_B": ["CJ", "C9", "C7", "C10", "C8"],
        "straight_flush_multi_ace_low_straights_A": ["HA", "H3", "H4", "H2", "H5"],
        "straight_flush_multi_ace_low_straights_B": ["CA", "C3", "C4", "C2", "C5"],
        "straight_flush_multi_ace_low_straights_C": ["SA", "S3", "S4", "S2", "S5"],
        "straight_flush_multi_ace_low_straights_D": ["DK", "D10", "DJ", "D9", "DQ"],
        "quads_multi_A": ["DK", "SA", "SK", "CK", "HK"],
        "quads_multi_B": ["D7", "S7", "H7", "DK", "C7"],
        "quads_multi_C": ["H9", "C7", "H7", "S7", "D7"],
        "quads_multi_D": ["H7", "S7", "C2", "D7", "C7"],
        "quads_multi_E": ["S5", "H5", "D7", "C5", "D5"],
        "quads_multi_tie_A": ["D7", "S7", "H7", "S9", "C7"],
        "quads_multi_tie_B": ["D7", "S7", "H7", "H9", "C7"],
        "quads_multi_tie_C": ["D7", "S7", "H7", "D4", "C7"],
        "quads_multi_tie_D": ["D7", "S7", "H7", "C4", "C7"],
        "quads_multi_tie_exact_A": ["D7", "S7", "H7", "D4", "C7"],
        "full_house_multi_A": ["DA", "S2", "C2", "HA", "SA"],
        "full_house_multi_B": ["DK", "S9", "C9", "HK", "SK"],
        "full_house_multi_C": ["DK", "C7", "SK", "S7", "CK"],
        "full_house_multi_D": ["DQ", "SA", "CA", "HQ", "SQ"],
        "full_house_multi_E": ["S2", "C3", "H3", "D2", "H2"],
        "full_house_multi_tie_A": ["DA", "SA", "CA", "H4", "D4"],
        "full_house_multi_tie_B": ["DA", "HA", "CA", "C4", "S4"],
        "full_house_multi_tie_C": ["HK", "SQ", "DQ", "CQ", "CK"],
        "full_house_multi_tie_D": ["CQ", "CK", "SK", "HQ", "DQ"],
        "full_house_multi_tie_E": ["CQ", "DK", "SK", "HQ", "SQ"],
        "full_house_multi_tie_exact_A": ["DA", "SA", "CA", "H4", "D4"],
        "flush_multi_A": ["H6", "HA", "H5", "H7", "H9"],
        "flush_multi_B": ["C9", "C6", "C7", "C4", "CA"],
        "flush_multi_C": ["HA", "H9", "H7", "H4", "H3"],
        "flush_multi_D": ["CA", "C7", "C2", "C4", "C3"],
        "flush_multi_E": ["SJ", "SQ", "S6", "S7", "S10"],
        "flush_multi_tie_A": ["D7", "D4", "DA", "DK", "D10"],
        "flush_multi_tie_B": ["CK", "C10", "C7", "C4", "CA"],
        "flush_multi_tie_C": ["H4", "H10", "H9", "HQ", "H7"],
        "flush_multi_tie_D": ["S4", "SQ", "S7", "S10", "S9"],
        "flush_multi_tie_exact_A": ["D7", "D4", "DA", "DK", "D10"],
        "flush_multi_tie_exact_B": ["DA", "DK", "D7", "D4", "D10"],
        "flush_multi_tie_exact_C": ["DK", "D10", "D7", "D4", "DA"],
        "flush_multi_tie_exact_D": ["DQ", "D10", "D8", "D2", "D4"],
        "flush_multi_tie_exact_E": ["DQ", "D10", "D8", "D2", "D4"],
        "straight_multi_A": ["DK", "D10", "SQ", "HJ", "S9"],
        "straight_multi_B": ["S7", "C10", "SJ", "H8", "C9"],
        "straight_multi_C": ["S6", "H2", "H4", "S5", "S3"],
        "straight_multi_D": ["SA", "H3", "C4", "D2", "S5"],
        "straight_multi_tie_A": ["H10", "HQ", "CJ", "C9", "D8"],
        "straight_multi_tie_B": ["C10", "CQ", "SJ", "S9", "H8"],
        "straight_multi_tie_C": ["S10", "SQ", "HJ", "H9", "S8"],
        "straight_multi_tie_D": ["H8", "C6", "S4", "D5", "D7"],
        "straight_multi_tie_E": ["C8", "S6", "H4", "D5", "S7"],
        "straight_multi_tie_exact_A": ["H10", "HQ", "CJ", "C9", "D8"],
        "straight_multi_tie_exact_B": ["H10", "HQ", "CJ", "C9", "D8"],
        "straight_multi_ace_low_straights_A": ["SK", "D9", "D10", "SQ", "CJ"],
        "straight_multi_ace_low_straights_B": ["DA", "S3", "H4", "H5", "D2"],
        "straight_multi_ace_low_straights_C": ["HA", "C3", "S4", "S5", "S2"],
        "straight_multi_ace_low_straights_D": ["SA", "H3", "C4", "D5", "H2"],
        "straight_all_ace_low_straights_A": ["DA", "S3", "H4", "H5", "D2"],
        "straight_all_ace_low_straights_B": ["HA", "C3", "S4", "S5", "S2"],
        "straight_all_ace_low_straights_C": ["SA", "H3", "C4", "D5", "H2"],
        "trips_multi_A": ["D10", "S10", "SA", "S2", "H10"],
        "trips_multi_B": ["D10", "D2", "D7", "C7", "H7"],
        "trips_multi_C": ["H9", "S6", "C7", "D7", "H7"],
        "trips_multi_D": ["S7", "C9", "D7", "H2", "H7"],
        "trips_multi_E": ["C4", "S4", "C2", "H3", "D4"],
        "trips_multi_tie_A": ["S7", "C9", "D7", "H2", "H7"],
        "trips_multi_tie_B": ["H7", "D9", "C7", "H2", "S7"],
        "trips_multi_tie_C": ["C7", "H9", "S7", "C2", "D7"],
        "trips_multi_tie_exact_A": ["S7", "C9", "D7", "H2", "H7"],
        "trips_multi_tie_exact_B": ["S7", "C9", "D7", "H2", "H7"],
        "trips_multi_tie_exact_C": ["S7", "C9", "D7", "H2", "H7"],
        "two_pair_multi_A": ["HJ", "H2", "CJ", "D2", "S7"],
        "two_pair_multi_B": ["H9", "C6", "D6", "D9", "DJ"],
        "two_pair_multi_C": ["H9", "C4", "D4", "D9", "DJ"],
        "two_pair_multi_D": ["S9", "C4", "H4", "C9", "D7"],
        "two_pair_multi_E": ["H9", "C2", "D2", "D9", "DJ"],
        "two_pair_multi_tie_A": ["H9", "C4", "D4", "D9", "DJ"], 
        "two_pair_multi_tie_B": ["D9", "S4", "H4", "H9", "CJ"],
        "two_pair_multi_tie_C": ["S9", "C4", "H4", "C9", "D7"], 
        "two_pair_multi_tie_D": ["C9", "D4", "S4", "H9", "H7"],
        "two_pair_multi_tie_exact_A": ["S9", "C4", "H4", "C9", "D7"],
        "two_pair_multi_tie_exact_B": ["S9", "C4", "H4", "C9", "D7"],
        "pair_multi_A": ["D10", "C10", "CJ", "H3", "D7"],
        "pair_multi_B": ["H7", "D7", "SK", "S10", "S9"],
        "pair_multi_C": ["C7", "S7", "HK", "S10", "S8"],
        "pair_multi_D": ["S7", "C7", "CK", "H8", "H5"],
        "pair_multi_E": ["D7", "C7", "SJ", "S8", "C3"],
        "pair_multi_F": ["H4", "D4", "HJ", "C9", "S2"],
        "pair_multi_tie_A": ["H7", "D7", "SK", "S10", "S9"],
        "pair_multi_tie_B": ["C7", "S7", "HK", "H10", "C9"],
        "pair_multi_tie_exact_A": ["H7", "D7", "SK", "S10", "S9"],
        "pair_multi_tie_exact_B": ["H7", "D7", "SK", "S10", "S9"],
        "high_card_multi_A": ["HK", "SQ", "C4", "C7", "H9"],
        "high_card_multi_B": ["HK", "SQ", "C2", "C7", "H9"],
        "high_card_multi_C": ["HK", "SQ", "C4", "C6", "H9"],
        "high_card_multi_tie_A": ["HK", "SQ", "C4", "C7", "H9"],
        "high_card_multi_tie_B": ["DK", "DQ", "H4", "S7", "C9"],
        "high_card_multi_tie_exact_A": ["HK", "SQ", "C4", "C7", "H9"],
        "high_card_multi_tie_exact_B": ["HK", "SQ", "C4", "C7", "H9"],
        "one_hand_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "two_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "two_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "three_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "three_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "three_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "four_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "four_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "four_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "four_hands_mixed_D": ["H6", "HA", "H5", "H7", "H9"],
        "five_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "five_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "five_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "five_hands_mixed_D": ["H6", "HA", "H5", "H7", "H9"],
        "five_hands_mixed_E": ["S7", "C10", "SJ", "H8", "C9"],
        "six_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "six_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "six_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "six_hands_mixed_D": ["H6", "HA", "H5", "H7", "H9"],
        "six_hands_mixed_E": ["S7", "C10", "SJ", "H8", "C9"],
        "six_hands_mixed_F": ["D10", "S10", "SA", "S2", "H10"],
        "seven_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "seven_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "seven_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "seven_hands_mixed_D": ["H6", "HA", "H5", "H7", "H9"],
        "seven_hands_mixed_E": ["S7", "C10", "SJ", "H8", "C9"],
        "seven_hands_mixed_F": ["D10", "S10", "SA", "S2", "H10"],
        "seven_hands_mixed_G": ["H9", "C2", "D2", "D9", "DJ"],
        "eight_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "eight_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "eight_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "eight_hands_mixed_D": ["H6", "HA", "H5", "H7", "H9"],
        "eight_hands_mixed_E": ["S7", "C10", "SJ", "H8", "C9"],
        "eight_hands_mixed_F": ["D10", "S10", "SA", "S2", "H10"],
        "eight_hands_mixed_G": ["H9", "C2", "D2", "D9", "DJ"],
        "eight_hands_mixed_H": ["D10", "C10", "CJ", "H3", "D7"],
        "nine_hands_mixed_A": ["CJ", "C9", "C7", "C10", "C8"],
        "nine_hands_mixed_B": ["DK", "SA", "SK", "CK", "HK"],
        "nine_hands_mixed_C": ["S2", "C3", "H3", "D2", "H2"],
        "nine_hands_mixed_D": ["H6", "HA", "H5", "H7", "H9"],
        "nine_hands_mixed_E": ["S7", "C10", "SJ", "H8", "C9"],
        "nine_hands_mixed_F": ["D10", "S10", "SA", "S2", "H10"],
        "nine_hands_mixed_G": ["H9", "C2", "D2", "D9", "DJ"],
        "nine_hands_mixed_H": ["D10", "C10", "CJ", "H3", "D7"],
        "nine_hands_mixed_I": ["HK", "SQ", "C4", "C6", "H9"]
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
    }[hand_name]

    return [[get_card(descriptors) for descriptors in cards] for cards in hand_sets]


def get_rank_dictionary(rank_dict_name):
    return {
        "straight_flush_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: 'Straight Flush (Ace to Ten)'},
            2: {PLAYERS: ["player_b"], HAND_DESC: 'Straight Flush (King to Nine)'},
            3: {PLAYERS: ["player_c"], HAND_DESC: 'Straight Flush (Ten to Six)'},
            4: {PLAYERS: ["player_d"], HAND_DESC: 'Straight Flush (Eight to Four)'},
            5: {PLAYERS: ["player_e"], HAND_DESC: 'Straight Flush (Five to Ace)'}
        },
        "straight_flush_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Straight Flush (King to Nine)"},
            2: {PLAYERS: ["player_c", "player_d", "player_e"], HAND_DESC: "Straight Flush (Jack to Seven)"}
        },
        "straight_flush_multi_tie_exact": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Queen to Eight)"},
            2: {PLAYERS: ["player_b", "player_c"], HAND_DESC: "Straight Flush (Jack to Seven)"}
        },
        "straight_flush_multi_ace_low_straights": {
            1: {PLAYERS: ["player_d"], HAND_DESC: "Straight Flush (King to Nine)"},
            2: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Straight Flush (Five to Ace)"}
        },
        "straight_flush_all_ace_low_straights": {
            1: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Straight Flush (Five to Ace)"}
        },
        "quads_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: 'Quads (Kings with Ace kicker)'},
            2: {PLAYERS: ["player_b"], HAND_DESC: 'Quads (Sevens with King kicker)'},
            3: {PLAYERS: ["player_c"], HAND_DESC: 'Quads (Sevens with Nine kicker)'},
            4: {PLAYERS: ["player_d"], HAND_DESC: 'Quads (Sevens with Two kicker)'},
            5: {PLAYERS: ["player_e"], HAND_DESC: 'Quads (Fives with Seven kicker)'}
        },
        "quads_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Quads (Sevens with Nine kicker)"},
            2: {PLAYERS: ["player_c", "player_d"], HAND_DESC: "Quads (Sevens with Four kicker)"}
        },
        "quads_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Quads (Sevens with Four kicker)"}
        },
        "full_house_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Full House (Aces full of Twos)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Full House (Kings full of Nines)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Kings full of Sevens)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Full House (Queens full of Aces)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Full House (Twos full of Threes)"},
        },
        "full_house_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Full House (Aces full of Fours)"},
            2: {PLAYERS: ["player_c", "player_d", "player_e"], HAND_DESC: "Full House (Queens full of Kings)"},
        },
        "full_house_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Full House (Aces full of Fours)"}
        },
        "flush_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Four)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Flush (Ace, Nine, Seven, Four, Three)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Seven, Four, Three, Two)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Flush (Queen, Jack, Ten, Seven, Six)"}
        },
        "flush_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Flush (Ace, King, Ten, Seven, Four)"},
            2: {PLAYERS: ["player_c", "player_d"], HAND_DESC: "Flush (Queen, Ten, Nine, Seven, Four)"}
        },
        "flush_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Flush (Ace, King, Ten, Seven, Four)"},
            2: {PLAYERS: ["player_d", "player_e"], HAND_DESC: "Flush (Queen, Ten, Eight, Four, Two)"}
        },
        "straight_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight (King to Nine)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Straight (Jack to Seven)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Straight (Six to Two)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Straight (Five to Ace)"}
        },
        "straight_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Straight (Queen to Eight)"},
            2: {PLAYERS: ["player_d", "player_e"], HAND_DESC: "Straight (Eight to Four)"}
        },
        "straight_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Straight (Queen to Eight)"}
        },
        "straight_multi_ace_low_straights": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight (King to Nine)"},
            2: {PLAYERS: ["player_b", "player_c", "player_d"], HAND_DESC: "Straight (Five to Ace)"}
        },
        "straight_all_ace_low_straights": {
            1: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Straight (Five to Ace)"}
        },
        "trips_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Trips (Tens with kickers Ace, Two)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Trips (Sevens with kickers Ten, Two)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Trips (Sevens with kickers Nine, Six)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Trips (Sevens with kickers Nine, Two)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Trips (Fours with kickers Three, Two)"}
        },
        "trips_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Trips (Sevens with kickers Nine, Two)"}
        },
        "trips_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b", "player_c"], HAND_DESC: "Trips (Sevens with kickers Nine, Two)"}
        },
        "two_pair_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Two Pair (Jacks and Twos with kicker Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Two Pair (Nines and Sixs with kicker Jack)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Two Pair (Nines and Fours with kicker Jack)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Two Pair (Nines and Fours with kicker Seven)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Two Pair (Nines and Twos with kicker Jack)"}
        },
        "two_pair_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Two Pair (Nines and Fours with kicker Jack)"},
            2: {PLAYERS: ["player_c", "player_d"], HAND_DESC: "Two Pair (Nines and Fours with kicker Seven)"}
        },
        "two_pair_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Two Pair (Nines and Fours with kicker Seven)"}
        },
        "pair_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Pair (Tens with kickers Jack, Seven, Three)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Pair (Sevens with kickers King, Ten, Nine)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Pair (Sevens with kickers King, Ten, Eight)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Pair (Sevens with kickers King, Eight, Five)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Pair (Sevens with kickers Jack, Eight, Three)"},
            6: {PLAYERS: ["player_f"], HAND_DESC: "Pair (Fours with kickers Jack, Nine, Two)"}
        },
        "pair_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Pair (Sevens with kickers King, Ten, Nine)"}
        },
        "pair_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "Pair (Sevens with kickers King, Ten, Nine)"}
        },
        "high_card_multi": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "High Card (King, Queen, Nine, Seven, Four)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "High Card (King, Queen, Nine, Seven, Two)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "High Card (King, Queen, Nine, Six, Four)"}
        },
        "high_card_multi_tie": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "High Card (King, Queen, Nine, Seven, Four)"}
        },
        "high_card_multi_tie_exact": {
            1: {PLAYERS: ["player_a", "player_b"], HAND_DESC: "High Card (King, Queen, Nine, Seven, Four)"}
        },
        "one_hand_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"}
        },
        "two_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"}
        },
        "three_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"}
        },
        "four_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"}
        },
        "five_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Straight (Jack to Seven)"},
        },
        "six_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Straight (Jack to Seven)"},
            6: {PLAYERS: ["player_f"], HAND_DESC: "Trips (Tens with kickers Ace, Two)"},
        },
        "seven_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Straight (Jack to Seven)"},
            6: {PLAYERS: ["player_f"], HAND_DESC: "Trips (Tens with kickers Ace, Two)"},
            7: {PLAYERS: ["player_g"], HAND_DESC: "Two Pair (Nines and Twos with kicker Jack)"},
        },
        "eight_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Straight (Jack to Seven)"},
            6: {PLAYERS: ["player_f"], HAND_DESC: "Trips (Tens with kickers Ace, Two)"},
            7: {PLAYERS: ["player_g"], HAND_DESC: "Two Pair (Nines and Twos with kicker Jack)"},
            8: {PLAYERS: ["player_h"], HAND_DESC: "Pair (Tens with kickers Jack, Seven, Three)"},
        },
        "nine_hands_mixed": {
            1: {PLAYERS: ["player_a"], HAND_DESC: "Straight Flush (Jack to Seven)"},
            2: {PLAYERS: ["player_b"], HAND_DESC: "Quads (Kings with Ace kicker)"},
            3: {PLAYERS: ["player_c"], HAND_DESC: "Full House (Twos full of Threes)"},
            4: {PLAYERS: ["player_d"], HAND_DESC: "Flush (Ace, Nine, Seven, Six, Five)"},
            5: {PLAYERS: ["player_e"], HAND_DESC: "Straight (Jack to Seven)"},
            6: {PLAYERS: ["player_f"], HAND_DESC: "Trips (Tens with kickers Ace, Two)"},
            7: {PLAYERS: ["player_g"], HAND_DESC: "Two Pair (Nines and Twos with kicker Jack)"},
            8: {PLAYERS: ["player_h"], HAND_DESC: "Pair (Tens with kickers Jack, Seven, Three)"},
            9: {PLAYERS: ["player_i"], HAND_DESC: "High Card (King, Queen, Nine, Six, Four)"},
        }
    }[rank_dict_name]


def get_player_hands_dict(scenario):
    """
    test helper method to generate a player ahnd dictionary

    :param scenario: scenario name
    :return:
    """

    return {
        "straight_flush_multi": {
            "player_a": get_hand("straight_flush_multi_A"), "player_b": get_hand("straight_flush_multi_B"),
            "player_c": get_hand("straight_flush_multi_C"), "player_d": get_hand("straight_flush_multi_D"),
            "player_e": get_hand("straight_flush_multi_E")
        },
        "straight_flush_multi_tie": {
            "player_a": get_hand("straight_flush_multi_tie_A"),  "player_b": get_hand("straight_flush_multi_tie_B"),
            "player_c": get_hand("straight_flush_multi_tie_C"),  "player_d": get_hand("straight_flush_multi_tie_D"),
            "player_e": get_hand("straight_flush_multi_tie_E")
        },
        "straight_flush_multi_tie_exact": {
            "player_a": get_hand("straight_flush_multi_tie_exact_A"),
            "player_b": get_hand("straight_flush_multi_tie_exact_B"),
            "player_c": get_hand("straight_flush_multi_tie_exact_B")
        },
        "straight_flush_multi_ace_low_straights": {
            "player_a": get_hand("straight_flush_multi_ace_low_straights_A"),
            "player_b": get_hand("straight_flush_multi_ace_low_straights_B"),
            "player_c": get_hand("straight_flush_multi_ace_low_straights_C"),
            "player_d": get_hand("straight_flush_multi_ace_low_straights_D"),
        },
        "straight_flush_all_ace_low_straights": {
            "player_a": get_hand("straight_flush_multi_ace_low_straights_A"),
            "player_b": get_hand("straight_flush_multi_ace_low_straights_B"),
            "player_c": get_hand("straight_flush_multi_ace_low_straights_C"),
        },
        "quads_multi": {
            "player_a": get_hand("quads_multi_A"), "player_b": get_hand("quads_multi_B"),
            "player_c": get_hand("quads_multi_C"), "player_d": get_hand("quads_multi_D"),
            "player_e": get_hand("quads_multi_E")
        },
        "quads_multi_tie": {
            "player_a": get_hand("quads_multi_tie_A"), "player_b": get_hand("quads_multi_tie_B"),
            "player_c": get_hand("quads_multi_tie_C"), "player_d": get_hand("quads_multi_tie_D")
        },
        "quads_multi_tie_exact": {
            "player_a": get_hand("quads_multi_tie_exact_A"), "player_b": get_hand("quads_multi_tie_exact_A")
        },
        "full_house_multi": {
            "player_a": get_hand("full_house_multi_A"), "player_b": get_hand("full_house_multi_B"),
            "player_c": get_hand("full_house_multi_C"), "player_d": get_hand("full_house_multi_D"),
            "player_e": get_hand("full_house_multi_E")
        },
        "full_house_multi_tie": {
            "player_a": get_hand("full_house_multi_tie_A"), "player_b": get_hand("full_house_multi_tie_B"),
            "player_c": get_hand("full_house_multi_tie_C"), "player_d": get_hand("full_house_multi_tie_D"),
            "player_e": get_hand("full_house_multi_tie_E")
        },
        "full_house_multi_tie_exact": {
            "player_a": get_hand("full_house_multi_tie_exact_A"), "player_b": get_hand("full_house_multi_tie_exact_A")
        },
        "flush_multi": {
            "player_a": get_hand("flush_multi_A"), "player_b": get_hand("flush_multi_B"),
            "player_c": get_hand("flush_multi_C"), "player_d": get_hand("flush_multi_D"),
            "player_e": get_hand("flush_multi_E")
        },
        "flush_multi_tie": {
            "player_a": get_hand("flush_multi_tie_A"), "player_b": get_hand("flush_multi_tie_B"),
            "player_c": get_hand("flush_multi_tie_C"), "player_d": get_hand("flush_multi_tie_D"),
        },
        "flush_multi_tie_exact": {
            "player_a": get_hand("flush_multi_tie_exact_A"), "player_b": get_hand("flush_multi_tie_exact_B"),
            "player_c": get_hand("flush_multi_tie_exact_C"), "player_d": get_hand("flush_multi_tie_exact_D"),
            "player_e": get_hand("flush_multi_tie_exact_E")
        },
        "straight_multi": {
            "player_a": get_hand("straight_multi_A"), "player_b": get_hand("straight_multi_B"),
            "player_c": get_hand("straight_multi_C"), "player_d": get_hand("straight_multi_D")
        },
        "straight_multi_tie": {
            "player_a": get_hand("straight_multi_tie_A"), "player_b": get_hand("straight_multi_tie_B"),
            "player_c": get_hand("straight_multi_tie_C"), "player_d": get_hand("straight_multi_tie_D"),
            "player_e": get_hand("straight_multi_tie_E")
        },
        "straight_multi_tie_exact": {
            "player_a": get_hand("straight_multi_tie_exact_A"), "player_b": get_hand("straight_multi_tie_exact_B"),
        },
        "straight_multi_ace_low_straights": {
            "player_a": get_hand("straight_multi_ace_low_straights_A"), "player_b": get_hand("straight_multi_ace_low_straights_B"),
            "player_c": get_hand("straight_multi_ace_low_straights_C"), "player_d": get_hand("straight_multi_ace_low_straights_D")
        },
        "straight_all_ace_low_straights": {
            "player_a": get_hand("straight_all_ace_low_straights_A"),
            "player_b": get_hand("straight_all_ace_low_straights_B"),
            "player_c": get_hand("straight_all_ace_low_straights_C"),
        },
        "trips_multi": {
            "player_a": get_hand("trips_multi_A"), "player_b": get_hand("trips_multi_B"),
            "player_c": get_hand("trips_multi_C"), "player_d": get_hand("trips_multi_D"),
            "player_e": get_hand("trips_multi_E")
        },
        "trips_multi_tie": {
            "player_a": get_hand("trips_multi_tie_A"), "player_b": get_hand("trips_multi_tie_B"),
            "player_c": get_hand("trips_multi_tie_C")
        },
        "trips_multi_tie_exact": {
            "player_a": get_hand("trips_multi_tie_exact_A"), "player_b": get_hand("trips_multi_tie_exact_B"),
            "player_c": get_hand("trips_multi_tie_exact_C")
        },
        "two_pair_multi": {
            "player_a": get_hand("two_pair_multi_A"), "player_b": get_hand("two_pair_multi_B"),
            "player_c": get_hand("two_pair_multi_C"), "player_d": get_hand("two_pair_multi_D"),
            "player_e": get_hand("two_pair_multi_E")
        },
        "two_pair_multi_tie": {
            "player_a": get_hand("two_pair_multi_tie_A"), "player_b": get_hand("two_pair_multi_tie_B"),
            "player_c": get_hand("two_pair_multi_tie_C"), "player_d": get_hand("two_pair_multi_tie_D"),
        },
        "two_pair_multi_tie_exact": {
            "player_a": get_hand("two_pair_multi_tie_exact_A"), "player_b": get_hand("two_pair_multi_tie_exact_B")
        },
        "pair_multi": {
            "player_a": get_hand("pair_multi_A"), "player_b": get_hand("pair_multi_B"),
            "player_c": get_hand("pair_multi_C"), "player_d": get_hand("pair_multi_D"),
            "player_e": get_hand("pair_multi_E"), "player_f": get_hand("pair_multi_F")
        },
        "pair_multi_tie": {
            "player_a": get_hand("pair_multi_tie_A"), "player_b": get_hand("pair_multi_tie_B"),
        },
        "pair_multi_tie_exact": {
            "player_a": get_hand("pair_multi_tie_exact_A"), "player_b": get_hand("pair_multi_tie_exact_B"),
        },
        "high_card_multi": {
            "player_a": get_hand("high_card_multi_A"), "player_b": get_hand("high_card_multi_B"),
            "player_c": get_hand("high_card_multi_C")
        },
        "high_card_multi_tie": {
            "player_a": get_hand("high_card_multi_tie_A"), "player_b": get_hand("high_card_multi_tie_B"),
        },
        "high_card_multi_tie_exact": {
            "player_a": get_hand("high_card_multi_tie_exact_A"), "player_b": get_hand("high_card_multi_tie_exact_B"),
        },
        "one_hand_mixed": {
            "player_a": get_hand("one_hand_mixed_A")
        },
        "two_hands_mixed": {
            "player_a": get_hand("two_hands_mixed_A"), "player_b": get_hand("two_hands_mixed_B")
        },
        "three_hands_mixed": {
            "player_a": get_hand("three_hands_mixed_A"), "player_b": get_hand("three_hands_mixed_B"),
            "player_c": get_hand("three_hands_mixed_C")
        },
        "four_hands_mixed": {
            "player_a": get_hand("four_hands_mixed_A"), "player_b": get_hand("four_hands_mixed_B"),
            "player_c": get_hand("four_hands_mixed_C"), "player_d": get_hand("four_hands_mixed_D")
        },
        "five_hands_mixed": {
            "player_a": get_hand("five_hands_mixed_A"), "player_b": get_hand("five_hands_mixed_B"),
            "player_c": get_hand("five_hands_mixed_C"), "player_d": get_hand("five_hands_mixed_D"),
            "player_e": get_hand("five_hands_mixed_E")
        },
        "six_hands_mixed": {
            "player_a": get_hand("six_hands_mixed_A"), "player_b": get_hand("six_hands_mixed_B"),
            "player_c": get_hand("six_hands_mixed_C"), "player_d": get_hand("six_hands_mixed_D"),
            "player_e": get_hand("six_hands_mixed_E"), "player_f": get_hand("six_hands_mixed_F")
        },
        "seven_hands_mixed": {
            "player_a": get_hand("seven_hands_mixed_A"), "player_b": get_hand("seven_hands_mixed_B"),
            "player_c": get_hand("seven_hands_mixed_C"), "player_d": get_hand("seven_hands_mixed_D"),
            "player_e": get_hand("seven_hands_mixed_E"), "player_f": get_hand("seven_hands_mixed_F"),
            "player_g": get_hand("seven_hands_mixed_G")
        },
        "eight_hands_mixed": {
            "player_a": get_hand("eight_hands_mixed_A"), "player_b": get_hand("eight_hands_mixed_B"),
            "player_c": get_hand("eight_hands_mixed_C"), "player_d": get_hand("eight_hands_mixed_D"),
            "player_e": get_hand("eight_hands_mixed_E"), "player_f": get_hand("eight_hands_mixed_F"),
            "player_g": get_hand("eight_hands_mixed_G"), "player_h": get_hand("eight_hands_mixed_H")
        },
        "nine_hands_mixed": {
            "player_a": get_hand("nine_hands_mixed_A"), "player_b": get_hand("nine_hands_mixed_B"),
            "player_c": get_hand("nine_hands_mixed_C"), "player_d": get_hand("nine_hands_mixed_D"),
            "player_e": get_hand("nine_hands_mixed_E"), "player_f": get_hand("nine_hands_mixed_F"),
            "player_g": get_hand("nine_hands_mixed_G"), "player_h": get_hand("nine_hands_mixed_H"),
            "player_i": get_hand("nine_hands_mixed_I")
        }
        }[scenario]
