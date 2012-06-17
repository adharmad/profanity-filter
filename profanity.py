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

GROUP_SIZE = 2
CHAR_MATCH_HEURISTIC = 0.8

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
                words_count[pw] += 1

        # Check if profane words is a substring of the word
        for pw in profane_words:
            if w.find(pw) != -1 and not inDict:
                words_count[pw] += 1


    # Take words GROUP_SIZE at a time and see if they either form a
    # profane word, or the beginning of one. 
    # If they form a profane word, update the count. If they form the
    # beginning of a profane word, then see if it actually matches one
    # and then count as one

    for i in range(len(words)-GROUP_SIZE):
        concat_word = words[i] + words[i+1] + words[i+2]
        concat_word = utilities.rot13(concat_word)

        for pw in profane_words:
            
            if pw.find(concat_word) != -1:
                if checkMatchPercent(len(concat_word), len(pw)):
                    words_count[pw] += 1
                    break

                # check further...
                j = 2
                while True:
                    j += 1
                    if i + j > len(words)-1:
                        break

                    concat_word += utilities.rot13(words[i+j])

                    # continue while we keep on concatenating the
                    # letters and find that it is a substring of an
                    # actual profane word
                    if pw.find(concat_word) != -1:
                        continue
                    # once the concatenated word is not a substring of
                    # an actual profane word, see how far we have
                    # reached i.e. does the word match a significant
                    # number of characters of a profane word to be
                    # counted as an actual profanity or not. 
                    # If that is the case, and the word is not a
                    # dictionary word, then count it as an actual
                    # profanity that was disguised
                    elif checkMatchPercent(len(concat_word)-1, len(pw)):
                        words_count[pw] += 1
                        break
    
    #utilities.prettyPrintDict(words_count)

    # compute the score
    running_sum = 0
    count = 0
    for w in words_count.keys():
        running_sum += words_count[w] * profane_word_weights[w]
        count += words_count[w]

    if count == 0:
        score = 0
    else:
        score = running_sum/count

    return score
        
            
def getTransposedWords(word):
    """
    Get a list of possible transpositions of the current profane word.
    Transpositions include:
        - Transposing two adjacent characters: eg - siht (for shit)
        - Replacing two letters with **: eg - f**k
        - Replacing letters with special characters: eg - $hit
    eg - For the word "shit", we will return the following:
        ['siht', 'shti', 's**it', 'sh**t', '$hit', 'sh!t']
    """
    ret = []

    # First iterate through the word and transpose 2 adjacent characters
    # (leaving out the first and the last)
    for i in range(1, len(word)-1):
        ret.append(word[:i] + word[i+1] + word[i] + word[i+2:])

    # Now replace letter pairs with *. Once again, skip the first and last
    # characters
    for i in range(1, len(word)-1):
        ret.append(word[:i] + '**' + word[i+2:])

    # Now repalce words with special characters
    for ch in SPECIAL_CHAR_ALIASES.keys():
        if word.find(ch) != -1:
            ret.append(word.replace(ch, SPECIAL_CHAR_ALIASES[ch]))

    return ret

def checkMatchPercent(partialWordLen, wordLen):
    if wordLen <= 4 and partialWordLen >= 3:
            return True
    elif partialWordLen/wordLen > CHAR_MATCH_HEURISTIC:
            return True
    else: 
        return False
