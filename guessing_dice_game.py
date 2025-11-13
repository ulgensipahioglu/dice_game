import json
import random
import os

# Constant file name. Values that should not change during program execution are written in capital letters
DATA_FILE = "scores.json" 


# This class handles the game calculations and saves the scores
class GameManager:
    
    # Initializes the game and loads any existing scores
    def __init__(self):
        self.scores = self._load_data()
    
        
        '''
        REMINDER
        Methods preceded by a single underscore (_) are internal/helper methods (like private in Java)
        That MUST NOT be called from outside the class.
        These are used only to assist other methods within the class (e.g., __init__ or add_score)
       '''
    #Reads saved scores from the file. Handles missing or corrupt files
    def _load_data(self):
        try:
            # Checks if the file exists and is not empty
            if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
                return [] #return empty
            #else open scores file, just "read(r)" and add '"utf-8" for special characters. My name is Ülgen :)
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f) #return the scores list
        except FileNotFoundError:
            # No problem if the file doesn't exist
            return [] #return empty
        except json.JSONDecodeError:
            # Catches corrupt or incorrect file format
            print("Warning: scores.json could not be read (corrupt or incorrect file format).")
            return [] #return empty
        
    # Writes the current score list to the file
    def _save_data(self):
        #open scores file, write(w) and add '"utf-8" for special characters
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            # take the score list
            # edit it with 4 space indent
            # save it to the file we opened
            # while preserving special characters(åöäçü)
            json.dump(self.scores, f, indent=4, ensure_ascii=False) 
            
    # Simulates dice rolling
    def roll_dice(self, num_dice, sides = 6):
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        # num_dice: How many dice to roll
        # sides: How many sides the die has (default 6)
        # Rolls 1 to sides for num_dice times
        total_score = sum(rolls)
        return total_score, rolls #in a tuple
        
     # The main formula for calculating the score: The closer the guess, the better the score
    def calculate_guess_score(self, total_roll, user_guess, max_possible_score):
        # Find the absolute difference between the actual result and the guess
        difference = abs(total_roll - user_guess)
        max_point = max_possible_score
        # Score = Max Points - Difference. If difference is 0, max points are achieved.
        final_score = max(0, max_point - difference) #Take the maximum of two numbers
        return final_score
    
    # Adds a new score to the list and saves the file     
    def add_score(self, name, score, num_dice, guess):
        new_entry = {
            "name": name,
            "score": score,
            "dice_count": num_dice,
            "user_guess": guess
        }
        self.scores.append(new_entry)
        self._save_data()
        
    # Finds and sorts the highest scores
    def high_scores(self):
        # Sorts scores from high to low based on score
        sorted_scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)
        return sorted_scores

        
class TerminalIO: #input/output