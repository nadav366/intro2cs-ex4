from hangman import update_word_pattern


def checker():
    """
    Test for the update_word_pattern function
    Prints a result for all test
    :return: Boolean value, if the test succeeded
    """
    flag = True

    if update_word_pattern("word", "__r_", 'h') != "__r_":
        flag = False

    elif update_word_pattern("aaaa", "____", 'a') != "aaaa":
        flag = False

    elif update_word_pattern("nnxaxsfx", "___a____", 'x') != "__xax__x":
        flag = False

    elif update_word_pattern("abcde", "a_c_e", 'c') != "a_c_e":
        flag = False

    if flag:  # Check if everything is succeeded
        print('Function "update_word_pattern" test success')
    else:
        print('Function "update_word_pattern" test fail')

    return flag


if __name__ == '__main__':
    """
    main function
    """
    checker()
