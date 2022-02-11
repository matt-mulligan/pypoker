"""
pypoker.engine.texas_holdem module
----------------------------------

module containing the poker engine for the texas holdem game type.
inherits from the BasePokerEngine class.
"""
from itertools import combinations
from typing import List, Dict

from pypoker.constants import GameTypes, TexasHoldemHandType
from pypoker.constructs import Card, Hand, Deck, AnyCard
from pypoker.engine import BasePokerEngine
from pypoker.exceptions import RankingError
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

    def find_outs(self, player: BasePlayer, hand_type: TexasHoldemHandType, board: List[Card], deck: Deck) -> List[List[Card]]:
        """
        abstract method to find the possible draws a player has to make the specified hand type with the current
        board cards and the possible draws remaining.

        :param player: pypoker player object representing the player we are looking for outs for.
        :param hand_type: hand type enum used for determining the type of hand to find outs for.
        :param deck: Pypoker deck object containing the remaining cards that are drawable

        :return: list of each combination of cards that would give the player this type of hand. Cards in these combinations
        are explict normal cards (7H, 9D, etc) for cards required to make the out and AnyCard special cards for
        any surplus draw cards not required to make the hand.
        """

        current_cards = player.hole_cards + board
        drawable_cards = deck.cards_available
        draws_remaining = 5 - len(board)

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
        }[hand_type](current_cards, drawable_cards, draws_remaining)

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
                    GameTypes.TexasHoldem,
                    TexasHoldemHandType.StraightFlush,
                    cards,
                    tiebreaker,
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
                Hand(
                    GameTypes.TexasHoldem,
                    TexasHoldemHandType.Straight,
                    cards,
                    tiebreaker,
                )
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

    def find_outs_straight_flush(self, current_cards: List[Card], available_cards: List[Card], remaining_draws: int) -> List[List[Card]]:
        """
        Texas Holdem Poker Engine Find Outs Method
        Method to find all possible outs for the a straight flush hand with the given current_cards and available_cards

        :param current_cards: List of the players hole cards and the current board cards.
        :param available_cards: List of cards remaining in the deck that could be drawn
        :param remaining_draws: the number of drawd remaining.

        :return List of draw combinations that would give a straight flush. with required draws being explict cards
        (D7, SK, etc) and surplus draws represented by AnyCard special cards
        """

        current_suits_grouped = self.group_cards_by_suit(current_cards)
        drawable_suits_grouped = self.group_cards_by_suit(available_cards)

        eligible_suits = {
            suit: (curr_cards, drawable_suits_grouped[suit])
            for suit, curr_cards in current_suits_grouped.items()
            if len(curr_cards) + len(drawable_suits_grouped[suit]) >= 5
        }

        if not eligible_suits:
            return []

        outs = []
        for curr_suit_cards, drawable_suit_cards in eligible_suits.values():
            for draw_size in range(1, remaining_draws + 1):
                straight_flushes = []
                draw_combos = self.find_all_unique_card_combos(drawable_suit_cards, draw_size)

                for draw_combo in draw_combos:
                    straight_flushes.extend(self.find_consecutive_value_cards(curr_suit_cards + draw_combo, run_size=5))

                straight_flushes = self.deduplicate_card_sets(straight_flushes)

                for cards in straight_flushes:
                    out_cards = [card for card in cards if card in drawable_suit_cards]
                    out_cards = out_cards + [AnyCard("")] * (remaining_draws - len(out_cards))
                    outs.append(out_cards)

        return self.deduplicate_card_sets(outs)

    def find_outs_quads(self, current_cards: List[Card], available_cards: List[Card], remaining_draws: int) -> \
    List[List[Card]]:
        """
        Texas Holdem Poker Engine Find Outs Method
        Method to find all possible outs for a quad hand with the given current_cards and available_cards

        :param current_cards: List of the players hole cards and the current board cards.
        :param available_cards: List of cards remaining in the deck that could be drawn
        :param remaining_draws: the number of drawd remaining.

        :return List of draw combinations that would give a quad hand. with required draws being explict cards
        (D7, SK, etc) and surplus draws represented by AnyCard special cards
        """

        current_cards_by_value = self.group_cards_by_value(current_cards)
        available_cards_by_value = self.group_cards_by_value(available_cards)

        possible_values = [
            value for value in range(2, 15)
            if len(current_cards_by_value[value]) + remaining_draws >= 4
            and len(current_cards_by_value[value]) + len(available_cards_by_value[value]) >= 4
        ]

        outs = []
        for quad_value in possible_values:
            required_quad_draws = 4 - len(current_cards_by_value[quad_value])
            surplus_draws = [AnyCard("")] * (remaining_draws - required_quad_draws)

            for draw_combo in self.find_all_unique_card_combos(available_cards_by_value[quad_value], required_quad_draws):
                outs.append(self.order_cards(draw_combo + surplus_draws))

        return outs

    def find_outs_full_house(self, current_cards: List[Card], available_cards: List[Card], remaining_draws: int) -> \
    List[List[Card]]:
        """
        Texas Holdem Poker Engine Find Outs Method
        Method to find all possible outs for a full house hand with the given current_cards and available_cards

        :param current_cards: List of the players hole cards and the current board cards.
        :param available_cards: List of cards remaining in the deck that could be drawn
        :param remaining_draws: the number of draws remaining.

        :return List of draw combinations that would give a full house hand. with required draws being explict cards
        (D7, SK, etc) and surplus draws represented by AnyCard special cards
        """

        current_cards_by_value = self.group_cards_by_value(current_cards)
        available_cards_by_value = self.group_cards_by_value(available_cards)

        # find all values that could make a triple with the remaining number of draws
        trip_possible_values = [
            value for value in range(2, 15)
            if len(current_cards_by_value[value]) + remaining_draws >= 3
            and len(current_cards_by_value[value]) + len(available_cards_by_value[value]) >= 3
        ]

        # find all values that could make a pair with the remaining number of draws
        pair_possible_values = [
            value for value in range(2, 15)
            if len(current_cards_by_value[value]) + remaining_draws >= 2
               and len(current_cards_by_value[value]) + len(available_cards_by_value[value]) >= 2
        ]

        full_house_values = [
            (trip_value, pair_value)
            for trip_value in trip_possible_values
            for pair_value in pair_possible_values
            if trip_value != pair_value
            and max(3-len(current_cards_by_value[trip_value]), 0) + max(2-len(current_cards_by_value[pair_value]), 0) <= remaining_draws
        ]

        outs = []
        for trip_value, pair_value in full_house_values:
            trip_req_draws = max(3 - len(current_cards_by_value[trip_value]), 0)
            pair_req_draws = max(2 - len(current_cards_by_value[pair_value]), 0)

            trip_draw_combos = self.find_all_unique_card_combos(available_cards_by_value[trip_value], trip_req_draws) \
                if trip_req_draws \
                else []

            pair_draw_combos = self.find_all_unique_card_combos(available_cards_by_value[pair_value], pair_req_draws) \
                if pair_req_draws \
                else []

            if not trip_draw_combos and not pair_draw_combos:
                outs.append([AnyCard("")] * remaining_draws)

            elif not trip_draw_combos:
                outs.extend([
                    pair_draw + [AnyCard("")] * (remaining_draws - len(pair_draw))
                    for pair_draw in pair_draw_combos
                ])

            elif not pair_draw_combos:
                outs.extend([
                    trip_draw + [AnyCard("")] * (remaining_draws - len(trip_draw))
                    for trip_draw in trip_draw_combos
                ])

            else:
                outs.extend([
                    trip_draw + pair_draw + [AnyCard("")] * (remaining_draws - len(trip_draw) - len(pair_draw))
                    for trip_draw in trip_draw_combos for pair_draw in pair_draw_combos
                ])

        return self.deduplicate_card_sets(outs)
