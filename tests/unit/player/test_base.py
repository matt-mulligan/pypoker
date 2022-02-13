import re

from pytest import mark, raises

from pypoker.constants import GameTypes, TexasHoldemHandType
from pypoker.constructs import Card, Hand
from pypoker.player import BasePlayer


def test_when_base_player_created_and_no_optionals_then_player_attr_correct():
    player = BasePlayer("Matt")

    assert player.name == "Matt"
    assert player.chips is None
    assert player.hole_cards is None
    assert player.table_pos is None
    assert player.hand is None
    assert player.current_bet is None


def test_when_base_player_created_and_all_optionals_then_attr_correct(get_test_cards):
    player = BasePlayer(
        "Matt", chips=12345, hole_cards=get_test_cards("H2|D4"), table_pos=1,
        hand=Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|S9|C8|CK"), [7, 13, 9, 8])
    )
    assert player.name == "Matt"
    assert player.chips == 12345
    assert player.hole_cards == [Card("H2"), Card("D4")]
    assert player.table_pos == 1
    assert player.hand == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|S9|C8|CK"), [7, 13, 9, 8])
    assert player.current_bet is None


def test_when_base_player_and_properties_set_then_attr_correct(get_test_cards):
    player = BasePlayer("Matt")
    player.chips = 9001
    player.hole_cards = [Card("DK"), Card("DA")]
    player.table_pos = 9
    player.current_bet = 1000
    player.hand = Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|S9|C8|CK"), [7, 13, 9, 8])

    assert player.name == "Matt"
    assert player.chips == 9001
    assert player.hole_cards == [Card("DK"), Card("DA")]
    assert player.table_pos == 9
    assert player.current_bet == 1000
    assert player.hand == Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Pair, get_test_cards("D7|H7|S9|C8|CK"), [7, 13, 9, 8])


@mark.parametrize("chips", ["123", -45])
def test_when_base_player_and_bad_chips_then_raise_error(chips):
    with raises(ValueError, match="Player chips must be set to a positive integer"):
        BasePlayer("Billy Sastard", chips)

    good_player = BasePlayer("Matt", 1234)
    with raises(ValueError, match="Player chips must be set to a positive integer"):
        good_player.chips = chips


@mark.parametrize(
    "cards, err_msg",
    [
        ((Card("H2")), "hole cards must be a list object"),
        ([Card("H2"), "D4"], "hole card objects must all be card objects"),
    ],
)
def test_when_base_player_and_bad_hole_cards_then_raise_error(cards, err_msg):
    with raises(ValueError, match=err_msg):
        BasePlayer("Billy Sastard", hole_cards=cards)

    good_player = BasePlayer("Matt", 1234)
    with raises(ValueError, match=err_msg):
        good_player.hole_cards = cards


@mark.parametrize("pos", ["7", 0, 10])
def test_when_base_player_and_bad_table_pos_then_raise_error(pos):
    with raises(ValueError, match="table position must be set to between 1 and 9"):
        BasePlayer("Billy Sastard", table_pos=pos)

    good_player = BasePlayer("Matt", 1234)
    with raises(ValueError, match="table position must be set to between 1 and 9"):
        good_player.table_pos = pos


@mark.parametrize("bet", ["7", -1, 12345.67])
def test_when_base_player_and_bad_current_bet_then_raise_error(bet):
    good_player = BasePlayer("Matt", 1234)
    with raises(ValueError, match="bet must be set to a positive integer or zero"):
        good_player.current_bet = bet


def test_when_bnase_player_and_bad_hand_then_raise_error():
    good_player = BasePlayer("Matt", 1234)
    with raises(ValueError, match=re.escape("player.hand values must be of type Hand")):
        good_player.hand = "left"
