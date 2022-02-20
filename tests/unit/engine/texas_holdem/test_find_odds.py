from decimal import Decimal

from pytest import mark

import pypoker.engine.texas_holdem.find_odds as odds
from pypoker.player.human import HumanPlayer


# find_player_odds_enumerate tests
# --------------------------------
@mark.parametrize("a_cards,b_cards,board_cards,a_odds,b_odds,tie_odds", [
    ("S6|S7", "DA|C9", "S8|S9|HA|H3", Decimal("31.82"), Decimal("68.18"), Decimal("0")),  # Open-ended straight flush draw vs Over Pair
    ("HA|CQ", "D7|C7", "S2|S9|S4|SK", Decimal("9.09"), Decimal("70.45"), Decimal("20.45")),  # Two over cards vs lower pair, chance of board flushing for tie
    ("HA|C7", "DA|C9", "S2|S8|D4|C2", Decimal("6.82"), Decimal("79.55"), Decimal("13.64")),  # Dominated Ace
    ("H9|C7", "D6|C6", "S9|SK|D2|H4", Decimal("95.45"), Decimal("4.55"), Decimal("0")),  # pair vs pair
    ("H9|C7", "D6|CA", "S6|ST|D2|H5", Decimal("22.73"), Decimal("77.27"), Decimal("0")),  # inside straight draw vs pair
    ("H9|C9", "DJ|D8", "D9|SJ|D2|C4", Decimal("81.82"), Decimal("18.18"), Decimal("0")),  # trips vs possible trips and flush draws
    ("HA|CA", "DJ|S8", "DA|SJ|CJ|H5", Decimal("97.73"), Decimal("2.27"), Decimal("0")),  # full house vs quads draw
    ("HA|CK", "DK|S2", "CQ|SJ|HT|C9", Decimal("93.18"), Decimal("0"), Decimal("6.82")),  # straight over straight
])
def test_when_find_player_odds_enumerate_and_two_player_and_one_draw_then_correct_values_returned(
        th_engine, get_test_cards, get_deck_minus_set,
        a_cards, b_cards, board_cards, a_odds, b_odds, tie_odds
):
    players = [
        HumanPlayer(name="player_a", hole_cards=get_test_cards(a_cards)),
        HumanPlayer(name="player_b", hole_cards=get_test_cards(b_cards))
    ]
    board = get_test_cards(board_cards)
    drawable_cards = get_deck_minus_set(players[0].hole_cards + players[1].hole_cards + board)

    result = odds.find_player_odds_enumerate(th_engine, players, board, drawable_cards)

    assert result["player_a"] == a_odds
    assert result["player_b"] == b_odds
    if tie_odds:
        assert result["TIE(player_a,player_b)"] == tie_odds
    else:
        assert "TIE(player_a,player_b)" not in result.keys()


@mark.parametrize("a_cards,b_cards,board_cards,a_odds,b_odds,tie_odds", [
    ("S6|S7", "DA|C9", "S8|S9|HA", Decimal("48.79"), Decimal("51.21"), 0),  # Open-ended straight flush draw vs Over Pair
    ("HA|CQ", "D7|C7", "S2|S9|S4", Decimal("23.94"), Decimal("71.52"), Decimal("4.55")),  # Two over cards vs lower pair, chance of board flushing for tie
    ("HA|C7", "DA|C9", "S2|S8|D4", Decimal("13.74"), Decimal("81.92"), Decimal("4.34")),  # Dominated Ace
    ("H9|C7", "D6|C6", "S9|SK|D2", Decimal("91.21"), Decimal("8.79"), Decimal("0")),  # pair vs pair
    ("H9|C7", "D6|CA", "S6|ST|D2", Decimal("36.87"), Decimal("63.13"), Decimal("0")),  # inside straight draw vs pair
    ("H9|C9", "DJ|D8", "D9|SJ|D2", Decimal("68.69"), Decimal("31.31"), Decimal("0")),  # trips vs possible trips and flush draws
    ("HA|CA", "DJ|S8", "DA|SJ|CJ", Decimal("95.66"), Decimal("4.34"), Decimal("0")),  # full house vs quads draw
    ("HA|CK", "DK|S2", "CQ|SJ|HT", Decimal("86.97"), Decimal("0"), Decimal("13.03")),  # straight over straight
    ("HA|CA", "DA|SA", "CQ|SJ|HT", Decimal("0"), Decimal("0"), Decimal("100")),  # same pair, guaranteed chop
    ("HA|CA", "DA|SA", "HQ|HJ|S6", Decimal("4.55"), Decimal("0"), Decimal("95.45")),  # same pair, possible flush out
])
def test_when_find_player_odds_enumerate_and_two_player_and_two_draws_then_correct_values_returned(
        th_engine, get_test_cards, get_deck_minus_set,
        a_cards, b_cards, board_cards, a_odds, b_odds, tie_odds
):
    players = [
        HumanPlayer(name="player_a", hole_cards=get_test_cards(a_cards)),
        HumanPlayer(name="player_b", hole_cards=get_test_cards(b_cards))
    ]
    board = get_test_cards(board_cards)
    drawable_cards = get_deck_minus_set(players[0].hole_cards + players[1].hole_cards + board)

    result = odds.find_player_odds_enumerate(th_engine, players, board, drawable_cards)

    assert result["player_a"] == a_odds
    assert result["player_b"] == b_odds
    if tie_odds:
        assert result["TIE(player_a,player_b)"] == tie_odds
    else:
        assert "TIE(player_a,player_b)" not in result.keys()


@mark.parametrize("a_cards,b_cards,a_odds,b_odds,tie_odds", [
    ("S6|D6", "DA|HJ", Decimal("53.99"), Decimal("45.62"), Decimal("0.39")),  # pair vs two over cards
])
def test_when_find_player_odds_simulate_and_two_players_and_five_draws_and_10000_sample_then_correct_values_returned(
        th_engine, get_test_cards, get_deck_minus_set,
        a_cards, b_cards, a_odds, b_odds, tie_odds
):
    players = [
        HumanPlayer(name="player_a", hole_cards=get_test_cards(a_cards)),
        HumanPlayer(name="player_b", hole_cards=get_test_cards(b_cards))
    ]
    board = []
    drawable_cards = get_deck_minus_set(players[0].hole_cards + players[1].hole_cards)

    results = {
        "player_a": [],
        "player_b": [],
        "TIE(player_a,player_b)": [],
    }
    for val in range(1, 2):
        result = odds.find_player_odds_simulate(th_engine, players, board, drawable_cards, 10000)
        results["player_a"].append(result["player_a"])
        results["player_b"].append(result["player_b"])
        results["TIE(player_a,player_b)"].append(result["TIE(player_a,player_b)"])

    print(f"PLAYER_A: \texpected: {Decimal('53.99')} \t actual_avg: {sum(results['player_a']) / 100} \t min: {min(results['player_a'])} \t max: {max(results['player_a'])}")
    print(
        f"PLAYER_B: \texpected: {Decimal('45.62')} \t actual_avg: {sum(results['player_b']) / 100} \t min: {min(results['player_b'])} \t max: {max(results['player_b'])}")
    print(
        f"TIE: \texpected: {Decimal('0.39')} \t actual_avg: {sum(results['TIE(player_a,player_b)']) / 100} \t min: {min(results['TIE(player_a,player_b)'])} \t max: {max(results['TIE(player_a,player_b)'])}")




