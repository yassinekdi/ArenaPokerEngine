import unittest
from poker_game_engine.game_engine import Game
from poker_game_engine.action_handlers import ActionHandler
from poker_game_engine.game_logger import GameLogger
from decorators import verify_game_phase

class TestPokerRound(unittest.TestCase):

    def setUp(self):
        self.nb_players = 4
        self.game = Game(players=self.nb_players)
        self.logger = GameLogger(game=self.game,
                                 log_to_console=False,
                                 log_to_file=False)
        self.action_handler = ActionHandler(game=self.game,
                                            logger=self.logger)
        self.small_blind = 10
        self.big_blind = 20

        # Start a new round and deal two cards to each player
        self.game.start_new_round()

        # Set up blinds
        self.small_blind_player = self.game.get_small_blind_player()
        self.big_blind_player = self.game.get_big_blind_player()
        self.action_handler.handle_bet(self.small_blind_player, self.small_blind)
        self.action_handler.handle_bet(self.big_blind_player, self.big_blind)

        # Deal hole cards to each player
        for player in self.game.players:
            self.action_handler.handle_deal_card(player)
            self.action_handler.handle_deal_card(player)

    @verify_game_phase
    def test_round(self):
        # Pre-flop action (all players call)
        for player in self.game.players:
            if player.phase_bet < self.game.last_bet:
                self.action_handler.handle_call(player)

        # Flop phase: deal 3 community cards
        self.action_handler.deal_community_cards(3)

        # Player 2 bets 20 during the flop phase
        self.action_handler.handle_bet(self.game.players[2], 20)

        # Remaining players call the bet
        for player in self.game.players:
            if player != self.game.players[2]:
                self.action_handler.handle_call(player)

        # Turn phase: deal 1 community card
        self.action_handler.deal_community_cards(1)

        # All players check (no further bets)
        for player in self.game.players:
            self.action_handler.handle_check(player)

        # River phase: deal 1 community card
        self.action_handler.deal_community_cards(1)

        # All players check again (no further bets)
        for player in self.game.players:
            self.action_handler.handle_check(player)

        # Expected results after all phases
        expected_results = {
            "bankrolls": [960, 960, 960, 960],  # Adjusted for the bet by Player 2 and calls by others
            "pot": 160,  
            "last_bet": 20,
            "active_players":[True,True,True,True]
        }
        return expected_results

if __name__ == '__main__':
    unittest.main()
