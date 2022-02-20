import pypoker.engine.texas_holdem.find_outs as outs


def test_when_find_outs_straight_flush_and_no_eligible_suits_then_return_empty_list(get_test_cards):
    current_cards = get_test_cards("D7|D9|ST|SJ|C6|C5")
    available_cards = get_test_cards("D8|DT|SQ|SK|C2|C4")
    remaining_draws = 1

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_straight_flush_and_no_connecting_cards_then_return_empty_list(get_test_cards):
    current_cards = get_test_cards("D7|D9|DT|D6|C6")
    available_cards = get_test_cards("D5|D4|DJ|DQ|C2|C4")
    remaining_draws = 2

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_straight_flush_and_one_draw_inside_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("D7|D9|DT|D6|C6")
    available_cards = get_test_cards("D5|D4|DJ|D8|C2|C4")
    remaining_draws = 1

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1
    assert get_test_cards("D8") in result


def test_when_find_outs_straight_flush_and_one_draw_open_ended_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("D7|D9|DT|D8|C6")
    available_cards = get_test_cards("D6|D4|DJ|C2|C4")
    remaining_draws = 1

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 2
    assert get_test_cards("D6") in result
    assert get_test_cards("DJ") in result


def test_when_find_outs_straight_flush_and_one_draw_already_have_hand_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("D7|D9|DT|D8|C6|D6")
    available_cards = get_test_cards("D5|C2|C4")
    remaining_draws = 1

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 2
    assert get_test_cards("ANY_CARD") in result
    assert get_test_cards("D5") in result


def test_when_find_outs_straight_flush_and_two_draw_inside_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("D7|DT|D6|C6")
    available_cards = get_test_cards("D5|D4|DJ|D8|C2|D9|C4")
    remaining_draws = 2

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1
    assert get_test_cards("D9|D8") in result


def test_when_find_outs_straight_flush_and_two_draw_open_ended_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("CA|D9|DT|D8|C6")
    available_cards = get_test_cards("D7|D4|DJ|C2|DQ|C4")
    remaining_draws = 2

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 2
    assert get_test_cards("DJ|D7") in result
    assert get_test_cards("DQ|DJ") in result


def test_when_find_outs_straight_flush_and_two_draw_inside_outside_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("CA|D9|DT|D7|C6")
    available_cards = get_test_cards("D8|D4|DJ|C2|DQ|C4")
    remaining_draws = 2

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1
    assert get_test_cards("DJ|D8") in result


def test_when_find_outs_straight_flush_and_two_draw_already_have_hand_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("D7|D9|DT|D8|C6|D6")
    available_cards = get_test_cards("D5|C2|C4|DJ|C7|DQ")
    remaining_draws = 2

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 4
    assert get_test_cards("ANY_CARD|ANY_CARD") in result
    assert get_test_cards("D5|ANY_CARD") in result
    assert get_test_cards("DJ|ANY_CARD") in result
    assert get_test_cards("DQ|DJ") in result


def test_when_find_outs_straight_flush_and_three_draw_inside_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("CQ|DT|D6|C6")
    available_cards = get_test_cards("D7|D4|DJ|D8|C2|D9|C4")
    remaining_draws = 3

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1
    assert get_test_cards("D9|D8|D7") in result


def test_when_find_outs_straight_flush_and_three_draw_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("CA|D9|DT|C2")
    available_cards = get_test_cards("D8|D4|DJ|DK|DQ|C4|D7|D6|DJ|DQ|DK|C3|C5|C4|C7")
    remaining_draws = 3

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 5
    assert get_test_cards("D8|D7|D6") in result
    assert get_test_cards("DJ|D8|D7") in result
    assert get_test_cards("DQ|DJ|D8") in result
    assert get_test_cards("DK|DQ|DJ") in result
    assert get_test_cards("C5|C4|C3") in result


def test_when_find_outs_straight_flush_and_three_draw_already_have_hand_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("D7|D9|DT|D8|C6|D6")
    available_cards = get_test_cards("D5|C2|C4|DJ|C7|DQ|D4")
    remaining_draws = 3

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 5

    assert get_test_cards("ANY_CARD|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("D5|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("DJ|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("DQ|DJ|ANY_CARD") in result
    assert get_test_cards("D5|D4|ANY_CARD") in result


def test_when_find_outs_straight_flush_and_five_draw_then_correct_values_returned(get_test_cards):
    current_cards = get_test_cards("CA|D9")
    available_cards = get_test_cards("CK|CQ|CJ|CT|C9|C8|C7|C6|C5|C4|C3|C2|DA|DK|DQ|DJ|DT|D8|D7|D6|D5|D4|D3|D2|HA|HK|HQ|HJ|HT|H9|H8|H7|H6|H5|H4|H3|H2")
    remaining_draws = 5

    result = outs.find_outs_straight_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 30

    assert get_test_cards("CK|CQ|CJ|CT|ANY_CARD") in result
    assert get_test_cards("CK|CQ|CJ|CT|C9") in result
    assert get_test_cards("CQ|CJ|CT|C9|C8") in result
    assert get_test_cards("CJ|CT|C9|C8|C7") in result
    assert get_test_cards("CT|C9|C8|C7|C6") in result
    assert get_test_cards("C9|C8|C7|C6|C5") in result
    assert get_test_cards("C8|C7|C6|C5|C4") in result
    assert get_test_cards("C7|C6|C5|C4|C3") in result
    assert get_test_cards("C6|C5|C4|C3|C2") in result
    assert get_test_cards("C5|C4|C3|C2|ANY_CARD") in result

    assert get_test_cards("DA|DK|DQ|DJ|DT") in result
    assert get_test_cards("DK|DQ|DJ|DT|ANY_CARD") in result
    assert get_test_cards("DQ|DJ|DT|D8|ANY_CARD") in result
    assert get_test_cards("DJ|DT|D8|D7|ANY_CARD") in result
    assert get_test_cards("DT|D8|D7|D6|ANY_CARD") in result
    assert get_test_cards("D8|D7|D6|D5|ANY_CARD") in result
    assert get_test_cards("D8|D7|D6|D5|D4") in result
    assert get_test_cards("D7|D6|D5|D4|D3") in result
    assert get_test_cards("D6|D5|D4|D3|D2") in result
    assert get_test_cards("DA|D5|D4|D3|D2") in result

    assert get_test_cards("HA|HK|HQ|HJ|HT") in result
    assert get_test_cards("HK|HQ|HJ|HT|H9") in result
    assert get_test_cards("HQ|HJ|HT|H9|H8") in result
    assert get_test_cards("HJ|HT|H9|H8|H7") in result
    assert get_test_cards("HT|H9|H8|H7|H6") in result
    assert get_test_cards("H9|H8|H7|H6|H5") in result
    assert get_test_cards("H8|H7|H6|H5|H4") in result
    assert get_test_cards("H7|H6|H5|H4|H3") in result
    assert get_test_cards("H6|H5|H4|H3|H2") in result
    assert get_test_cards("HA|H5|H4|H3|H2") in result


def test_when_find_outs_quads_and_none_possible_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("D5|S9|SK|ST|C5|H9")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_quads(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_quads_and_none_possible_via_deck_exhaustion_then_return_empty_list(get_test_cards):
    current_cards = get_test_cards("D5|S9|C9|ST|C5|H9")
    available_cards = get_test_cards("D8|SA|CJ|S5")
    remaining_draws = 2

    result = outs.find_outs_quads(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_quads_and_already_have_then_return_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("D5|S9|H5|S5|C5|HJ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_quads(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1

    assert get_test_cards("ANY_CARD|ANY_CARD") in result


def test_when_find_outs_quads_and_one_draw_and_outs_then_return_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("D5|S9|H5|C9|C5|H9")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_quads(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 2

    assert get_test_cards("S5") in result
    assert get_test_cards("D9") in result


def test_when_find_outs_quads_and_two_draw_and_outs_then_return_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("D5|S9|H5|C5|H9")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_quads(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 2

    assert get_test_cards("S5|ANY_CARD") in result
    assert get_test_cards("D9|C9") in result


def test_when_find_outs_quads_and_five_draw_and_outs_then_return_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|SK")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 5

    result = outs.find_outs_quads(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 13

    assert get_test_cards("S2|H2|D2|C2|ANY_CARD") in result
    assert get_test_cards("S3|H3|D3|C3|ANY_CARD") in result
    assert get_test_cards("S4|H4|D4|C4|ANY_CARD") in result
    assert get_test_cards("S5|H5|D5|C5|ANY_CARD") in result
    assert get_test_cards("S6|H6|D6|C6|ANY_CARD") in result
    assert get_test_cards("S7|H7|D7|C7|ANY_CARD") in result
    assert get_test_cards("S8|H8|D8|C8|ANY_CARD") in result
    assert get_test_cards("S9|H9|D9|C9|ANY_CARD") in result
    assert get_test_cards("ST|HT|DT|CT|ANY_CARD") in result
    assert get_test_cards("SJ|HJ|DJ|CJ|ANY_CARD") in result
    assert get_test_cards("SQ|HQ|DQ|CQ|ANY_CARD") in result
    assert get_test_cards("HK|DK|CK|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|HA|CA|ANY_CARD|ANY_CARD") in result


def test_when_find_outs_full_house_and_no_possible_trips_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|HK|C2|D9|S6|H4")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_full_house(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_full_house_and_not_enough_draws_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|HA|C2|D9|S6|H4")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_full_house(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_full_house_one_draw_and_outs_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|HA|C2|CA|S2|H4")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_full_house(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 6

    assert get_test_cards("ANY_CARD") in result
    assert get_test_cards("S4") in result
    assert get_test_cards("C4") in result
    assert get_test_cards("D4") in result
    assert get_test_cards("D2") in result
    assert get_test_cards("H2") in result


def test_when_find_outs_full_house_two_draws_and_outs_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|HA|C2|S2|H4")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_full_house(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 19

    assert get_test_cards("SA|ANY_CARD") in result
    assert get_test_cards("CA|ANY_CARD") in result

    assert get_test_cards("H2|ANY_CARD") in result
    assert get_test_cards("D2|ANY_CARD") in result

    assert get_test_cards("S4|D4") in result
    assert get_test_cards("D4|C4") in result
    assert get_test_cards("S4|C4") in result

    assert get_test_cards("SA|S4") in result
    assert get_test_cards("SA|D4") in result
    assert get_test_cards("SA|C4") in result

    assert get_test_cards("CA|S4") in result
    assert get_test_cards("CA|D4") in result
    assert get_test_cards("CA|C4") in result

    assert get_test_cards("S4|H2") in result
    assert get_test_cards("D4|H2") in result
    assert get_test_cards("C4|H2") in result

    assert get_test_cards("S4|D2") in result
    assert get_test_cards("D4|D2") in result
    assert get_test_cards("C4|D2") in result


def test_when_find_outs_full_house_and_five_draws_and_outs_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|HA")
    available_cards = get_test_cards("SA|CA|S7|H7|D7|C7|S2|H2")
    remaining_draws = 5

    result = outs.find_outs_full_house(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 22

    assert get_test_cards("SA|S7|H7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|S7|D7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|S7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|H7|D7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|H7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|D7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|S2|H2|ANY_CARD|ANY_CARD") in result

    assert get_test_cards("CA|S7|H7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("CA|S7|D7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("CA|S7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("CA|H7|D7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("CA|H7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("CA|D7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("CA|S2|H2|ANY_CARD|ANY_CARD") in result

    assert get_test_cards("S7|H7|D7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("S7|H7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("S7|D7|C7|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("H7|D7|C7|ANY_CARD|ANY_CARD") in result

    assert get_test_cards("S7|H7|D7|S2|H2") in result
    assert get_test_cards("S7|H7|C7|S2|H2") in result
    assert get_test_cards("S7|D7|C7|S2|H2") in result
    assert get_test_cards("H7|D7|C7|S2|H2") in result


def test_when_find_outs_flush_and_no_suits_possible_because_draw_numbers_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("DA|HA|S7|C2|S2|H2")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_flush_and_no_suits_possible_becuase_deck_depleted_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK|C7|C2|S2|H2")
    available_cards = get_test_cards("DA|SK|H7|D2|S2|H2")
    remaining_draws = 2

    result = outs.find_outs_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_flush_and_already_have_one_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK|C7|C2|S2|H2|C4")
    available_cards = get_test_cards("DA|SK|H7|D2|S2|H2")
    remaining_draws = 2

    result = outs.find_outs_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1

    assert get_test_cards("ANY_CARD|ANY_CARD") in result


def test_when_find_outs_flush_and_one_draw_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK|C7|C2|S2|S9")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 9

    assert get_test_cards("CQ") in result
    assert get_test_cards("CJ") in result
    assert get_test_cards("CT") in result
    assert get_test_cards("C9") in result
    assert get_test_cards("C8") in result
    assert get_test_cards("C6") in result
    assert get_test_cards("C5") in result
    assert get_test_cards("C4") in result
    assert get_test_cards("C3") in result


def test_when_find_outs_flush_and_two_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK|C7|C2|S2|S9|SK")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 54

    assert get_test_cards("CQ|ANY_CARD") in result
    assert get_test_cards("CJ|ANY_CARD") in result
    assert get_test_cards("CT|ANY_CARD") in result
    assert get_test_cards("C9|ANY_CARD") in result
    assert get_test_cards("C8|ANY_CARD") in result
    assert get_test_cards("C6|ANY_CARD") in result
    assert get_test_cards("C5|ANY_CARD") in result
    assert get_test_cards("C4|ANY_CARD") in result
    assert get_test_cards("C3|ANY_CARD") in result

    assert get_test_cards("SA|SQ") in result
    # not asserting all 54 outs


def test_when_find_outs_flush_and_five_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 5

    result = outs.find_outs_flush(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 4026

    assert get_test_cards("CQ|CJ|CT|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("SA|S7|S6|S3|S2") in result
    assert get_test_cards("HT|H9|H5|H4|H2") in result
    assert get_test_cards("DQ|D9|D6|D4|D3") in result
    # not asserting all 4026 outs


def test_when_find_outs_straight_and_no_possible_values_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK|D5|C8|H8|S8")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_straight(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_straight_and_single_inner_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CK|D5|C8|HJ|ST")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_straight(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 4

    assert get_test_cards("SQ") in result
    assert get_test_cards("HQ") in result
    assert get_test_cards("CQ") in result
    assert get_test_cards("DQ") in result


def test_when_find_outs_straight_and_single_open_ender_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("C3|CK|D4|C8|H2|S5")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_straight(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 8

    assert get_test_cards("SA") in result
    assert get_test_cards("HA") in result
    assert get_test_cards("CA") in result
    assert get_test_cards("DA") in result
    assert get_test_cards("S6") in result
    assert get_test_cards("H6") in result
    assert get_test_cards("C6") in result
    assert get_test_cards("D6") in result


def test_when_find_outs_straight_and_multiple_straights_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|D5|C8|HJ|ST")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_straight(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 48

    # not asserting all 48 outs
    assert get_test_cards("SK|SQ") in result
    assert get_test_cards("SK|DQ") in result
    assert get_test_cards("CK|SQ") in result
    assert get_test_cards("HK|CQ") in result

    assert get_test_cards("SQ|S9") in result
    assert get_test_cards("SQ|D9") in result
    assert get_test_cards("CQ|S9") in result
    assert get_test_cards("HQ|C9") in result

    assert get_test_cards("S9|S7") in result
    assert get_test_cards("S9|D7") in result
    assert get_test_cards("C9|S7") in result
    assert get_test_cards("H9|C7") in result


def test_when_find_outs_straight_and_surplus_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|D5|CK|HJ|ST")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_straight(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 20

    assert get_test_cards("SQ|ANY_CARD") in result
    assert get_test_cards("DQ|ANY_CARD") in result
    assert get_test_cards("HQ|ANY_CARD") in result
    assert get_test_cards("CQ|ANY_CARD") in result

    assert get_test_cards("SQ|S9") in result
    assert get_test_cards("SQ|H9") in result
    assert get_test_cards("SQ|C9") in result
    assert get_test_cards("SQ|D9") in result

    assert get_test_cards("DQ|S9") in result
    assert get_test_cards("DQ|H9") in result
    assert get_test_cards("DQ|C9") in result
    assert get_test_cards("DQ|D9") in result

    assert get_test_cards("HQ|S9") in result
    assert get_test_cards("HQ|H9") in result
    assert get_test_cards("HQ|C9") in result
    assert get_test_cards("HQ|D9") in result

    assert get_test_cards("CQ|S9") in result
    assert get_test_cards("CQ|H9") in result
    assert get_test_cards("CQ|C9") in result
    assert get_test_cards("CQ|D9") in result


def test_when_find_outs_straight_and_already_have_one_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|CK|HJ|ST")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_straight(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 21

    assert get_test_cards("ANY_CARD|ANY_CARD") in result

    assert get_test_cards("S9|ANY_CARD") in result
    assert get_test_cards("D9|ANY_CARD") in result
    assert get_test_cards("H9|ANY_CARD") in result
    assert get_test_cards("C9|ANY_CARD") in result

    assert get_test_cards("S9|S8") in result
    assert get_test_cards("S9|H8") in result
    assert get_test_cards("S9|C8") in result
    assert get_test_cards("S9|D8") in result
    assert get_test_cards("D9|S8") in result
    assert get_test_cards("D9|H8") in result
    assert get_test_cards("D9|C8") in result
    assert get_test_cards("D9|D8") in result
    assert get_test_cards("H9|S8") in result
    assert get_test_cards("H9|H8") in result
    assert get_test_cards("H9|C8") in result
    assert get_test_cards("H9|D8") in result
    assert get_test_cards("C9|S8") in result
    assert get_test_cards("C9|H8") in result
    assert get_test_cards("C9|C8") in result
    assert get_test_cards("C9|D8") in result


def test_when_find_outs_trips_and_no_possible_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|CK|HJ|ST")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_trips(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_trips_and_already_have_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|DA|HJ|HA")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_trips(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 1

    assert get_test_cards("ANY_CARD") in result


def test_when_find_outs_trips_and_one_draw_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|DA|HJ|CJ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_trips(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 4

    assert get_test_cards("HA") in result
    assert get_test_cards("SA") in result
    assert get_test_cards("SJ") in result
    assert get_test_cards("DJ") in result


def test_when_find_outs_trips_and_two_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|DA|H7|CJ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_trips(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 11

    assert get_test_cards("HA|ANY_CARD") in result
    assert get_test_cards("SA|ANY_CARD") in result

    assert get_test_cards("SQ|HQ") in result
    assert get_test_cards("SQ|CQ") in result
    assert get_test_cards("HQ|CQ") in result

    assert get_test_cards("S7|D7") in result
    assert get_test_cards("S7|C7") in result
    assert get_test_cards("D7|C7") in result

    assert get_test_cards("SJ|HJ") in result
    assert get_test_cards("SJ|DJ") in result
    assert get_test_cards("HJ|DJ") in result


def test_when_find_outs_trips_and_five_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CQ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 5

    result = outs.find_outs_trips(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 50

    # not asserting all 50
    assert get_test_cards("SA|HA|ANY_CARD|ANY_CARD|ANY_CARD")
    assert get_test_cards("SA|DA|ANY_CARD|ANY_CARD|ANY_CARD")
    assert get_test_cards("HA|DA|ANY_CARD|ANY_CARD|ANY_CARD")

    assert get_test_cards("SQ|HQ|ANY_CARD|ANY_CARD|ANY_CARD")
    assert get_test_cards("SQ|DQ|ANY_CARD|ANY_CARD|ANY_CARD")
    assert get_test_cards("HQ|DQ|ANY_CARD|ANY_CARD|ANY_CARD")

    assert get_test_cards("SK|HK|DK|ANY_CARD|ANY_CARD")
    assert get_test_cards("SK|HK|CK|ANY_CARD|ANY_CARD")
    assert get_test_cards("SK|DK|CK|ANY_CARD|ANY_CARD")
    assert get_test_cards("HK|DK|CK|ANY_CARD|ANY_CARD")


def test_when_find_outs_two_pair_and_not_possible_then_return_empty_list(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|D2|H7|CJ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_two_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 0


def test_when_find_outs_two_pair_and_already_have_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DJ|DA|H7|C7")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_two_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 4

    assert get_test_cards("ANY_CARD") in result
    assert get_test_cards("SJ") in result
    assert get_test_cards("HJ") in result
    assert get_test_cards("CJ") in result


def test_when_find_outs_two_pair_and_one_draw_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DJ|D2|H7|C7")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_two_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 9

    assert get_test_cards("SA") in result
    assert get_test_cards("HA") in result
    assert get_test_cards("DA") in result
    assert get_test_cards("SJ") in result
    assert get_test_cards("HJ") in result
    assert get_test_cards("CJ") in result
    assert get_test_cards("S2") in result
    assert get_test_cards("H2") in result
    assert get_test_cards("C2") in result


def test_when_find_outs_two_pair_and_two_draw_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DJ|D2|H7|C7")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_two_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 90

    # not asserting all 90
    assert get_test_cards("SA|ANY_CARD") in result
    assert get_test_cards("HA|ANY_CARD") in result
    assert get_test_cards("DA|ANY_CARD") in result
    assert get_test_cards("SJ|ANY_CARD") in result
    assert get_test_cards("HJ|ANY_CARD") in result
    assert get_test_cards("CJ|ANY_CARD") in result
    assert get_test_cards("S2|ANY_CARD") in result
    assert get_test_cards("H2|ANY_CARD") in result
    assert get_test_cards("C2|ANY_CARD") in result

    assert get_test_cards("SA|SJ") in result
    assert get_test_cards("SA|HJ") in result
    assert get_test_cards("SA|CJ") in result
    assert get_test_cards("HA|SJ") in result
    assert get_test_cards("HA|HJ") in result
    assert get_test_cards("HA|CJ") in result
    assert get_test_cards("DA|SJ") in result
    assert get_test_cards("DA|HJ") in result
    assert get_test_cards("DA|CJ") in result

    assert get_test_cards("SQ|HQ") in result
    assert get_test_cards("SQ|DQ") in result
    assert get_test_cards("SQ|CQ") in result
    assert get_test_cards("HQ|DQ") in result
    assert get_test_cards("HQ|CQ") in result
    assert get_test_cards("DQ|CQ") in result


def test_when_find_outs_pair_and_already_have_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|DA|HJ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 1

    result = outs.find_outs_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 7

    assert get_test_cards("ANY_CARD") in result
    assert get_test_cards("SQ") in result
    assert get_test_cards("HQ") in result
    assert get_test_cards("CQ") in result
    assert get_test_cards("SJ") in result
    assert get_test_cards("DJ") in result
    assert get_test_cards("CJ") in result


def test_when_find_outs_pair_and_two_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|DQ|DA|H7|CJ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 2

    result = outs.find_outs_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 64

    # not asserting all 64
    assert get_test_cards("ANY_CARD|ANY_CARD") in result

    assert get_test_cards("SQ|ANY_CARD") in result
    assert get_test_cards("HQ|ANY_CARD") in result
    assert get_test_cards("CQ|ANY_CARD") in result

    assert get_test_cards("S8|H8") in result
    assert get_test_cards("S8|D8") in result
    assert get_test_cards("S8|C8") in result
    assert get_test_cards("H8|D8") in result
    assert get_test_cards("H8|C8") in result
    assert get_test_cards("D8|C8") in result


def test_when_find_outs_pair_and_five_draws_then_return_outs(get_test_cards, get_deck_minus_set):
    current_cards = get_test_cards("CA|CQ")
    available_cards = get_deck_minus_set(current_cards)
    remaining_draws = 5

    result = outs.find_outs_pair(current_cards, available_cards, remaining_draws)

    assert isinstance(result, list)
    assert len(result) == 72

    # not asserting all 50
    assert get_test_cards("SA|ANY_CARD|ANY_CARD|ANY_CARD|ANY_CARD")
    assert get_test_cards("HA|ANY_CARD|ANY_CARD|ANY_CARD|ANY_CARD")
    assert get_test_cards("DA|ANY_CARD|ANY_CARD|ANY_CARD|ANY_CARD")

    assert get_test_cards("S8|H8|ANY_CARD|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("S8|D8|ANY_CARD|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("S8|C8|ANY_CARD|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("H8|D8|ANY_CARD|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("H8|C8|ANY_CARD|ANY_CARD|ANY_CARD") in result
    assert get_test_cards("D8|C8|ANY_CARD|ANY_CARD|ANY_CARD") in result
