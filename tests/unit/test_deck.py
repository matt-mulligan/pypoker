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
    return [Card(3,1), Card(14,1), Card(12,0), Card(7,2), Card(9,3)]

###########################
#  CARD CLASS UNIT TESTS  #
###########################


@mark.parametrize("card_val, suit_val, card_name", [
    (2, 0, "Two of Clubs"),
    (3, 0, "Three of Clubs"),
    (4, 0, "Four of Clubs"),
    (5, 0, "Five of Clubs"),
    (6, 0, "Six of Clubs"),
    (7, 0, "Seven of Clubs"),
    (8, 0, "Eight of Clubs"),
    (9, 0, "Nine of Clubs"),
    (10, 0, "Ten of Clubs"),
    (11, 0, "Jack of Clubs"),
    (12, 0, "Queen of Clubs"),
    (13, 0, "King of Clubs"),
    (14, 0, "Ace of Clubs"),
    (2, 1, "Two of Diamonds"),
    (3, 1, "Three of Diamonds"),
    (4, 1, "Four of Diamonds"),
    (5, 1, "Five of Diamonds"),
    (6, 1, "Six of Diamonds"),
    (7, 1, "Seven of Diamonds"),
    (8, 1, "Eight of Diamonds"),
    (9, 1, "Nine of Diamonds"),
    (10, 1, "Ten of Diamonds"),
    (11, 1, "Jack of Diamonds"),
    (12, 1, "Queen of Diamonds"),
    (13, 1, "King of Diamonds"),
    (14, 1, "Ace of Diamonds"),
    (2, 2, "Two of Hearts"),
    (3, 2, "Three of Hearts"),
    (4, 2, "Four of Hearts"),
    (5, 2, "Five of Hearts"),
    (6, 2, "Six of Hearts"),
    (7, 2, "Seven of Hearts"),
    (8, 2, "Eight of Hearts"),
    (9, 2, "Nine of Hearts"),
    (10, 2, "Ten of Hearts"),
    (11, 2, "Jack of Hearts"),
    (12, 2, "Queen of Hearts"),
    (13, 2, "King of Hearts"),
    (14, 2, "Ace of Hearts"),
    (2, 3, "Two of Spades"),
    (3, 3, "Three of Spades"),
    (4, 3, "Four of Spades"),
    (5, 3, "Five of Spades"),
    (6, 3, "Six of Spades"),
    (7, 3, "Seven of Spades"),
    (8, 3, "Eight of Spades"),
    (9, 3, "Nine of Spades"),
    (10, 3, "Ten of Spades"),
    (11, 3, "Jack of Spades"),
    (12, 3, "Queen of Spades"),
    (13, 3, "King of Spades"),
    (14, 3, "Ace of Spades")
])
def test_when_card_init_then_correct_values_set(card_val, suit_val, card_name):
    card = Card(card_val, suit_val)
    assert card.name == card_name


@mark.parametrize("card_val", [
    1, 16, "3", "ace", "Nine"
])
def test_when_card_init_and_card_value_bad_then_raise_error(card_val):
    with raises(ValueError, match=f"Specified card value {card_val} is not in value mapping dictionary"):
        Card(card_val, 0)


@mark.parametrize("suit_val", [
    -1, 6, "3", "SPADES", "Clubs", "hearts"
])
def test_when_card_init_and_suit_value_bad_then_raise_error(suit_val):
    with raises(ValueError, match=f"Suit value '{suit_val}'  is not in list of valid values"):
        Card(5, suit_val)


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
        [Card(7, 1), Card(4, 1), Card(14, 1), Card(12, 1)],
        ["Four of Diamonds", "Seven of Diamonds", "Queen of Diamonds", "Ace of Diamonds"],
        False
    ),
    (
        [Card(7, 1), Card(4, 1), Card(14, 0), Card(12, 0)],
        ["Queen of Clubs", "Ace of Clubs", "Four of Diamonds", "Seven of Diamonds"],
        False
    ),
    (
        [Card(7, 1), Card(4, 1), Card(14, 1), Card(12, 1)],
        ["Ace of Diamonds", "Queen of Diamonds", "Seven of Diamonds", "Four of Diamonds"],
        True
    ),
    (
        [Card(7, 1), Card(4, 1), Card(14, 0), Card(12, 0)],
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
    cards = [Card(5, 1), "Six of Spades", Card(9, 3)]
    with raises(ValueError, match="All objects within cards value must be an instance of the Cards Class"):
        deck.order_cards(cards)
