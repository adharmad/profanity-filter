# Driver for profanity filter

import profanity

if __name__ == '__main__':
    #text = 'hello fucker this. is a shitty test.'
    #text = 'transpose fcuk asshloe'
    #text = 'all good here'
    #text = 'f u c k'
    text = 'john is an a s s h o l e'
    score = profanity.profanityScore(text)
    print(score)
