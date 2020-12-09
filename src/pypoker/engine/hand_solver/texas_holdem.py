from collections import Counter
from itertools import combinations, product, groupby
from typing import List, Dict

from pypoker.deck import Card, Deck
from pypoker.engine.hand_solver.base import BaseHandSolver
from pypoker.engine.hand_solver.constants import (
    HAND_TITLE,
    HAND_RANK,
    BEST_HAND,
    HAND_DESCRIPTION,
    OUTS_METHOD,
    OUTS_TB_METHOD,
    SUIT_HEARTS,
    SUIT_SPADES,
    SUIT_DIAMONDS,
    SUIT_CLUBS,
    TIEBREAKER,
    CARD_VALUES,
    OUT_STRING, HAND_TYPE_STRAIGHT_FLUSH, HAND_TYPE_QUADS, HAND_TYPE_FULL_HOUSE, HAND_TYPE_FLUSH, HAND_TYPE_STRAIGHT,
    HAND_TYPE_TRIPS, HAND_TYPE_TWO_PAIR, HAND_TYPE_PAIR, HAND_TYPE_HIGH_CARD, GAME_TYPE_TEXAS_HOLDEM,
)
from pypoker.engine.hand_solver.functions import hand_test, rank_hand_type, describe_hand
from pypoker.engine.hand_solver.utils import get_all_combinations


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
                HAND_TITLE: HAND_TYPE_STRAIGHT_FLUSH,
                HAND_RANK: 1,
                OUTS_METHOD: self._outs_straight_flush,
                OUTS_TB_METHOD: self._outs_tb_straight_flush,
            },
            {
                HAND_TITLE: HAND_TYPE_QUADS,
                HAND_RANK: 2,
                OUTS_METHOD: self._outs_quads,
                OUTS_TB_METHOD: self._outs_tb_quads,
            },
            {
                HAND_TITLE: HAND_TYPE_FULL_HOUSE,
                HAND_RANK: 3,
                OUTS_METHOD: self._outs_full_house,
                OUTS_TB_METHOD: self._outs_tb_full_house,
            },
            {
                HAND_TITLE: HAND_TYPE_FLUSH,
                HAND_RANK: 4,
                OUTS_METHOD: self._outs_flush,
                OUTS_TB_METHOD: self._outs_tb_flush,
            },
            {
                HAND_TITLE: HAND_TYPE_STRAIGHT,
                HAND_RANK: 5,
                OUTS_METHOD: self._outs_straight,
                OUTS_TB_METHOD: self._outs_tb_straight,
            },
            {
                HAND_TITLE: HAND_TYPE_TRIPS,
                HAND_RANK: 6,
                OUTS_METHOD: self._outs_trips,
                OUTS_TB_METHOD: self._outs_tb_trips,
            },
            {
                HAND_TITLE: HAND_TYPE_TWO_PAIR,
                HAND_RANK: 7,
                OUTS_METHOD: self._outs_two_pair,
                OUTS_TB_METHOD: self._outs_tb_two_pair,
            },
            {
                HAND_TITLE: HAND_TYPE_PAIR,
                HAND_RANK: 8,
                OUTS_METHOD: self._outs_pair,
                OUTS_TB_METHOD: self._outs_tb_pair,
            },
            {
                HAND_TITLE: HAND_TYPE_HIGH_CARD,
                HAND_RANK: 9,
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
        all_hands = get_all_combinations(hole_cards, board_cards, hand_size)
        for hand_ranking in self._hand_rankings:
            matched_hands = [hand for hand in all_hands if hand_test(GAME_TYPE_TEXAS_HOLDEM, hand_ranking[HAND_TITLE],
                                                                     hand=hand)]

            if matched_hands:
                best_hand = rank_hand_type(GAME_TYPE_TEXAS_HOLDEM, hand_ranking[HAND_TITLE], hands=matched_hands)[1][0]
                return {
                    BEST_HAND: best_hand,
                    HAND_TITLE: hand_ranking[HAND_TITLE],
                    HAND_RANK: hand_ranking[HAND_RANK],
                    HAND_DESCRIPTION: describe_hand(GAME_TYPE_TEXAS_HOLDEM, hand_ranking[HAND_TITLE], hand=best_hand)
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
            subranked_hands = rank_hand_type(GAME_TYPE_TEXAS_HOLDEM, self._hand_rankings[rank - 1][HAND_TITLE],
                                             hands=hands)
            subranked_players = self._link_subranked_hands_to_players(
                subranked_hands, players_hands
            )

            for players in subranked_players.values():
                current_rank += 1
                hand_desc = describe_hand(GAME_TYPE_TEXAS_HOLDEM,  self._hand_rankings[rank - 1][HAND_TITLE],
                                          hand=players_hands[players[0]])
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

    #############################
    #  OUTS TIEBREAKER METHODS  #
    ######################1#######

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

    #########################
    #  MISC HELPER METHODS  #
    #########################
    def _group_player_hands_by_rank(self, players_hands):
        """
        Helper method that will group player hands together by their hand ranks.

        :param players_hands: Dict in format of {PLAYER_NAME: [LIST_OF_CARDS]}
        :return: dictionary in format of {RANK: {PLAYER: [LIST_OF_CARDS]}}
        """

        player_hands_by_rank = dict()
        for player, hand in players_hands.items():
            for hand_type in self._hand_rankings:
                if hand_test(GAME_TYPE_TEXAS_HOLDEM, hand_type[HAND_TITLE], hand=hand):
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
