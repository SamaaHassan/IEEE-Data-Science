import random
from config import GAME_CONFIG

def get_level_settings(choice):
    """Returns the settings for the selected level."""
    return GAME_CONFIG.get(str(choice))

def generate_secret_number(limit):
    """Generates a random number within the given limit."""
    return random.randint(1, limit)

def process_guess(user_guess, secret_number):
    """
    Core Logic: Compares the user's guess with the secret number.
    Returns: 'win', 'increase', or 'decrease'.
    """
    if user_guess == secret_number:
        return "win"
    elif user_guess < secret_number:
        return "increase"
    else:
        return "decrease"

def validate_input(user_input):
    """Checks if the input is a valid positive integer."""
    return user_input.isdigit()