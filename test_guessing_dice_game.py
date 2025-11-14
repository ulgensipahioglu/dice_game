import unittest
from guessing_dice_game import GameManager

class TestGame(unittest.TestCase):
    
    
    def setUp(self):
        self.manager = GameManager() #Create a new game before each test
        self.manager.scores = []  # Do not touch real file
        

    # Check if the correct number of dice are rolled
    def test_roll_dice_length(self):
        total, rolls = self.manager.roll_dice(3)
        self.assertEqual(len(rolls),3)
        
        
    # All dice results between 1 and 6
    def test_roll_dice_range(self):
        total, rolls = self.manager.roll_dice(5)
        for r in rolls:
            self.assertTrue(1 <= r <= 6)
        

    # Perfect guess should return max points (difference is 0 )
    def test_calculate_guess_score(self):
        score = self.manager.calculate_guess_score(10,10,20)
        self.assertEqual(score, 20) 
        
    # Save score
    def test_add_score_saves(self):
        self.manager.add_score("Ülgen", 12, 3, 11)
        self.assertEqual(len(self.manager.scores), 1)
        entry = self.manager.scores[0]
        self.assertEqual(entry["name"], "Ülgen")
        self.assertEqual(entry["score"], 12)

    def test_get_high_scores_sorted(self):
        self.manager.scores = [
            {"name": "A", "score": 2},
            {"name": "B", "score": 10},
            {"name": "C", "score": 5}
        ]
        sorted_scores = self.manager.get_high_scores()
        # highest score first
        self.assertEqual(sorted_scores[0]["name"], "B")
        self.assertEqual(sorted_scores[1]["name"], "C")
        self.assertEqual(sorted_scores[2]["name"], "A")
        
        
if __name__ == '__main__':
    unittest.main()
    
