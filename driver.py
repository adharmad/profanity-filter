# Driver for profanity filter

import profanity

if __name__ == '__main__':
    text = 'hello fucker this is a shitty test'
    score = profanity.profanityScore(text)
    print(score)
