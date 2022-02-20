"""
pypoker.engine.texas_holdem module
----------------------------------

module containing the poker engine for the texas holdem game type.
inherits from the BasePokerEngine class.
"""
from decimal import Decimal
from typing import List, Dict

from pypoker.constants import TexasHoldemHandType, FindOddsMethod
from pypoker.constructs import Card, Hand
from pypoker.engine import BasePokerEngine, find_all_unique_card_combos
from pypoker.exceptions import RankingError, OutsError
from pypoker.player import BasePlayer

import pypoker.engine.texas_holdem.make_hands as hands
import pypoker.engine.texas_holdem.find_outs as outs
import pypoker.engine.texas_holdem.find_odds as odds


class TexasHoldemPokerEngine(BasePokerEngine):
    """
    concrete implementation of the PokerEngine class for Texas Hold'em game type
    """

    # Concrete Implementation of public methods
    # -----------------------------------------
    def find_player_best_hand(
        self, player: BasePlayer, board: List[Card]
    ) -> List[Hand]:
        """
        Find a given players best possible hand with the current cards available.

        :param player: the Player object to find the best hand for
        :param board: list containing the current board cards. If preflop then this list should be empty
        """

        available_cards = player.hole_cards + board

        for hand_type in TexasHoldemHandType:
            made_hands = {
                TexasHoldemHandType.StraightFlush: hands.make_straight_flush_hands,
                TexasHoldemHandType.Quads: hands.make_quads_hands,
                TexasHoldemHandType.FullHouse: hands.make_full_house_hands,
                TexasHoldemHandType.Flush: hands.make_flush_hands,
                TexasHoldemHandType.Straight: hands.make_straight_hands,
                TexasHoldemHandType.Trips: hands.make_trips_hands,
                TexasHoldemHandType.TwoPair: hands.make_two_pair_hands,
                TexasHoldemHandType.Pair: hands.make_pair_hands,
                TexasHoldemHandType.HighCard: hands.make_high_card_hands,
            }[hand_type](available_cards)

            if made_hands:
                best_hand_tiebreaker = made_hands[0].tiebreakers
                return [
                    hand
                    for hand in made_hands
                    if hand.tiebreakers == best_hand_tiebreaker
                ]

    def rank_player_hands(
        self, players: List[BasePlayer]
    ) -> Dict[int, List[BasePlayer]]:
        """
        For the given list of players, rank them based on the player.hand attributes.

        If any player in the list does not have a hand attribute set, raise exception.

        :param players: List of players to rank

        :returns: Dictionary where key is the rank (1 being highest) and value is a list of player objects sharing
        that rank.
        """

        if not all(isinstance(player, BasePlayer) for player in players):
            raise RankingError("All values of players list must be of BasePlayer Type")

        if any(player.hand is None for player in players):
            raise RankingError(
                "All players must have their player.hand attribute set to rank them."
            )

        players = sorted(
            players,
            key=lambda player: (player.hand.strength, player.hand.tiebreakers),
            reverse=True,
        )

        ranked_players = dict()
        rank = 1
        current_strength = None
        current_tb = None

        for player in players:
            if not current_strength:
                current_strength = player.hand.strength
                current_tb = player.hand.tiebreakers
                ranked_players[rank] = [player]

            elif (
                player.hand.strength == current_strength
                and player.hand.tiebreakers == current_tb
            ):
                ranked_players[rank].append(player)

            else:
                rank += 1
                current_strength = player.hand.strength
                current_tb = player.hand.tiebreakers
                ranked_players[rank] = [player]

        return ranked_players

    def find_player_outs(
        self,
        player: BasePlayer,
        hand_type: TexasHoldemHandType,
        board: List[Card],
        possible_cards: List[Card],
    ) -> List[List[Card]]:
        """
        abstract method to find the possible draws a player has to make the specified hand type with the current
        board cards and the possible draws remaining.

        :param player: pypoker player object representing the player we are looking for outs for.
        :param hand_type: hand type enum used for determining the type of hand to find outs for.
        :param possible_cards: List of card objects that could be drawn
        (Note this could be the available cards from the deck or the "implied" available cards)

        :return: list of each combination of cards that would give the player this type of hand. Cards in these combinations
        are explict normal cards (7H, 9D, etc) for cards required to make the out and AnyCard special cards for
        any surplus draw cards not required to make the hand.
        """

        if hand_type == TexasHoldemHandType.HighCard:
            raise OutsError(
                "Cannot find outs for hand type HighCard, you always have this hand type made."
            )

        current_cards = player.hole_cards + board
        draws_remaining = 5 - len(board)

        return {
            TexasHoldemHandType.StraightFlush: outs.find_outs_straight_flush,
            TexasHoldemHandType.Quads: outs.find_outs_quads,
            TexasHoldemHandType.FullHouse: outs.find_outs_full_house,
            TexasHoldemHandType.Flush: outs.find_outs_flush,
            TexasHoldemHandType.Straight: outs.find_outs_straight,
            TexasHoldemHandType.Trips: outs.find_outs_trips,
            TexasHoldemHandType.TwoPair: outs.find_outs_two_pair,
            TexasHoldemHandType.Pair: outs.find_outs_pair,
        }[hand_type](current_cards, possible_cards, draws_remaining)

    def find_player_odds(self, players: List[BasePlayer], board: List[Card], drawable_cards: List[Card], method: FindOddsMethod = None) -> Dict[
        str, Decimal]:
        """
        Texas Holdem Engine concrete implementation of abstract method to find the win probability of each player.

        :param players: List of pypoker player object representing the player we are looking for odds fos.
        :param board: List of card objects representing the cards that have already been dealt on the board.
        :param drawable_cards: List of card objects representing the remaining possible cards to draw.

        :return: dict of player win probabilities from 0.0 to 100.0 rounded to two decimal places. This dictionary should also contain entries for
        ties in the format of 'TIE(player_a,player_b,player_c)'
        """

        draws_remaining = 5 - len(board)

        # if method isnt set, then use simulate if pre-flop as there are too many combinations of draws.
        if not method:
            method = FindOddsMethod.Simulate100 if draws_remaining == 5 else FindOddsMethod.Enumerate

        func, args = {
            FindOddsMethod.Enumerate: (odds.find_player_odds_enumerate, [self, players, board, drawable_cards]),
            FindOddsMethod.Simulate100: (odds.find_player_odds_simulate, [self, players, board, drawable_cards, 100000]),
        }[method]

        return func(*args)
