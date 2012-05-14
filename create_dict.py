# collect dictionary words from numerous files and output a file
# of the format:
# "a" : [... words starting with a...]
# "b" : [... words starting with b...]
# ...

import string, os

if __name__ == '__main__':
    path = os.path.join(os.getcwd(), "words")

    fw = open('dict_words.txt', 'w')

    for fileName in os.listdir(path):
        filePath = os.path.join(path, fileName)
        f = open(filePath, 'r')
        alpha = fileName.lower()[0]
        
        line_to_write = alpha + ' : '
        lines = f.readlines()
        for idx in range(len(lines)):
            line = lines[idx]
            line_to_write += line.strip()
            if idx < len(lines)-1:
                line_to_write += ','

        line_to_write += '\n'
        fw.write(line_to_write)
        f.close()

    fw.close()
