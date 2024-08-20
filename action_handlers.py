from game_engine import Player, Game
from game_logger import GameLogger
from constants import actions_vals

class ActionHandler:
    '''
    Manages the actions that players can take during the game, updating the game state accordingly.
    '''

    def __init__(self, game: Game, logger: GameLogger) -> None:
        self.game = game 
        self.logger = logger 

    def handle_fold(self, player: Player) -> None:
        '''
        Handles the action of a player folding their hand, setting their active status to False.
        '''
        player.fold()
        self.game.next_turn()

    def handle_bet(self, player: Player, amount: int) -> None:
        '''
        Handles the action of a player betting an amount, deducting the amount from their bankroll,
        adding it to their current bet, and updating the game's pot.
        '''
        minimum_raise = self.game.last_bet
        if amount >= minimum_raise:
            if player.bet(amount):
                self.game.pot += amount
                self.game.last_bet = amount
                self.game.next_turn()
                return True
        return False

    def handle_check(self, player: Player) -> None:
        '''
        Handles the action of a player checking
        '''
        self.game.next_turn()

    def handle_call(self, player: Player) -> bool:
        max_bet = self.game.get_max_phase_bet()
        call_amount = max(max_bet - player.total_game_bet,0)
        if player.bet(call_amount):
            self.game.pot += call_amount
            self.game.next_turn()
            return True
        return False

    def handle_deal_card(self, player: Player) -> None:
        '''
        Deals a card to a player if the deck is not empty.
        '''
        card = self.game.deck.deal()
        if card:
            player.add_card(card)

    def deal_community_cards(self, number_of_cards: int) -> None:
        '''
        Deals a specified number of community cards to the table, typically used for the flop, turn, and river in Texas Hold'em.
        '''
        for _ in range(number_of_cards):
            self.game.deal_community_card()

    def player_action_input(self, player: Player,choice: str, amount_bet=0) -> bool:
        '''
        Prompts the player for their action and processes it.
        '''
        if choice == '1':
            self.handle_fold(player)
            return True
            
        elif choice == '2':
            bet_handled=self.handle_bet(player, amount_bet)
            if not bet_handled :
                self.logger.log_warning("Bet failed, not enough bankroll. Try a different action.")
                return False            

        elif choice == '3':
            if not self.can_player_check(player):
                self.logger.log_warning("Check is not permissible. There's a bet to match.")
                return False
        
        elif choice == '4':
            if not self.handle_call(player):
                self.logger.log_warning("Call failed, not enough bankroll or incorrect call amount.")
                return False 
                
        else:
            self.logger.log_warning("Invalid choice. Please choose again.")
            return False
        
        self.logger.log_player_action(action=actions_vals[choice],amount=amount_bet)
        return True
        

    def can_player_check(self, player: Player):
        # Check if any player has placed a bet that hasn't been matched yet
        round_bet = player.phase_bet
        for p in self.game.players:
            if p.phase_bet != round_bet:
                return False
        return True