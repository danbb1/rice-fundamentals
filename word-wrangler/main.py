"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import urllib2
# import poc_simpletest

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    no_duplicates = list(list1)

    for index, element in enumerate(list1):
        if index < len(list1) - 1 and element == list1[index + 1]:
            no_duplicates.remove(element)

    return no_duplicates


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersected = []

    for x_element in list1 if len(list1) <= len(list2) else list2:
        for y_element in list2 if len(list1) <= len(list2) else list1:
            if x_element == y_element:
                intersected.append(x_element)
                break
            elif y_element > x_element:
                break

    return intersected

# Functions to perform merge sort


def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    merged = []

    len_1 = len(list1)
    len_2 = len(list2)

    list1_index, list2_index = 0, 0

    while list1_index < len_1 and list2_index < len_2:
        if list1[list1_index] < list2[list2_index]:
            merged.append(list1[list1_index])
            list1_index += 1
        else:
            merged.append(list2[list2_index])
            list2_index += 1

    return merged + list1[list1_index:] + list2[list2_index:]


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    median_index = len(list1) // 2

    first_half = list1[:median_index]
    second_half = list1[median_index:]

    if len(first_half) > 1:
        first_half = merge_sort(first_half)

    if len(second_half) > 1:
        second_half = merge_sort(second_half)

    return merge(first_half, second_half)

# Function to generate all strings for the word wrangler game


def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
      return [""]
    
    if len(word) == 1:
      return["", word]
    
    cloned_word = list(word)
    first_letter = cloned_word[0]
    cloned_word.pop(0)
    rest_strings = list(gen_all_strings(''.join(cloned_word)))
    new_strings = []
    for r_string in rest_strings:
      string_as_list = list(r_string)
      for index in range(len(string_as_list) + 1):
        cloned_string_list = list(string_as_list)
        cloned_string_list.insert(index, first_letter)
        temp = ''.join(cloned_string_list)
        new_strings.append(temp)
    
    return rest_strings + new_strings

# Function to load words from a file


def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    
    words = []
    
    word_file = urllib2.urlopen(codeskulptor.file2url(filename))
    for line in word_file.readlines():
      words.append(line[:-1])
    
    return words


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    print words
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()


# def test_suite():
#     suite = poc_simpletest.TestSuite()

#     suite.run_test(remove_duplicates(["a", "a", "b", "b", "c", "c"]), [
#                    "a", "b", "c"], "Test #1")
#     suite.run_test(remove_duplicates(
#         ["a" for x in range(50)]), ["a"], "Test #2")
#     suite.run_test(remove_duplicates(
#         ["a" for x in range(50)] + ["b"]), ["a", "b"], "Test #3")

#     suite.run_test(intersect(["a", "b", "c"], ["a", "b", "c"]), [
#                    "a", "b", "c"], "Test #4")
#     suite.run_test(intersect(["a", "b", "c", "d", "e"], [
#                    "a", "b", "c"]), ["a", "b", "c"], "Test #5")
#     suite.run_test(intersect(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
#                    "k", "l", "m", "n", "o", "p", "q", "r", "s"], ["s"]), ["s"], "Test #6")

#     suite.run_test(merge(["a", "c", "e"], ["b", "d", "f"]), [
#                    "a", "b", "c", "d", "e", "f"], "Test # 7")
#     suite.run_test(merge(["a", "b", "c"], ["d", "e", "f"]), [
#                    "a", "b", "c", "d", "e", "f"], "Test # 7")
#     suite.run_test(merge(["a", "b", "c"], ["a", "b", "c"]), [
#                    "a", "b", "c"], "Test # 7")

#     suite.run_test(merge_sort(["c", "b", "a"]), ["a", "b", "c"], "Test #8")
#     suite.run_test(merge_sort(["f", "l", "d", "a", "p"]), [
#                    "a", "d", "f", "l", "p"], "Test #8")
    
#     suite.run_test(gen_all_strings("baa"), ["", "b", "a", "ab", "ba", "a", "ab", "ba", "aa", "aa", "aab", "aab", "aba", "aba", "baa", "baa"], "Test #9")

#     suite.report_results()


# test_suite()
