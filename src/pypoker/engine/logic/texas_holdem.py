from itertools import groupby
from typing import List, Dict

from pypoker.deck import Card, Deck
from pypoker.engine.logic.base import BaseHandSolver
from pypoker.engine.logic.constants import (
    HAND_TITLE,
    HAND_RANK,
    BEST_HAND,
    HAND_DESCRIPTION,
    TIEBREAKER,
    OUT_STRING,
    HAND_TYPE_STRAIGHT_FLUSH,
    HAND_TYPE_QUADS,
    HAND_TYPE_FULL_HOUSE,
    HAND_TYPE_FLUSH,
    HAND_TYPE_STRAIGHT,
    HAND_TYPE_TRIPS,
    HAND_TYPE_TWO_PAIR,
    HAND_TYPE_PAIR,
    HAND_TYPE_HIGH_CARD,
    GAME_TYPE_TEXAS_HOLDEM,
    TB_DRAWS_KWAGRS,
    TB_DRAWS_KWARGS_ALL,
    TB_DRAWS_KWARGS_TIEBREAKER,
)
from pypoker.engine.logic.functions import (
    hand_test,
    tiebreak_hands,
    describe_hand,
    find_outs_scenarios,
)
from pypoker.engine.logic.functions.outs import get_all_combinations_for_out_string
from pypoker.engine.logic.utils import get_all_combinations


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
            {HAND_TITLE: HAND_TYPE_STRAIGHT_FLUSH, HAND_RANK: 1},
            {HAND_TITLE: HAND_TYPE_QUADS, HAND_RANK: 2},
            {HAND_TITLE: HAND_TYPE_FULL_HOUSE, HAND_RANK: 3},
            {HAND_TITLE: HAND_TYPE_FLUSH, HAND_RANK: 4},
            {HAND_TITLE: HAND_TYPE_STRAIGHT, HAND_RANK: 5},
            {HAND_TITLE: HAND_TYPE_TRIPS, HAND_RANK: 6},
            {HAND_TITLE: HAND_TYPE_TWO_PAIR, HAND_RANK: 7},
            {HAND_TITLE: HAND_TYPE_PAIR, HAND_RANK: 8},
            {HAND_TITLE: HAND_TYPE_HIGH_CARD, HAND_RANK: 9},
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
            matched_hands = [
                hand
                for hand in all_hands
                if hand_test(
                    GAME_TYPE_TEXAS_HOLDEM, hand_ranking[HAND_TITLE], hand=hand
                )
            ]

            if matched_hands:
                best_hand = tiebreak_hands(
                    GAME_TYPE_TEXAS_HOLDEM,
                    hand_ranking[HAND_TITLE],
                    hands=matched_hands,
                )[0]["hands"][0]
                return {
                    BEST_HAND: best_hand,
                    HAND_TITLE: hand_ranking[HAND_TITLE],
                    HAND_RANK: hand_ranking[HAND_RANK],
                    HAND_DESCRIPTION: describe_hand(
                        GAME_TYPE_TEXAS_HOLDEM, hand_ranking[HAND_TITLE], hand=best_hand
                    ),
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
            subranked_hands = tiebreak_hands(
                GAME_TYPE_TEXAS_HOLDEM,
                self._hand_rankings[rank - 1][HAND_TITLE],
                hands=hands,
            )
            subranked_players = self._link_subranked_hands_to_players(
                subranked_hands, players_hands
            )

            for players in subranked_players.values():
                current_rank += 1
                hand_desc = describe_hand(
                    GAME_TYPE_TEXAS_HOLDEM,
                    self._hand_rankings[rank - 1][HAND_TITLE],
                    hand=players_hands[players[0]],
                )
                ranked_player_hands[current_rank] = {
                    "players": players,
                    "hand_description": hand_desc,
                }

        return ranked_player_hands

    def find_odds(self, player_hole_cards: Dict[str, List[Card]], board_cards: List[Card], debug=False):
        """
        Method to find the odds for each player in a given situation.

        :param player_hole_cards:
        :param board_cards:
        :param debug:
        :return:
        """

        # Setup important variables
        player_claimed_outs = {player: set() for player in player_hole_cards.keys()}
        all_claimed_outs = set()
        drawable_cards = self._determine_unused_cards(player_hole_cards, board_cards)

        # determine current best hand
        current_hands = {player: self.find_best_hand(hole_cards, board_cards) for player, hole_cards in player_hole_cards.items()}
        current_ranked_hands = self.rank_hands({player: hand_info[BEST_HAND] for player, hand_info in current_hands.items()})
        current_winners = current_ranked_hands[1]["players"]
        current_winner_rank = current_hands[current_winners[0]]["hand_rank"]

        # Find all player out strings
        ranked_player_outs = {}
        for hand_type in self._hand_rankings:
            if hand_type[HAND_RANK] > current_winner_rank:
                continue

            rank_out_strings = {}
            for player, hole_cards in player_hole_cards.items():
                kwargs = dict(hole_cards=hole_cards, board_cards=board_cards, available_cards=drawable_cards)
                out_scenarios = find_outs_scenarios(GAME_TYPE_TEXAS_HOLDEM, hand_type[HAND_TITLE], **kwargs)
                out_strings = [out_dict[OUT_STRING] for out_dict in out_scenarios]
                rank_out_strings[player] = out_strings
            ranked_player_outs[hand_type[HAND_RANK]] = rank_out_strings

        # Assigned wins
        for rank, player_out_strings in ranked_player_outs.items():
            players_with_outs = [player for player, out_strings in player_out_strings.items() if out_strings]
            if not players_with_outs:
                print(f"No player has outs at rank {rank}")
                continue

            if rank == current_winner_rank:
                print(f"Testing/Assigning wins for current highest hand rank of {rank}.")

                # Find each players potential outs
                player_potential_outs = dict()
                for player in players_with_outs:
                    potential_outs = [
                        get_all_combinations_for_out_string(all_claimed_outs, out_string, drawable_cards)
                        for out_string in player_out_strings[player]
                    ]
                    potential_outs = [item for sublist in potential_outs for item in sublist]
                    potential_outs = list(set(potential_outs))
                    player_potential_outs[player] = potential_outs

                # Tiebreak all possible outs as current leader needs to be assessed against each out possibility.
                all_outs = [outs for outs in player_potential_outs.values()]
                all_outs = [item for sublist in all_outs for item in sublist]
                all_outs = list(set(all_outs))

                # tiebreak "conflicted" outs
                for out in all_outs:
                    # find players with this out + add current winners
                    eligable_players = [test_player for test_player, possible_outs in player_potential_outs.items()
                                        if out in possible_outs]
                    eligable_players.extend(current_winners)
                    eligable_players = list(set(eligable_players))

                    # if only one player has this out then award win and move on
                    if len(eligable_players) == 1:
                        player_claimed_outs[eligable_players[0]].add(out)
                        all_claimed_outs.add(out)
                        continue

                    # build board object for this out string
                    drawn_cards = [Card(card_id) for card_id in out.split("-")]
                    new_board = board_cards.copy()
                    new_board.extend(drawn_cards)

                    # find hands for each player (look to optimise via use of private methods, not searching thru all ranks)
                    tb_hands = {
                        tb_player: self.find_best_hand(player_hole_cards[tb_player], new_board)[BEST_HAND]
                        for tb_player in eligable_players
                    }

                    # Rank the players hands
                    hand_title = [hand_info[HAND_TITLE] for hand_info in self._hand_rankings if hand_info[HAND_RANK] == rank][0]
                    tb_ranks = tiebreak_hands(GAME_TYPE_TEXAS_HOLDEM, hand_title, list(tb_hands.values()))

                    # Find winners and award wins
                    winners = sorted([tb_player for tb_player, hand in tb_hands.items() if hand in tb_ranks[0]["hands"]])
                    winners = winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"
                    if winners in player_claimed_outs.keys():
                        player_claimed_outs[winners].add(out)
                    else:
                        player_claimed_outs[winners] = {out}
                    all_claimed_outs.add(out)

            elif len(players_with_outs) == 1:
                print(f"Only player '{players_with_outs[0]}' has outs for rank {rank}.  Assigning Wins.")

                # get all possible combinations for player's out strings
                potential_outs = [
                    get_all_combinations_for_out_string(all_claimed_outs, out_string, drawable_cards)
                    for out_string in player_out_strings[players_with_outs[0]]
                ]
                potential_outs = [item for sublist in potential_outs for item in sublist]

                # deduplicate and award all outs to player
                awarded_outs = set(potential_outs)
                player_claimed_outs[players_with_outs[0]].update(awarded_outs)
                all_claimed_outs.update(awarded_outs)

            elif len(players_with_outs) > 1:
                print(f"Multiple players '{players_with_outs}' have outs for rank {rank}. Tiebreaking Outs.")

                # Find each players potential outs
                player_potential_outs = dict()
                for player in players_with_outs:
                    potential_outs = [
                        get_all_combinations_for_out_string(all_claimed_outs, out_string, drawable_cards)
                        for out_string in player_out_strings[player]
                    ]
                    potential_outs = [item for sublist in potential_outs for item in sublist]
                    potential_outs = set(potential_outs)
                    player_potential_outs[player] = potential_outs

                # Award wins for uncontested outs, tiebreak conflict outs
                for player, potential_outs in player_potential_outs.items():
                    # Get list of already claimed outs - must be updated for each new player

                    # find current player and opposition possible outs
                    my_outs = [out for out in potential_outs if out not in all_claimed_outs]
                    their_outs = [outs for other_player, outs in player_potential_outs.items() if other_player != player]
                    their_outs = set([item for sublist in their_outs for item in sublist])

                    # define conflicted and uncontested outs
                    uncontested_outs = set([out for out in my_outs if out not in their_outs])
                    conflicted_outs = [out for out in my_outs if out not in uncontested_outs]

                    # claim uncontested outs
                    player_claimed_outs[player].update(uncontested_outs)
                    all_claimed_outs.update(uncontested_outs)

                    # tiebreak conflicted outs
                    for out in conflicted_outs:
                        # find players with this out
                        eligable_players = [test_player for test_player, possible_outs in player_potential_outs.items() if out in possible_outs]

                        # build board object for this out string
                        drawn_cards = [Card(card_id) for card_id in out.split("-")]
                        new_board = board_cards.copy()
                        new_board.extend(drawn_cards)

                        # find hands for each player (look to optimise via use of private methods, not searching thru all ranks)
                        tb_hands = {
                            tb_player: self.find_best_hand(player_hole_cards[tb_player], new_board)[BEST_HAND]
                            for tb_player in eligable_players
                        }

                        # Rank the players hands
                        hand_title = [hand_info[HAND_TITLE] for hand_info in self._hand_rankings if hand_info[HAND_RANK] == rank][0]
                        tb_ranks = tiebreak_hands(GAME_TYPE_TEXAS_HOLDEM, hand_title, list(tb_hands.values()))

                        # Find winners and award wins
                        winners = sorted([tb_player for tb_player, hand in tb_hands.items() if hand in tb_ranks[0]["hands"]])
                        winners = winners[0] if len(winners) == 1 else f"TIE({','.join(winners)})"
                        if winners in player_claimed_outs.keys():
                            player_claimed_outs[winners].add(out)
                        else:
                            player_claimed_outs[winners] = {out}
                        all_claimed_outs.add(out)

        # find total number of draws evaluating for
        total_draw_combinations = 1
        cards_to_draw = 5 - len(board_cards)
        for draw in range(cards_to_draw):
            cards_available = len(drawable_cards) - draw
            total_draw_combinations *= cards_available
        total_draw_combinations /= cards_to_draw

        # give all unassigned wins to current leader
        win_counts = {player: len(outs) for player, outs in player_claimed_outs.items()}
        claimed_outs_count = sum([outs for outs in win_counts.values()])
        bricked_draws_count = total_draw_combinations - claimed_outs_count

        current_winners = current_winners[0] if len(current_winners) == 1 else f"TIE({','.join(current_winners)})"
        if current_winners not in win_counts.keys():
            win_counts[current_winners] = bricked_draws_count
        else:
            win_counts[current_winners] += bricked_draws_count

        odds = {
            player: round(win_count / total_draw_combinations * 100, 2) for player, win_count in win_counts.items()
        }

        if debug:
            print("FINAL CLAIMED OUTS:")
            for player, outs in player_claimed_outs.items():
                print(f"\t{player}: {outs}")

        return odds

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
        for subrank_info in subranked_hands:
            for hand in subrank_info["hands"]:
                hand.sort(key=lambda card: card.value, reverse=True)

            matched_players = [
                player
                for player, player_hand in players_hands.items()
                if player_hand in subrank_info["hands"]
            ]
            linked_subrank_players[subrank_info["rank"]] = matched_players

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
