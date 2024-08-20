from functools import wraps

def verify_game_phase(test_func):
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        # Run the original test function
        expected_results = test_func(self, *args, **kwargs)
        
        # After running the test, verify the expected game state
        actual_bankrolls = [player.bankroll for player in self.game.players]
        active_players = [player.active for player in self.game.players]
        actual_pot = self.game.pot
        actual_last_bet = self.game.last_bet
        
        self.assertEqual(actual_bankrolls, expected_results["bankrolls"])
        self.assertEqual(actual_pot, expected_results["pot"])
        self.assertEqual(actual_last_bet, expected_results["last_bet"])
        self.assertEqual(active_players, expected_results["active_players"])
    
    return wrapper

