import random

# Words used by the game. You can add more words to this list.
WORDS = [
    "python", "computer", "programming", "keyboard", "internet",
    "science", "hangman", "student", "software", "developer"
]

# Hangman drawings: index 0 is the empty gallows; index 6 is game over.
HANGMAN_PICTURES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]


def display_game(secret_word, correct_guesses, wrong_guesses):
    """Display the current gallows, masked word, and guessed letters."""
    print(HANGMAN_PICTURES[len(wrong_guesses)])

    masked_word = ""
    for letter in secret_word:
        if letter in correct_guesses:
            masked_word += letter + " "
        else:
            masked_word += "_ "

    print("Word:             ", masked_word)
    print("Correct guesses:  ", " ".join(sorted(correct_guesses)) or "None")
    print("Incorrect guesses:", " ".join(wrong_guesses) or "None")
    print("Attempts left:    ", 6 - len(wrong_guesses))


def play_game():
    """Run one complete round of Hangman."""
    secret_word = random.choice(WORDS)
    correct_guesses = set()
    wrong_guesses = []

    print("\n===================================")
    print("       HANGMAN WORD GAME")
    print("===================================")
    print("Guess the hidden word one letter at a time.")
    print("You can make up to 6 incorrect guesses.")

    while len(wrong_guesses) < 6:
        display_game(secret_word, correct_guesses, wrong_guesses)

        # Check whether all letters have been guessed.
        if all(letter in correct_guesses for letter in secret_word):
            print("\nCongratulations! You guessed the word:", secret_word)
            print("YOU WIN!")
            return

        guess = input("\nEnter one letter: ").strip().lower()

        # Validate the user's input.
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter exactly one alphabet letter.")
            continue

        # A repeated guess must not cost an attempt.
        if guess in correct_guesses or guess in wrong_guesses:
            print("You already guessed that letter. Try another one.")
            continue

        if guess in secret_word:
            correct_guesses.add(guess)
            print("Correct guess!")
        else:
            wrong_guesses.append(guess)
            print("Incorrect guess!")

    # Show the final drawing and reveal the word after 6 mistakes.
    display_game(secret_word, correct_guesses, wrong_guesses)
    print("\nGAME OVER! You used all 6 incorrect attempts.")
    print("The correct word was:", secret_word)


def main():
    """Ask the user whether to play another round."""
    while True:
        play_game()
        again = input("\nWould you like to play again? (y/n): ").strip().lower()

        if again != "y":
            print("\nThank you for playing Hangman. Goodbye!")
            break


if __name__ == "__main__":
    main()

