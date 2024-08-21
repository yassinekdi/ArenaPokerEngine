from decorators import verify_game_phase
import unittest
from poker_game_engine.game_engine import Game
from poker_game_engine.action_handlers import ActionHandler
from poker_game_engine.game_logger import GameLogger


class TestPokerPhase(unittest.TestCase):

    def setUp(self):
        self.nb_players = 4
        self.game = Game(players=self.nb_players)
        self.action_handler = ActionHandler(game=self.game,
                                            logger=None)
        self.small_blind = 10
        self.big_blind = 20

        # Start a new round and deal two cards to each player
        self.game.start_new_round()

        # Set up blinds
        self.small_blind_player = self.game.get_small_blind_player()
        self.big_blind_player = self.game.get_big_blind_player()
        self.action_handler.handle_bet(self.small_blind_player, self.small_blind)
        self.action_handler.handle_bet(self.big_blind_player, self.big_blind)

    @verify_game_phase
    def test_scenario1(self):
        # Scenario 1: Player 3 calls, Player 0 calls, Player 1 calls, Player 2 checks
        self.action_handler.handle_call(self.game.players[3])
        self.action_handler.handle_call(self.game.players[0])
        self.action_handler.handle_call(self.game.players[1])
        self.action_handler.handle_check(self.game.players[2])

        # Define the expected results
        expected_results = {
            "bankrolls": [980, 980, 980, 980], # Player 0, 1, 2, 3 bankrolls after bets
            "pot": 80,
            "last_bet": 20,
            "active_players":[True,True,True,True]
        }
        return expected_results

    @verify_game_phase
    def test_scenario2(self):
        # Scenario 2: Player 3 calls, Player 0 calls, Player 1 raises 20, Player 2 calls, Player 3 calls, Player 0 calls
        self.action_handler.handle_call(self.game.players[3])
        self.action_handler.handle_call(self.game.players[0])
        self.action_handler.handle_bet(self.game.players[1], 20)  # Raise by 20
        self.action_handler.handle_call(self.game.players[2])
        self.action_handler.handle_call(self.game.players[3])
        self.action_handler.handle_call(self.game.players[0])

        # Define the expected results
        expected_results = {
            "bankrolls": [970, 970, 970, 970], # Player 0, 1, 2, 3 bankrolls after bets
            "pot": 120,
            "last_bet": 20,
            "active_players":[True,True,True,True]
        }
        return expected_results

    @verify_game_phase
    def test_scenario3(self):
        # Scenario 3: Player 3 calls, Player 0 calls, Player 1 raises 20, Player 2 raises 30, the rest call.
        self.action_handler.handle_call(self.game.players[3])
        self.action_handler.handle_call(self.game.players[0])
        self.action_handler.handle_bet(self.game.players[1], 20)  
        self.action_handler.handle_bet(self.game.players[2], 30)  
        self.action_handler.handle_call(self.game.players[3])  
        self.action_handler.handle_call(self.game.players[0])  
        self.action_handler.handle_call(self.game.players[1])  

        expected_results = {
            "bankrolls": [950, 950, 950, 950],  # Player 0, 1, 2, 3 bankrolls after bets
            "pot": 200,  # Total pot after all calls
            "last_bet": 30 , # Last bet amount was 30
            "active_players":[True,True,True,True]
        }
        return expected_results

    @verify_game_phase
    def test_scenario4(self):
        # Scenario 4: Player 3 calls, Player 0 folds, the rest call.
        self.action_handler.handle_call(self.game.players[3])
        self.action_handler.handle_fold(self.game.players[0])  # Player 0 folds
        self.action_handler.handle_call(self.game.players[1])  # Player 1 calls
        self.action_handler.handle_call(self.game.players[2])  # Player 2 calls

        expected_results = {
            "bankrolls": [1000, 980, 980, 980],  # Player 0's bankroll remains the same; others decrease
            "pot": 60,  # Total pot after calls
            "last_bet": 20,  # Last bet amount was 20,
            "active_players":[False,True,True,True]
        }
        return expected_results

    def test_bet_more_than_bankroll(self):
        is_bet=self.action_handler.handle_bet(self.game.players[1], 2000)
        self.assertFalse(is_bet)

if __name__ == '__main__':
    unittest.main()
