from poker_game_engine.game_engine import Game
from poker_game_engine.action_handlers import ActionHandler
from poker_game_engine.game_logger import GameLogger

def get_player_input(player,game_last_bet):
    amount=0
    choice = input("Enter your choice 1: Fold, 2: Bet, 3: Check, 4: Call ")
    if choice=="2":
        amount = int(input("Enter bet amount: "))
    elif choice == "4":
        amount = max(game_last_bet - player.total_game_bet,0)
    return (choice,amount)
   
            
def handle_betting_round(game, logger, action_handler, nb_players, current_index):
    new_bet_made = True 
    
    while new_bet_made:
        new_bet_made = False  # Assume no new bets at the start of each pass
        for _ in range(nb_players):  # Loop through all players
            player = game.players[current_index]
            if player.active and (player.phase_bet <= game.last_bet or player.phase_bet == 0):
                logger.log_info(f"Player {player.player_id}'s turn. Bankroll: {player.bankroll}, Bet to Call: {game.get_max_phase_bet()}")
                valid_action = False
                while not valid_action:
                    choice, amount = get_player_input(player, game.last_bet)
                    valid_action = action_handler.player_action_input(player, choice, amount)
                    if valid_action and choice == '2' and player.phase_bet > game.last_bet:
                        new_bet_made = True  # A new bet or raise has been made
                        game.last_bet = player.phase_bet  # Update the last highest bet to this new amount
                        # last_aggressor_index = current_index  # Update the last aggressor
            current_index = (current_index + 1) % nb_players

        if new_bet_made:
            # Ensure that the cycle continues until it reaches the player right after the last aggressor
            new_bet_made = True



def run_game_simulation():
    nb_players = 4
    game = Game(players=nb_players)
    logger = GameLogger(game=game,
                        log_to_console=True,
                        log_to_file=False)
    action_handler = ActionHandler(game=game,
                                   logger=logger)
    
    # Log game start
    logger.log_event(f"Game started with {nb_players} players.")
    
    # Simulate several rounds
    for round in range(2):  # simulate 5 rounds
        logger.log_event(f"Starting round {round + 1}")
        game.start_new_round()
        
        # Blinds -----------------------------------
        small_blind = 10
        big_blind = 20
        logger.log_event(f"Blinding..")
        
        # Small blind
        small_blind_player = game.get_small_blind_player()
        action_handler.handle_bet(small_blind_player, small_blind)
        logger.log_info(f"Small blind by {small_blind_player}, of : {small_blind}")
        
        # Big blind
        big_blind_player = game.get_big_blind_player()
        action_handler.handle_bet(big_blind_player, big_blind)
        logger.log_info(f"Big blind by {big_blind_player}, of : {big_blind}")

        # Deal 2 cards to each player ------------------------
        logger.log_event(f"Dealing first cards..")
        for player in game.players:
            if player.active:
                action_handler.handle_deal_card(player)
                action_handler.handle_deal_card(player)
  

        # PHASE 1 : PREFLOP ---------------------------
        logger.log_event(f"Preflop betting..")
        start_index = (game.dealer_index + 3) % nb_players
        current_index = start_index
        # last_aggressor_index = game.dealer_index + 2
        
        handle_betting_round(game, logger, action_handler, nb_players,current_index)
        
        
        action_handler.deal_community_cards(3)
        logger.log_community_cards()
        logger.log_phase()
        game.reset_players_phase_bets()
        
        # PHASE 2 : FLOP --------------------------
        logger.log_event(f"Flop..")
        handle_betting_round(game, logger, action_handler, nb_players,current_index)
        
        
        action_handler.deal_community_cards(1)
        logger.log_community_cards()
        logger.log_phase()
        game.reset_players_phase_bets()
        
        # PHASE 3: Turn ---------------------------------
        logger.log_event(f"Turn..")
        handle_betting_round(game, logger, action_handler, nb_players,current_index)
        
        
        action_handler.deal_community_cards(1)
        logger.log_community_cards()
        logger.log_phase()
        game.reset_players_phase_bets()
        
        # PHASE 4 : River --------------------------------------
        logger.log_event(f"River..")
        handle_betting_round(game, logger, action_handler, nb_players,current_index) 
        
        # Log end of round
        logger.log_event(f"Ending round {round + 1}")
        logger.log_community_cards()
        logger.log_game_state()
        game.reset_players_phase_bets()

        # Move dealer
        game.move_dealer()



run_game_simulation()

