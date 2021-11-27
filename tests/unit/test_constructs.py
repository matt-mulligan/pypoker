from unittest.mock import patch, call

from pytest import mark, raises, fixture

from pypoker.constants import GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, TH_HAND_STRAIGHT_FLUSH, TH_HAND_QUADS, \
    TH_HAND_FULL_HOUSE, TH_HAND_FLUSH, TH_HAND_STRAIGHT, TH_HAND_TRIPS, TH_HAND_TWO_PAIR, TH_HAND_PAIR
from pypoker.constructs import Card, Deck, Hand
from pypoker.exceptions import InvalidGameError, InvalidHandError, InvalidHandTypeError, GameMismatchError

"""
Test Fixtures
"""
@fixture
def deck_card_names():
    return [
        "Two of Clubs",
        "Three of Clubs",
        "Four of Clubs",
        "Five of Clubs",
        "Six of Clubs",
        "Seven of Clubs",
        "Eight of Clubs",
        "Nine of Clubs",
        "Ten of Clubs",
        "Jack of Clubs",
        "Queen of Clubs",
        "King of Clubs",
        "Ace of Clubs",
        "Two of Spades",
        "Three of Spades",
        "Four of Spades",
        "Five of Spades",
        "Six of Spades",
        "Seven of Spades",
        "Eight of Spades",
        "Nine of Spades",
        "Ten of Spades",
        "Jack of Spades",
        "Queen of Spades",
        "King of Spades",
        "Ace of Spades",
        "Two of Diamonds",
        "Three of Diamonds",
        "Four of Diamonds",
        "Five of Diamonds",
        "Six of Diamonds",
        "Seven of Diamonds",
        "Eight of Diamonds",
        "Nine of Diamonds",
        "Ten of Diamonds",
        "Jack of Diamonds",
        "Queen of Diamonds",
        "King of Diamonds",
        "Ace of Diamonds",
        "Two of Hearts",
        "Three of Hearts",
        "Four of Hearts",
        "Five of Hearts",
        "Six of Hearts",
        "Seven of Hearts",
        "Eight of Hearts",
        "Nine of Hearts",
        "Ten of Hearts",
        "Jack of Hearts",
        "Queen of Hearts",
        "King of Hearts",
        "Ace of Hearts",
    ]


@fixture
def cards_five():
    return [Card("D3"), Card("DA"), Card("CQ"), Card("H7"), Card("S9")]


"""
Card Construct Tests
"""
@mark.parametrize(
    "card_val, card_rank, card_suit, card_name, card_id",
    [
        (2, "Two", "Clubs", "Two of Clubs", "C2"),
        (3, "Three", "Clubs", "Three of Clubs", "C3"),
        (4, "Four", "Clubs", "Four of Clubs", "C4"),
        (5, "Five", "Clubs", "Five of Clubs", "C5"),
        (6, "Six", "Clubs", "Six of Clubs", "C6"),
        (7, "Seven", "Clubs", "Seven of Clubs", "C7"),
        (8, "Eight", "Clubs", "Eight of Clubs", "C8"),
        (9, "Nine", "Clubs", "Nine of Clubs", "C9"),
        (10, "Ten", "Clubs", "Ten of Clubs", "CT"),
        (11, "Jack", "Clubs", "Jack of Clubs", "CJ"),
        (12, "Queen", "Clubs", "Queen of Clubs", "CQ"),
        (13, "King", "Clubs", "King of Clubs", "CK"),
        (14, "Ace", "Clubs", "Ace of Clubs", "CA"),
        (2, "Two", "Diamonds", "Two of Diamonds", "D2"),
        (3, "Three", "Diamonds", "Three of Diamonds", "D3"),
        (4, "Four", "Diamonds", "Four of Diamonds", "D4"),
        (5, "Five", "Diamonds", "Five of Diamonds", "D5"),
        (6, "Six", "Diamonds", "Six of Diamonds", "D6"),
        (7, "Seven", "Diamonds", "Seven of Diamonds", "D7"),
        (8, "Eight", "Diamonds", "Eight of Diamonds", "D8"),
        (9, "Nine", "Diamonds", "Nine of Diamonds", "D9"),
        (10, "Ten", "Diamonds", "Ten of Diamonds", "DT"),
        (11, "Jack", "Diamonds", "Jack of Diamonds", "DJ"),
        (12, "Queen", "Diamonds", "Queen of Diamonds", "DQ"),
        (13, "King", "Diamonds", "King of Diamonds", "DK"),
        (14, "Ace", "Diamonds", "Ace of Diamonds", "DA"),
        (2, "Two", "Hearts", "Two of Hearts", "H2"),
        (3, "Three", "Hearts", "Three of Hearts", "H3"),
        (4, "Four", "Hearts", "Four of Hearts", "H4"),
        (5, "Five", "Hearts", "Five of Hearts", "H5"),
        (6, "Six", "Hearts", "Six of Hearts", "H6"),
        (7, "Seven", "Hearts", "Seven of Hearts", "H7"),
        (8, "Eight", "Hearts", "Eight of Hearts", "H8"),
        (9, "Nine", "Hearts", "Nine of Hearts", "H9"),
        (10, "Ten", "Hearts", "Ten of Hearts", "HT"),
        (11, "Jack", "Hearts", "Jack of Hearts", "HJ"),
        (12, "Queen", "Hearts", "Queen of Hearts", "HQ"),
        (13, "King", "Hearts", "King of Hearts", "HK"),
        (14, "Ace", "Hearts", "Ace of Hearts", "HA"),
        (2, "Two", "Spades", "Two of Spades", "S2"),
        (3, "Three", "Spades", "Three of Spades", "S3"),
        (4, "Four", "Spades", "Four of Spades", "S4"),
        (5, "Five", "Spades", "Five of Spades", "S5"),
        (6, "Six", "Spades", "Six of Spades", "S6"),
        (7, "Seven", "Spades", "Seven of Spades", "S7"),
        (8, "Eight", "Spades", "Eight of Spades", "S8"),
        (9, "Nine", "Spades", "Nine of Spades", "S9"),
        (10, "Ten", "Spades", "Ten of Spades", "ST"),
        (11, "Jack", "Spades", "Jack of Spades", "SJ"),
        (12, "Queen", "Spades", "Queen of Spades", "SQ"),
        (13, "King", "Spades", "King of Spades", "SK"),
        (14, "Ace", "Spades", "Ace of Spades", "SA"),
    ],
)
def test_when_card_init_then_correct_values_set(
    card_val, card_rank, card_suit, card_name, card_id
):
    card = Card(card_id)
    assert card.name == card_name
    assert card.identity == card_id
    assert card.suit == card_suit
    assert card.rank == card_rank
    assert card.value == card_val


@mark.parametrize("card_id", ["C", "D12"])
def test_when_card_init_and_card_id_not_2_chars_then_raise_error(card_id):
    with raises(ValueError, match="Card ID provided must be exactly 2 characters long"):
        Card(card_id)


@mark.parametrize(
    "card_val",
    [
        1,
        "N",
    ],
)
def test_when_card_init_and_card_rank_bad_then_raise_error(card_val):
    with raises(
        ValueError,
        match=f"Card ID second character '{card_val}' "
        f"is not within valid list of rank identifiers",
    ):
        Card(f"H{card_val}")


@mark.parametrize("suit_val", [3, "s", "c", "h", "d"])
def test_when_card_init_and_suit_value_bad_then_raise_error(suit_val):
    with raises(
        ValueError,
        match=f"Card ID first character '{suit_val}' is not within valid list of suit identifiers",
    ):
        Card(f"{suit_val}6")


@mark.parametrize(
    "card_a, card_b, expected",
    [
        (Card("D7"), Card("DT"), False),
        (Card("HQ"), Card("H3"), True),
        (Card("S3"), Card("CK"), False),
        (Card("CT"), Card("H4"), True),
        (Card("H7"), Card("S7"), False),
    ],
)
def test_when_card_greater_than_then_correct_result_returned(card_a, card_b, expected):
    actual = card_a > card_b
    assert actual == expected


@mark.parametrize(
    "card_a, card_b, expected",
    [
        (Card("D7"), Card("DT"), True),
        (Card("HQ"), Card("H3"), False),
        (Card("S3"), Card("CK"), True),
        (Card("CT"), Card("H4"), False),
        (Card("H7"), Card("S7"), False),
    ],
)
def test_when_card_less_than_then_correct_result_returned(card_a, card_b, expected):
    actual = card_a < card_b
    assert actual == expected


"""
Deck Construct Tests
"""
def test_when_deck_init_then_cards_all_correct(deck_card_names):
    deck = Deck()
    card_names = []
    for card in deck.cards_all:
        card_names.append(card.name)

    assert len(deck.cards_all) == 52
    assert card_names.sort() == deck_card_names.sort()


def test_when_deck_init_then_cards_available_correct(deck_card_names):
    deck = Deck()
    card_names = []
    for card in deck.cards_available:
        card_names.append(card.name)

    assert len(deck.cards_available) == 52
    assert card_names.sort() == deck_card_names.sort()


def test_when_deck_init_then_cards_used_correct():
    deck = Deck()
    assert len(deck.cards_used) == 0


def test_when_deck_shuffle_then_shuffle_command_used():
    deck = Deck()

    with patch("pypoker.constructs.random") as random_mock:
        deck.shuffle()

    random_mock.assert_has_calls([call.shuffle(deck.cards_available)])


def test_when_deck_draw_single_card_then_correct_card_returned(cards_five):
    deck = Deck()
    deck.cards_available = cards_five.copy()
    drawn_cards = deck.draw()

    assert len(drawn_cards) == 1
    assert drawn_cards[0] == cards_five[0]


def test_when_deck_draw_single_card_and_not_enough_cards_available_then_raise_error():
    deck = Deck()
    deck.cards_available = []

    with raises(ValueError, match="Not enough cards left in the deck!"):
        deck.draw()


def test_when_deck_draw_single_card_then_card_in_cards_used(cards_five):
    deck = Deck()
    deck.cards_available = cards_five.copy()
    drawn_cards = deck.draw()

    assert len(deck.cards_used) == 1
    assert deck.cards_used[0] == drawn_cards[0]


def test_when_deck_draw_single_card_then_card_not_in_cards_available(cards_five):
    deck = Deck()
    deck.cards_available = cards_five.copy()
    drawn_cards = deck.draw()

    assert len(deck.cards_available) == 4
    assert drawn_cards[0] not in deck.cards_available


def test_when_deck_draw_multiple_card_then_correct_card_returned(cards_five):
    deck = Deck()
    deck.cards_available = cards_five.copy()
    drawn_cards = deck.draw(num=3)

    assert len(drawn_cards) == 3
    assert drawn_cards == cards_five[:3]


def test_when_deck_draw_nultiple_card_and_not_enough_cards_available_then_raise_error():
    deck = Deck()
    deck.cards_available = []

    with raises(ValueError, match="Not enough cards left in the deck!"):
        deck.draw(num=3)


def test_when_deck_draw_multiple_card_then_card_in_cards_used(cards_five):
    deck = Deck()
    deck.cards_available = cards_five.copy()
    drawn_cards = deck.draw(num=3)

    assert len(deck.cards_used) == 3
    assert deck.cards_used == drawn_cards[:3]


def test_when_deck_draw_multiple_card_then_card_not_in_cards_available(cards_five):
    deck = Deck()
    deck.cards_available = cards_five.copy()
    drawn_cards = deck.draw(num=3)

    assert len(deck.cards_available) == 2
    for card in drawn_cards:
        assert card not in deck.cards_available


def test_when_deck_reset_then_cards_used_reset(cards_five):
    deck = Deck()
    deck.cards_used = cards_five.copy()

    deck.reset()

    assert deck.cards_used == []


def test_when_deck_reset_then_cards_available_reset(cards_five, deck_card_names):
    deck = Deck()
    deck.cards_available = cards_five.copy()

    deck.reset()

    card_names = []
    for card in deck.cards_available:
        card_names.append(card.name)

    assert len(deck.cards_available) == 52
    assert card_names.sort() == deck_card_names.sort()


@mark.parametrize(
    "cards, expected_card_names, descending",
    [
        (
            [Card("D7"), Card("D4"), Card("DA"), Card("DQ")],
            [
                "Four of Diamonds",
                "Seven of Diamonds",
                "Queen of Diamonds",
                "Ace of Diamonds",
            ],
            False,
        ),
        (
            [Card("D7"), Card("D4"), Card("CA"), Card("CQ")],
            ["Queen of Clubs", "Ace of Clubs", "Four of Diamonds", "Seven of Diamonds"],
            False,
        ),
        (
            [Card("D7"), Card("D4"), Card("DA"), Card("DQ")],
            [
                "Ace of Diamonds",
                "Queen of Diamonds",
                "Seven of Diamonds",
                "Four of Diamonds",
            ],
            True,
        ),
        (
            [Card("D7"), Card("D4"), Card("CA"), Card("CQ")],
            ["Ace of Clubs", "Queen of Clubs", "Seven of Diamonds", "Four of Diamonds"],
            True,
        ),
    ],
)
def test_when_deck_order_cards_then_correct_reordering_occurs(
    cards, expected_card_names, descending
):
    deck = Deck()
    reordered_cards = deck.order_cards(cards, descending=descending)

    reordered_card_names = [card.name for card in reordered_cards]
    assert reordered_card_names == expected_card_names


def test_when_deck_order_cards_and_non_card_passed_then_raise_error():
    deck = Deck()
    cards = [Card("C5"), "Six of Spades", Card("S9")]
    with raises(
        ValueError,
        match="All objects within cards value must be an instance of the Cards Class",
    ):
        deck.order_cards(cards)


"""
Hand Construct Tests
"""


def test_when_hand_and_bad_game_type_then_raise_error(get_test_cards):
    cards = get_test_cards("C9")

    with raises(InvalidGameError, match="Game type 'DERP' is invalid"):
        Hand("DERP", TH_HAND_HIGH_CARD, cards, [1])


def test_when_hand_and_bad_hand_type_then_raise_error(get_test_cards):
    cards = get_test_cards("C9")

    with raises(InvalidHandTypeError, match="Hand type 'DERP' is invalid"):
        Hand(GAME_TEXAS_HOLDEM, "DERP", cards, [1])


def test_when_hand_and_cards_are_not_all_cards_then_raise_error(get_test_cards):
    cards = get_test_cards("C9")
    cards.append("D9")

    with raises(ValueError, match="Cards object passed to hand must be a list of Card objects"):
        Hand(GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, cards, [1])


@mark.parametrize("game, hand_type, cards, min_cards, max_cards", [
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, "C4|C5|C6|C7", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, "C4|C5|C6|C7|C8|C9", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_QUADS, "C4|S4|H4", 4, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_QUADS, "C4|S4|H4|D4|HA|SQ", 4, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, "C4|S4|H4|DA", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, "C4|S4|H4|DA|SA|CA", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, "C4|CA|C8|C2", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, "C4|CA|C8|C2|CJ|CT", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, "C4|S5|H6|D7", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, "C4|S5|H6|D7|C8|C9", 5, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, "C4|S4", 3, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, "C4|S4|D4|D8|DJ|DA", 3, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, "C4|S4|HA", 4, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, "C4|S4|HA|DA|D6|ST", 4, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_PAIR, "C4", 2, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_PAIR, "C4|D4|ST|HA|C9|H7", 2, 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, "C4|D4|ST|HA|C9|H7", 1, 5),
])
def test_when_hand_and_incorrect_num_cards_then_raise_error(get_test_cards, game, hand_type, cards, min_cards, max_cards):
    cards = get_test_cards(cards)

    with raises(ValueError, match=f"{game} {hand_type} hand required between {min_cards} and {max_cards} cards"):
        Hand(game, hand_type, cards, [1])


def test_when_hand_and_tiebreakers_not_int_or_none_then_raise_error(get_test_cards):
    cards = get_test_cards("C4|C5|C6|C7|C8")

    with raises(ValueError, match="all arguments in tiebreakers must be integers or Nonetype"):
        Hand(GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, cards, ["DERP"])


@mark.parametrize("game, hand_type, cards, tiebreakers, tb", [
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, "C4|C5|C6|C7|C8", [8, 7], 1),
    (GAME_TEXAS_HOLDEM, TH_HAND_QUADS, "C4|S4|H4|D4|HA", [4], 2),
    (GAME_TEXAS_HOLDEM, TH_HAND_QUADS, "C4|S4|H4|D4|HA", [4, 14, 12], 2),
    (GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, "C4|S4|H4|DA|SA", [14], 2),
    (GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, "C4|S4|H4|DA|SA", [14, 4, 2], 2),
    (GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, "C4|CA|C8|C2|CJ", [3, 4, 5, 6], 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, "C4|CA|C8|C2|CJ", [3, 4, 5, 6, 8, 12], 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, "C4|S5|H6|D7|C8", [3, 5], 1),
    (GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, "C4|S4|D4|D8|DJ", [4, 7], 3),
    (GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, "C4|S4|D4|D8|DJ", [4, 7, 5, 3], 3),
    (GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, "C4|S4|HA|DA|D6", [5], 3),
    (GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, "C4|S4|HA|DA|D6", [5, 6, 9, 13], 3),
    (GAME_TEXAS_HOLDEM, TH_HAND_PAIR, "C4|D4|ST|HA|C9", [5, 7, 8], 4),
    (GAME_TEXAS_HOLDEM, TH_HAND_PAIR, "C4|D4|ST|HA|C9", [5, 7, 8, 3, 12], 4),
    (GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, "C4|D4|ST|HA|C9", [3, 7, 2, 5], 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, "C4|D4|ST|HA|C9", [3, 7, 2, 5, 12, 14], 5),
])
def test_when_hand_and_incorrect_num_tiebreakers_then_raise_error(get_test_cards, game, hand_type, cards, tiebreakers, tb):
    cards = get_test_cards(cards)

    with raises(ValueError, match=f"{game} {hand_type} hand requires {tb} tiebreakers"):
        Hand(game, hand_type, cards, tiebreakers)


@mark.parametrize("game, hand_type, cards, tiebreakers, strength", [
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT_FLUSH, "C4|C5|C6|C7|C8", [8], 9),
    (GAME_TEXAS_HOLDEM, TH_HAND_QUADS, "C4|S4|H4|D4|HA", [4, 14], 8),
    (GAME_TEXAS_HOLDEM, TH_HAND_QUADS, "C4|S4|H4|D4", [4, None], 8),
    (GAME_TEXAS_HOLDEM, TH_HAND_FULL_HOUSE, "C4|S4|H4|DA|SA", [4, 14], 7),
    (GAME_TEXAS_HOLDEM, TH_HAND_FLUSH, "C4|CA|C8|C2|CJ", [14, 11, 8, 4, 2], 6),
    (GAME_TEXAS_HOLDEM, TH_HAND_STRAIGHT, "C4|S5|H6|D7|C8", [8], 5),
    (GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, "C4|S4|D4|D8|DJ", [4, 11, 8], 4),
    (GAME_TEXAS_HOLDEM, TH_HAND_TRIPS, "C4|S4|D4|D8", [4, 8, None], 4),
    (GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, "C4|S4|HA|DA|D6", [14, 4, 6], 3),
    (GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, "C4|S4|HA|DA", [14, 4, None], 3),
    (GAME_TEXAS_HOLDEM, TH_HAND_PAIR, "C4|D4|ST|HA|C9", [4, 14, 10, 9], 2),
    (GAME_TEXAS_HOLDEM, TH_HAND_PAIR, "C4|D4", [4, None, None, None], 2),
    (GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, "C4|D2|ST|HA|C9", [14, 10, 9, 4, 2], 1),
    (GAME_TEXAS_HOLDEM, TH_HAND_HIGH_CARD, "ST|HA|C9", [14, 10, 9, None, None], 1),
])
def test_when_hand_then_correct_values_set(get_test_cards, game, hand_type, cards, tiebreakers, strength):
    cards = get_test_cards(cards)

    hand = Hand(game, hand_type, cards, tiebreakers)

    assert hand.game == game
    assert hand.type == hand_type
    assert hand.cards == cards
    assert hand.tiebreakers == tiebreakers
    assert hand.strength == strength


def test_when_hand_equality_and_diff_games_then_raise_error(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])

    hand_b.game = "diff_game"

    with raises(GameMismatchError, match="Hand comparisons can only occur for hands of the same game type"):
        equal = hand_a == hand_b


def test_when_hand_equality_and_diff_strength_then_return_false(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D5|H5|H9|C9|SA"), [9, 5, 14])

    result = hand_a == hand_b
    assert result is False


def test_when_hand_equality_and_tiebreaker_top_level_diff_then_return_false(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D6|H6|H9|CJ|SA"), [6, 14, 11, 9])

    result = hand_a == hand_b
    assert result is False


def test_when_hand_equality_and_tiebreaker_lower_level_diff_then_return_false(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CQ|SA"), [5, 14, 12, 9])

    result = hand_a == hand_b
    assert result is False


def test_when_hand_equality_and_tiebreaker_with_nones_dff_then_return_false(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|S2"), [5, 11, 9, 2])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|SJ"), [5, 11, 9, None])

    result = hand_a == hand_b
    assert result is False


def test_when_hand_equality_and_equal_then_return_true(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|SJ|DA"), [5, 14, 11, 9])

    result = hand_a == hand_b
    assert result is True


def test_when_hand_equality_and_equal_with_nones_then_return_true(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9"), [5, 9, None, None])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9"), [5, 9, None, None])

    result = hand_a == hand_b
    assert result is True


def test_when_hand_greater_than_and_diff_games_then_raise_error(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])

    hand_b.game = "diff_game"

    with raises(GameMismatchError, match="Hand comparisons can only occur for hands of the same game type"):
        equal = hand_a > hand_b

    with raises(GameMismatchError, match="Hand comparisons can only occur for hands of the same game type"):
        equal = hand_a >= hand_b


def test_when_hand_greater_than_and_diff_strength_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D5|H5|H9|C9|SA"), [9, 5, 14])

    result = hand_a > hand_b
    assert result is False

    result = hand_b > hand_a
    assert result is True

    result = hand_a >= hand_b
    assert result is False

    result = hand_b >= hand_a
    assert result is True


def test_when_hand_greater_than_and_tiebreaker_top_level_diff_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D6|H6|H9|CJ|SA"), [6, 14, 11, 9])

    result = hand_a > hand_b
    assert result is False

    result = hand_b > hand_a
    assert result is True

    result = hand_a >= hand_b
    assert result is False

    result = hand_b >= hand_a
    assert result is True


def test_when_hand_greater_than_and_tiebreaker_lower_level_diff_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CQ|SA"), [5, 14, 12, 9])

    result = hand_a > hand_b
    assert result is False

    result = hand_b > hand_a
    assert result is True

    result = hand_a >= hand_b
    assert result is False

    result = hand_b >= hand_a
    assert result is True


def test_when_hand_greater_than_and_tiebreaker_with_nones_dff_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|S2"), [5, 11, 9, 2])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|SJ"), [5, 11, 9, None])

    result = hand_a > hand_b
    assert result is True

    result = hand_b > hand_a
    assert result is False

    result = hand_a >= hand_b
    assert result is True

    result = hand_b >= hand_a
    assert result is False


def test_when_hand_greater_than_and_equal_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|SJ|DA"), [5, 14, 11, 9])

    result = hand_a > hand_b
    assert result is False

    result = hand_b > hand_a
    assert result is False

    result = hand_a >= hand_b
    assert result is True

    result = hand_b >= hand_a
    assert result is True


def test_when_hand_greater_than_and_equal_with_nones_then_return_true(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9"), [5, 9, None, None])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9"), [5, 9, None, None])

    result = hand_a > hand_b
    assert result is False

    result = hand_b > hand_a
    assert result is False

    result = hand_a >= hand_b
    assert result is True

    result = hand_b >= hand_a
    assert result is True


def test_when_hand_less_than_and_diff_games_then_raise_error(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])

    hand_b.game = "diff_game"

    with raises(GameMismatchError, match="Hand comparisons can only occur for hands of the same game type"):
        equal = hand_a < hand_b

    with raises(GameMismatchError, match="Hand comparisons can only occur for hands of the same game type"):
        equal = hand_a <= hand_b


def test_when_hand_less_than_and_diff_strength_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_TWO_PAIR, get_test_cards("D5|H5|H9|C9|SA"), [9, 5, 14])

    result = hand_a < hand_b
    assert result is True

    result = hand_b < hand_a
    assert result is False

    result = hand_a <= hand_b
    assert result is True

    result = hand_b <= hand_a
    assert result is False


def test_when_hand_less_than_and_tiebreaker_top_level_diff_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D6|H6|H9|CJ|SA"), [6, 14, 11, 9])

    result = hand_a < hand_b
    assert result is True

    result = hand_b < hand_a
    assert result is False

    result = hand_a <= hand_b
    assert result is True

    result = hand_b <= hand_a
    assert result is False


def test_when_hand_less_than_and_tiebreaker_lower_level_diff_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CQ|SA"), [5, 14, 12, 9])

    result = hand_a < hand_b
    assert result is True

    result = hand_b < hand_a
    assert result is False

    result = hand_a <= hand_b
    assert result is True

    result = hand_b <= hand_a
    assert result is False


def test_when_hand_less_than_and_tiebreaker_with_nones_dff_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|S2"), [5, 11, 9, 2])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|SJ"), [5, 11, 9, None])

    result = hand_a < hand_b
    assert result is False

    result = hand_b < hand_a
    assert result is True

    result = hand_a <= hand_b
    assert result is False

    result = hand_b <= hand_a
    assert result is True


def test_when_hand_less_than_and_equal_then_correct_returns(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|CJ|SA"), [5, 14, 11, 9])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9|SJ|DA"), [5, 14, 11, 9])

    result = hand_a < hand_b
    assert result is False

    result = hand_b < hand_a
    assert result is False

    result = hand_a <= hand_b
    assert result is True

    result = hand_b <= hand_a
    assert result is True


def test_when_hand_less_than_and_equal_with_nones_then_return_true(get_test_cards):
    hand_a = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9"), [5, 9, None, None])
    hand_b = Hand(GAME_TEXAS_HOLDEM, TH_HAND_PAIR, get_test_cards("D5|H5|H9"), [5, 9, None, None])

    result = hand_a < hand_b
    assert result is False

    result = hand_b < hand_a
    assert result is False

    result = hand_a <= hand_b
    assert result is True

    result = hand_b <= hand_a
    assert result is True