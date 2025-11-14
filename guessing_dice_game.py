import json
import random
import os

# file to store results
DATA_FILE = "scores.json" 


# This class handles the game calculations and saves the scores
class GameManager:
    
    # Initializes the game and loads any existing scores
    def __init__(self):
        self.scores = self._load_data()
    
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
        rolls = [random.randint(1, sides) 
            for _ in range(num_dice)]
        # num_dice: How many dice to roll
        # sides: How many sides the die has (default 6)
        # Rolls 1 to sides for num_dice times
        total_score = sum(rolls)
        return total_score, rolls
        
     # The main formula for calculating the score: The closer the guess, the better the score.
    def calculate_guess_score(self, total_roll, user_guess, max_possible_score):
        # Find the absolute difference between the actual result and the guess
        difference = abs(total_roll - user_guess)
        max_point = max_possible_score
        # Score = Max Points - Difference. If difference is 0, max points are achieved
        final_score = max(0, max_point - difference) #Take the big one
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
    def get_high_scores(self):
        # Sorts scores from high to low based on score
        sorted_scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)
        return sorted_scores

        
class TerminalIO: #input/output
    # This class only handles writing to the screen and getting input from the user
    # Game logic is not here
    
    @staticmethod
    # REMINDER: This method doesn't need 'self' because it doesn't use any class data.
    # It just takes input and returns a value, making it independent and clean.
    def get_user_input_int(prompt, min_val=1, max_val=100):
        # Asks the user for a number and keeps trying until correct
        while True:
            try:
                user_input = input(prompt)
                value = int(user_input)
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Invalid value. Please enter a number between {min_val} and {max_val}.")
            except ValueError: #if value type is not int
                print("That wasn't a number! Please try again.")

    @staticmethod
    # REMINDER: This method doesn't need 'self' either. It only prints the data it receives
    def display_summary(scores):
        print("\n" "PREVIOUS HIGH SCORES (Guessing Game)")
        print("-" * 70)
        if not scores: #if scores is empty
            print("No scores saved yet.")
            print("-" * 70)

            return #method ends
    
        print(f"{'Name'} | {'Score'} | {'Dice Count'} | {'Guess'}")    
        print("-" * 70)

        for i, entry in enumerate(scores):
            # Checks for missing data to prevent errors
            dice_info = entry.get('dice_count', 'Unknown') #don't give error, write unknown
            guess_info = entry.get('user_guess', 'Unknown') #don't give error, write unknown
            
            print(f"{entry.get('name', 'Anonymous')} |  {entry.get('score', 0)}  |  {dice_info}  |  {guess_info}") #don't give error, write Anonymous
            if i >= 2: # Show only the top 3
                break
        print("-" * 70)
        
    @staticmethod
    # REMINDER: This method is also static, as it only asks a question and returns a True/False answer
    # Asks the user "we play again?"
    def prompt_restart():
        while True: #if answer is not yes or no, loop keeps going
            restart = input("\nDo you want to play again? (yes/no): ")
            if restart == 'yes':
                return True
            elif restart == 'no':
                print("\nThank you for playing! The program is shutting down.")
                return False
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")
                
# Runs one complete round of the game.
def run_game_session(manager):
    
    # PHASE 1: Start
    print("-" * 70)
    print("WELCOME TO THE GUESSING DICE GAME!")
    print("-" * 70)
    
    TerminalIO.display_summary(manager.get_high_scores())
    
    player_name = input("Enter your name: ")
    if not player_name:
        player_name = "Anonymous"
    
    
    #CONSTANTS
    DICE_SIDES = 6
    MIN_DICE = 1
    MAX_DICE = 5   
                
    # PHASE 2: Interactive Choice Steps

    # Choice Step 1: Number of Dice
    num_dice = TerminalIO.get_user_input_int(
        prompt=f"How many dice do you want to roll? ({MIN_DICE}-{MAX_DICE}): ",
        min_val=MIN_DICE,
        max_val=MAX_DICE
        )
    min_possible_score = num_dice * 1
    max_possible_score = num_dice * DICE_SIDES

    # Choice Step 2: The Guess
    user_guess = TerminalIO.get_user_input_int(
        prompt=f"What is your guess for the total score? (between {min_possible_score} and {max_possible_score}): ",
        min_val=min_possible_score,
        max_val=max_possible_score
        )
        
    print(f"\nRolling {num_dice} dice...")

    # PHASE 3: Result
    # Roll the dice
    total_roll, rolls = manager.roll_dice(num_dice, DICE_SIDES)
        
    # Calculate final score based on guess proximity
    final_score = manager.calculate_guess_score(total_roll, user_guess, max_possible_score)
        
    print(f"ROLL RESULT: {rolls} (Total: {total_roll})")
    print(f"YOUR GUESS: {user_guess}")
    print(f"DIFFERENCE: {abs(total_roll - user_guess)}")
    print(f"CONGRATULATIONS, {player_name.upper()}!")
    print(f"Your Score is: {final_score} (Max possible score: {max_possible_score})")
    print("\n" + "-" * 70)
        
    # Save the result
    manager.add_score(player_name, final_score, num_dice, user_guess)
    print("Your score has been saved!") 


def main():
    game_manager = GameManager() 
    while True:
        run_game_session(game_manager)
    
        # Ask for restart
        if not TerminalIO.prompt_restart():
            break
    

if __name__ == "__main__":
    main()
