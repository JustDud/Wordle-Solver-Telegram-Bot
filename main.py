# importing required libraries
import math
import random

global previous_guesses
previous_guesses = []

with open('words.txt', 'r') as file:
    words = [line.strip() for line in file]


# generating the clue (which letters are right and which are not) for the word entered
def generate_clue(guess: str, word: str) -> str:
    clue = []

    for guess_char, word_char in zip(guess, word):
        if guess_char == word_char:
            # Appending G which stands for Green
            clue.append("G")
        elif guess_char in secret_word:
            # Appending Y which stands for Yellow
            clue.append("Y")
        else:
            # Appending B which stands for Black (Not grey as G is taken)
            clue.append("B")

    return ''.join(clue)


# The function runs a guess against all possible hidden words and counts clue frequencies
def entropy_calculate(words: list[str], guess: str) -> float:
    clue_frequency = {}

    for word in words:
        clue = generate_clue(guess, word)
        # print(clue)
        if clue in clue_frequency:
            clue_frequency[clue] += 1
        else:
            clue_frequency[clue] = 1

    entropy = 0
    total_words = len(words)

    for frequency in clue_frequency.values():
        probability = frequency/total_words
        entropy -= probability * math.log2(probability)

    return entropy


# Suggests the best next guess by calculating the entropy for each possible guess
def suggest_best_guess(words: list[str], previous_guesses: list[str]) -> str:
    best_guess = None
    max_entropy = -1

    for guess in words:
        if guess in previous_guesses:
            continue  # Skip previously guessed words

        entropy = entropy_calculate(words, guess)
        if entropy > max_entropy:
            max_entropy = entropy
            best_guess = guess

    return best_guess

# Update the list of words after the guess based on the clue given
def words_update(words: list[str], guess: str, clue: str) -> list:



    # clue_list = list(clue)  # Convert clue string to a list
    # print(f"Clue words update {clue_list}")
    # print(guess)
    #
    # clue_list = list(clue)  # Convert clue string to list
    #
    # # Precompute constraints for efficient lookup
    # greens = {i: guess[i] for i in range(5) if clue_list[i] == "G"}
    # yellows = {guess[i] for i in range(5) if clue_list[i] == "Y"}
    # blacks = {guess[i] for i in range(5) if clue_list[i] == "B"}
    #
    # def is_word_valid(word: str) -> bool:
    #     """
    #     Efficiently validates if the word matches the guess and clue constraints.
    #
    #     :param word: Word to check
    #     :return: True if the word is valid, False otherwise
    #     """
    #     # Check for Greens (exact match positions)
    #     for i, char in greens.items():
    #         if word[i] != char:
    #             return False
    #
    #     # Check for Yellows (present but not in the same position)
    #     for i in range(5):
    #         if clue_list[i] == "Y":
    #             if guess[i] not in word or word[i] == guess[i]:
    #                 return False
    #
    #     # Check for Blacks (must not be present anywhere in the word)
    #     for char in blacks:
    #         if char in word:
    #             return False
    #
    #     # Also ensure all yellows exist in the word
    #     if not yellows.issubset(set(word)):
    #         return False
    #
    #     return True
    #
    # # Modify the original list in place
    # words[:] = [word for word in words if is_word_valid(word)]
    # return words

    for word in words[:]:
        if word == "apple":
            print("APPLE")
        for index_char in range(5):

            if clue[index_char] == "G" and guess[index_char] != word[index_char]:
                if word == "apple":
                    print("APPLE")
                    print(clue[index_char], guess[index_char])
                words.remove(word)
                break

            elif clue[index_char] == "Y" and guess[index_char] not in word:
                if word == "apple":
                    print("APPLE")
                    print(clue[index_char], guess[index_char])
                words.remove(word)
                break

            elif clue[index_char] == "B" and guess[index_char] in word:
                if word == "apple":
                    print("APPLE")
                    print(clue[index_char], guess[index_char])

                words.remove(word)
                break

    return words


def guess_word(words: list[str], guess: str, secret_word: str, previous_guesses: list[str]) -> str:
    # guess_attempts = 0
    while secret_word != guess:
        entropy = entropy_calculate(words, guess)
        print(f"Entropy for '{guess}': {entropy:.4f} bits")
        previous_guesses.append(guess)
        words_update(words, guess, generate_clue(guess, secret_word))
        print(f"Suggested best guess: {suggest_best_guess(words, previous_guesses)}")
        guess = suggest_best_guess(words, previous_guesses)
        # guess_attempts += 1

    return secret_word


def convert_clue(clue_passed) -> str:
    clue = []
    print(clue_passed)
    for i in clue_passed:
        if i == '0':
            clue.append('B')
        elif i == '1':
            clue.append('Y')
        else:
            clue.append('G')
    return ''.join(clue)

# def main():
#     stop = False
#     with open('words.txt', 'r') as file:
#         words = [line.strip() for line in file]
#
#     guess = 'crate'
#     previous_guesses = []
#
#     guess_word_bot(words, guess, previous_guesses)


def guess_word_bot(stop: bool, words: list[str], guess: str, clue) -> str:
    global previous_guesses
    # guess_attempts = 0
    if not stop:
        entropy = entropy_calculate(words, guess)
        # print(f"Entropy for '{guess}': {entropy:.4f} bits")
        previous_guesses.append(guess)
        words_update(words, guess, convert_clue(clue))
        # print(f"Suggested best guess: {suggest_best_guess(words, previous_guesses)}")
        print(f"Prev guesses{previous_guesses}")
        print(len(words))
        guess = suggest_best_guess(words, previous_guesses)
        # guess_attempts += 1
        print(f"Guess {guess}")
        return guess

# accessing the file with words and converting it into a list
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file]

# randomly choosing the word to be guessed
secret_word = words[random.randint(0, len(words)-1)]
# print(secret_word)
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
#check for secret word gonys

# guess = 'crate'
# previous_guesses = []
# average_guesses_num = 0
#
# for word in words:
#     print(word)
#     secret_word = word
#     average_guesses_num += guess_word(words, guess, secret_word, previous_guesses)
#
# print(average_guesses_num/len(words))

# print(f"Secret word is: {guess_word(words, guess, secret_word, previous_guesses)}")