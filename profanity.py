# profanity filter
# The list of profane words is in profane_words.txt. Each word has a
# "score" associated with it between 1-10 to indicate the severity of the
# profanity
#
# Following steps are followed:
# 1. Check for individual words: eg - fuck
# 2. Check for transposed words: eg - fcuk, f**k, sh!t
# 3. Check for compound/broken words: eg - ass hole, ass-hole.
# 4. Check for adjectivish words: eg - assholish behavior

import string
from collections import defaultdict
import json

import utilities

SPECIAL_CHAR_ALIASES = {
    's' : '$',
    'i' : '!',
    'l' : '1',
    'a' : '@',
    'e' : '3',
    'g' : '8',
    'o' : '0',
    'u' : '4'
}

def profanityScore(text):
    """
    Returns a number between 1 and 10 that represents the profanity score
    for the text of string
    """

    profane_word_weights = utilities.readPropertiesFile('profane_words.txt', 'int')
    profane_words = profane_word_weights.keys()

    words_dict = utilities.readPropertiesFile('dict_words.txt', 'list')

    profane_words_transpose = {}
    for w in profane_words:
        profane_words_transpose[w] = getTransposedWords(w)

    #utilities.prettyPrintDict(profane_words_transpose)

    words = [w.rstrip('.') for w in text.lower().split()]

    score = 0.0
    words_count = defaultdict(int)

    for w in words:
        inDict = w in words_dict[w[0]]

        w = utilities.rot13(w)

        # If the exact word appears in the list of profane words
        if w in profane_words:
            words_count[w] += 1

        # Check if the word is a transpose of the profane words
        for pw in profane_words_transpose.keys():
            if w in profane_words_transpose[pw]:
                words_count[w] += 1

        # Check if profane words is a substring of the word
        for pw in profane_words:
            if w.find(pw) != -1 and not inDict:
                words_count[w] += 1

    #utilities.prettyPrintDict(words_count)

    # compute the score
    running_sum = 0
    count = 0
    for w in words_count.keys():
        running_sum += words_count[w] * profane_word_weights[w]
        count += words_count[w]

    score = running_sum/count

    return score
        
            
def getTransposedWords(word):
    """
    Get a list of possible transpositions of the current profane word.
    eg - 
    """
    ret = []

    # First iterate through the word and transpose 2 adjacent characters
    # (leaving out the first and the last)
    for i in range(1, len(word)-1):
        ret.append(word[:i] + word[i+1] + word[i] + word[i+1:])

    # Now replace letter pairs with *. Once again, skip the first and last
    # characters
    for i in range(1, len(word)-1):
        ret.append(word[:i] + '**' + word[i+1:])

    # Now repalce words with special characters
    for ch in SPECIAL_CHAR_ALIASES.keys():
        if word.find(ch) != -1:
            ret.append(word.replace(ch, SPECIAL_CHAR_ALIASES[ch]))

    return ret

