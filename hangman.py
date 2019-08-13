import hangman_helper


CHAR_A = 97
LETTERS_NUM = 26  # The number of letters in the language

def letter_to_index(letter):
    """ Return the index of the given letter in an alphabet list. """
    return ord(letter) - CHAR_A


def index_to_letter(index):
    """ Return the letter corresponding to the given index. """
    return chr(index + CHAR_A)


def update_word_pattern(word, pattern, letter):
    """
    function that updates the pattern according to the selected new character
    :param word: String, the correct word
    :param pattern: String, current format
    :param letter: String, the selected letter
    :return: String, the new template, after the update
    """
    new_pattern = str()
    for index in range(len(word)):
        if word[index] == letter:
            new_pattern += letter
        else:
            new_pattern += pattern[index]
    return new_pattern


def check_integrity_letter(new_input, pattern, wrong_guesses_list):
    """
    A function that checks whether the resulting input is correct,
    and if not what the reason
    :param new_input: String, input from the user
    :param pattern: String, current format
    :param wrong_guesses_list:
    :return:list, strings of selected letters that no in word
    """
    if len(new_input) != 1 or\
            letter_to_index(new_input) < 0 or letter_to_index(new_input) > 25:
        return False, hangman_helper.NON_VALID_MSG

    if new_input in wrong_guesses_list or new_input in pattern:
        return False, hangman_helper.ALREADY_CHOSEN_MSG + new_input

    return True, hangman_helper.DEFAULT_MSG


def letter_handling(new_input, pattern, wrong_guesses_list, word):
    """
    A function that handles a letter received from the user
    :param new_input: String, input from the user
    :param pattern: String, current format
    :param wrong_guesses_list:list,strings of selected letters that no in word
    :param word: String, the correct word
    :return: A message, pattern, and wrong list guesses
    """
    # Check the integrity of the input:
    valid_input, msg = check_integrity_letter(new_input,
                                              pattern, wrong_guesses_list)

    if valid_input:
        if new_input in word:  # The selected letter appears in the word
            pattern = update_word_pattern(word, pattern, new_input)
        else:
            wrong_guesses_list.append(new_input)

    return msg, pattern, wrong_guesses_list


def one_turn(word, words_list, pattern, wrong_guesses_list, msg):
    """
    A function that is the rotation of one choice of the user
    :param word: String, the correct word
    :param words_list: List, a collection of all the optional words
    :param pattern: String, current format
    :param wrong_guesses_list:list,strings of selected letters that no in word
    :param msg: String, message to user
    :return: A message, template, and wrong list are updated after the turn
    """
    hangman_helper.display_state(pattern, len(wrong_guesses_list),
                                 wrong_guesses_list, msg)
    types, new_input = hangman_helper.get_input()

    # Adjust message according to input
    if types == hangman_helper.HINT:
        words_list = filter_words_list(words_list,
                                       pattern, wrong_guesses_list)
        msg = hangman_helper.HINT_MSG + choose_letter(words_list, pattern)

    if types == hangman_helper.LETTER:
        msg, pattern, wrong_guesses_list =\
            letter_handling(new_input, pattern, wrong_guesses_list, word)

    return pattern, wrong_guesses_list, msg


def run_single_game(words_list):
    """
    A function that plays an entire game
    :param words_list: List, a collection of all the optional words
    :return: Boolean, play another game?
    """
    word = hangman_helper.get_random_word(words_list)

    wrong_guesses_list = []
    pattern = '_' * len(word)
    msg = hangman_helper.DEFAULT_MSG

    while word != pattern and \
            len(wrong_guesses_list) < hangman_helper.MAX_ERRORS:
        pattern, wrong_guesses_list, msg =\
            one_turn(word, words_list, pattern, wrong_guesses_list, msg)

    completion_reason(pattern, word, wrong_guesses_list)


def completion_reason(pattern, word, wrong_guesses_list):
    """
    Function that prints the reason for the end of the game
    :param pattern: String, current format
    :param word: String, the correct word
    :param wrong_guesses_list:list,strings of selected letters that no in word
    """
    if pattern == word:
        msg = hangman_helper.WIN_MSG
    else:
        msg = hangman_helper.LOSS_MSG + word
    hangman_helper.display_state(pattern, len(wrong_guesses_list),
                                 wrong_guesses_list, msg, ask_play=True)


# Handling hint request:


def choose_letter(good_words_list, pattern):
    """
    A function that selects a letter to be a hint
    :param good_words_list: List, all the appropriate words
    :param pattern: String, current format
    :return: String, hint letter
    """
    cuonter_letters_list = [0] * LETTERS_NUM

    for word in good_words_list:
        for index in range(len(word)):
            if word[index] not in pattern:
                cuonter_letters_list[letter_to_index(word[index])] += 1

    return select_specific_letter(cuonter_letters_list)


def filter_words_list(words_list, pattern, wrong_guesses_list):
    """
    A function that sorts only the correct words for a hint
    :param words_list: List, a collection of all the optional words
    :param pattern: String, current format
    :param wrong_guesses_list:list, strings of selected letters that no in word
    :return: List, all the appropriate words
    """
    good_words = []
    for word in words_list:
        if hint_word_check(word, pattern, wrong_guesses_list):
            good_words.append(word)
    return good_words


def hint_word_check(checked_word, pattern, wrong_guesses_list):
    """
    A function that checks whether a word matches the hint list
    :param checked_word: String, word for review
    :param pattern: String, current format
    :param wrong_guesses_list: list,strings of selected letters that no in word
    :return: Boolean, is the word appropriate
    """
    if len(checked_word) != len(pattern):
        return False

    for letter in wrong_guesses_list:
        if letter in checked_word:
            return False

    for index in range(len(checked_word)):
        if pattern[index] != "_":
            if checked_word[index] != pattern[index]:
                return False
        elif checked_word[index] in pattern:
            # Whether the letter already exists in the pattern
            return False

    return True


def select_specific_letter(index_counter_letter):
    """
    A function that calculates which letter is the hint
    :param index_counter_letter: list, how many times each letter appears
    :return: String, signal to be a hint
    """
    max_index = 0
    max_value = 0

    for index in range(len(index_counter_letter)):
        if index_counter_letter[index] > max_value:
            max_value = index_counter_letter[index]
            max_index = index
    return index_to_letter(max_index)


def main():
    """
    main function, runs the games
    """
    words_list = hangman_helper.load_words()
    more_play = True

    while more_play:
        run_single_game(words_list)
        types, more_play = hangman_helper.get_input()
        # Input, whether to play another game


if __name__ == '__main__':
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()

