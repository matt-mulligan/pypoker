from pytest import fixture, mark

from fixtures.cards import get_hand
from pypoker.poker_engine.hand_solver.texas_holdem import TexasHoldemHandSolver


@fixture
def solver_instance():
    return TexasHoldemHandSolver()


@mark.parametrize("hole_cards, board_cards, best_hand, hand_rank, hand_title, hand_description", [
    ("hole_cards_straight_flush_001", "board_cards_straight_flush_001", "hand_straight_flush_001",
     1, "Straight Flush", "Straight Flush (Ace to Ten of Diamonds)"),  # straight flush - all hole cards
    ("hole_cards_straight_flush_002", "board_cards_straight_flush_002", "hand_straight_flush_002",
     1, "Straight Flush", "Straight Flush (Ten to Six of Hearts)"),  # straight flush - 1 hole cards
    ("hole_cards_straight_flush_003", "board_cards_straight_flush_003", "hand_straight_flush_003",
     1, "Straight Flush", "Straight Flush (Seven to Three of Clubs)"),  # straight flush - no hole cards
    ("hole_cards_straight_flush_004", "board_cards_straight_flush_004", "hand_straight_flush_004",
     1, "Straight Flush", "Straight Flush (King to Nine of Diamonds)"),  # straight flush - multiple
    ("hole_cards_straight_flush_005", "board_cards_straight_flush_005", "hand_straight_flush_005",
     1, "Straight Flush", "Straight Flush (Ace to Ten of Hearts)"),  # Straight Flush - possible trips
    ("hole_cards_straight_flush_006", "board_cards_straight_flush_006", "hand_straight_flush_006",
     1, "Straight Flush", "Straight Flush (Eight to Four of Diamonds)"),  # Straight Flush - possible two pair
    ("hole_cards_straight_flush_007", "board_cards_straight_flush_007", "hand_straight_flush_007",
     1, "Straight Flush", "Straight Flush (Jack to Seven of Clubs)"),  # Straight Flush - possible pair

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
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - all hole cards
    ("hole_cards_flush_002", "board_cards_flush_002", "hand_flush_002",
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - 1 hole cards
    ("hole_cards_flush_003", "board_cards_flush_003", "hand_flush_003",
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - no hole cards
    ("hole_cards_flush_004", "board_cards_flush_004", "hand_flush_004",
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - possible trips
    ("hole_cards_flush_005", "board_cards_flush_005", "hand_flush_005",
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - possible two pair
    ("hole_cards_flush_006", "board_cards_flush_006", "hand_flush_006",
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - possible pair
    ("hole_cards_flush_007", "board_cards_flush_007", "hand_flush_007",
     4, "Flush", "Flush (Hearts with cards King, Nine, Eight, Seven, Four)"),  # Flush - possible straight

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

    ("hole_cards_trips_001", "board_cards_trips_001", "hand_trips_001",
     6, "Trips", "Trips (Kings with kickers Nine, Eight)"),  # Trips - ALl hole cards
    ("hole_cards_trips_002", "board_cards_trips_002", "hand_trips_002",
     6, "Trips", "Trips (Kings with kickers Nine, Eight)"),  # Trips - One hole cards
    ("hole_cards_trips_003", "board_cards_trips_003", "hand_trips_003",
     6, "Trips", "Trips (Kings with kickers Nine, Eight)"),  # Trips - No hole cards

    ("hole_cards_two_pair_001", "board_cards_two_pair_001", "hand_two_pair_001",
     7, "Two Pair", "Two Pair (Nines and Sevens with kicker Ten)"),  # Two Pair - all hole cards
    ("hole_cards_two_pair_002", "board_cards_two_pair_002", "hand_two_pair_002",
     7, "Two Pair", "Two Pairr (Nines and Sevens with kicker Ten)"),  # Two Pair - one hole cards
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
