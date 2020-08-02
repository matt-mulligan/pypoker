from pytest import mark, fixture
from pypoker.deck import Card

###################
#  TEST FIXTURES  #
###################
from pypoker.poker_engine.hand_solver import PokerHandSolver


@fixture
def hand_solver():
    return PokerHandSolver()


###################
#  CARD PROVIDER  #
###################
def get_card(card):
    """
    This helper method will build and return a card object based on the card value passed
    :param card: String containing 'SUIT-VALUE' where suit is the first letter of the suit [C,S,D,H] and value is an
    integer from 2-14
    :return: Card Object
    """

    suit = int({"C": 0, "D": 1, "H": 2, "S": 3}[card.split("-")[0]])
    value = int(card.split("-")[1])
    return Card(value, suit)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["H-5", "H-8"], ["C-7", "C-6", "H-6", "H-7", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 2 from hand, 3 from board, board of 5
    (["S-3", "H-7"], ["S-7", "H-6", "H-5", "H-8", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 1 from hand, 4 from board, board of 5
    (["D-3", "H-14"], ["H-7", "H-6", "H-5", "H-8", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 0 from hand, 5 from board, board of 5
    (["H-14", "H-13"], ["H-11", "C-6", "H-12", "H-10"], ["H-14", "H-13", "H-12", "H-11", "H-10"]),  # Hearts, 2 from hand, 3 from board, board of 4
    (["D-12", "H-9"], ["H-10", "H-13", "H-11", "H-12"], ["H-13", "H-12", "H-11", "H-10", "H-9"]),  # Hearts, 1 from hand, 4 from board, board of 4
    (["H-5", "H-8"], ["H-6", "H-7", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 2 from hand, 3 from board, board of 3
    (["H-6", "H-9"], ["H-8", "H-7", "H-12", "H-10", "H-11"], ["H-12", "H-11", "H-10", "H-9", "H-8"]),  # Hearts, multiple matches, board of 5
    (["H-6", "H-9"], ["H-8", "H-7", "H-10", "H-11"], ["H-11", "H-10", "H-9", "H-8", "H-7"]),  # Hearts, multiple matches, board of 4
    (["C-4", "C-7"], ['C-8', 'S-6', 'S-5', 'C-5', 'C-6'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 2 from hand, 3 from board, board of 5
    (["D-2", "C-6"], ['C-4', 'C-8', 'D-6', 'C-5', 'C-7'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 1 from hand, 4 from board, board of 5
    (["H-2", "C-13"], ['C-6', 'C-8', 'C-7', 'C-4', 'C-5'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 0 from hand, 5 from board, board of 5
    (["C-13", "C-12"], ['C-11', 'C-10', 'S-5', 'C-9'], ["C-13", "C-12", "C-11", "C-10", "C-9"]),  # Clubs, 2 from hand, 3 from board, board of 4
    (["H-11", "C-8"], ['C-10', 'C-9', 'C-11', 'C-12'], ["C-12", "C-11", "C-10", "C-9", "C-8"]),  # Clubs, 1 from hand, 4 from board, board of 4
    (["C-4", "C-7"], ['C-6', 'C-5', 'C-8'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 2 from hand, 3 from board, board of 3
    (["C-5", "C-6"], ['C-9', 'C-7', 'C-8', 'C-10', 'C-11'], ["C-11", "C-10", "C-9", "C-8", "C-7"]),  # Clubs, multiple matches, board of 5
    (["C-5", "C-8"], ['C-9', 'C-10', 'C-6', 'C-7'], ["C-10", "C-9", "C-8", "C-7", "C-6"]),  # Clubs, multiple matches, board of 4
    (["D-3", "D-6"], ['D-4', 'H-6', 'D-7', 'H-7', 'D-5'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 2 from hand, 3 from board, board of 5
    (["C-3", "D-5"], ['C-7', 'D-3', 'D-7', 'D-4', 'D-6'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 1 from hand, 4 from board, board of 5
    (["S-3", "D-12"], ['D-6', 'D-4', 'D-5', 'D-7', 'D-3'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 0 from hand, 5 from board, board of 5
    (["D-12", "D-11"], ['D-8', 'D-9', 'D-10', 'H-6'], ["D-12", "D-11", "D-10", "D-9", "D-8"]),  # Diamonds, 2 from hand, 3 from board, board of 4
    (["S-12", "D-7"], ['D-11', 'D-9', 'D-8', 'D-10'], ["D-11", "D-10", "D-9", "D-8", "D-7"]),  # Diamonds, 1 from hand, 4 from board, board of 4
    (["D-3", "D-6"], ['D-4', 'D-7', 'D-5'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 2 from hand, 3 from board, board of 3
    (["D-4", "D-7"], ['D-6', 'D-5', 'D-10', 'D-8', 'D-9'], ["D-10", "D-9", "D-8", "D-7", "D-6"]),  # Diamonds, multiple matches, board of 5
    (["D-4", "D-7"], ['D-9', 'D-8', 'D-6', 'D-5'], ["D-9", "D-8", "D-7", "D-6", "D-5"]),  # Diamonds, multiple matches, board of 4
    (["S-7", "S-10"], ["H-7", "H-6", "S-8", "S-9", "S-11"], ["S-11", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 2 from hand, 3 from board, board of 5
    (["C-3", "S-9"], ["C-7", "S-8", "S-7", "S-10", "S-11"], ["S-11", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 1 from hand, 4 from board, board of 5
    (["D-3", "S-14"], ["S-9", "S-8", "S-7", "S-10", "S-11"], ["S-11", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 0 from hand, 5 from board, board of 5
    (["S-14", "S-13"], ["S-11", "H-6", "S-12", "S-10"], ["S-14", "S-13", "S-12", "S-11", "S-10"]),  # Spades, 2 from hand, 3 from board, board of 4
    (["D-12", "S-9"], ["S-10", "S-13", "S-11", "S-12"], ["S-13", "S-12", "S-11", "S-10", "S-9"]),  # Spades, 1 from hand, 4 from board, board of 4
    (["S-7", "S-10"], ["S-8", "S-9", "S-11"], ["S-11", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 2 from hand, 3 from board, board of 3
    (["S-8", "S-11"], ["S-10", "S-9", "S-14", "S-12", "S-13"], ["S-14", "S-13", "S-12", "S-11", "S-10"]),  # Spades, multiple matches, board of 5
    (["S-8", "S-11"], ["S-10", "S-9", "S-12", "S-13"], ["S-13", "S-12", "S-11", "S-10", "S-9"]),  # Spades, multiple matches, board of 4
])
def test_when_find_player_best_hand_and_texas_holdem_and_straight_flush_then_straight_flush_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Straight Flush"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["D-4", "H-4"], ["S-4", "C-4", "S-12", "D-10", "D-8"], ["D-4", "H-4", "S-4", "C-4", "S-12"]),
    (["D-7", "H-4"], ["S-7", "C-4", "C-7", "D-10", "H-7"], ["D-7", "H-7", "S-7", "C-7", "D-10"]),
    (["D-13", "H-4"], ["S-10", "C-10", "C-7", "D-10", "H-10"], ["D-10", "H-10", "S-10", "C-10", "D-13"]),
    (["D-9", "H-9"], ["S-9", "C-9", "C-7", "D-10"], ["D-9", "H-9", "S-9", "C-9", "D-10"]),
    (["D-6", "H-5"], ["S-6", "C-6", "C-4", "H-6"], ["D-6", "H-6", "S-6", "C-6", "H-5"]),
    (["D-8", "H-13"], ["S-2", "C-2", "D-2", "H-2"], ["D-2", "H-2", "S-2", "C-2", "H-13"]),
    (["D-13", "H-13"], ["S-13", "C-13", "D-8"], ["D-13", "H-13", "S-13", "C-13", "D-8"]),
    (["D-11", "H-9"], ["S-11", "C-11", "H-11"], ["D-11", "H-11", "S-11", "C-11", "H-9"]),
])
def test_when_find_player_best_hand_and_texas_holdem_and_quads_then_quads_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Quads"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["D-7", "H-7"], ["C-4", "H-12", "C-7", "D-4", "S-2"], ["D-7", "H-7", "C-7", "C-4", "D-4"]),
    (["D-9", "H-12"], ["C-4", "D-12", "C-7", "D-4", "S-4"], ["C-4", "D-4", "S-4", "H-12", "D-12"]),
    (["D-9", "H-12"], ["C-8", "D-8", "C-2", "D-2", "S-8"], ["C-8", "D-8", "S-8", "C-2", "D-2"]),
    (["D-9", "H-12"], ["C-9", "D-12", "S-9", "D-7", "S-7"], ["C-9", "D-9", "S-9", "H-12", "D-12"]),
    (["D-9", "H-6"], ["C-9", "D-6", "S-9", "D-7", "S-7"], ["C-9", "D-9", "S-9", "D-7", "S-7"]),
    (["S-5", "D-11"], ["H-11", "C-11", "H-3", "C-5"], ["H-11", "C-11", "D-11", "S-5", "C-5"]),
    (["S-5", "D-11"], ["H-10", "C-10", "H-5", "D-10"], ["D-10", "C-10", "H-10", "S-5", "H-5"]),
    (["S-5", "D-11"], ["H-11", "C-11", "C-5"], ["H-11", "C-11", "D-11", "S-5", "C-5"]),
])
def test_when_find_player_best_hand_and_texas_holdem_and_full_house_then_full_house_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Full House"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)
