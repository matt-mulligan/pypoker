"""
pypoker.engine.texas_holdem module
----------------------------------

module containing the poker engine for the texas holdem game type.
inherits from the BasePokerEngine class.
"""
from itertools import combinations
from typing import List, Dict

from pypoker.constants import GameTypes, TexasHoldemHandType, HandType, CardSuit
from pypoker.constructs import Card, Hand, AnyCard
from pypoker.engine import BasePokerEngine
from pypoker.exceptions import RankingError, InvalidHandTypeError
from pypoker.player import BasePlayer


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
                TexasHoldemHandType.StraightFlush: self.make_straight_flush_hands,
                TexasHoldemHandType.Quads: self.make_quads_hands,
                TexasHoldemHandType.FullHouse: self.make_full_house_hands,
                TexasHoldemHandType.Flush: self.make_flush_hands,
                TexasHoldemHandType.Straight: self.make_straight_hands,
                TexasHoldemHandType.Trips: self.make_trips_hands,
                TexasHoldemHandType.TwoPair: self.make_two_pair_hands,
                TexasHoldemHandType.Pair: self.make_pair_hands,
                TexasHoldemHandType.HighCard: self.make_high_card_hands,
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
            self, player: BasePlayer, board: List[Card], possible_draws: List[Card], target_hand: TexasHoldemHandType
    ) -> List[List[Card]]:
        """
        Concreet method to determine all possible outs a player has to get the the specified hand type with the possible draws remaining.
        If no way to get to the hand type then return empty list
        This method uses SpecialCard constructs (e.g. any 7, any heart, any card at all) to limit the return set to
        logical outs not direct outs.
        """

        if not isinstance(target_hand, TexasHoldemHandType):
            raise InvalidHandTypeError("target_hand provided is not of type TexasHoldemHandType")

        current_cards = player.hole_cards + board
        remaining_draws = 5 - len(board)

        return {
            TexasHoldemHandType.StraightFlush: self.find_outs_straight_flush,
            TexasHoldemHandType.Quads: self.find_outs_quads,
            TexasHoldemHandType.FullHouse: self.find_outs_full_house,
            TexasHoldemHandType.Flush: self.find_outs_flush,
            TexasHoldemHandType.Straight: self.find_outs_straight,
            TexasHoldemHandType.Trips: self.find_outs_trips,
            TexasHoldemHandType.TwoPair: self.find_outs_two_pair,
            TexasHoldemHandType.Pair: self.find_outs_pair,
            TexasHoldemHandType.HighCard: self.find_outs_high_card,
        }[target_hand](current_cards, possible_draws, remaining_draws)

    # Public "Hand Maker" methods
    # ---------------------------
    def make_straight_flush_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible straight flush hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each straight flush hand possible.
        """

        if len(available_cards) < 5:
            return []

        suits_grouped = self.group_cards_by_suit(available_cards)
        eligible_suits = [cards for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return []

        straight_flushes = [
            self.find_consecutive_value_cards(cards, treat_ace_low=True, run_size=5)
            for cards in eligible_suits
        ]
        straight_flushes = [val for sublist in straight_flushes for val in sublist]

        hands = []
        for cards in straight_flushes:
            tiebreaker = [max([card.value for card in cards])]
            if tiebreaker == [14] and any(card.value == 5 for card in cards):
                tiebreaker = [5]
            hands.append(
                Hand(
                    GameTypes.TexasHoldem, TexasHoldemHandType.StraightFlush, cards, tiebreaker
                )
            )

        return sorted(hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_quads_hands(
        self, available_cards: List[Card], include_kickers: bool = True
    ) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible quads hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each quad hand possible.
        """

        if len(available_cards) < 4:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = [
            key for key, cards in value_grouped_cards.items() if len(cards) == 4
        ]
        if not eligible_values:
            return []

        quad_hands = []
        for quad_value in eligible_values:
            quad_cards = value_grouped_cards[quad_value]
            other_cards = [card for card in available_cards if card.value != quad_value]
            if (
                not include_kickers or not other_cards
            ):  # manages for the usecase of only getting 4 cards of the same value and no kickers
                quad_hands.append(
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.Quads,
                        quad_cards,
                        [quad_value, None],
                    )
                )
            else:
                quad_hands.extend(
                    [
                        Hand(
                            GameTypes.TexasHoldem,
                            TexasHoldemHandType.Quads,
                            quad_cards + [card],
                            [quad_value, card.value],
                        )
                        for card in other_cards
                    ]
                )

        return sorted(quad_hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_full_house_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible full house hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each full house hand possible.
        """

        if len(available_cards) < 5:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        trips_values = [
            key for key, cards in value_grouped_cards.items() if len(cards) >= 3
        ]
        pair_values = [
            key for key, cards in value_grouped_cards.items() if len(cards) >= 2
        ]

        pair_combos = [
            self.find_all_unique_card_combos(value_grouped_cards[value], 2)
            for value in pair_values
        ]
        pair_combos = [val for sublist in pair_combos for val in sublist]

        full_houses = []
        for trip_value in trips_values:
            trip_cards = value_grouped_cards[trip_value]
            trip_combos = self.find_all_unique_card_combos(trip_cards, 3)

            hands = [
                Hand(
                    GameTypes.TexasHoldem,
                    TexasHoldemHandType.FullHouse,
                    trip_combo + pair_combo,
                    [trip_value, pair_combo[0].value],
                )
                for trip_combo in trip_combos
                for pair_combo in pair_combos
                if pair_combo[0].value != trip_value
            ]

            full_houses.extend(hands)

        return sorted(full_houses, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_flush_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible flush hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each flush hand possible.
        """

        if len(available_cards) < 5:
            return []

        suits_grouped = self.group_cards_by_suit(available_cards)
        eligible_suits = [cards for cards in suits_grouped.values() if len(cards) >= 5]
        if not eligible_suits:
            return []

        flushes = [
            self.find_all_unique_card_combos(cards, 5) for cards in eligible_suits
        ]
        flushes = [val for sublist in flushes for val in sublist]
        flushes = [
            Hand(
                GameTypes.TexasHoldem,
                TexasHoldemHandType.Flush,
                cards,
                sorted([card.value for card in cards], reverse=True),
            )
            for cards in flushes
        ]

        return sorted(flushes, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_straight_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible straight hands with the given cards

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each straight hand possible.
        """

        if len(available_cards) < 5:
            return []

        straights = self.find_consecutive_value_cards(
            available_cards, treat_ace_low=True, run_size=5
        )

        hands = []
        for cards in straights:
            tiebreaker = [max([card.value for card in cards])]
            if tiebreaker == [14] and any(card.value == 5 for card in cards):
                tiebreaker = [5]
            hands.append(
                Hand(GameTypes.TexasHoldem, TexasHoldemHandType.Straight, cards, tiebreaker)
            )

        return sorted(hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_trips_hands(
        self, available_cards: List[Card], include_kickers: bool = True
    ) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible trips hands with the given cards.
        Note that this method will build ONLY trips hands, and exclude any hands that feature three of a kind but
        technically is a stronger hand. for example, if given three queens(QH-QS-QC), two aces(AH-AS) and a four(4S),
        this method would return you only two possible trips hands, (QH-QS-QC-AH-4S) and (QH-QS-QC-AS-4S)
        The other option for a full hand here would give a full house instead, which means it is excluded from
        this method.

        :param available_cards: List of card objects available to use.
        :param include_kickers: Boolean indicating if the returned hands should include the kicker cards or
            if the combinations should just be the cards required to make the trips.
            Note that setting this to true will return many more hands as it builds all hands possible with kickers.
        :return: Ordered list of Hand objects that represent each trips hand possible.
        """

        if len(available_cards) < 3:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = {
            key: cards for key, cards in value_grouped_cards.items() if len(cards) >= 3
        }

        if not eligible_values:
            return []

        trip_hands = []
        for trip_value, trip_cards in eligible_values.items():
            trip_card_combos = self.find_all_unique_card_combos(trip_cards, 3)
            kicker_cards = [
                card for card in available_cards if card.value != trip_value
            ]

            if not include_kickers or not kicker_cards:
                trip_hands.extend(
                    [
                        Hand(
                            GameTypes.TexasHoldem,
                            TexasHoldemHandType.Trips,
                            trip_combo,
                            [trip_combo[0].value, None, None],
                        )
                        for trip_combo in trip_card_combos
                    ]
                )
            else:
                kicker_cards_combos = self.find_all_unique_card_combos(kicker_cards, 2)
                kicker_cards_combos = [
                    sorted(combo, key=lambda card: card.value, reverse=True)
                    for combo in kicker_cards_combos
                    if combo[0].value != combo[1].value
                ]

                if not kicker_cards_combos:
                    kicker_cards_combos = kicker_cards
                    trip_hands.extend(
                        [
                            Hand(
                                GameTypes.TexasHoldem,
                                TexasHoldemHandType.Trips,
                                trip_combo + [kicker_card],
                                [trip_value, kicker_card.value, None],
                            )
                            for trip_combo in trip_card_combos
                            for kicker_card in kicker_cards_combos
                        ]
                    )

                else:
                    trip_hands.extend(
                        [
                            Hand(
                                GameTypes.TexasHoldem,
                                TexasHoldemHandType.Trips,
                                trip_combo + kicker_combo,
                                [
                                    trip_value,
                                    kicker_combo[0].value,
                                    kicker_combo[1].value,
                                ],
                            )
                            for trip_combo in trip_card_combos
                            for kicker_combo in kicker_cards_combos
                        ]
                    )

        return sorted(trip_hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_two_pair_hands(
        self, available_cards: List[Card], include_kickers: bool = True
    ) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible two-pair hands with the given cards, optionally including kickers.
        Note that this method will build ONLY two-pair hands, and exclude any hands that feature two-pairs but
        technically is a stronger hand. for example, if given three queens(QH-QS-QC), two aces(AH-AS) and a four(4S),
        this method would return you hands that do not feature all three queens as this would instead be trips or
        full houses and they are stronger hands than two-pair

        :param available_cards: List of card objects available to use.
        :param include_kickers: Boolean indicating if the returned hands should include the kicker cards or
            if the combinations should just be the cards required to make the two-pair.
            Note that setting this to true will return many more hands as it builds all hands possible with kickers.
        :return: Ordered list of Hand objects that represent each two-pair hand possible.
        """

        if len(available_cards) < 4:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = {
            key: cards for key, cards in value_grouped_cards.items() if len(cards) >= 2
        }

        if len(eligible_values) < 2:
            return []

        two_pair_values = list(eligible_values.keys())
        two_pair_value_combos = [
            list(value) for value in combinations(two_pair_values, 2)
        ]

        two_pair_hands = []
        for two_pair_value_list in two_pair_value_combos:
            two_pair_value_a = two_pair_value_list[0]
            two_pair_value_b = two_pair_value_list[1]

            two_pairs_a = self.find_all_unique_card_combos(
                eligible_values[two_pair_value_a], 2
            )
            two_pairs_b = self.find_all_unique_card_combos(
                eligible_values[two_pair_value_b], 2
            )
            two_pair_sets = [a + b for a in two_pairs_a for b in two_pairs_b]

            kicker_cards = [
                cards
                for value, cards in value_grouped_cards.items()
                if value not in two_pair_value_list
            ]
            kicker_cards = [val for sublist in kicker_cards for val in sublist]

            if not include_kickers or not kicker_cards:
                two_pair_hands.extend(
                    [
                        Hand(
                            GameTypes.TexasHoldem,
                            TexasHoldemHandType.TwoPair,
                            two_pair,
                            [max(two_pair_value_list), min(two_pair_value_list), None],
                        )
                        for two_pair in two_pair_sets
                    ]
                )
                continue

            two_pair_hands.extend(
                [
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.TwoPair,
                        two_pair + [kicker],
                        [
                            max(two_pair_value_list),
                            min(two_pair_value_list),
                            kicker.value,
                        ],
                    )
                    for two_pair in two_pair_sets
                    for kicker in kicker_cards
                ]
            )

        return sorted(two_pair_hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_pair_hands(
        self, available_cards: List[Card], include_kickers: bool = True
    ) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible pair hands with the given cards, optionally including kickers.
        Note that this method will build ONLY pair hands, and exclude any hands that feature a pair but
        technically is a stronger hand. for example, if given three queens(QH-QS-QC), two aces(AH-AS) and a four(4S),
        this method would return you hands that do not feature a pair of aces and a pair of queens as this would
        instead be a two-pair hand and they are stronger hands than pairs

        :param available_cards: List of card objects available to use.
        :param include_kickers: Boolean indicating if the returned hands should include the kicker cards or
            if the combinations should just be the cards required to make the pair.
            Note that setting this to true will return many more hands as it builds all hands possible with kickers.
        :return: Ordered list of Hand objects that represent each pair hand possible.
        """

        if len(available_cards) < 2:
            return []

        value_grouped_cards = self.group_cards_by_value(available_cards)
        eligible_values = {
            key: cards for key, cards in value_grouped_cards.items() if len(cards) >= 2
        }

        if not eligible_values:
            return []

        pair_hands = []
        for pair_value, pair_cards in eligible_values.items():
            pairs = self.find_all_unique_card_combos(pair_cards, 2)
            kicker_cards = [
                card for card in available_cards if card.value != pair_value
            ]

            if not include_kickers or not kicker_cards:
                pair_hands.extend(
                    [
                        Hand(
                            GameTypes.TexasHoldem,
                            TexasHoldemHandType.Pair,
                            pair,
                            [pair_value, None, None, None],
                        )
                        for pair in pairs
                    ]
                )
                continue

            kicker_sets = self.find_all_unique_card_combos(kicker_cards, 3)
            kicker_sets = [
                sorted(kicker_set, key=lambda card: card.value, reverse=True)
                for kicker_set in kicker_sets
                if self.check_all_card_values_unique(kicker_set)
            ]

            if kicker_sets:
                pair_hands.extend(
                    [
                        Hand(
                            GameTypes.TexasHoldem,
                            TexasHoldemHandType.Pair,
                            pair + kicker_set,
                            [
                                pair_value,
                                kicker_set[0].value,
                                kicker_set[1].value,
                                kicker_set[2].value,
                            ],
                        )
                        for pair in pairs
                        for kicker_set in kicker_sets
                    ]
                )
                continue

            kicker_sets = self.find_all_unique_card_combos(kicker_cards, 2)
            kicker_sets = [
                sorted(kicker_set, key=lambda card: card.value, reverse=True)
                for kicker_set in kicker_sets
                if self.check_all_card_values_unique(kicker_set)
            ]

            if kicker_sets:
                pair_hands.extend(
                    [
                        Hand(
                            GameTypes.TexasHoldem,
                            TexasHoldemHandType.Pair,
                            pair + kicker_set,
                            [
                                pair_value,
                                kicker_set[0].value,
                                kicker_set[1].value,
                                None,
                            ],
                        )
                        for pair in pairs
                        for kicker_set in kicker_sets
                    ]
                )
                continue

            pair_hands.extend(
                [
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.Pair,
                        pair + [card],
                        [pair_value, card.value, None, None],
                    )
                    for pair in pairs
                    for card in kicker_cards
                ]
            )

        return sorted(pair_hands, key=lambda hand: hand.tiebreakers, reverse=True)

    def make_high_card_hands(self, available_cards: List[Card]) -> List[Hand]:
        """
        Texas Holdem Poker Engine Hand Maker Method
        method to make all possible high card hands with the given cards.
        Note that this method will build ONLY high card hands, and exclude any hands that feature a technically
        stronger hand

        :param available_cards: List of card objects available to use.
        :return: Ordered list of Hand objects that represent each high card hand possible.
        """

        card_combos = self.find_all_unique_card_combos(available_cards, 5)
        card_combos = [
            sorted(cards, key=lambda card: card.value, reverse=True)
            for cards in card_combos
            if self.check_all_card_values_unique(cards)
            and not self.check_all_card_suits_match(cards)
            and not self.check_cards_consecutive(cards)
        ]

        if card_combos:
            return sorted(
                [
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.HighCard,
                        cards,
                        sorted([card.value for card in cards], reverse=True),
                    )
                    for cards in card_combos
                ],
                key=lambda hand: hand.tiebreakers,
                reverse=True,
            )

        card_combos = self.find_all_unique_card_combos(available_cards, 4)
        card_combos = [
            sorted(cards, key=lambda card: card.value, reverse=True)
            for cards in card_combos
            if self.check_all_card_values_unique(cards)
        ]

        if card_combos:
            return sorted(
                [
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.HighCard,
                        cards,
                        sorted([card.value for card in cards], reverse=True) + [None],
                    )
                    for cards in card_combos
                ],
                key=lambda hand: hand.tiebreakers,
                reverse=True,
            )

        card_combos = self.find_all_unique_card_combos(available_cards, 3)
        card_combos = [
            sorted(cards, key=lambda card: card.value, reverse=True)
            for cards in card_combos
            if self.check_all_card_values_unique(cards)
        ]

        if card_combos:
            return sorted(
                [
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.HighCard,
                        cards,
                        sorted([card.value for card in cards], reverse=True)
                        + [None, None],
                    )
                    for cards in card_combos
                ],
                key=lambda hand: hand.tiebreakers,
                reverse=True,
            )

        card_combos = self.find_all_unique_card_combos(available_cards, 2)
        card_combos = [
            sorted(cards, key=lambda card: card.value, reverse=True)
            for cards in card_combos
            if self.check_all_card_values_unique(cards)
        ]

        if card_combos:
            return sorted(
                [
                    Hand(
                        GameTypes.TexasHoldem,
                        TexasHoldemHandType.HighCard,
                        cards,
                        sorted([card.value for card in cards], reverse=True)
                        + [None, None, None],
                    )
                    for cards in card_combos
                ],
                key=lambda hand: hand.tiebreakers,
                reverse=True,
            )

        return sorted(
            [
                Hand(
                    GameTypes.TexasHoldem,
                    TexasHoldemHandType.HighCard,
                    [card],
                    [card.value, None, None, None, None],
                )
                for card in available_cards
            ],
            key=lambda hand: hand.tiebreakers,
            reverse=True,
        )

    # Public "Find Outs" methods
    # ---------------------------

    def find_outs_straight_flush(self, current_cards, possible_draws, remaining_draws):
        """
        Public "find outs" method for texas holdem engine
        attempt to find all the logical out combinations using special cards for the player to build a straight flush.

        This method should return you all logical draws to make all possible straight flushes, better or worse ones.
        """

        cards_by_suit = self.group_cards_by_suit(current_cards)

        eligible_suits = [suit for suit in CardSuit if len(cards_by_suit.get(suit.name, [])) + remaining_draws >= 5]
        outs = []

        for suit in eligible_suits:
            current_suited_cards = [card for card in sorted(current_cards, key=lambda card: card.value, reverse=True) if card.suit == suit]
            drawable_suited_cards = [card for card in sorted(possible_draws, key=lambda card: card.value, reverse=True) if card.suit == suit]

            # Lazy/Slow approach, inject each unique combo of draw cards into the current cards and run them through
            # find_consecutive_cards

            for draw_combo in self.find_all_unique_card_combos(drawable_suited_cards, remaining_draws):
                test_cards = current_suited_cards + draw_combo
                straight_flushes = self.find_consecutive_value_cards(test_cards, True, 5)

                for straight_flush in straight_flushes:
                    drawn_cards = [card for card in straight_flush if card in draw_combo]
                    drawn_cards += [AnyCard("")] * (remaining_draws - len(drawn_cards))
                    outs.append(drawn_cards)

            # Smarter/Faster approach, comparing values of current and drawbale cards, looks for what gaps can be
            # plugged to make 5+ card hands

            # not sure how :'(

        return [list(x) for x in set(tuple(x) for x in outs)]

    def find_outs_quads(self, current_cards, possible_draws, remaining_draws):
        """
        Public "find outs" method for texas holdem engine
        attempt to find all the logical out combinations using special cards for the player to build a quads hand.

        This method should return you all logical draws to make all possible straight flushes, better or worse ones.
        """

        drawn_cards_by_value = self.group_cards_by_value(current_cards)
        drawable_cards_by_value = self.group_cards_by_value(possible_draws)
        eligible_values = [
            value
            for value, cards in drawn_cards_by_value.items()
            if len(cards) + remaining_draws >= 4
            and len(cards) + len(drawable_cards_by_value.get(value, [])) == 4
        ]

        outs = []
        for value in eligible_values:
            draws_needed = len(drawable_cards_by_value.get(value, []))
            any_cards = [AnyCard("")] * (remaining_draws - draws_needed)

            outs.append(drawable_cards_by_value.get(value, []) + any_cards)

        return outs


