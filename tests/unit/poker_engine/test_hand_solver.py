from unittest.mock import patch

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
    :param card: String containing 'SUIT-VALUE' where suit is the first letter of the suit [C,S,D,H] and value is a
    string from 2-A
    :return: Card Object
    """

    suit = card.split("-")[0]
    value = card.split("-")[1]
    return Card(value, suit)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["H-5", "H-8"], ["C-7", "C-6", "H-6", "H-7", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 2 from hand, 3 from board, board of 5
    (["S-3", "H-7"], ["S-7", "H-6", "H-5", "H-8", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 1 from hand, 4 from board, board of 5
    (["D-3", "H-A"], ["H-7", "H-6", "H-5", "H-8", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 0 from hand, 5 from board, board of 5
    (["H-A", "H-K"], ["H-J", "C-6", "H-Q", "H-10"], ["H-A", "H-K", "H-Q", "H-J", "H-10"]),  # Hearts, 2 from hand, 3 from board, board of 4
    (["D-Q", "H-9"], ["H-10", "H-K", "H-J", "H-Q"], ["H-K", "H-Q", "H-J", "H-10", "H-9"]),  # Hearts, 1 from hand, 4 from board, board of 4
    (["H-5", "H-8"], ["H-6", "H-7", "H-9"], ["H-9", "H-8", "H-7", "H-6", "H-5"]),  # Hearts, 2 from hand, 3 from board, board of 3
    (["H-6", "H-9"], ["H-8", "H-7", "H-Q", "H-10", "H-J"], ["H-Q", "H-J", "H-10", "H-9", "H-8"]),  # Hearts, multiple matches, board of 5
    (["H-6", "H-9"], ["H-8", "H-7", "H-10", "H-J"], ["H-J", "H-10", "H-9", "H-8", "H-7"]),  # Hearts, multiple matches, board of 4
    (["C-4", "C-7"], ['C-8', 'S-6', 'S-5', 'C-5', 'C-6'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 2 from hand, 3 from board, board of 5
    (["D-2", "C-6"], ['C-4', 'C-8', 'D-6', 'C-5', 'C-7'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 1 from hand, 4 from board, board of 5
    (["H-2", "C-K"], ['C-6', 'C-8', 'C-7', 'C-4', 'C-5'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 0 from hand, 5 from board, board of 5
    (["C-K", "C-Q"], ['C-J', 'C-10', 'S-5', 'C-9'], ["C-K", "C-Q", "C-J", "C-10", "C-9"]),  # Clubs, 2 from hand, 3 from board, board of 4
    (["H-J", "C-8"], ['C-10', 'C-9', 'C-J', 'C-Q'], ["C-Q", "C-J", "C-10", "C-9", "C-8"]),  # Clubs, 1 from hand, 4 from board, board of 4
    (["C-4", "C-7"], ['C-6', 'C-5', 'C-8'], ["C-8", "C-7", "C-6", "C-5", "C-4"]),  # Clubs, 2 from hand, 3 from board, board of 3
    (["C-5", "C-6"], ['C-9', 'C-7', 'C-8', 'C-10', 'C-J'], ["C-J", "C-10", "C-9", "C-8", "C-7"]),  # Clubs, multiple matches, board of 5
    (["C-5", "C-8"], ['C-9', 'C-10', 'C-6', 'C-7'], ["C-10", "C-9", "C-8", "C-7", "C-6"]),  # Clubs, multiple matches, board of 4
    (["D-3", "D-6"], ['D-4', 'H-6', 'D-7', 'H-7', 'D-5'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 2 from hand, 3 from board, board of 5
    (["C-3", "D-5"], ['C-7', 'D-3', 'D-7', 'D-4', 'D-6'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 1 from hand, 4 from board, board of 5
    (["S-3", "D-Q"], ['D-6', 'D-4', 'D-5', 'D-7', 'D-3'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 0 from hand, 5 from board, board of 5
    (["D-Q", "D-J"], ['D-8', 'D-9', 'D-10', 'H-6'], ["D-Q", "D-J", "D-10", "D-9", "D-8"]),  # Diamonds, 2 from hand, 3 from board, board of 4
    (["S-Q", "D-7"], ['D-J', 'D-9', 'D-8', 'D-10'], ["D-J", "D-10", "D-9", "D-8", "D-7"]),  # Diamonds, 1 from hand, 4 from board, board of 4
    (["D-3", "D-6"], ['D-4', 'D-7', 'D-5'], ["D-7", "D-6", "D-5", "D-4", "D-3"]),  # Diamonds, 2 from hand, 3 from board, board of 3
    (["D-4", "D-7"], ['D-6', 'D-5', 'D-10', 'D-8', 'D-9'], ["D-10", "D-9", "D-8", "D-7", "D-6"]),  # Diamonds, multiple matches, board of 5
    (["D-4", "D-7"], ['D-9', 'D-8', 'D-6', 'D-5'], ["D-9", "D-8", "D-7", "D-6", "D-5"]),  # Diamonds, multiple matches, board of 4
    (["S-7", "S-10"], ["H-7", "H-6", "S-8", "S-9", "S-J"], ["S-J", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 2 from hand, 3 from board, board of 5
    (["C-3", "S-9"], ["C-7", "S-8", "S-7", "S-10", "S-J"], ["S-J", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 1 from hand, 4 from board, board of 5
    (["D-3", "S-A"], ["S-9", "S-8", "S-7", "S-10", "S-J"], ["S-J", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 0 from hand, 5 from board, board of 5
    (["S-A", "S-K"], ["S-J", "H-6", "S-Q", "S-10"], ["S-A", "S-K", "S-Q", "S-J", "S-10"]),  # Spades, 2 from hand, 3 from board, board of 4
    (["D-Q", "S-9"], ["S-10", "S-K", "S-J", "S-Q"], ["S-K", "S-Q", "S-J", "S-10", "S-9"]),  # Spades, 1 from hand, 4 from board, board of 4
    (["S-7", "S-10"], ["S-8", "S-9", "S-J"], ["S-J", "S-10", "S-9", "S-8", "S-7"]),  # Spades, 2 from hand, 3 from board, board of 3
    (["S-8", "S-J"], ["S-10", "S-9", "S-A", "S-Q", "S-K"], ["S-A", "S-K", "S-Q", "S-J", "S-10"]),  # Spades, multiple matches, board of 5
    (["S-8", "S-J"], ["S-10", "S-9", "S-Q", "S-K"], ["S-K", "S-Q", "S-J", "S-10", "S-9"]),  # Spades, multiple matches, board of 4
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
    (["D-4", "H-4"], ["S-4", "C-4", "S-Q", "D-10", "D-8"], ["D-4", "H-4", "S-4", "C-4", "S-Q"]),
    (["D-7", "H-4"], ["S-7", "C-4", "C-7", "D-10", "H-7"], ["D-7", "H-7", "S-7", "C-7", "D-10"]),
    (["D-K", "H-4"], ["S-10", "C-10", "C-7", "D-10", "H-10"], ["D-10", "H-10", "S-10", "C-10", "D-K"]),
    (["D-9", "H-9"], ["S-9", "C-9", "C-7", "D-10"], ["D-9", "H-9", "S-9", "C-9", "D-10"]),
    (["D-6", "H-5"], ["S-6", "C-6", "C-4", "H-6"], ["D-6", "H-6", "S-6", "C-6", "H-5"]),
    (["D-8", "H-K"], ["S-2", "C-2", "D-2", "H-2"], ["D-2", "H-2", "S-2", "C-2", "H-K"]),
    (["D-K", "H-K"], ["S-K", "C-K", "D-8"], ["D-K", "H-K", "S-K", "C-K", "D-8"]),
    (["D-J", "H-9"], ["S-J", "C-J", "H-J"], ["D-J", "H-J", "S-J", "C-J", "H-9"]),
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
    (["D-7", "H-7"], ["C-4", "H-Q", "C-7", "D-4", "S-2"], ["D-7", "H-7", "C-7", "C-4", "D-4"]),
    (["D-9", "H-Q"], ["C-4", "D-Q", "C-7", "D-4", "S-4"], ["C-4", "D-4", "S-4", "H-Q", "D-Q"]),
    (["D-9", "H-Q"], ["C-8", "D-8", "C-2", "D-2", "S-8"], ["C-8", "D-8", "S-8", "C-2", "D-2"]),
    (["D-9", "H-Q"], ["C-9", "D-Q", "S-9", "D-7", "S-7"], ["C-9", "D-9", "S-9", "H-Q", "D-Q"]),
    (["D-9", "H-6"], ["C-9", "D-6", "S-9", "D-7", "S-7"], ["C-9", "D-9", "S-9", "D-7", "S-7"]),
    (["S-5", "D-J"], ["H-J", "C-J", "H-3", "C-5"], ["H-J", "C-J", "D-J", "S-5", "C-5"]),
    (["S-5", "D-J"], ["H-10", "C-10", "H-5", "D-10"], ["D-10", "C-10", "H-10", "S-5", "H-5"]),
    (["S-5", "D-J"], ["H-J", "C-J", "C-5"], ["H-J", "C-J", "D-J", "S-5", "C-5"]),
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


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["H-Q", "H-2"], ["C-Q", "H-3", "D-Q", "H-9", "H-4"], ["H-Q", "H-9", "H-4", "H-3", "H-2"]),
    (["D-Q", "C-2"], ["D-2", "D-9", "D-7", "H-9", "D-4"], ["D-Q", "D-9", "D-7", "D-4", "D-2"]),
    (["C-Q", "H-9"], ["S-Q", "S-3", "S-J", "S-9", "S-4"], ["S-Q", "S-J", "S-9", "S-4", "S-3"]),
    (["S-3", "S-8"], ["S-Q", "S-6", "S-J", "S-9", "S-4"], ["S-Q", "S-J", "S-9", "S-8", "S-6"]),
    (["H-3", "H-4"], ["H-Q", "H-6", "H-J", "H-9", "H-7"], ["H-Q", "H-J", "H-9", "H-7", "H-6"]),
    (["D-4", "D-10"], ["D-J", "S-10", "D-6", "D-8"], ["D-J", "D-10", "D-8", "D-6", "D-4"]),
    (["S-6", "D-6"], ["S-9", "S-K", "S-4", "S-2"], ["S-K", "S-9", "S-6", "S-4", "S-2"]),
    (["D-2", "D-9"], ["D-J", "D-6", "D-Q", "D-8"], ["D-Q", "D-J", "D-9", "D-8", "D-6"]),
    (["C-10", "C-J"], ["C-2", "C-7", "C-6"], ["C-J", "C-10", "C-7", "C-6", "C-2"])
])
def test_when_find_player_best_hand_and_texas_holdem_and_flush_then_flush_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Flush"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["H-Q", "D-9"], ["C-10", "D-3", "S-J", "H-8", "C-Q"], ["H-Q", "S-J", "C-10", "D-9", "H-8"]),
    (["H-Q", "D-9"], ["C-10", "D-3", "S-7", "H-8", "C-6"], ["C-10", "D-9", "H-8", "S-7", "C-6"]),
    (["H-Q", "D-9"], ["C-4", "D-3", "S-5", "H-7", "C-6"], ["H-7", "C-6", "S-5", "C-4", "D-3"]),
    (["H-Q", "D-9"], ["C-10", "D-K", "S-J", "H-8", "C-7"], ["D-K", "H-Q", "S-J", "C-10", "D-9"]),
    (["H-6", "D-9"], ["C-10", "D-8", "S-J", "H-7", "C-5"], ["S-J", "C-10", "D-9", "D-8", "H-7"]),
    (["H-6", "D-5"], ["C-10", "D-8", "S-J", "H-7", "C-9"], ["S-J", "C-10", "C-9", "D-8", "H-7"]),
    (["H-Q", "D-9"], ["C-4", "S-10", "H-J", "D-8"], ["H-Q", "H-J", "S-10", "D-9", "D-8"]),
    (["H-Q", "D-9"], ["C-6", "S-10", "H-7", "D-8"], ["S-10", "D-9", "D-8", "H-7", "C-6"]),
    (["H-5", "D-9"], ["C-6", "S-10", "H-7", "D-8"], ["S-10", "D-9", "D-8", "H-7", "C-6"]),
    (["H-Q", "D-9"], ["C-J", "S-10", "H-7", "D-8"], ["H-Q", "C-J", "S-10", "D-9", "D-8"]),
    (["H-Q", "D-9"], ["C-J", "S-10", "D-8"], ["H-Q", "C-J", "S-10", "D-9", "D-8"])
])
def test_when_find_player_best_hand_and_texas_holdem_and_straight_then_straight_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Straight"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["D-4", "H-4"], ["S-4", "C-9", "S-Q", "D-10", "D-8"], ["D-4", "H-4", "S-4", "S-Q", "D-10"]),
    (["D-7", "H-4"], ["S-7", "C-9", "C-7", "D-10", "H-3"], ["D-7", "S-7", "C-7", "D-10", "C-9"]),
    (["D-K", "H-4"], ["S-10", "C-10", "C-7", "D-10", "H-6"], ["D-10", "S-10", "C-10", "D-K", "C-7"]),
    (["D-9", "H-9"], ["S-9", "C-J", "C-7", "D-10"], ["D-9", "H-9", "S-9", "C-J", "D-10"]),
    (["D-6", "H-5"], ["S-6", "C-6", "C-4", "H-J"], ["D-6", "S-6", "C-6", "H-J", "H-5"]),
    (["D-8", "H-K"], ["S-2", "C-9", "D-2", "H-2"], ["D-2", "H-2", "S-2", "H-K", "C-9"]),
    (["D-K", "H-K"], ["S-K", "D-8", "S-9"], ["D-K", "H-K", "S-K", "S-9", "D-8"]),
    (["D-J", "H-9"], ["S-J", "C-7", "H-J"], ["D-J", "H-J", "S-J", "H-9", "C-7"]),
    (["D-3", "H-9"], ["S-J", "C-J", "H-J"], ["H-J", "S-J", "C-J", "H-9", "D-3"])
])
def test_when_find_player_best_hand_and_texas_holdem_and_trips_then_trips_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Trips"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["D-7", "H-Q"], ["C-7", "D-2", "H-J", "S-Q", "D-3"], ["H-Q", "S-Q", "D-7", "C-7", "H-J"]),
    (["D-7", "H-Q"], ["C-7", "D-6", "H-J", "S-6", "D-3"], ["D-7", "C-7", "D-6", "S-6", "H-Q"]),
    (["D-7", "H-Q"], ["C-9", "D-2", "H-9", "S-3", "D-3"], ["C-9", "H-9", "S-3", "D-3", "H-Q"]),
    (["D-7", "H-4"], ["C-9", "D-Q", "H-9", "S-3", "D-3"], ["C-9", "H-9", "S-3", "D-3", "D-Q"]),
    (["D-3", "H-Q"], ["C-3", "D-2", "H-9", "S-Q"], ["H-Q", "S-Q", "D-3", "C-3", "H-9"]),
    (["D-3", "H-Q"], ["C-3", "D-2", "H-2", "S-6"], ["D-3", "C-3", "D-2", "H-2", "H-Q"]),
    (["D-3", "H-Q"], ["C-5", "D-5", "H-7", "S-7"], ["H-7", "S-7", "D-5", "C-5", "H-Q"]),
    (["D-3", "H-Q"], ["C-3", "H-9", "S-Q"], ["H-Q", "S-Q", "D-3", "C-3", "H-9"]),
    (["D-9", "H-Q"], ["C-7", "H-7", "S-Q"], ["H-Q", "S-Q", "C-7", "H-7", "D-9"]),
])
def test_when_find_player_best_hand_and_texas_holdem_and_two_pair_then_two_pair_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Two Pair"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["D-9", "C-9"], ["S-J", "C-7", "H-4", "H-3", "D-Q"], ["D-9", "C-9", "D-Q", "S-J", "C-7"]),
    (["D-4", "C-9"], ["S-J", "C-7", "H-4", "H-3", "D-Q"], ["D-4", "H-4", "D-Q", "S-J", "C-9"]),
    (["D-4", "C-3"], ["S-J", "C-J", "H-9", "H-6", "D-Q"], ["S-J", "C-J", "D-Q", "H-9", "H-6"]),
    (["D-10", "C-9"], ["S-J", "C-J", "H-3", "H-6", "D-Q"], ["S-J", "C-J", "D-Q", "D-10", "C-9"]),
    (["D-9", "C-9"], ["S-J", "C-7", "H-4", "H-3"], ["D-9", "C-9", "S-J", "C-7", "H-4"]),
    (["D-6", "C-9"], ["S-J", "C-7", "H-9", "H-3"], ["C-9", "H-9", "S-J", "C-7", "D-6"]),
    (["D-4", "C-9"], ["S-J", "C-5", "H-5", "H-10"], ["C-5", "H-5", "S-J", "H-10", "C-9"]),
    (["D-9", "C-9"], ["S-J", "C-7", "H-3"], ["D-9", "C-9", "S-J", "C-7", "H-3"]),
    (["D-K", "C-9"], ["S-J", "D-9", "H-3"], ["D-9", "C-9", "D-K", "S-J", "H-3"]),
    (["D-4", "C-9"], ["S-J", "C-7", "H-J"], ["S-J", "H-J", "C-9", "C-7", "D-4"]),
])
def test_when_find_player_best_hand_and_texas_holdem_and_pair_then_pair_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "Pair"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


@mark.parametrize("player_cards, board_cards, expected_hand", [
    (["D-K", "C-Q"], ["S-J", "C-7", "H-4", "H-3", "D-5"], ["D-K", "C-Q", "S-J", "C-7", "D-5"]),
    (["D-K", "C-2"], ["S-J", "C-7", "H-4", "H-Q", "D-5"], ["D-K", "H-Q", "S-J", "C-7", "D-5"]),
    (["D-2", "C-3"], ["S-J", "C-7", "H-4", "H-Q", "D-5"], ["H-Q", "S-J", "C-7", "D-5", "H-4"]),
    (["D-K", "C-Q"], ["S-J", "C-7", "H-4", "H-3"], ["D-K", "C-Q", "S-J", "C-7", "H-4"]),
    (["D-2", "C-10"], ["S-J", "C-7", "H-9", "H-3"], ["S-J", "C-10", "H-9", "C-7", "H-3"]),
    (["D-4", "C-9"], ["S-J", "C-7", "H-8"], ["S-J", "C-9", "C-7", "H-8", "D-4"])
])
def test_when_find_player_best_hand_and_texas_holdem_and_high_card_then_high_card_returned(
        hand_solver, player_cards, board_cards, expected_hand):
    player_card_objs = [get_card(card) for card in player_cards]
    board_card_objs = [get_card(card) for card in board_cards]
    expected_card_objs = [get_card(card) for card in expected_hand]

    hand_type, hand = hand_solver.find_player_best_hand(player_card_objs, board_card_objs)

    assert hand_type == "High Card"
    assert all(card in hand for card in expected_card_objs)
    assert all(card in expected_card_objs for card in hand)


def test_when_rank_players_hands_and_straight_flushes_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Straight Flush", [get_card(card) for card in ["S-9", "S-J", "S-8", "S-Q", "S-10"]]),  # Queen High Flush
        ("Straight Flush", [get_card(card) for card in ["S-9", "S-8", "S-10", "S-6", "S-7"]]),  # 10 high flush
        ("Straight Flush", [get_card(card) for card in ["S-J", "S-9", "S-Q", "S-8", "S-10"]]),  # Queen High Flush
        ("Straight Flush", [get_card(card) for card in ["S-9", "S-8", "S-10", "S-7", "S-J"]]),  # Jack high flush
        ("Straight Flush", [get_card(card) for card in ["S-Q", "S-9", "S-J", "S-K", "S-10"]]),  # King High Flush
        ("Straight Flush", [get_card(card) for card in ["S-7", "S-9", "S-J", "S-8", "S-10"]]),  # Jack High Flush
        ("Straight Flush", [get_card(card) for card in ["S-10", "S-Q", "S-9", "S-J", "S-8"]])  # Queen High Flush
    ]

    players = [
        {"name": "QUEEN_A", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "TEN", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "QUEEN_B", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "JACK_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "KING", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "JACK_B", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "QUEEN_C", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "KING", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 9, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "QUEEN_A", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 9, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "QUEEN_B", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 9, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "QUEEN_C", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 9, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "JACK_A", "hand_rank": 3, "hand_rank_tie": True,
                                                              "hand_strength": 9, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "JACK_B", "hand_rank": 3, "hand_rank_tie": True,
                                                              "hand_strength": 9, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "TEN", "hand_rank": 4, "hand_rank_tie": False,
                                                              "hand_strength": 9, "tiebreaker_rank": 4}.items())


def test_when_rank_players_hands_and_quads_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Quads", [get_card(card) for card in ["S-7", "D-7", "S-3", "H-7", "C-7"]]),  # Quad 7's 3 kick
        ("Quads", [get_card(card) for card in ["S-2", "S-9", "D-9", "H-9", "C-9"]]),  # Quad 9's 2 kick
        ("Quads", [get_card(card) for card in ["S-3", "C-3", "H-3", "D-3", "C-5"]]),  # Quad 3's 5 kick
        ("Quads", [get_card(card) for card in ["S-7", "C-7", "H-7", "S-Q", "D-7"]]),  # Quad 7's Q kick
        ("Quads", [get_card(card) for card in ["S-8", "S-9", "C-9", "H-9", "D-9"]]),  # Quad 9's 8 kick
        ("Quads", [get_card(card) for card in ["S-9", "C-9", "S-K", "H-9", "D-9"]]),  # Quad 9's K kicks
        ("Quads", [get_card(card) for card in ["S-7", "S-Q", "C-7", "H-7", "D-7"]]),  # Quad 7's Q kicks
    ]

    players = [  # player_cards irrelevant due to side effect usage
        {"name": "SEVENS_2ND", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "NINES_3RD", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "THREES", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "SEVENS_1ST_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "NINES_2ND", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "NINES_1ST", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "SEVENS_1ST_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]  # board cards irrelevant due to side effect usage

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "NINES_1ST", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 8, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "NINES_2ND", "hand_rank": 2, "hand_rank_tie": False,
                                                              "hand_strength": 8, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "NINES_3RD", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 8, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "SEVENS_1ST_TIE_A", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 8, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "SEVENS_1ST_TIE_B", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 8, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "SEVENS_2ND", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 8, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "THREES", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 8, "tiebreaker_rank": 6}.items())


def test_when_rank_players_hands_and_full_house_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Full House", [get_card(card) for card in ["S-7", "D-7", "S-3", "H-3", "C-7"]]),  # 7's full of 3's
        ("Full House", [get_card(card) for card in ["C-2", "S-2", "D-9", "H-9", "C-9"]]),  # 9's full of 2's
        ("Full House", [get_card(card) for card in ["S-3", "C-3", "H-3", "D-5", "C-5"]]),  # 3's full of 5's
        ("Full House", [get_card(card) for card in ["S-7", "C-7", "H-Q", "S-Q", "D-7"]]),  # 7's full of Q's
        ("Full House", [get_card(card) for card in ["S-8", "S-9", "C-9", "H-8", "D-9"]]),  # 9's full of 8's
        ("Full House", [get_card(card) for card in ["S-9", "C-K", "S-K", "H-9", "D-9"]]),  # 9's full of K's
        ("Full House", [get_card(card) for card in ["D-Q", "S-Q", "C-7", "H-7", "D-7"]]),  # 7's full of Q's
    ]

    players = [  # player_cards irrelevant due to side effect usage
        {"name": "SEVENS_THREES", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "NINES_TWOS", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "THREES_FIVES", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "SEVENS_QUEENS_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "NINES_EIGHTS", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "NINES_KINGS", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "SEVENS_QUEENS_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]  # board cards irrelevant due to side effect usage

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "NINES_KINGS", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 7, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "NINES_EIGHTS", "hand_rank": 2, "hand_rank_tie": False,
                                                              "hand_strength": 7, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "NINES_TWOS", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 7, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "SEVENS_QUEENS_TIE_A", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 7, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "SEVENS_QUEENS_TIE_B", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 7, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "SEVENS_THREES", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 7, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "THREES_FIVES", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 7, "tiebreaker_rank": 6}.items())


def test_when_rank_players_hands_and_flushes_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Flush", [get_card(card) for card in ["S-2", "S-7", "S-8", "S-Q", "S-10"]]),  # Queen/Ten High Flush
        ("Flush", [get_card(card) for card in ["S-9", "S-2", "S-10", "S-6", "S-5"]]),  # 10/9 high flush
        ("Flush", [get_card(card) for card in ["S-J", "S-4", "S-Q", "S-8", "S-6"]]),  # Queen/Jack High Flush Tie
        ("Flush", [get_card(card) for card in ["S-6", "S-8", "S-4", "S-7", "S-J"]]),  # Jack/8 high flush
        ("Flush", [get_card(card) for card in ["S-Q", "S-9", "S-5", "S-K", "S-10"]]),  # King/Queen High Flush
        ("Flush", [get_card(card) for card in ["S-7", "S-9", "S-J", "S-4", "S-10"]]),  # Jack/10 High Flush
        ("Flush", [get_card(card) for card in ["S-J", "S-4", "S-Q", "S-8", "S-6"]])  # Queen/Jack High Flush Tie
    ]

    players = [
        {"name": "QUEEN_TEN", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "TEN_NINE", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "QUEEN_JACK_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "JACK_EIGHT", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "KING_QUEEN", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "JACK_TEN", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "QUEEN_JACK_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "KING_QUEEN", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 6, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "QUEEN_JACK_TIE_A", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 6, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "QUEEN_JACK_TIE_B", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 6, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "QUEEN_TEN", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 6, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "JACK_TEN", "hand_rank": 4, "hand_rank_tie": False,
                                                              "hand_strength": 6, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "JACK_EIGHT", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 6, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "TEN_NINE", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 6, "tiebreaker_rank": 6}.items())


def test_when_rank_players_hands_and_straight_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Straight", [get_card(card) for card in ["D-9", "C-J", "S-8", "H-Q", "S-10"]]),  # Queen High Straight
        ("Straight", [get_card(card) for card in ["S-9", "D-8", "H-10", "S-6", "C-7"]]),  # 10 high Straight
        ("Straight", [get_card(card) for card in ["C-J", "D-9", "S-Q", "S-8", "S-10"]]),  # Queen High Straight
        ("Straight", [get_card(card) for card in ["S-9", "D-8", "S-10", "S-7", "C-J"]]),  # Jack high Straight
        ("Straight", [get_card(card) for card in ["S-Q", "C-9", "S-J", "S-K", "S-10"]]),  # King High Straight
        ("Straight", [get_card(card) for card in ["S-7", "C-9", "S-J", "D-8", "S-10"]]),  # Jack High Straight
        ("Straight", [get_card(card) for card in ["S-10", "C-Q", "S-9", "S-J", "D-8"]])  # Queen High Straight
    ]

    players = [
        {"name": "QUEEN_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "TEN", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "QUEEN_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "JACK_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "KING", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "JACK_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "QUEEN_TIE_C", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "KING", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 5, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "QUEEN_TIE_A", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 5, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "QUEEN_TIE_B", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 5, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "QUEEN_TIE_C", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 5, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "JACK_TIE_A", "hand_rank": 3, "hand_rank_tie": True,
                                                              "hand_strength": 5, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "JACK_TIE_B", "hand_rank": 3, "hand_rank_tie": True,
                                                              "hand_strength": 5, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "TEN", "hand_rank": 4, "hand_rank_tie": False,
                                                              "hand_strength": 5, "tiebreaker_rank": 4}.items())


def test_when_rank_players_hands_and_trips_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Trips", [get_card(card) for card in ["S-7", "D-7", "S-3", "H-2", "C-7"]]),  # Trips 7's 3 kick
        ("Trips", [get_card(card) for card in ["S-2", "S-6", "D-9", "H-9", "C-9"]]),  # Trips 9's 6 kick
        ("Trips", [get_card(card) for card in ["S-3", "C-3", "H-3", "D-4", "C-5"]]),  # Trips 3's 5 kick
        ("Trips", [get_card(card) for card in ["S-7", "C-7", "H-7", "S-Q", "D-9"]]),  # Trips 7's Q kick TIE
        ("Trips", [get_card(card) for card in ["S-8", "S-9", "C-9", "H-4", "D-9"]]),  # Trips 9's 8 kick
        ("Trips", [get_card(card) for card in ["S-9", "C-9", "S-K", "H-8", "D-9"]]),  # Trips 9's K kicks
        ("Trips", [get_card(card) for card in ["S-7", "S-Q", "C-7", "H-7", "D-9"]]),  # Trips 7's Q kicks TIE
    ]

    players = [  # player_cards irrelevant due to side effect usage
        {"name": "SEVENS_THREE", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "NINES_SIX", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "THREES_FIVE", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "SEVENS_QUEEN_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "NINES_EIGHT", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "NINES_KING", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "SEVENS_QUEEN_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]  # board cards irrelevant due to side effect usage

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "NINES_KING", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 4, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "NINES_EIGHT", "hand_rank": 2, "hand_rank_tie": False,
                                                              "hand_strength": 4, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "NINES_SIX", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 4, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "SEVENS_QUEEN_TIE_A", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 4, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "SEVENS_QUEEN_TIE_B", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 4, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "SEVENS_THREE", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 4, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "THREES_FIVE", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 4, "tiebreaker_rank": 6}.items())


def test_when_rank_players_hands_and_two_pair_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Two Pair", [get_card(card) for card in ["S-7", "D-7", "S-3", "H-3", "C-8"]]),  # 7,3 pairs 8
        ("Two Pair", [get_card(card) for card in ["C-8", "S-8", "D-A", "H-9", "C-9"]]),  # 9,8 pairs A
        ("Two Pair", [get_card(card) for card in ["S-3", "C-9", "H-3", "D-5", "C-5"]]),  # 5,3 pairs 9
        ("Two Pair", [get_card(card) for card in ["S-3", "C-7", "H-Q", "S-Q", "D-7"]]),  # Q,7 pairs 3 - TIE
        ("Two Pair", [get_card(card) for card in ["S-8", "S-9", "C-9", "H-8", "D-5"]]),  # 9,8 pairs 5
        ("Two Pair", [get_card(card) for card in ["S-9", "C-K", "S-K", "H-10", "D-9"]]),  # K,9 pairs 10
        ("Two Pair", [get_card(card) for card in ["S-Q", "C-7", "H-Q", "S-3", "D-7"]]),  # Q,7 pairs 3 - TIE
    ]

    players = [  # player_cards irrelevant due to side effect usage
        {"name": "SEVENS_THREES", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "NINES_EIGHTS_ACE", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "FIVES_THREES", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "QUEENS_SEVENS_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "NINES_EIGHTS_FIVE", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "KINGS_NINES", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "QUEENS_SEVENS_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]  # board cards irrelevant due to side effect usage

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "KINGS_NINES", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 3, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "QUEENS_SEVENS_TIE_A", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 3, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "QUEENS_SEVENS_TIE_B", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 3, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "NINES_EIGHTS_ACE", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 3, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "NINES_EIGHTS_FIVE", "hand_rank": 4, "hand_rank_tie": False,
                                                              "hand_strength": 3, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "SEVENS_THREES", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 3, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "FIVES_THREES", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 3, "tiebreaker_rank": 6}.items())


def test_when_rank_players_hands_and_pair_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("Pair", [get_card(card) for card in ["S-7", "D-8", "S-3", "H-2", "C-7"]]),  # Pair 7's 8 kick
        ("Pair", [get_card(card) for card in ["S-2", "S-6", "D-9", "H-9", "C-3"]]),  # Pair 9's 6 kick
        ("Pair", [get_card(card) for card in ["S-3", "C-3", "H-2", "D-4", "C-5"]]),  # Pair 3's 5 kick
        ("Pair", [get_card(card) for card in ["S-7", "C-7", "H-3", "S-Q", "D-2"]]),  # Pair 7's Q kick TIE
        ("Pair", [get_card(card) for card in ["S-8", "S-9", "C-9", "H-4", "D-3"]]),  # Pair 9's 8 kick
        ("Pair", [get_card(card) for card in ["S-9", "C-9", "S-K", "H-8", "D-2"]]),  # Pair 9's K kicks
        ("Pair", [get_card(card) for card in ["S-7", "S-Q", "C-7", "H-2", "D-3"]]),  # Pair 7's Q kicks TIE
    ]

    players = [  # player_cards irrelevant due to side effect usage
        {"name": "SEVENS_EIGHT", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "NINES_SIX", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "THREES_FIVE", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "SEVENS_QUEEN_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "NINES_EIGHT", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "NINES_KING", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "SEVENS_QUEEN_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]  # board cards irrelevant due to side effect usage

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "NINES_KING", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 2, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "NINES_EIGHT", "hand_rank": 2, "hand_rank_tie": False,
                                                              "hand_strength": 2, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "NINES_SIX", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 2, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "SEVENS_QUEEN_TIE_A", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 2, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "SEVENS_QUEEN_TIE_B", "hand_rank": 4, "hand_rank_tie": True,
                                                              "hand_strength": 2, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "SEVENS_EIGHT", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 2, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "THREES_FIVE", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 2, "tiebreaker_rank": 6}.items())


def test_when_rank_players_hands_and_high_card_then_rank_correct(hand_solver):
    player_best_hand_side_effects = [
        ("High Card", [get_card(card) for card in ["S-7", "D-8", "S-3", "H-2", "C-7"]]),  # 8 high
        ("High Card", [get_card(card) for card in ["S-2", "S-6", "D-9", "H-8", "C-3"]]),  # 9 high, 8,6
        ("High Card", [get_card(card) for card in ["S-7", "C-3", "H-2", "D-4", "C-5"]]),  # 7 high
        ("High Card", [get_card(card) for card in ["S-7", "C-9", "H-3", "S-Q", "D-2"]]),  # Q high - TIE
        ("High Card", [get_card(card) for card in ["S-8", "S-7", "C-9", "H-4", "D-3"]]),  # 9 high, 8,7
        ("High Card", [get_card(card) for card in ["S-4", "C-9", "S-K", "H-8", "D-2"]]),  # K High
        ("High Card", [get_card(card) for card in ["S-7", "C-9", "H-3", "S-Q", "D-2"]]),  # Q high - TIE
    ]

    players = [  # player_cards irrelevant due to side effect usage
        {"name": "EIGHT", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "NINE_EIGHT_SIX", "player_cards": [get_card(card) for card in ["H-4", "D-7"]]},
        {"name": "SEVEN", "player_cards": [get_card(card) for card in ["S-J", "S-Q"]]},
        {"name": "QUEEN_TIE_A", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
        {"name": "NINE_EIGHT_SEVEN", "player_cards": [get_card(card) for card in ["S-K", "S-Q"]]},
        {"name": "KING", "player_cards": [get_card(card) for card in ["S-J", "H-10"]]},
        {"name": "QUEEN_TIE_B", "player_cards": [get_card(card) for card in ["S-J", "D-J"]]},
    ]
    board_cards = [get_card(card) for card in ["S-9", "S-7", "S-8", "S-6", "S-10"]]  # board cards irrelevant due to side effect usage

    with patch.object(hand_solver, "find_player_best_hand", side_effect=player_best_hand_side_effects):
        players_ranked = hand_solver.rank_player_hands(players, board_cards)

    assert len(players_ranked) == 7

    assert all(item in players_ranked[0].items() for item in {"name": "KING", "hand_rank": 1, "hand_rank_tie": False,
                                                              "hand_strength": 1, "tiebreaker_rank": 1}.items())
    assert all(item in players_ranked[1].items() for item in {"name": "QUEEN_TIE_A", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 1, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[2].items() for item in {"name": "QUEEN_TIE_B", "hand_rank": 2, "hand_rank_tie": True,
                                                              "hand_strength": 1, "tiebreaker_rank": 2}.items())
    assert all(item in players_ranked[3].items() for item in {"name": "NINE_EIGHT_SEVEN", "hand_rank": 3, "hand_rank_tie": False,
                                                              "hand_strength": 1, "tiebreaker_rank": 3}.items())
    assert all(item in players_ranked[4].items() for item in {"name": "NINE_EIGHT_SIX", "hand_rank": 4, "hand_rank_tie": False,
                                                              "hand_strength": 1, "tiebreaker_rank": 4}.items())
    assert all(item in players_ranked[5].items() for item in {"name": "EIGHT", "hand_rank": 5, "hand_rank_tie": False,
                                                              "hand_strength": 1, "tiebreaker_rank": 5}.items())
    assert all(item in players_ranked[6].items() for item in {"name": "SEVEN", "hand_rank": 6, "hand_rank_tie": False,
                                                              "hand_strength": 1, "tiebreaker_rank": 6}.items())