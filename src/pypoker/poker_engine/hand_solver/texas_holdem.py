from collections import Counter
from itertools import combinations, product, groupby
from typing import List, Dict

from pypoker.deck import Card, Deck
from pypoker.poker_engine.hand_solver.base import BaseHandSolver
from pypoker.poker_engine.hand_solver.constants import (
    HAND_TITLE,
    HAND_RANK,
    TEST_METHOD,
    BEST_HAND,
    HAND_DESCRIPTION,
    DESCRIPTION_METHOD,
    RANK_METHOD,
    OUTS_METHOD,
    OUTS_TB_METHOD,
    SUIT_HEARTS,
    SUIT_SPADES,
    SUIT_DIAMONDS,
    SUIT_CLUBS,
    TIEBREAKER,
    CARD_VALUES,
    OUT_STRING,
    PLAYING_BOARD,
)


class TexasHoldemHandSolver(BaseHandSolver):
    """
    The Texas Hold'em implementation of the BaseHandSolver class.
    Responsible for determining a players best hand and comparsions against each others hands

    The core of this class is the hand_ranking list which defines key attributes and methods for each texas holdem hand type:
        HAND_TITLE:         plain english hand title
        HAND_RANK:          numeric ranking of hand types against one another
        TEST_METHOD:        method pointer accepting a list of card objects.
                            Tests of the hand given to the method is this kind of hand.
        RANK_METHOD:        method pointer accepting a list of hands. ranks the hands of that type for tiebreaker purposes
        DESCRIPTION_METHOD: method pointer accepting a players hand of Card objects. Gives a plain english
                            description of the hand.
        OUTS_METHOD:        method pointer accepting the the players hole cards, the board cards and all available cards.
                            finds the out_strings for the player to make that type of hand with the draws and
                            available cards remaining
        OUTS_TB_METHOD:     method pointer accepting player outs_tb dict, player hole cards dict, board cards list,
                            drawn cards list.
                            finds out which player is assigned the win of a draw combination when the combo gives both
                            players this specific hand type.
    """

    def __init__(self):
        self._hand_rankings = [
            {
                HAND_TITLE: "Straight Flush",
                HAND_RANK: 1,
                TEST_METHOD: self._test_straight_flush,
                RANK_METHOD: self._rank_straight_flush,
                DESCRIPTION_METHOD: self._hand_description_straight_flush,
                OUTS_METHOD: self._outs_straight_flush,
                OUTS_TB_METHOD: self._outs_tb_straight_flush,
            },
            {
                HAND_TITLE: "Quads",
                HAND_RANK: 2,
                TEST_METHOD: self._test_quads,
                RANK_METHOD: self._rank_quads,
                DESCRIPTION_METHOD: self._hand_description_quads,
                OUTS_METHOD: self._outs_quads,
                OUTS_TB_METHOD: self._outs_tb_quads,
            },
            {
                HAND_TITLE: "Full House",
                HAND_RANK: 3,
                TEST_METHOD: self._test_full_house,
                RANK_METHOD: self._rank_full_house,
                DESCRIPTION_METHOD: self._hand_description_full_house,
                OUTS_METHOD: self._outs_full_house,
                OUTS_TB_METHOD: self._outs_tb_full_house,
            },
            {
                HAND_TITLE: "Flush",
                HAND_RANK: 4,
                TEST_METHOD: self._test_flush,
                RANK_METHOD: self._rank_flush,
                DESCRIPTION_METHOD: self._hand_description_flush,
                OUTS_METHOD: self._outs_flush,
                OUTS_TB_METHOD: self._outs_tb_flush,
            },
            {
                HAND_TITLE: "Straight",
                HAND_RANK: 5,
                TEST_METHOD: self._test_straight,
                RANK_METHOD: self._rank_straight,
                DESCRIPTION_METHOD: self._hand_description_straight,
                OUTS_METHOD: self._outs_straight,
                OUTS_TB_METHOD: self._outs_tb_straight,
            },
            {
                HAND_TITLE: "Trips",
                HAND_RANK: 6,
                TEST_METHOD: self._test_trips,
                RANK_METHOD: self._rank_trips,
                DESCRIPTION_METHOD: self._hand_description_trips,
                OUTS_METHOD: self._outs_trips,
                OUTS_TB_METHOD: self._outs_tb_trips,
            },
            {
                HAND_TITLE: "Two Pair",
                HAND_RANK: 7,
                TEST_METHOD: self._test_two_pair,
                RANK_METHOD: self._rank_two_pair,
                DESCRIPTION_METHOD: self._hand_description_two_pair,
                OUTS_METHOD: self._outs_two_pair,
                OUTS_TB_METHOD: self._outs_tb_two_pair,
            },
            {
                HAND_TITLE: "Pair",
                HAND_RANK: 8,
                TEST_METHOD: self._test_pair,
                RANK_METHOD: self._rank_pair,
                DESCRIPTION_METHOD: self._hand_description_pair,
                OUTS_METHOD: self._outs_pair,
                OUTS_TB_METHOD: self._outs_tb_pair,
            },
            {
                HAND_TITLE: "High Card",
                HAND_RANK: 9,
                TEST_METHOD: self._test_high_card,
                RANK_METHOD: self._rank_high_card,
                DESCRIPTION_METHOD: self._hand_description_high_card,
                OUTS_METHOD: self._outs_high_card,
                OUTS_TB_METHOD: self._outs_tb_high_card,
            },
        ]

    ########################
    #  PUBLIC API METHODS  #
    ########################

    def find_best_hand(self, hole_cards: List[Card], board_cards: List[Card]):
        """
        Abstract method to implement to find a players best hand.

        :param hole_cards: List of card objects, representing the players hole cards
        :param board_cards: List of card objects, representing the board cards available to use.
        :return: dictionary of player hand information. including at least the following keys:
        {
            "best_hand": List of card objects representing the players best hand
            "hand_title": Str the english title of the best hand type the player has (Straight, Flush, Two Pair, etc)
            "hand_rank": Int ranking of the hand type, with 1 signifying the best type of hand (e.g. straight flush
                         would have a ranking of 1 in texas holdem)
        }
        child classes implementing this abstract method can choose to expand the dictionary where
        appropriate but must at minimum have the above keys
        """

        hand_size = (
            5
            if len(hole_cards) + len(board_cards) >= 5
            else len(hole_cards) + len(board_cards)
        )
        all_hands = self.get_all_combinations(hole_cards, board_cards, hand_size)
        for hand_type in self._hand_rankings:
            matched_hands = [hand for hand in all_hands if hand_type[TEST_METHOD](hand)]

            if matched_hands:
                best_hand = hand_type[RANK_METHOD](matched_hands)[1][0]
                return {
                    BEST_HAND: best_hand,
                    HAND_TITLE: hand_type[HAND_TITLE],
                    HAND_RANK: hand_type[HAND_RANK],
                    HAND_DESCRIPTION: hand_type[DESCRIPTION_METHOD](best_hand),
                }

    def rank_hands(self, players_hands: Dict[str, List[Card]]):
        """
        Public method that will rank players texas hold'em hands against each other

        :param players_hands: Dict in format of
        {
            "PLAYER_NAME": [LIST_OF_CARDS]
        }

        :return: dict in the following format:
        {
            <RANK>: {
                "players": ["LIST OF PLAYER NAMES"],
                "hand_description": "HAND_DESCRIPTION"
            }
        }
        """

        player_hands_by_rank = self._group_player_hands_by_rank(players_hands)
        ranks = sorted(list(player_hands_by_rank.keys()))

        current_rank = 0
        ranked_player_hands = dict()

        for rank in ranks:
            hands = list(player_hands_by_rank[rank].values())
            subranked_hands = self._hand_rankings[rank - 1][RANK_METHOD](hands)
            subranked_players = self._link_subranked_hands_to_players(
                subranked_hands, players_hands
            )

            for players in subranked_players.values():
                current_rank += 1
                hand_desc = self._hand_rankings[rank - 1][DESCRIPTION_METHOD](
                    players_hands[players[0]]
                )
                ranked_player_hands[current_rank] = {
                    "players": players,
                    "hand_description": hand_desc,
                }

        return ranked_player_hands

    def find_odds(
        self, player_hole_cards: Dict[str, List[Card]], board_cards: List[Card]
    ):
        """
        Abstract method to implement to find the odds of all players winning from the current situation.

        :param player_hole_cards: Dictionary, of player names and their hole cards
        :param board_cards: List of cards representing the current board cards
        :return: Dictionary of player names and their likelyhood of winning from this situation.
        """

        drawable_cards = self._determine_unused_cards(player_hole_cards, board_cards)
        player_current_hand = {
            player: self.find_best_hand(hole_cards, board_cards)
            for player, hole_cards in player_hole_cards.items()
        }
        current_best_hand_rank = max(
            [best_hand[HAND_RANK] for best_hand in player_current_hand.values()]
        )

        ranked_player_outs = {}
        for hand_info in self._hand_rankings:
            for player, current_hand in player_current_hand.items():
                if (
                    current_hand[HAND_RANK]
                    >= hand_info[HAND_RANK]
                    <= current_best_hand_rank
                ):
                    player_outs = hand_info[OUTS_METHOD](
                        player_hole_cards[player], board_cards, drawable_cards
                    )
                    if hand_info[HAND_RANK] not in ranked_player_outs.keys():
                        ranked_player_outs[hand_info[HAND_RANK]] = {player: player_outs}
                    else:
                        ranked_player_outs[hand_info[HAND_RANK]][player] = player_outs

        utilised_outs = []
        wins = {player: 0 for player in player_hole_cards.keys()}
        wins["ties"] = 0

        for rank, player_out_scenarios in ranked_player_outs.items():
            print(f"Assigning wins for rank {rank} outs")
            players_with_outs = [
                player
                for player, out_scenarios in player_out_scenarios.items()
                if out_scenarios
            ]
            if not players_with_outs:
                print("No players with outs for this rank")
                continue
            elif len(players_with_outs) == 1:
                player_name = players_with_outs[0]
                print(
                    f"Only player {player_name} has outs for this rank.  Assigning wins"
                )
                potential_outs = [
                    scenario[OUT_STRING]
                    for scenario in player_out_scenarios[player_name]
                ]
                claimed_outs = self.claim_out_strings(
                    utilised_outs, potential_outs, drawable_cards
                )
                wins[player_name] += len(claimed_outs)
                utilised_outs.extend(claimed_outs)
            else:
                print(
                    f"Multiple players found to have outs at this rank: {players_with_outs}.  Tiebreaking outs."
                )
                combined_outs = {player: [] for player in players_with_outs}
                for player, out_scenarios in player_out_scenarios.items():
                    if not out_scenarios:
                        continue
                    for scenario in out_scenarios:
                        scenario["OUTS"] = self.claim_out_strings(
                            utilised_outs, [scenario[OUT_STRING]], drawable_cards
                        )
                        combined_outs[player].extend(scenario["OUTS"])

                for player, out_scenarios in player_out_scenarios.items():
                    if not out_scenarios:
                        continue
                    combined_outs[player].sort()
                    my_outs = list(combo for combo, _ in groupby(combined_outs[player]))
                    my_outs = [out for out in my_outs if out not in utilised_outs]
                    their_outs = [
                        outs
                        for player_name, outs in combined_outs.items()
                        if player_name != player
                    ]
                    their_outs = [item for sublist in their_outs for item in sublist]
                    their_outs.sort()
                    their_outs = list(combo for combo, _ in groupby(their_outs))
                    their_outs = [out for out in their_outs if out not in utilised_outs]

                    unique_outs = [out for out in my_outs if out not in their_outs]
                    conflicted_outs = [out for out in my_outs if out not in unique_outs]

                    wins[player] += len(unique_outs)
                    utilised_outs.extend(unique_outs)

                    for out_ids in conflicted_outs:
                        valid_players = [
                            player_name
                            for player_name, outs in combined_outs.items()
                            if out_ids in outs
                        ]

                        tiebreakers = {}
                        hole_cards = {}
                        for player in valid_players:
                            tiebreakers[player] = [
                                scenario[TIEBREAKER]
                                for scenario in player_out_scenarios[player]
                                if out_ids in scenario["OUTS"]
                            ][0]
                            hole_cards[player] = player_hole_cards[player]

                        drawn_cards = [Card(card_id) for card_id in out_ids]
                        winner = self._hand_rankings[rank - 1][OUTS_TB_METHOD](
                            tiebreakers, hole_cards, board_cards, drawn_cards
                        )
                        if winner not in wins.keys():
                            wins[winner] = 1
                        else:
                            wins[winner] += 1
                        utilised_outs.append(out_ids)

        draw_combo_num = 1
        cards_to_draw = 5 - len(board_cards)
        for draw in range(cards_to_draw):
            cards_available = len(drawable_cards) - draw
            draw_combo_num *= cards_available
        draw_combo_num /= cards_to_draw

        odds = {
            player: win_count / draw_combo_num for player, win_count in wins.items()
        }
        return odds

    #######################
    #  TEST HAND METHODS  #
    #######################

    def _test_straight_flush(self, hand: List[Card]):
        """
        Private method to test if a hand is a straight flush hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return (
            len(hand) == 5
            and self.hand_all_same_suit(hand)
            and self.hand_values_continuous(hand)
        )

    def _test_quads(self, hand: List[Card]):
        """
        Private method to test if a hand is a quads hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return bool(self.hand_highest_value_tuple(hand, 4))

    def _test_full_house(self, hand: List[Card]):
        """
        Private method to test if a hand is a quads hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        trips_value = self.hand_highest_value_tuple(hand, 3)
        remaining_cards = filter(lambda card: card.value != trips_value, hand)
        pair_value = self.hand_highest_value_tuple(remaining_cards, 2)

        return bool(trips_value and pair_value)

    def _test_flush(self, hand: List[Card]):
        """
        Private method to test if a hand is a flush hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return len(hand) == 5 and self.hand_all_same_suit(hand)

    def _test_straight(self, hand: List[Card]):
        """
        Private method to test if a hand is a straight hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return len(hand) == 5 and self.hand_values_continuous(hand)

    def _test_trips(self, hand: List[Card]):
        """
        Private method to test if a hand is a trips hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return bool(self.hand_highest_value_tuple(hand, 3))

    def _test_two_pair(self, hand: List[Card]):
        """
        Private method to test if a hand is a two pair hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        high_pair_value = self.hand_highest_value_tuple(hand, 2)
        remaining_cards = list(filter(lambda card: card.value != high_pair_value, hand))
        low_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)

        return bool(high_pair_value and low_pair_value)

    def _test_pair(self, hand: List[Card]):
        """
        Private method to test if a hand is a two pair hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return bool(self.hand_highest_value_tuple(hand, 2))

    @staticmethod
    def _test_high_card(hand: List[Card]):
        """
        Private method to test if a hand is a two pair hand

        :param hand: List of Card objects representing a players hand
        :return: Boolean indicating if the hand is a straight flush
        """

        return True

    #######################
    #  RANK HAND METHODS  #
    #######################

    def _rank_straight_flush(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best straight flush hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a straight flush hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ordered_hands = self._reorder_ace_low_straight_hands(ordered_hands)

        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_quads(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best quads hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a quads hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_quads = [(hand, self.hand_highest_value_tuple(hand, 4)) for hand in hands]
        quad_values = list(set([tup[1] for tup in hands_quads]))
        quad_values.sort(reverse=True)

        ranked_hands = dict()

        for quad_value in quad_values:
            quad_value_hands = filter(
                lambda hand_tuple: hand_tuple[1] == quad_value, hands_quads
            )
            quad_value_hands = self.order_hands_highest_card(
                [tup[0] for tup in quad_value_hands]
            )

            current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
            ranked_hands[current_rank] = [quad_value_hands[0]]

            for hand in quad_value_hands[1:]:
                if self.hands_have_same_card_values(
                    hand, ranked_hands[current_rank][0]
                ):
                    ranked_hands[current_rank].append(hand)
                else:
                    current_rank += 1
                    ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_full_house(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best full house hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a full house hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = []

        for hand in hands:
            trips_value = self.hand_highest_value_tuple(hand, 3)
            remaining_cards = filter(lambda card: card.value != trips_value, hand)
            pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
            ordered_hands.append((hand, trips_value, pair_value))

        ordered_hands.sort(key=lambda tup: (tup[1], tup[2]), reverse=True)

        current_rank = 1
        ranked_hands = {current_rank: [ordered_hands[0][0]]}
        current_trip = ordered_hands[0][1]
        current_pair = ordered_hands[0][2]

        for hand, trip, pair in ordered_hands[1:]:
            if current_trip == trip and current_pair == pair:
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                current_trip = trip
                current_pair = pair
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_flush(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best flush hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a flush hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_straight(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best straight hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a straight hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ordered_hands = self._reorder_ace_low_straight_hands(ordered_hands)
        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_trips(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best trips hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a trips hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_trips = [(hand, self.hand_highest_value_tuple(hand, 3)) for hand in hands]
        trips_values = list(set([tup[1] for tup in hands_trips]))
        trips_values.sort(reverse=True)

        ranked_hands = dict()

        for trips_value in trips_values:
            trips_value_hands = filter(
                lambda hand_tuple: hand_tuple[1] == trips_value, hands_trips
            )
            trips_value_hands = self.order_hands_highest_card(
                [tup[0] for tup in trips_value_hands]
            )

            current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
            ranked_hands[current_rank] = [trips_value_hands[0]]

            for hand in trips_value_hands[1:]:
                if self.hands_have_same_card_values(
                    hand, ranked_hands[current_rank][0]
                ):
                    ranked_hands[current_rank].append(hand)
                else:
                    current_rank += 1
                    ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_two_pair(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best two pair hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a two pair hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_two_pair_kicker = []

        for hand in hands:
            high_pair_value = self.hand_highest_value_tuple(hand, 2)
            remaining_cards = filter(lambda card: card.value != high_pair_value, hand)
            low_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
            kicker_value = list(
                filter(
                    lambda card: card.value != high_pair_value
                    and card.value != low_pair_value,
                    hand,
                )
            )[0].value
            hands_two_pair_kicker.append(
                (hand, high_pair_value, low_pair_value, kicker_value)
            )

        hands_two_pair_kicker.sort(
            key=lambda tup: (tup[1], tup[2], tup[3]), reverse=True
        )

        current_rank = 1
        current_high_pair = hands_two_pair_kicker[0][1]
        current_low_pair = hands_two_pair_kicker[0][2]
        current_kicker = hands_two_pair_kicker[0][3]
        ranked_hands = {current_rank: [hands_two_pair_kicker[0][0]]}

        for hand, high_pair, low_pair, kicker in hands_two_pair_kicker[1:]:
            if (
                high_pair == current_high_pair
                and low_pair == current_low_pair
                and kicker == current_kicker
            ):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                current_high_pair = high_pair
                current_low_pair = low_pair
                current_kicker = kicker
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_pair(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best pair hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a pair hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        hands_pair = [(hand, self.hand_highest_value_tuple(hand, 2)) for hand in hands]
        pair_values = list(set([tup[1] for tup in hands_pair]))
        pair_values.sort(reverse=True)

        ranked_hands = dict()

        for pair_value in pair_values:
            pair_value_hands = filter(
                lambda hand_tuple: hand_tuple[1] == pair_value, hands_pair
            )
            pair_value_hands = self.order_hands_highest_card(
                [tup[0] for tup in pair_value_hands]
            )

            current_rank = 1 if not ranked_hands else max(ranked_hands.keys()) + 1
            ranked_hands[current_rank] = [pair_value_hands[0]]

            for hand in pair_value_hands[1:]:
                if self.hands_have_same_card_values(
                    hand, ranked_hands[current_rank][0]
                ):
                    ranked_hands[current_rank].append(hand)
                else:
                    current_rank += 1
                    ranked_hands[current_rank] = [hand]

        return ranked_hands

    def _rank_high_card(self, hands: List[List[Card]]):
        """
        Private tiebreaker method to determine the best high card hand in the list of hands

        :param hands: List of list of cards. each internal list of cards represents a high card hand
        :return: Dictionary in the following format of KEY = Rank number (1,2,3,4...) VALUE = List of hands for that rank
            If there are tied hands, then multiple hands will appear as the value for that rank.
        """

        ordered_hands = self.order_hands_highest_card(hands)
        ranked_hands = {1: [ordered_hands[0]]}

        for hand in ordered_hands[1:]:
            current_rank = max(ranked_hands.keys())

            if self.hands_have_same_card_values(hand, ranked_hands[current_rank][0]):
                ranked_hands[current_rank].append(hand)
            else:
                current_rank += 1
                ranked_hands[current_rank] = [hand]

        return ranked_hands

    #########################
    #  OUTS FINDER METHODS  #
    #########################

    def _outs_straight_flush(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards
        suit_drawn = {
            SUIT_HEARTS: sum([1 for card in drawn_cards if card.suit == SUIT_HEARTS]),
            SUIT_CLUBS: sum([1 for card in drawn_cards if card.suit == SUIT_CLUBS]),
            SUIT_DIAMONDS: sum(
                [1 for card in drawn_cards if card.suit == SUIT_DIAMONDS]
            ),
            SUIT_SPADES: sum([1 for card in drawn_cards if card.suit == SUIT_SPADES]),
        }
        suit_remaining = {
            SUIT_HEARTS: sum(
                [1 for card in available_cards if card.suit == SUIT_HEARTS]
            ),
            SUIT_CLUBS: sum([1 for card in available_cards if card.suit == SUIT_CLUBS]),
            SUIT_DIAMONDS: sum(
                [1 for card in available_cards if card.suit == SUIT_DIAMONDS]
            ),
            SUIT_SPADES: sum(
                [1 for card in available_cards if card.suit == SUIT_SPADES]
            ),
        }

        suit_eligable = [
            suit
            for suit, count in suit_drawn.items()
            if count + draws >= 5 and suit_remaining[suit] >= (5 - count)
        ]

        for suit in suit_eligable:
            drawn_suit_cards = [card for card in drawn_cards if card.suit == suit]
            available_suit_cards = [
                card for card in available_cards if card.suit == suit
            ]

            drawn_suit_cards = sorted(
                drawn_suit_cards, key=lambda card: card.value, reverse=True
            )
            available_suit_cards = sorted(
                available_suit_cards, key=lambda card: card.value, reverse=True
            )

            for draws_used in range(1, draws + 1):
                for hypothetical_draw_cards in self.get_all_combinations(
                    available_suit_cards, [], draws_used
                ):
                    usable_cards = drawn_suit_cards + hypothetical_draw_cards
                    usable_card_vals = [card.value for card in usable_cards]
                    usable_card_vals.sort()

                    gaps = [
                        [s, e]
                        for s, e in zip(usable_card_vals, usable_card_vals[1:])
                        if s + 1 < e
                    ]
                    edges = iter(
                        usable_card_vals[:1] + sum(gaps, []) + usable_card_vals[-1:]
                    )
                    runs = list(zip(edges, edges))

                    qualifying_straights = [
                        run
                        for run in runs
                        if run[1] - run[0] >= 4
                        and all(
                            (run[1] - 4) <= card.value <= run[1]
                            for card in hypothetical_draw_cards
                        )
                    ]

                    for straight_vals in qualifying_straights:
                        suits = []
                        values = []
                        for card in hypothetical_draw_cards:
                            suits.append(card.suit)
                            values.append(card.value)
                        draw_scenarios.append(
                            {
                                OUT_STRING: self.build_out_string(suits, values, draws),
                                TIEBREAKER: straight_vals[1],
                            }
                        )

        return draw_scenarios

    def _outs_quads(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards

        drawn_value_counter = Counter([card.value for card in drawn_cards])
        available_values_counter = Counter([card.value for card in available_cards])
        value_eligable = [
            value
            for value, count in drawn_value_counter.items()
            if count + draws >= 4 and available_values_counter[value] + value >= 4
        ]

        for value in value_eligable:
            cards_needed = 4 - drawn_value_counter[value]
            suits = ["ANY" for _ in range(cards_needed)]
            values = [value for _ in range(cards_needed)]

            draw_scenarios.append(
                {
                    OUT_STRING: self.build_out_string(suits, values, draws),
                    TIEBREAKER: value,
                }
            )

        return draw_scenarios

    def _outs_full_house(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards

        drawn_value_counter = Counter([card.value for card in drawn_cards])
        available_values_counter = Counter([card.value for card in available_cards])

        trips_eligable = [
            (value, drawn_value_counter[value])
            for value in CARD_VALUES
            if drawn_value_counter[value] + draws >= 3
            and available_values_counter[value] + drawn_value_counter[value] >= 3
        ]

        pair_eligable = [
            (value, drawn_value_counter[value])
            for value in CARD_VALUES
            if drawn_value_counter[value] + draws >= 2
            and available_values_counter[value] + drawn_value_counter[value] >= 2
        ]

        for trip_info, pair_info in product(trips_eligable, pair_eligable):
            # check we havent selected the same value for both trips and pairs
            if trip_info[0] == pair_info[0]:
                continue

            trip_draws_required = max([3 - trip_info[1], 0])
            pair_draws_required = max([2 - pair_info[1], 0])

            if trip_draws_required + pair_draws_required > draws:
                continue

            suits = ["ANY" for _ in range(trip_draws_required + pair_draws_required)]
            values = [trip_info[0] for _ in range(trip_draws_required)]
            values.extend([pair_info[0] for _ in range(pair_draws_required)])

            draw_scenarios.append(
                {
                    OUT_STRING: self.build_out_string(suits, values, draws),
                    TIEBREAKER: (trip_info[0], pair_info[0]),
                }
            )
        return draw_scenarios

    def _outs_flush(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards
        suit_drawn = {
            SUIT_HEARTS: sum([1 for card in drawn_cards if card.suit == SUIT_HEARTS]),
            SUIT_CLUBS: sum([1 for card in drawn_cards if card.suit == SUIT_CLUBS]),
            SUIT_DIAMONDS: sum(
                [1 for card in drawn_cards if card.suit == SUIT_DIAMONDS]
            ),
            SUIT_SPADES: sum([1 for card in drawn_cards if card.suit == SUIT_SPADES]),
        }
        suit_remaining = {
            SUIT_HEARTS: sum(
                [1 for card in available_cards if card.suit == SUIT_HEARTS]
            ),
            SUIT_CLUBS: sum([1 for card in available_cards if card.suit == SUIT_CLUBS]),
            SUIT_DIAMONDS: sum(
                [1 for card in available_cards if card.suit == SUIT_DIAMONDS]
            ),
            SUIT_SPADES: sum(
                [1 for card in available_cards if card.suit == SUIT_SPADES]
            ),
        }

        suit_eligable = [
            suit
            for suit, count in suit_drawn.items()
            if count + draws >= 5 and suit_remaining[suit] >= (5 - count)
        ]

        for suit in suit_eligable:
            draws_required = max([5 - suit_drawn[suit], 0])
            suits = [suit for _ in range(draws_required)]
            values = ["ANY" for _ in range(draws_required)]

            draw_scenarios.append(
                {
                    OUT_STRING: self.build_out_string(suits, values, draws),
                    TIEBREAKER: suit,
                }
            )

        return draw_scenarios

    def _outs_straight(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards

        drawn_values = sorted(
            list(set([card.value for card in drawn_cards])), reverse=True
        )
        available_values = sorted(
            list(set([card.value for card in available_cards])), reverse=True
        )
        not_drawn_values = [
            value for value in available_values if value not in drawn_values
        ]

        for draws_used in range(1, draws + 1):
            for possible_draw in combinations(not_drawn_values, draws_used):
                combined_values = sorted(drawn_values + list(possible_draw))

                gaps = [
                    [s, e]
                    for s, e in zip(combined_values, combined_values[1:])
                    if s + 1 < e
                ]
                edges = iter(combined_values[:1] + sum(gaps, []) + combined_values[-1:])
                runs = list(zip(edges, edges))

                qualifying_straights = [
                    run
                    for run in runs
                    if run[1] - run[0] >= 4
                    and all((run[1] - 4) <= value <= run[1] for value in possible_draw)
                ]

                for straight_vals in qualifying_straights:
                    suits = ["ANY" for _ in possible_draw]
                    values = [value for value in possible_draw]
                    draw_scenarios.append(
                        {
                            OUT_STRING: self.build_out_string(suits, values, draws),
                            TIEBREAKER: straight_vals[1],
                        }
                    )
        return draw_scenarios

    def _outs_trips(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards

        drawn_value_counter = Counter([card.value for card in drawn_cards])
        available_values_counter = Counter([card.value for card in available_cards])

        trips_eligable = [
            (value, drawn_value_counter[value])
            for value in CARD_VALUES
            if drawn_value_counter[value] + draws >= 3
            and available_values_counter[value] + drawn_value_counter[value] >= 3
        ]

        for value, count in trips_eligable:
            draws_required = max([3 - count, 0])
            suits = ["ANY" for _ in range(draws_required)]
            values = [value for _ in range(draws_required)]

            draw_scenarios.append(
                {
                    OUT_STRING: self.build_out_string(suits, values, draws),
                    TIEBREAKER: value,
                }
            )

        return draw_scenarios

    def _outs_two_pair(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards

        drawn_value_counter = Counter([card.value for card in drawn_cards])
        available_values_counter = Counter([card.value for card in available_cards])

        pair_eligable = [
            (value, drawn_value_counter[value])
            for value in CARD_VALUES
            if drawn_value_counter[value] + draws >= 2
            and available_values_counter[value] + drawn_value_counter[value] >= 2
        ]

        for pair_a, pair_b in combinations(pair_eligable, 2):
            high_pair = pair_a if pair_a[0] > pair_b[0] else pair_b
            low_pair = pair_a if pair_a[0] < pair_b[0] else pair_b

            high_pair_draws_req = max([2 - high_pair[1], 0])
            low_pair_draws_req = max([2 - low_pair[1], 0])
            if high_pair_draws_req + low_pair_draws_req <= draws:
                suits = ["ANY" for _ in range(high_pair_draws_req + low_pair_draws_req)]
                values = [high_pair[0] for _ in range(high_pair_draws_req)]
                values.extend([low_pair[0] for _ in range(low_pair_draws_req)])
                draw_scenarios.append(
                    {
                        OUT_STRING: self.build_out_string(suits, values, draws),
                        TIEBREAKER: (high_pair[0], low_pair[0]),
                    }
                )

        return draw_scenarios

    def _outs_pair(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        draw_scenarios = []
        draws = 5 - len(board_cards)
        drawn_cards = hole_cards + board_cards

        drawn_value_counter = Counter([card.value for card in drawn_cards])
        available_values_counter = Counter([card.value for card in available_cards])

        pair_eligable = [
            (value, drawn_value_counter[value])
            for value in CARD_VALUES
            if drawn_value_counter[value] + draws >= 2
            and available_values_counter[value] + drawn_value_counter[value] >= 2
        ]

        for pair in pair_eligable:
            draws_req = max([2 - pair[1], 0])
            suits = ["ANY" for _ in range(draws_req)]
            values = [pair[0] for _ in range(draws_req)]
            draw_scenarios.append(
                {
                    OUT_STRING: self.build_out_string(suits, values, draws),
                    TIEBREAKER: pair[0],
                }
            )

        return draw_scenarios

    def _outs_high_card(self, hole_cards, board_cards, available_cards):
        """
        Private method to find all of the possible draw scenarios to get the player this specific draw type.
        :param hole_cards: List of card objects representing the players hole cards
        :param board_cards: List of card objects representing the cards that have been dealt to the board.
        :param available_cards: List of card objects representing the cards that can be drawn.
        """

        return []

    #############################
    #  OUTS TIEBREAKER METHODS  #
    #############################

    @staticmethod
    def _outs_tb_straight_flush(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger straight flush hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
        winners = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker == max_tiebreaker
        ]
        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_quads(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger quads hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
        possible_winners = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker == max_tiebreaker
        ]

        if len(possible_winners) == 1:
            return possible_winners[0]

        player_kickers = {}
        for player in possible_winners:
            player_values = [card.value for card in hole_cards[player]]
            player_values.extend([card.value for card in board_cards])
            player_values.extend([card.value for card in drawn_cards])
            player_values = [
                value for value in player_values if value != max_tiebreaker
            ]

            player_kickers[player] = max(player_values)

        max_kicker = max([kicker for kicker in player_kickers.values()])
        winners = [
            player for player, kicker in player_kickers.items() if kicker == max_kicker
        ]
        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_full_house(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger full house hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_trips = max([tiebreaker[0] for tiebreaker in tiebreakers.values()])
        max_trips_players = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker[0] == max_trips
        ]

        if len(max_trips_players) == 1:
            return max_trips_players[0]

        max_pair = max(
            [
                tiebreaker[1]
                for player, tiebreaker in tiebreakers.items()
                if player in max_trips_players
            ]
        )
        max_pair_players = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker[1] == max_pair and player in max_trips_players
        ]

        return (
            max_pair_players[0]
            if len(max_pair_players) == 1
            else f"TIE({','.join(max_pair_players)})"
        )

    @staticmethod
    def _outs_tb_flush(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger flush hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        player_flush_values = {}
        for player, cards in hole_cards.items():
            flush_values = [
                card.value for card in cards if card.suit == tiebreakers[player]
            ]
            flush_values.extend(
                [card.value for card in board_cards if card.suit == tiebreakers[player]]
            )
            flush_values.extend(
                [card.value for card in drawn_cards if card.suit == tiebreakers[player]]
            )

            player_flush_values[player] = sorted(flush_values, reverse=True)

        winners = [player for player in hole_cards.keys()]

        for index in range(5):
            max_index_value = max(
                [
                    values[index]
                    for player, values in player_flush_values.items()
                    if player in winners
                ]
            )

            winners = [
                player
                for player in winners
                if player_flush_values[player][index] == max_index_value
            ]

        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_straight(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger straight hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
        winners = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker == max_tiebreaker
        ]
        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_trips(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger trips hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
        possible_winners = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker == max_tiebreaker
        ]

        if len(possible_winners) == 1:
            return possible_winners[0]

        player_kickers = {}
        for player in possible_winners:
            player_values = [card.value for card in hole_cards[player]]
            player_values.extend([card.value for card in board_cards])
            player_values.extend([card.value for card in drawn_cards])
            player_values = [
                value for value in player_values if value != max_tiebreaker
            ]

            player_kickers[player] = sorted(player_values, reverse=True)

        winners = [player for player in possible_winners]
        for index in range(2):
            max_index_value = max(
                [
                    values[index]
                    for player, values in player_kickers.items()
                    if player in winners
                ]
            )

            winners = [
                player
                for player in winners
                if player_kickers[player][index] == max_index_value
            ]

        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_two_pair(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger two pair hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_high_pair = max([tiebreaker[0] for tiebreaker in tiebreakers.values()])
        max_high_pair_players = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker[0] == max_high_pair
        ]

        if len(max_high_pair_players) == 1:
            return max_high_pair_players[0]

        max_low_pair = max(
            [
                tiebreaker[1]
                for player, tiebreaker in tiebreakers.items()
                if player in max_high_pair_players
            ]
        )
        max_low_pair_players = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker[1] == max_low_pair and player in max_high_pair_players
        ]

        if len(max_low_pair_players) == 1:
            return max_low_pair_players[0]

        player_kickers = {}
        for player in max_low_pair_players:
            player_values = [card.value for card in hole_cards[player]]
            player_values.extend([card.value for card in board_cards])
            player_values.extend([card.value for card in drawn_cards])
            player_values = [
                value
                for value in player_values
                if value not in [max_high_pair, max_low_pair]
            ]

            player_kickers[player] = max(player_values)

        max_kicker = max([kicker for kicker in player_kickers.values()])
        winners = [
            player for player, kicker in player_kickers.items() if kicker == max_kicker
        ]
        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_pair(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger pair hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        max_tiebreaker = max([tiebreaker for tiebreaker in tiebreakers.values()])
        possible_winners = [
            player
            for player, tiebreaker in tiebreakers.items()
            if tiebreaker == max_tiebreaker
        ]

        if len(possible_winners) == 1:
            return possible_winners[0]

        player_kickers = {}
        for player in possible_winners:
            player_values = [card.value for card in hole_cards[player]]
            player_values.extend([card.value for card in board_cards])
            player_values.extend([card.value for card in drawn_cards])
            player_values = [
                value for value in player_values if value != max_tiebreaker
            ]

            player_kickers[player] = sorted(player_values, reverse=True)

        winners = [player for player in possible_winners]
        for index in range(3):
            max_index_value = max(
                [
                    values[index]
                    for player, values in player_kickers.items()
                    if player in winners
                ]
            )

            winners = [
                player
                for player in winners
                if player_kickers[player][index] == max_index_value
            ]

        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    @staticmethod
    def _outs_tb_high_card(
        tiebreakers: Dict,
        hole_cards: Dict[str, List[Card]],
        board_cards: List[Card],
        drawn_cards: List[Card],
    ) -> str:
        """
        Private method to determine which player would have the stronger high card hand. given the drawn cards.

        :param tiebreakers: dictionary of each players tiebreak information for this draw.
        :param hole_cards: dictionary of each players hole cards
        :param board_cards: List of the board cards that have been dealt
        :param drawn_cards: List of cards that would be drawn in this scenario

        :return: Name of the winning player. if a tie occurs, then return a TIE(<PLAYER_NAMES>) where PLAYER_NAMES is
                 a comma-separated list of the players who have tied
        """

        player_kickers = {}
        for player in hole_cards.keys():
            player_values = [card.value for card in hole_cards[player]]
            player_values.extend([card.value for card in board_cards])
            player_values.extend([card.value for card in drawn_cards])

            player_kickers[player] = sorted(player_values, reverse=True)

        winners = [player for player in tiebreakers.keys()]
        for index in range(5):
            max_index_value = max(
                [
                    values[index]
                    for player, values in player_kickers.items()
                    if player in winners
                ]
            )

            winners = [
                player
                for player in winners
                if player_kickers[player][index] == max_index_value
            ]

        return winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"

    ##############################
    #  HAND DESCRIPTION METHODS  #
    ##############################

    def _hand_description_straight_flush(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a straight flush hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        if self.hand_is_ace_low_straight(hand):
            return f"Straight Flush ({hand[1].rank} to {hand[0].rank})"
        else:
            return f"Straight Flush ({hand[0].rank} to {hand[4].rank})"

    def _hand_description_quads(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a quads hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        quads_value = self.hand_highest_value_tuple(hand, 4)
        quads_rank = list(filter(lambda card: card.value == quads_value, hand))[0].rank
        kicker_rank = list(filter(lambda card: card.value != quads_value, hand))[0].rank
        return f"Quads ({quads_rank}s with {kicker_rank} kicker)"

    def _hand_description_full_house(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a full house hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        trips_value = self.hand_highest_value_tuple(hand, 3)
        trips_rank = list(filter(lambda card: card.value == trips_value, hand))[0].rank
        remaining_cards = filter(lambda card: card.value != trips_value, hand)
        pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
        pair_rank = list(filter(lambda card: card.value == pair_value, hand))[0].rank
        return f"Full House ({trips_rank}s full of {pair_rank}s)"

    @staticmethod
    def _hand_description_flush(hand: List[Card]):
        """
        Private method that produces the proper hand description for flush hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        return f"Flush ({hand[0].rank}, {hand[1].rank}, {hand[2].rank}, {hand[3].rank}, {hand[4].rank})"

    def _hand_description_straight(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for straight hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        if self.hand_is_ace_low_straight(hand):
            return f"Straight ({hand[1].rank} to {hand[0].rank})"
        else:
            return f"Straight ({hand[0].rank} to {hand[4].rank})"

    def _hand_description_trips(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a quads hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        trips_value = self.hand_highest_value_tuple(hand, 3)
        trips_rank = list(filter(lambda card: card.value == trips_value, hand))[0].rank
        kickers = list(filter(lambda card: card.value != trips_value, hand))
        kickers.sort(key=lambda card: card.value, reverse=True)
        return (
            f"Trips ({trips_rank}s with kickers {kickers[0].rank}, {kickers[1].rank})"
        )

    def _hand_description_two_pair(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a two pair hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        higher_pair_value = self.hand_highest_value_tuple(hand, 2)
        higher_pair_rank = list(
            filter(lambda card: card.value == higher_pair_value, hand)
        )[0].rank

        remaining_cards = list(
            filter(lambda card: card.value != higher_pair_value, hand)
        )
        lower_pair_value = self.hand_highest_value_tuple(remaining_cards, 2)
        lower_pair_rank = list(
            filter(lambda card: card.value == lower_pair_value, remaining_cards)
        )[0].rank

        kicker_rank = list(
            filter(lambda card: card.value != lower_pair_value, remaining_cards)
        )[0].rank

        return f"Two Pair ({higher_pair_rank}s and {lower_pair_rank}s with kicker {kicker_rank})"

    def _hand_description_pair(self, hand: List[Card]):
        """
        Private method that produces the proper hand description for a pair hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        pair_value = self.hand_highest_value_tuple(hand, 2)
        pair_rank = list(filter(lambda card: card.value == pair_value, hand))[0].rank

        kickers = list(filter(lambda card: card.value != pair_value, hand))
        kickers.sort(key=lambda card: card.value, reverse=True)
        kickers = [kicker.rank for kicker in kickers]

        if kickers:
            return f"Pair ({pair_rank}s with kickers {', '.join(kickers)})"
        else:
            return f"Pair ({pair_rank}s)"

    @staticmethod
    def _hand_description_high_card(hand: List[Card]):
        """
        Private method that produces the proper hand description for a high card hand.

        :param hand: List of Card objects representing a players hand
        :return: String of the hand description
        """

        hand.sort(key=lambda card: card.value, reverse=True)
        ranks = [card.rank for card in hand]

        return f"High Card ({', '.join(ranks)})"

    #########################
    #  MISC HELPER METHODS  #
    #########################

    def _reorder_ace_low_straight_hands(self, ordered_hands):
        """
        Private helper method to reorder ace low straight hands to end of ordered hands list
        :param ordered_hands:
        :return:
        """

        ace_low_straight_hands = [
            True if self.hand_is_ace_low_straight(hand) else False
            for hand in ordered_hands
        ]
        ace_low_straight_index_hand = [
            (index, ordered_hands[index])
            for index, is_ace_low_straight in enumerate(ace_low_straight_hands)
            if is_ace_low_straight
        ]
        ace_low_straight_index_hand.sort(key=lambda tup: tup[0], reverse=True)

        for index, hand in ace_low_straight_index_hand:
            del ordered_hands[index]
            ordered_hands.append(hand)

        return ordered_hands

    def _group_player_hands_by_rank(self, players_hands):
        """
        Helper method that will group player hands together by their hand ranks.

        :param players_hands: Dict in format of {PLAYER_NAME: [LIST_OF_CARDS]}
        :return: dictionary in format of {RANK: {PLAYER: [LIST_OF_CARDS]}}
        """

        player_hands_by_rank = dict()
        for player, hand in players_hands.items():
            for hand_type in self._hand_rankings:
                if hand_type[TEST_METHOD](hand):
                    if hand_type[HAND_RANK] not in player_hands_by_rank.keys():
                        player_hands_by_rank[hand_type[HAND_RANK]] = {player: hand}
                    else:
                        player_hands_by_rank[hand_type[HAND_RANK]][player] = hand
                    break
        return player_hands_by_rank

    @staticmethod
    def _link_subranked_hands_to_players(subranked_hands, players_hands):
        """
        Helper method to link player names (found in players_hands dict) back to their hand within the subranked_hands
        dict

        :param subranked_hands: Dict in form of {SUBRANK: [LIST_OF_HANDS]}
        :param players_hands: Dict in format of {PLAYER: [LIST_OF_CARDS]}
        :return:
        """
        for hand in players_hands.values():
            hand.sort(key=lambda card: card.value, reverse=True)

        linked_subrank_players = dict()
        for subrank, subrank_hands in subranked_hands.items():
            for hand in subrank_hands:
                hand.sort(key=lambda card: card.value, reverse=True)

            matched_players = [
                player
                for player, player_hand in players_hands.items()
                if player_hand in subrank_hands
            ]
            linked_subrank_players[subrank] = matched_players

        return linked_subrank_players

    @staticmethod
    def _determine_unused_cards(player_cards, board_cards):
        """
        private helper method that finds all of the possible remaining cards based on the hole and boaard cards
        that are known.

        :param player_cards: Dictionary, of player names and their hole cards
        :param board_cards: List of cards representing the current board cards
        :return:
        """

        used_cards = board_cards.copy()
        for cards in player_cards.values():
            used_cards.extend(cards)

        return [card for card in Deck().cards_all if card not in used_cards]
