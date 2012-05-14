# utilities

import string, json

def rot13(chars):
    "Simple rot-13 encoder"
    lalpha = 'abcdefghijklmnopqrstuvwxyz'
    ualpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ret = []

    for c in chars:
        if c in lalpha:
            ret.append(lalpha[(lalpha.find(c) + 13) % 26])
        elif c in ualpha:
            ret.append(ualpha[(ualpha.find(c) + 13) % 26])
        else:
            ret.append(c)

    return "".join(ret)

def readPropertiesFile(fileName, valtype):
    """
    Reads a properties file which has name - value properties in the
    following format:
        name1 : value1
        name2 : value2
        ...
    valtype can be 'list' or 'int', in which case the values will be
    interpreted accordingly
    Returns a dict
    """

    props = {}
    f = open(fileName, 'r')
    
    for line in f.readlines():
        if line.startswith('#'):
            pass

        (val1, val2) = line.split(' : ')

        if valtype == 'int':
            props[val1] = int(val2)
        elif valtype == 'list':
            props[val1] = val2.split(',')

    f.close()
        
    return props

def prettyPrintDict(d):
    "Pretty print a dict"
    for k in d.keys():
        print(k, " ==> ", d[k])

