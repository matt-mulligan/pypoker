from unittest.mock import patch, call

from pytest import mark, raises, fixture

from pypoker.deck import Card, Deck


###################
#  TEST FIXTURES  #
###################

@fixture
def deck_card_names():
    return [
        "Two of Clubs", "Three of Clubs", "Four of Clubs", "Five of Clubs", "Six of Clubs", "Seven of Clubs",
        "Eight of Clubs", "Nine of Clubs", "Ten of Clubs", "Jack of Clubs", "Queen of Clubs", "King of Clubs",
        "Ace of Clubs", "Two of Spades", "Three of Spades", "Four of Spades", "Five of Spades", "Six of Spades",
        "Seven of Spades", "Eight of Spades", "Nine of Spades", "Ten of Spades", "Jack of Spades", "Queen of Spades",
        "King of Spades", "Ace of Spades", "Two of Diamonds", "Three of Diamonds", "Four of Diamonds",
        "Five of Diamonds", "Six of Diamonds", "Seven of Diamonds", "Eight of Diamonds", "Nine of Diamonds",
        "Ten of Diamonds", "Jack of Diamonds", "Queen of Diamonds", "King of Diamonds", "Ace of Diamonds",
        "Two of Hearts", "Three of Hearts", "Four of Hearts", "Five of Hearts", "Six of Hearts", "Seven of Hearts",
        "Eight of Hearts", "Nine of Hearts", "Ten of Hearts", "Jack of Hearts", "Queen of Hearts", "King of Hearts",
        "Ace of Hearts"
    ]


@fixture
def cards_five():
    return [Card(3, "D"), Card("A", "D"), Card("Q", "C"), Card(7, "H"), Card(9, "S")]

###########################
#  CARD CLASS UNIT TESTS  #
###########################


@mark.parametrize("card_val, suit_val, card_name", [
    (2, "C", "Two of Clubs"),
    (3, "C", "Three of Clubs"),
    (4, "C", "Four of Clubs"),
    (5, "C", "Five of Clubs"),
    (6, "C", "Six of Clubs"),
    (7, "C", "Seven of Clubs"),
    (8, "C", "Eight of Clubs"),
    (9, "C", "Nine of Clubs"),
    (10, "C", "Ten of Clubs"),
    ("J", "C", "Jack of Clubs"),
    ("Q", "C", "Queen of Clubs"),
    ("K", "C", "King of Clubs"),
    ("A", "C", "Ace of Clubs"),
    (2, "D", "Two of Diamonds"),
    (3, "D", "Three of Diamonds"),
    (4, "D", "Four of Diamonds"),
    (5, "D", "Five of Diamonds"),
    (6, "D", "Six of Diamonds"),
    (7, "D", "Seven of Diamonds"),
    (8, "D", "Eight of Diamonds"),
    (9, "D", "Nine of Diamonds"),
    (10, "D", "Ten of Diamonds"),
    ("J", "D", "Jack of Diamonds"),
    ("Q", "D", "Queen of Diamonds"),
    ("K", "D", "King of Diamonds"),
    ("A", "D", "Ace of Diamonds"),
    (2, "H", "Two of Hearts"),
    (3, "H", "Three of Hearts"),
    (4, "H", "Four of Hearts"),
    (5, "H", "Five of Hearts"),
    (6, "H", "Six of Hearts"),
    (7, "H", "Seven of Hearts"),
    (8, "H", "Eight of Hearts"),
    (9, "H", "Nine of Hearts"),
    (10, "H", "Ten of Hearts"),
    ("J", "H", "Jack of Hearts"),
    ("Q", "H", "Queen of Hearts"),
    ("K", "H", "King of Hearts"),
    ("A", "H", "Ace of Hearts"),
    (2, "S", "Two of Spades"),
    (3, "S", "Three of Spades"),
    (4, "S", "Four of Spades"),
    (5, "S", "Five of Spades"),
    (6, "S", "Six of Spades"),
    (7, "S", "Seven of Spades"),
    (8, "S", "Eight of Spades"),
    (9, "S", "Nine of Spades"),
    (10, "S", "Ten of Spades"),
    ("J", "S", "Jack of Spades"),
    ("Q", "S", "Queen of Spades"),
    ("K", "S", "King of Spades"),
    ("A", "S", "Ace of Spades")
])
def test_when_card_init_then_correct_values_set(card_val, suit_val, card_name):
    card = Card(card_val, suit_val)
    assert card.name == card_name


@mark.parametrize("card_val", [
    1, 16, "ace", "Nine"
])
def test_when_card_init_and_card_rank_bad_then_raise_error(card_val):
    with raises(ValueError, match=f"Specified card rank {card_val} is not in value mapping dictionary"):
        Card(card_val, "C")


@mark.parametrize("suit_val", [
    -1, 6, "3", "SPADES", "Clubs", "hearts"
])
def test_when_card_init_and_suit_value_bad_then_raise_error(suit_val):
    with raises(ValueError, match=f"Suit value '{suit_val}' is not in list of valid values"):
        Card(5, suit_val)


@mark.parametrize("card_a, card_b, expected", [
    (Card(7, "D"), Card(10, "D"), False),
    (Card("Q", "H"), Card(3, "H"), True),
    (Card(3, "S"), Card("K", "C"), False),
    (Card(10, "C"), Card(4, "H"), True),
    (Card(7, "H"), Card(7, "S"), False)
])
def test_when_card_greater_than_then_correct_result_returned(card_a, card_b, expected):
    actual = card_a > card_b
    assert actual == expected


@mark.parametrize("card_a, card_b, expected", [
    (Card(7, "D"), Card(10, "D"), True),
    (Card("Q", "H"), Card(3, "H"), False),
    (Card(3, "S"), Card("K", "C"), True),
    (Card(10, "C"), Card(4, "H"), False),
    (Card(7, "H"), Card(7, "S"), False)
])
def test_when_card_less_than_then_correct_result_returned(card_a, card_b, expected):
    actual = card_a < card_b
    assert actual == expected


###########################
#  DECK CLASS UNIT TESTS  #
###########################

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

    with patch("pypoker.deck.random") as random_mock:
        deck.shuffle()

    random_mock.assert_has_calls([
        call.shuffle(deck.cards_available)
    ])


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


@mark.parametrize("cards, expected_card_names, descending", [
    (
        [Card(7, "D"), Card(4, "D"), Card("A", "D"), Card("Q", "D")],
        ["Four of Diamonds", "Seven of Diamonds", "Queen of Diamonds", "Ace of Diamonds"],
        False
    ),
    (
        [Card(7, "D"), Card(4, "D"), Card("A", "C"), Card("Q", "C")],
        ["Queen of Clubs", "Ace of Clubs", "Four of Diamonds", "Seven of Diamonds"],
        False
    ),
    (
        [Card(7, "D"), Card(4, "D"), Card("A", "D"), Card("Q", "D")],
        ["Ace of Diamonds", "Queen of Diamonds", "Seven of Diamonds", "Four of Diamonds"],
        True
    ),
    (
        [Card(7, "D"), Card(4, "D"), Card("A", "C"), Card("Q", "C")],
        ["Ace of Clubs", "Queen of Clubs", "Seven of Diamonds", "Four of Diamonds"],
        True
    ),
])
def test_when_deck_order_cards_then_correct_reordering_occurs(cards, expected_card_names, descending):
    deck = Deck()
    reordered_cards = deck.order_cards(cards, descending=descending)

    reordered_card_names = [card.name for card in reordered_cards]
    assert reordered_card_names == expected_card_names


def test_when_deck_order_cards_and_non_card_passed_then_raise_error():
    deck = Deck()
    cards = [Card(5, "C"), "Six of Spades", Card(9, "S")]
    with raises(ValueError, match="All objects within cards value must be an instance of the Cards Class"):
        deck.order_cards(cards)
