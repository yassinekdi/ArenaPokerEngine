import logging
from game_engine import Game

class GameLogger:
    '''
    Provides functionality to log important game events and performance metrics.
    This includes player actions, game state changes, and statistical data relevant to evaluating strategies and outcomes.
    '''
    def __init__(self, game: Game, log_to_console: bool = False, log_to_file: bool = True):
        self.game = game

        # Configure logging handlers based on the specified arguments
        handlers = []
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            handlers.append(console_handler)
        
        if log_to_file:
            file_handler = logging.FileHandler('game_logs.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            handlers.append(file_handler)
        
        # Setting up the root logger with the handlers
        logging.basicConfig(level=logging.INFO, handlers=handlers)

    @staticmethod
    def log_event(message: str) -> None:
        logging.info(message+"\n")

    @staticmethod
    def log_info(message: str) -> None:
        logging.info(message)
        
    @staticmethod
    def log_warning(message: str) -> None:
        logging.warning(message)
    
    def get_current_player_id(self) -> int:
        return self.game.current_player_id

    def log_phase(self) -> None:
        logging.info(f" --- Game phase: {self.game.phase} --- ")

    def log_player_action(self, action: str, amount: int = 0) -> None:
        current_player_id = self.get_current_player_id()
        if "bet" in action.lower():
            logging.info(f"Player {current_player_id} performed action: {action} with amount: {amount}")
        if "fold" in action.lower():
            logging.info(f"Player {current_player_id} performed action: {action}")
        if "check" in action.lower():
            logging.info(f"Player {current_player_id} performed action: {action}")

    def log_game_state(self) -> None:
        active_players = len([p for p in self.game.players if p.active])
        community_cards = ', '.join(str(card) for card in self.game.community_cards)
        logging.info(f"Current pot: {self.game.pot}, Active Players: {active_players}, Community Cards: {community_cards}")

    def log_community_cards(self) -> None:
        community_cards = self.game.community_cards
        logging.info(f"\nCommunity cards: {community_cards}\n")

    def log_performance_metrics(self) -> None:
        pass  # Implement as needed
