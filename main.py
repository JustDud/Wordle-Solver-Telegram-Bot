# importing required libraries
import math
import random

global previous_guesses
global words
global guess
global clue
global best_guess_list




# generating the clue (which letters are right and which are not) for the word entered
def generate_clue(guess: str, word: str) -> str:
    """
        Generates a clue for the given guess compared to a single actual word.

        :param guess: The guessed word.
        :param word: The actual word.
        :return: Clue string (e.g., "GBYBB").
        """
    clue = ["B"] * 5  # Start with all Black clues
    word_remaining = list(word)  # Track unused letters in the word

    # First pass: Mark all Greens
    for i in range(5):
        if guess[i] == word[i]:
            clue[i] = "G"  # Mark Green
            word_remaining[i] = None  # Mark as matched and unavailable for Yellow

    # Second pass: Mark Yellows
    for i in range(5):
        if clue[i] == "B" and guess[i] in word_remaining:
            clue[i] = "Y"  # Mark Yellow
            word_remaining[word_remaining.index(guess[i])] = None  # Mark as used

    return "".join(clue)


# The function runs a guess against all possible hidden words and counts clue frequencies
def entropy_calculate(words: list[str], guess: str) -> float:
    clue_frequency = {}

    for word in words:
        clue = generate_clue(guess, word)
        if clue in clue_frequency:
            clue_frequency[clue] += 1
        else:
            clue_frequency[clue] = 1

    entropy = 0.0
    total_words = len(words)

    for frequency in clue_frequency.values():
        probability = frequency/total_words
        entropy -= probability * math.log2(probability)

    # print(f"Entropy calculated: {entropy}")  # Confirm result

    return entropy


# Suggests the best next guess by calculating the entropy for each possible guess
def suggest_best_guesses(words: list[str], previous_guesses: list[str]) -> list[str]:
    best_guess_list = []

    #print("Starting suggest_best_guesses...")  # Debug entry

    for index, guess in enumerate(words):
        if guess in previous_guesses:
            #print(f"Skipping {guess} (already guessed).")  # Debug skip
            continue

        #print(f"Processing guess {index + 1}/{len(words)}: {guess}")  # Progress debug

        entropy = entropy_calculate(words, guess)
        #print(f"Entropy for {guess}: {entropy}")  # Show calculated entropy)

        if len(best_guess_list) < 5:
            best_guess_list.append((entropy, guess))
            best_guess_list.sort(reverse=True, key=lambda x: x[0])
        else:
            if entropy > best_guess_list[-1][0]:
                best_guess_list[-1] = (entropy, guess)
                best_guess_list.sort(reverse=True, key=lambda x: x[0])

    #print(f"Final Best Guess List: {best_guess_list}")
    return [guess for _, guess in best_guess_list]


# Update the list of words after the guess based on the clue given
def words_update(words: list[str], guess: str, clue: list[str]) -> list[str]:
    """
    Updates the list of words based on guess and clue, ensuring correct filtering.

    :param words: List of possible words.
    :param guess: The guessed word.
    :param clue: List of clues for each position ('G', 'Y', 'B').
    :return: Filtered list of words.
    """
    print(f"Updating words based on guess '{guess}' and clue '{clue}'")

    for i in range(len(words) - 1, -1, -1):
        word = words[i]
        valid = True

        for index_char in range(5):
            if clue[index_char] == "G":
                # Green: must match exactly
                if guess[index_char] != word[index_char]:
                    # print(f"  Removing {word}: Green mismatch at {index_char}")
                    valid = False
                    break

            elif clue[index_char] == "Y":
                # Yellow: must exist but not in the same position
                if guess[index_char] not in word or word[index_char] == guess[index_char]:
                    # print(f"  Removing {word}: Yellow mismatch at {index_char}")
                    valid = False
                    break

            elif clue[index_char] == "B":
                # Black: letter must not appear, unless required for Green or Yellow positions
                if guess[index_char] in word:
                    if any(
                        word[pos] == guess[index_char] and clue[pos] in ["G", "Y"]
                        for pos in range(5)
                    ):
                        continue  # Letter is valid due to other clue
                    # print(f"  Removing {word}: Black mismatch at {index_char}")
                    valid = False
                    break

        if not valid:
            words.pop(i)

    print(f"Remaining words after update: {words}")
    return words


def convert_clue(clue_passed: list[str]) -> list[str]:
    clue = []
    for clue_char in clue_passed:
        if clue_char == '0':
            clue.append('B')
        elif clue_char == '1':
            clue.append('Y')
        else:
            clue.append('G')
    return clue


def get_different_words(words: list[str], best_guess_list: list[str]):
    removed_word = best_guess_list[0]
    if removed_word in words:
        words.remove(removed_word)
    return suggest_best_guesses(words, previous_guesses)


def solve_wordle(clue: list[str], first_guess: bool, change_word: bool):
    global words
    global previous_guesses
    global best_guess_list
    global clue_save

    if clue:
        clue_save = clue  # Save the latest clue

    if first_guess:
        # Load the word list and initialize guesses
        with open('words.txt', 'r') as file:
            words = [line.strip() for line in file]
        previous_guesses = ['crate']
        best_guess_list = ['crate']
        return

    if change_word:
        print("Entered Change Word Block")
        print(f"Before Change: Best Guess List: {best_guess_list}, Previous Guesses: {previous_guesses}")

        # Get the next best guesses and reset the logic
        best_guess_list = get_different_words(words, best_guess_list)

        if not best_guess_list:
            print("No valid guesses available after changing word.")
            return None

        # Use the new guess
        new_guess = best_guess_list[0]
        print(f"New Guess after Change: {new_guess}")
        previous_guesses.append(new_guess)

        # Re-filter using the saved clue for consistency
        words = words_update(words, new_guess, convert_clue(clue_save))

        if not words:
            print("No valid words remain after update.")
            return None

        print(f"Words Remaining After Update: {len(words)}")
        return new_guess

    # Handle normal flow after initial rounds
    words = words_update(words, best_guess_list[0], convert_clue(clue))

    if not words:
        print("No valid words remain after words_update.")
        return None

    best_guess_list = suggest_best_guesses(words, previous_guesses)

    if not best_guess_list:
        print("No guesses available after suggest_best_guesses.")
        return None

    previous_guesses.append(best_guess_list[0])
    return best_guess_list[0]
