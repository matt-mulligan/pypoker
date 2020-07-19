from pytest import mark, raises

from pypoker.deck import Card, Deck

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
