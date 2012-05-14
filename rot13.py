import utilities
import string, os, sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python rot13.py <infile> <outfile>")
        sys.exit(0)
   
    infile = sys.argv[1]
    outfile = sys.argv[2]

    f = open(infile, 'r')
    fw = open(outfile, 'w')

    for line in f.readlines():
        (val1, val2) = line.split(' : ')
        to_write = utilities.rot13(val1) + ' : ' + val2
        fw.write(to_write)

    fw.close()
    f.close()
