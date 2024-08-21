import unittest
from poker_game_engine.game_engine import Card, HandEvaluator

class TestHandEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = HandEvaluator()

    def test_high_card(self):
        cards = [Card('Hearts', '7'), Card('Diamonds', '5'), Card('Clubs', '2'), Card('Spades', '9'), Card('Hearts', 'J')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (0, 11, "High Card"))

    def test_one_pair(self):
        cards = [Card('Hearts', '7'), Card('Diamonds', '7'), Card('Clubs', '2'), Card('Spades', '9'), Card('Hearts', 'J')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (1, 7,"One Pair"))

    def test_two_pair(self):
        cards = [Card('Hearts', '7'), Card('Diamonds', '7'), Card('Clubs', '9'), Card('Spades', '9'), Card('Hearts', 'J')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (2, 9,"Two Pair"))

    def test_three_of_a_kind(self):
        cards = [Card('Hearts', '7'), Card('Diamonds', '7'), Card('Clubs', '7'), Card('Spades', '9'), Card('Hearts', 'J')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (3, 7,"Three of a Kind"))

    def test_straight(self):
        cards = [Card('Hearts', '3'), Card('Diamonds', '4'), Card('Clubs', '5'), Card('Spades', '6'), Card('Hearts', '7')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (4, 7,"Straight"))

    def test_flush(self):
        cards = [Card('Hearts', '2'), Card('Hearts', '5'), Card('Hearts', '9'), Card('Hearts', 'J'), Card('Hearts', '7')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (5, 11,"Flush"))

    def test_full_house(self):
        cards = [Card('Hearts', '7'), Card('Diamonds', '7'), Card('Clubs', '9'), Card('Spades', '9'), Card('Hearts', '9')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (6, 9,"Full House"))

    def test_four_of_a_kind(self):
        cards = [Card('Hearts', '9'), Card('Diamonds', '9'), Card('Clubs', '9'), Card('Spades', '9'), Card('Hearts', '7')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (7, 9,"Four of a Kind"))

    def test_straight_flush(self):
        cards = [Card('Hearts', '3'), Card('Hearts', '4'), Card('Hearts', '5'), Card('Hearts', '6'), Card('Hearts', '7')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (8, 7,"Straight Flush"))

    def test_royal_flush(self):
        cards = [Card('Hearts', '10'), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K'), Card('Hearts', 'A')]
        self.assertEqual(self.evaluator.evaluate_hand(cards), (9, 14,"Royal Flush"))

if __name__ == '__main__':
    unittest.main()
