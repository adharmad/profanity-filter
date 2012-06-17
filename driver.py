# Driver for profanity filter

import profanity

if __name__ == '__main__':
    #text = 'hello fucker this. is a shitty test.'
    text = 'transpose fcuk asshloe'
    #text = 'all good here'
    score = profanity.profanityScore(text)
    print(score)
