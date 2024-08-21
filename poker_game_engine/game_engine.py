from random import shuffle
from itertools import combinations
from collections import Counter
from poker_game_engine.constants import rank_values, hand_rankings, card_suits, card_values

class Card:
    '''
    Represents a single playing card, identified by suit and value.
    '''
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value} of {self.suit}"

class Deck:
    '''
    Represents a deck of playing cards. Provides methods to create a deck and deal cards.
    '''
    suits = card_suits
    values = card_values

    def __init__(self):
        self.cards = [Card(suit, value) for suit in Deck.suits for value in Deck.values]
        shuffle(self.cards)

    def deal(self) -> Card:
        if self.cards:
            return self.cards.pop()
        else:
            raise ValueError("Cannot deal from an empty deck")

class Player:
    '''
    Represents a player in the game, managing their cards, bankroll, and game actions like betting and folding.
    '''
    def __init__(self, player_id: int, bankroll: int):
        self.player_id = player_id
        self.bankroll = bankroll
        self.hand = []
        self.active = True  # Player is active unless folded or bankrupt
        self.phase_bet = 0
        self.total_game_bet = 0
        self.best_hand = None
        self.ai_flag = False

    def __repr__(self) -> str:
        return f"Player {self.player_id}"
        
    def fold(self) -> None:
        self.active = False

    def bet(self, amount: int) -> bool:
        if amount <= self.bankroll:
            self.total_game_bet += amount
            self.phase_bet += amount
            self.bankroll -= amount
            return True 
        return False

    def reset_round_bet(self):
        self.phase_bet=0

    def add_card(self, card: Card) -> None:
        self.hand.append(card)

class Game:
    '''
    Manages the entire game environment, including deck, players, and community cards.
    Orchestrates the flow of the game through different stages.
    '''
    def __init__(self, players: int):
        self.deck = Deck()
        self.players = [Player(pid, 1000) for pid in range(players)]
        self.dealer_index= 0
        self.community_cards = []
        self.pot = 0
        self.current_player_id = 0  # Track whose turn it is
        self.phase = "Pre-flop"
        self.last_bet = 0
        self.evaluator = HandEvaluator()

    def get_max_phase_bet(self) -> int:
        phase_bets = [p.phase_bet for p in self.players]
        return max(phase_bets)
    
    def next_turn(self) -> None:
        self.current_player_id = (self.current_player_id + 1) % len(self.players)

    def deal_community_card(self) -> None:
        card = self.deck.deal()
        if card:
            self.community_cards.append(card)
        if len(self.community_cards) == 3:
            self.phase = 'Flop'
        elif len(self.community_cards) == 4:
            self.phase = 'Turn'
        elif len(self.community_cards) == 5:
            self.phase = 'River'

    def move_dealer(self) -> None:
        # Move the dealer button to the next active player
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

    def start_new_round(self) -> None:
        self.deck = Deck()  # Reset deck
        self.community_cards = []
        for player in self.players:
            player.hand = []
            player.active = True if player.bankroll > 0 else False
        self.phase = "Pre-flop"
    
    def reset_players_phase_bets(self) -> None:
        for p in self.players:
            if p.active:
                p.reset_round_bet()

    def get_game_state(self) -> dict:
        players_info = [{
            "player_id": player.player_id,
            "bankroll": player.bankroll,
            "hand": [str(card) for card in player.hand],
            "active": player.active,
            "round_bet": player.phase_bet,
            "ai_flag": player.ai_flag,
        } for player in self.players]

        community_cards = [str(card) for card in self.community_cards]

        game_state = {
            "players": players_info,
            "pot": self.pot,
            "community_cards": community_cards,
            "current_player_id": self.current_player_id,
            "phase": self.phase
        }

        return game_state

    def get_small_blind_player(self):
        return self.players[(self.dealer_index + 1) % len(self.players)]

    def get_big_blind_player(self):
        return self.players[(self.dealer_index + 2) % len(self.players)]
    
    def update_game_state(self,action: str, player: Player, amount: int = 0) -> None:
        
        if action == "bet":
            if amount > 0:
                self.pot += amount
        elif action == "fold":
            player.active = False
        elif action == "deal":
            card = self.deck.deal()
            if card:
                player.add_card(card)
    
    def determine_winner(self) -> Player:
        best_hands = {player: self.evaluator.best_hand(player.hand + self.community_cards) for player in self.players if player.active}
        winning_player = max(best_hands.items(), key=lambda x: (x[1][0], x[1][1]))[0]
        return {winning_player: best_hands[winning_player]}

class HandEvaluator:
    def __init__(self):
        # Rank values to compare hands
        self.rank_values = rank_values
        self.hand_rankings = hand_rankings

    def evaluate_hand(self, cards: list) -> tuple:
        values = sorted(self.rank_values[card.value] for card in cards)
        suits = [card.suit for card in cards]
        value_counts = Counter(values)
        is_flush = len(set(suits)) == 1
        is_straight = len(set(values)) == 5 and (values[-1] - values[0] == 4)
        high_card = values[-1]

        if is_flush and is_straight:
            if high_card == 14 and min(values) == 10:  # Check for Royal Flush (A-K-Q-J-10)
                return (9, high_card, "Royal Flush")
            return (8, high_card, "Straight Flush")
        rank, most_common = value_counts.most_common(1)[0]
        if most_common == 4:
            return (7, rank, "Four of a Kind")
        elif most_common == 3:
            if 2 in value_counts.values():
                return (6, rank, "Full House")
            else:
                return (3, rank, "Three of a Kind")
        elif most_common == 2:
            pairs = [rank for rank, count in value_counts.items() if count == 2]
            if len(pairs) > 1:
                return (2, max(pairs), "Two Pair")
            else:
                return (1, pairs[0], "One Pair")
        elif is_flush:
            return (5, high_card, "Flush")
        elif is_straight:
            return (4, high_card, "Straight")
        else:
            return (0, high_card, "High Card")


    def best_hand(self, cards: list) -> tuple:
        # Generates all 5-card combinations from 7 cards and returns the best ranked hand
        return max((self.evaluate_hand(comb) for comb in combinations(cards, 5)), key=lambda x: (x[0], x[1]))