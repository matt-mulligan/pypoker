from pytest import fixture, mark

from fixtures.cards import get_hand, get_rank_dictionary, get_player_hands_dict, get_cards
from pypoker.engine.logic.texas_holdem import TexasHoldemHandSolver


@fixture
def solver_instance():
    return TexasHoldemHandSolver()


@mark.parametrize("hole_cards, board_cards, best_hand, hand_rank, hand_title, hand_description", [
    ("hole_cards_straight_flush_001", "board_cards_straight_flush_001", "hand_straight_flush_001",
     1, "Straight Flush", "Straight Flush (Ace to Ten)"),  # straight flush - all hole cards
    ("hole_cards_straight_flush_002", "board_cards_straight_flush_002", "hand_straight_flush_002",
     1, "Straight Flush", "Straight Flush (Ten to Six)"),  # straight flush - 1 hole cards
    ("hole_cards_straight_flush_003", "board_cards_straight_flush_003", "hand_straight_flush_003",
     1, "Straight Flush", "Straight Flush (Seven to Three)"),  # straight flush - no hole cards
    ("hole_cards_straight_flush_004", "board_cards_straight_flush_004", "hand_straight_flush_004",
     1, "Straight Flush", "Straight Flush (King to Nine)"),  # straight flush - multiple
    ("hole_cards_straight_flush_005", "board_cards_straight_flush_005", "hand_straight_flush_005",
     1, "Straight Flush", "Straight Flush (Ace to Ten)"),  # Straight Flush - possible trips
    ("hole_cards_straight_flush_006", "board_cards_straight_flush_006", "hand_straight_flush_006",
     1, "Straight Flush", "Straight Flush (Eight to Four)"),  # Straight Flush - possible two pair
    ("hole_cards_straight_flush_007", "board_cards_straight_flush_007", "hand_straight_flush_007",
     1, "Straight Flush", "Straight Flush (Jack to Seven)"),  # Straight Flush - possible pair
    ("hole_cards_straight_flush_008", "board_cards_straight_flush_008", "hand_straight_flush_008",
     1, "Straight Flush", "Straight Flush (Five to Ace)"),  # Straight Flush - Ace Low Straight

    ("hole_cards_quads_001", "board_cards_quads_001", "hand_quads_001",
     2, "Quads", "Quads (Fours with Queen kicker)"),  # Quads - all hole cards
    ("hole_cards_quads_002", "board_cards_quads_002", "hand_quads_002",
     2, "Quads", "Quads (Queens with Jack kicker)"),  # Quads - one hole card
    ("hole_cards_quads_003", "board_cards_quads_003", "hand_quads_003",
     2, "Quads", "Quads (Queens with Jack kicker)"),  # Quads -no hole cards
    ("hole_cards_quads_004", "board_cards_quads_004", "hand_quads_004",
     2, "Quads", "Quads (Queens with Jack kicker)"),  # Quads - possible full house / two pair

    ("hole_cards_full_house_001", "board_cards_full_house_001", "hand_full_house_001",
     3, "Full House", "Full House (Nines full of Kings)"),  # Full House - all hole cards
    ("hole_cards_full_house_002", "board_cards_full_house_002", "hand_full_house_002",
     3, "Full House", "Full House (Fours full of Jacks)"),  # Full House - 1 hole card
    ("hole_cards_full_house_003", "board_cards_full_house_003", "hand_full_house_003",
     3, "Full House", "Full House (Queens full of Jacks)"),  # Full House - no hole cards
    ("hole_cards_full_house_004", "board_cards_full_house_004", "hand_full_house_004",
     3, "Full House", "Full House (Tens full of Fours)"),  # Full House - Competing Trips
    ("hole_cards_full_house_005", "board_cards_full_house_005", "hand_full_house_005",
     3, "Full House", "Full House (Tens full of Nines)"),  # Full House - Competing Pairs

    ("hole_cards_flush_001", "board_cards_flush_001", "hand_flush_001",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - all hole cards
    ("hole_cards_flush_002", "board_cards_flush_002", "hand_flush_002",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - 1 hole cards
    ("hole_cards_flush_003", "board_cards_flush_003", "hand_flush_003",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - no hole cards
    ("hole_cards_flush_004", "board_cards_flush_004", "hand_flush_004",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - possible trips
    ("hole_cards_flush_005", "board_cards_flush_005", "hand_flush_005",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - possible two pair
    ("hole_cards_flush_006", "board_cards_flush_006", "hand_flush_006",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - possible pair
    ("hole_cards_flush_007", "board_cards_flush_007", "hand_flush_007",
     4, "Flush", "Flush (King, Nine, Eight, Seven, Four)"),  # Flush - possible straight

    ("hole_cards_straight_001", "board_cards_straight_001", "hand_straight_001",
     5, "Straight", "Straight (Jack to Seven)"),  # Straight - all hole cards
    ("hole_cards_straight_002", "board_cards_straight_002", "hand_straight_002",
     5, "Straight", "Straight (Jack to Seven)"),  # Straight - one hole cards
    ("hole_cards_straight_003", "board_cards_straight_003", "hand_straight_003",
     5, "Straight", "Straight (Jack to Seven)"),  # Straight - no hole cards
    ("hole_cards_straight_004", "board_cards_straight_004", "hand_straight_004",
     5, "Straight", "Straight (Jack to Seven)"),  # Straight - possible trips
    ("hole_cards_straight_005", "board_cards_straight_005", "hand_straight_005",
     5, "Straight", "Straight (Jack to Seven)"),  # Straight - possible two pair
    ("hole_cards_straight_006", "board_cards_straight_006", "hand_straight_006",
     5, "Straight", "Straight (Jack to Seven)"),  # Straight - possible pair
    ("hole_cards_straight_007", "board_cards_straight_007", "hand_straight_007",
     5, "Straight", "Straight (Five to Ace)"),  # Straight - Ace Low Straight

    ("hole_cards_trips_001", "board_cards_trips_001", "hand_trips_001",
     6, "Trips", "Trips (Kings with kickers Nine, Eight)"),  # Trips - ALl hole cards
    ("hole_cards_trips_002", "board_cards_trips_002", "hand_trips_002",
     6, "Trips", "Trips (Kings with kickers Nine, Eight)"),  # Trips - One hole cards
    ("hole_cards_trips_003", "board_cards_trips_003", "hand_trips_003",
     6, "Trips", "Trips (Kings with kickers Nine, Eight)"),  # Trips - No hole cards

    ("hole_cards_two_pair_001", "board_cards_two_pair_001", "hand_two_pair_001",
     7, "Two Pair", "Two Pair (Nines and Sevens with kicker Ten)"),  # Two Pair - all hole cards
    ("hole_cards_two_pair_002", "board_cards_two_pair_002", "hand_two_pair_002",
     7, "Two Pair", "Two Pair (Nines and Sevens with kicker Ten)"),  # Two Pair - one hole cards
    ("hole_cards_two_pair_003", "board_cards_two_pair_003", "hand_two_pair_003",
     7, "Two Pair", "Two Pair (Nines and Sevens with kicker Ten)"),  # Two Pair - no hole cards
    ("hole_cards_two_pair_004", "board_cards_two_pair_004", "hand_two_pair_004",
     7, "Two Pair", "Two Pair (Nines and Sevens with kicker Six)"),  # Two Pair - multiple options

    ("hole_cards_pair_001", "board_cards_pair_001", "hand_pair_001",
     8, "Pair", "Pair (Sevens with kickers Ace, Ten, Eight)"),  # Pair - all hole cards
    ("hole_cards_pair_002", "board_cards_pair_002", "hand_pair_002",
     8, "Pair", "Pair (Sevens with kickers Ace, Ten, Eight)"),  # Pair - one hole card
    ("hole_cards_pair_003", "board_cards_pair_003", "hand_pair_003",
     8, "Pair", "Pair (Sevens with kickers Ace, Ten, Eight)"),  # Pair - no hole cards

    ("hole_cards_high_card_001", "board_cards_high_card_001", "hand_high_card_001",
     9, "High Card", "High Card (Jack, Nine, Eight, Six, Four)"),  # High Card - all hole cards
    ("hole_cards_high_card_002", "board_cards_high_card_002", "hand_high_card_002",
     9, "High Card", "High Card (Jack, Nine, Eight, Six, Four)"),  # High Card - one hole cards
    ("hole_cards_high_card_003", "board_cards_high_card_003", "hand_high_card_003",
     9, "High Card", "High Card (Jack, Nine, Eight, Six, Four)"),  # High Card - no hole cards
])
def test_when_find_best_hand_then_correct_response_returned(hole_cards, board_cards, best_hand, hand_rank, hand_title,
                                                            hand_description, solver_instance):
    hole_cards = get_hand(hole_cards)
    board_cards = get_hand(board_cards)
    expected_best_hand = get_hand(best_hand)

    actual_result = solver_instance.find_best_hand(hole_cards, board_cards)

    assert all(
        expected_card in actual_result["best_hand"]
        for expected_card in expected_best_hand
    )

    assert all(
        actual_card in expected_best_hand
        for actual_card in actual_result["best_hand"]
    )

    assert hand_rank == actual_result["hand_rank"]
    assert hand_title == actual_result["hand_title"]
    assert hand_description == actual_result["hand_description"]


@mark.parametrize("test_case", [
    "straight_flush_multi", "straight_flush_multi_tie", "straight_flush_multi_tie_exact",
    "straight_flush_multi_ace_low_straights", "straight_flush_all_ace_low_straights", "quads_multi",
    "quads_multi_tie", "quads_multi_tie_exact", "full_house_multi", "full_house_multi_tie",
    "full_house_multi_tie_exact", "flush_multi", "flush_multi_tie", "flush_multi_tie_exact", "straight_multi",
    "straight_multi_tie", "straight_multi_tie_exact", "straight_multi_ace_low_straights",
    "straight_all_ace_low_straights", "trips_multi", "trips_multi_tie", "trips_multi_tie_exact",
    "two_pair_multi", "two_pair_multi_tie", "two_pair_multi_tie_exact", "pair_multi", "pair_multi_tie",
    "pair_multi_tie_exact", "high_card_multi", "high_card_multi_tie", "high_card_multi_tie_exact", "one_hand_mixed",
    "two_hands_mixed", "three_hands_mixed", "four_hands_mixed", "five_hands_mixed", "six_hands_mixed",
    "seven_hands_mixed", "eight_hands_mixed", "nine_hands_mixed"
])
def test_when_rank_hands_then_correct_dictionary_returned(test_case, solver_instance):
    hands = get_player_hands_dict(test_case)
    expected_rank_dict = get_rank_dictionary(test_case)

    rank_dict = solver_instance.rank_hands(hands)

    assert rank_dict.keys() == expected_rank_dict.keys()

    for rank, rank_info in rank_dict.items():
        assert rank_info["players"] == expected_rank_dict[rank]["players"]
        assert rank_info["hand_description"] == expected_rank_dict[rank]["hand_description"]


@mark.parametrize("hole_cards, board_cards, expected", [
    ("hole_2p_001_tt_v_ak", ["C4", "D8", "H5", "CQ"], {"player_a": 86.36, "player_b": 13.64}),  # pair v high cards - outs to over pairs
    ("hole_2p_001_tt_v_ak", ["S4", "S8", "H5", "CQ"], {"player_a": 68.18, "player_b": 31.82}),  # pair v high cards - outs to over pairs + flush
    ("hole_2p_001_tt_v_ak", ["S4", "S6", "HJ", "CQ"], {"player_a": 63.64, "player_b": 36.36}),  # pair v high cards - outs to over pairs + flush + single straight
    ("hole_2p_002_88_TKs", ["S4", "S6", "HJ", "CQ"], {"player_a": 54.55, "player_b": 45.45}),  # pair v high cards - outs to over pairs + flush + open straight
    ("hole_2p_003_AQo_TKs", ["HJ", "HK", "S7", "S4"], {"player_a": 11.36, "player_b": 88.64}),
])
def test_when_find_odds_and_one_draw_remaining_then_correct_odds_returned(hole_cards, board_cards, expected, solver_instance):
    hole_cards = get_player_hands_dict(hole_cards)
    board_cards = get_cards(board_cards)
    actual = solver_instance.find_odds(hole_cards, board_cards, True)

    assert actual == expected





##########################################
# PERFORMANCE TESTING FIND_OUTS
#
# Trying to test how performant my find_outs method is when using different strategies
# Im sure there are much better ways to store this but for now it will live here
#
# TESTS TYPES / CODE
# 1) Pre Flop:
# import datetime
# from pypoker.deck import Card
# from pypoker.engine.logic.texas_holdem import TexasHoldemHandSolver
# solver = TexasHoldemHandSolver()
# hole_cards = {"player_a": [Card("DT"), Card("ST")], "player_b": [Card("HA"), Card("HK")]}
# board_cards = []
#
#
# start = datetime.datetime.now()
# outs = solver.find_odds(hole_cards, board_cards)
# end = datetime.datetime.now()
# duration = end - start
# print(f"DURATION OF PRE-FLOP ODDS CALCULATION IS {duration}")
#
#
# 2) 1 Card flop
# import datetime
# from pypoker.deck import Card
# from pypoker.engine.logic.texas_holdem import TexasHoldemHandSolver
# solver = TexasHoldemHandSolver()
# hole_cards = {"player_a": [Card("DT"), Card("ST")], "player_b": [Card("HA"), Card("HK")]}
# board_cards = [Card("H3")]
#
#
# start = datetime.datetime.now()
# outs = solver.find_odds(hole_cards, board_cards)
# end = datetime.datetime.now()
# duration = end - start
# print(f"DURATION OF ONE CARD FLOP ODDS CALCULATION IS {duration}")
#
#
# 3) 2 Card flop
# import datetime
# from pypoker.deck import Card
# from pypoker.engine.logic.texas_holdem import TexasHoldemHandSolver
# solver = TexasHoldemHandSolver()
# hole_cards = {"player_a": [Card("DT"), Card("ST")], "player_b": [Card("HA"), Card("HK")]}
# board_cards = [Card("H3"), Card("SQ")]
#
#
# start = datetime.datetime.now()
# outs = solver.find_odds(hole_cards, board_cards)
# end = datetime.datetime.now()
# duration = end - start
# print(f"DURATION OF TWO CARD FLOP ODDS CALCULATION IS {duration}")
#
#
# 4) post-flop
# import datetime
# from pypoker.deck import Card
# from pypoker.engine.logic.texas_holdem import TexasHoldemHandSolver
# solver = TexasHoldemHandSolver()
# hole_cards = {"player_a": [Card("DT"), Card("ST")], "player_b": [Card("HA"), Card("HK")]}
# board_cards = [Card("H3"), Card("SQ"), Card("H5")]
#
#
# start = datetime.datetime.now()
# outs = solver.find_odds(hole_cards, board_cards)
# end = datetime.datetime.now()
# duration = end - start
# print(f"DURATION OF POST-FLOP ODDS CALCULATION IS {duration}")
#
#
# 5) Turn
# import datetime
# from pypoker.deck import Card
# from pypoker.engine.logic.texas_holdem import TexasHoldemHandSolver
# solver = TexasHoldemHandSolver()
# hole_cards = {"player_a": [Card("DT"), Card("ST")], "player_b": [Card("HA"), Card("HK")]}
# board_cards = [Card("H3"), Card("SQ"), Card("H5"), Card("CJ")]
#
#
# start = datetime.datetime.now()
# outs = solver.find_odds(hole_cards, board_cards)
# end = datetime.datetime.now()
# duration = end - start
# print(f"DURATION OF POST-TURN ODDS CALCULATION IS {duration}")
#
#
#
#
# RESULTS
# desc of change,                                       T1 time,    T2 time,        T3 time,    T4 time,    T5 time
# Base module (eed4304decbe587989b8),                   >900s,      >900s,          24.253824,  00.793782,  00.025991
# Convert Lists to Sets for comparison improvements,    >900s,      04:24.983775    20.025112,  00.799731,  00.027881
