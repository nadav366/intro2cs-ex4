from hangman import *


def test_update_word_pattern():
    assert update_word_pattern("word", "w___", "d") == "w__d"
    assert update_word_pattern("aaaa", "____", 'a') == "aaaa"
    assert update_word_pattern("aaaa", "____", 'b') == "____"
    assert update_word_pattern("nnxaxsfx", "___a____", 'x') == "__xax__x"
    assert update_word_pattern("", "", 'x') == ""
    assert update_word_pattern("abcde", "a_c_e", 'b') == "abc_e"


def hint_word_check():
    assert hint_word_check("word", "__rd", ['c', 'g']) is True
    assert hint_word_check("hallo", "___l_", ['c', 'g']) is False
