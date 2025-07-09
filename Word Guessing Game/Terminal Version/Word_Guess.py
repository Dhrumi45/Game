# Importing the 'random' module to select a random letter
import random

# Importing the 'string' module to get the list of uppercase letters
import string

# Defining the main function for the letter guessing game
def guess_letter_game():
    # This loop allows the player to play multiple rounds
    while True:
        # Randomly selecting one uppercase letter as the secret letter
        secret_letter = random.choice(string.ascii_uppercase)
        
        # Initializing the number of attempts to 0
        attempts = 0

        # Display a message to start the guessing
        print("\nGuess the secret letter (A–Z)!")
        
        # Inner loop for making guesses until the correct letter is guessed
        while True:
            # Asking the user to input a guess, removing whitespace, and converting to uppercase
            guess = input("Enter your guess: ").strip().upper()
            
            # Increment the attempt counter by 1
            attempts += 1

            # Check if the input is a single uppercase letter
            if len(guess) != 1 or guess not in string.ascii_uppercase:
                # If input is invalid, display error message and prompt again
                print("Invalid input. Please enter a single letter (A–Z).")
                continue  # Skip the rest and go to the next iteration

            # If guess is alphabetically before the secret letter
            if guess < secret_letter:
                print("Too low in the alphabet! Try a later letter.")
            # If guess is alphabetically after the secret letter
            elif guess > secret_letter:
                print("Too high in the alphabet! Try an earlier letter.")
            # If guess matches the secret letter
            else:
                # Congratulate the user and show number of attempts
                print(f"🎉 Correct! The secret letter was '{secret_letter}'.")
                print(f"You guessed it in {attempts} attempt(s).")
                break  # Exit the inner guessing loop

        # Ask if the user wants to play another round
        play_again = input("Do you want to play again? (Y/N): ").strip().upper()
        
        # If user inputs anything other than 'Y', end the game
        if play_again != 'Y':
            print("Thanks for playing! Goodbye.")
            break  # Exit the outer loop and end the function

# Call the function to run the game
guess_letter_game()
