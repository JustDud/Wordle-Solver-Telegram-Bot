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

    return entropy


# Suggests the best next guess by calculating the entropy for each possible guess
def suggest_best_guesses(words: list[str], previous_guesses: list[str]) -> list[str]:
    best_guess_list = []
    for guess in words:
        if guess in previous_guesses:
            continue  # Skip previously guessed words

        entropy = entropy_calculate(words, guess)

        if len(best_guess_list) < 5 and guess:
            best_guess_list.append((entropy,guess))
            best_guess_list.sort(reverse=True, key=lambda x: x[0])
        else:
            if entropy > best_guess_list[-1][0]:
                best_guess_list[-1] = (entropy, guess)
                best_guess_list.sort(reverse=True, key=lambda x: x[0])
    return [guess for _, guess in best_guess_list]


# Update the list of words after the guess based on the clue given
def words_update(words: list[str], guess: str, clue: list[str]) -> list:
    for i in range(len(words) - 1, -1, -1):
        word = words[i]
        valid = True
        green_positions = {j for j in range(5) if clue[j] == "G"}
        yellow_letters = {guess[j] for j in range(5) if clue[j] == "Y"}

        for index_char in range(5):
            if clue[index_char] == "G":
                if guess[index_char] != word[index_char]:
                    valid = False
                    break
            elif clue[index_char] == "Y":
                if guess[index_char] not in word or guess[index_char] == word[index_char]:
                    valid = False
                    break
            elif clue[index_char] == "B":
                if guess[index_char] in word:
                    # Ensure Black is valid unless it's required by a Green/Yellow elsewhere.
                    if not any(guess[index_char] == word[pos] for pos in green_positions):
                        valid = False
                        break
        if not valid:
            words.pop(i)

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


def guess_word_bot(guess: str, clue: list[str]) -> str:
    global words
    global previous_guesses
    previous_guesses.append(guess)
    words_update(words, guess, convert_clue(clue))
    best_guess_list = suggest_best_guesses(words, previous_guesses)
    return best_guess_list[0]


def game_reset():
    global previous_guesses
    global words
    global guess
    global clue
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file]
    previous_guesses = []
    guess = 'crate'
    clue = []
    return None


# accessing the file with words and converting it into a list
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file]

previous_guesses = []


