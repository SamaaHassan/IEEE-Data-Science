from game_logic import get_level_settings, generate_secret_number, process_guess, validate_input

def start_game():
    print("***** Welcome to the Smart Guessing Game *****")
    print("Levels: (1) Easy, (2) Intermediate, (3) Hard")
    
    while True:
            choice = input("Select level (1 , 2 , 3 ): ")
            settings = get_level_settings(choice)
    
            if settings:
              break
            else:
              print("Invalid choice! This level does not exist. Please choose from 1, 2, or 3.")

    secret_num = generate_secret_number(settings['limit'])
    max_trials = settings['max_trials'] 
    
    print(f"\nMode: {settings['name']} (Range: 1-{settings['limit']})")
    
    for i in range(1, max_trials + 1):
        user_input = input(f"\nAttempt {i}/{max_trials} - Enter your guess: ")
        
        if not validate_input(user_input):
            print("Invalid input! Please enter a number.")
            continue
            
        result = process_guess(int(user_input), secret_num)
        
        if result == "win":
            print(f"Congratulations! You guessed it in {i} trials. 🎉")
            return
        else:
            # calac number of reminder tring
            remaining = max_trials - i
            
            if result == "increase":
                print("Wrong! No, Increase! ⬆️")
            else:
                print("Wrong! No, Decrease! ⬇️")
            
            # if we have tring print it 
            if remaining > 0:
                print(f"Be careful! You only have {remaining} attempts left.")
            
    print(f"\n💥 Game Over! You've used all attempts. The number was: {secret_num}")

if __name__ == "__main__":
    start_game()